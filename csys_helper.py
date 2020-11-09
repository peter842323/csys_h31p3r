# Lib
import wx
import wx.xrc
import wx.grid
import json
import requests
import random
import csv

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from datetime import datetime

# Custom .Py
import gui_dialog
import setting

from course import Course
from login import Login

# random 27 character, you can use this website to create (https://1password.com/zh-tw/password-generator/)
encode_code = '9K0uDRXPQu96xQYvgzuczTCu22W'
# if you want to use functions of changelog and allowed-user, you can use it. But I recommend use Firebase!
google_doc_id = ''
# debug id, just for debug, do not use it to do something illegal, type debugger itouch id
debug_id = ''


class MainGui(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"CsYs_h31P3R v0.1.8.2 Build 20201109 2020雙11快樂版",
                          pos=wx.DefaultPosition, size=wx.Size(575, 700),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.app_version = '0.1.8.2'
        self.SetSizeHints(wx.Size(-1, 700), wx.Size(-1, 700))

        ################################################################################################################
        self.app_setting = setting.init_setting()
        self.console_login = Login(self.app_setting)
        self.student_login = Login(self.app_setting)
        self.course_request = None
        self.student_id = None
        self.student_pw = None

        self.user_setting_found = True
        try:
            with open('user.json', 'r+') as f:
                try:
                    self.user_setting = json.load(f)
                    try:
                        self.student_id = self.user_setting['id']
                        if self.user_setting['remember_all']:
                            new_id = self.student_id
                            if len(new_id) < 8:
                                new_id = (new_id + 'e6rM39jz')[0:8]
                            elif len(new_id) > 8:
                                new_id = new_id[0:8]
                            try:
                                f = Fernet(str.encode(new_id + encode_code + new_id + "="))
                                self.student_pw = bytes.decode(f.decrypt(str.encode(self.user_setting['pw'])))
                            except InvalidToken:
                                pass
                        else:
                            self.student_pw = ""
                    except KeyError:
                        pass
                except ValueError:
                    pass

        except FileNotFoundError:
            self.user_setting_found = False

        # 目前課程清單
        self.user_current_course_enrollment_list = None
        self.user_trace_course_list = None
        self.user_register_course_list = None
        self.user_append_course_list = None
        self.user_course_time_list = None

        # 驗證清單的選課資料
        self.online_course_data = {}

        # 輔助課程清單
        self.user_select_help_mode = u'加選'
        self.help_course_list_found = True
        self.help_course_list = None
        self.help_course_mode = None
        self.help_delay_time = None
        self.help_list_index = 0
        self.help_times = 0
        m_help_course_listChoices = []

        # 排程時間
        self.schedule = None

        # App 初始化
        self.app_init = True

        ################################################################################################################

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體"))
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTIONTEXT))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVEBORDER))

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        current_course_list_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"目前課程清單"), wx.VERTICAL)

        current_course_list_sizer.SetMinSize(wx.Size(200, 150))
        current_course_list_sizer_inside1 = wx.BoxSizer(wx.HORIZONTAL)

        current_course_list_sizer_inside1.SetMinSize(wx.Size(-1, 15))

        current_course_list_sizer_inside1_1 = wx.BoxSizer(wx.HORIZONTAL)

        current_course_list_sizer_inside1_1_1 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_current_course_enrollment_radiobtn = wx.RadioButton(current_course_list_sizer.GetStaticBox(), wx.ID_ANY,
                                                                   u"修課", wx.DefaultPosition, wx.DefaultSize, 0)

        current_course_list_sizer_inside1_1_1.Add(self.m_current_course_enrollment_radiobtn, 0, wx.ALL, 5)

        self.m_trace_course_radiobtn = wx.RadioButton(current_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"追蹤",
                                                      wx.DefaultPosition, wx.DefaultSize, 0)
        current_course_list_sizer_inside1_1_1.Add(self.m_trace_course_radiobtn, 0, wx.ALL, 5)

        self.m_reg_select_course_radiobtn = wx.RadioButton(current_course_list_sizer.GetStaticBox(), wx.ID_ANY,
                                                           u"登記", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.m_reg_select_course_radiobtn.SetMaxSize(wx.Size(-1, 15))

        current_course_list_sizer_inside1_1_1.Add(self.m_reg_select_course_radiobtn, 0, wx.ALL, 5)

        self.m_append_course_radiobtn = wx.RadioButton(current_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"遞補",
                                                      wx.DefaultPosition, wx.DefaultSize, 0)
        current_course_list_sizer_inside1_1_1.Add(self.m_append_course_radiobtn, 0, wx.ALL, 5)

        current_course_list_sizer_inside1_1.Add(current_course_list_sizer_inside1_1_1, 1, wx.EXPAND, 5)

        self.m_course_time_btn = wx.Button(current_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"功課表",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_course_time_btn.SetMinSize(wx.Size(70, 22))
        self.m_course_time_btn.SetMaxSize(wx.Size(70, 22))

        current_course_list_sizer_inside1_1.Add(self.m_course_time_btn, 0, wx.RIGHT | wx.LEFT, 5)

        self.m_get_user_all_course_data_btn = wx.Button(current_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"取得資料",
                                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_get_user_all_course_data_btn.SetMinSize(wx.Size(70, 22))
        self.m_get_user_all_course_data_btn.SetMaxSize(wx.Size(70, 22))

        current_course_list_sizer_inside1_1.Add(self.m_get_user_all_course_data_btn, 0, wx.RIGHT | wx.LEFT, 5)

        self.m_export_course_list_btn = wx.Button(current_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"匯出",
                                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_export_course_list_btn.Enable(False)
        self.m_export_course_list_btn.SetMinSize(wx.Size(70, 22))
        self.m_export_course_list_btn.SetMaxSize(wx.Size(70, 22))

        current_course_list_sizer_inside1_1.Add(self.m_export_course_list_btn, 0, wx.RIGHT | wx.LEFT, 5)

        current_course_list_sizer_inside1.Add(current_course_list_sizer_inside1_1, 1, wx.EXPAND, 5)

        current_course_list_sizer.Add(current_course_list_sizer_inside1, 1, wx.EXPAND, 5)

        self.m_current_course_list_grid = wx.grid.Grid(current_course_list_sizer.GetStaticBox(), wx.ID_ANY,
                                                       wx.DefaultPosition, wx.Size(-1, -1), 0)

        # Grid
        self.m_current_course_list_grid.CreateGrid(0, 13)
        self.m_current_course_list_grid.EnableEditing(False)
        self.m_current_course_list_grid.EnableGridLines(True)
        self.m_current_course_list_grid.EnableDragGridSize(False)
        self.m_current_course_list_grid.SetMargins(0, 0)

        # Columns
        self.m_current_course_list_grid.SetColSize(0, 1)
        self.m_current_course_list_grid.EnableDragColMove(False)
        self.m_current_course_list_grid.EnableDragColSize(True)
        self.m_current_course_list_grid.SetColLabelSize(30)
        self.m_current_course_list_grid.SetColLabelValue(0, u"代碼")
        self.m_current_course_list_grid.SetColLabelValue(1, u"名稱")
        self.m_current_course_list_grid.SetColLabelValue(2, u"類別")
        self.m_current_course_list_grid.SetColLabelValue(3, u"開課班級")
        self.m_current_course_list_grid.SetColLabelValue(4, u"學分")
        self.m_current_course_list_grid.SetColLabelValue(5, u"老師")
        self.m_current_course_list_grid.SetColLabelValue(6, u"時間-1")
        self.m_current_course_list_grid.SetColLabelValue(7, u"教室-1")
        self.m_current_course_list_grid.SetColLabelValue(8, u"時間-2")
        self.m_current_course_list_grid.SetColLabelValue(9, u"教室-2")
        self.m_current_course_list_grid.SetColLabelValue(10, u"時間-3")
        self.m_current_course_list_grid.SetColLabelValue(11, u"教室-3")
        self.m_current_course_list_grid.SetColLabelValue(12, u"備註")
        self.m_current_course_list_grid.AutoSizeColumns()

        self.m_current_course_list_grid.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # Rows
        self.m_current_course_list_grid.EnableDragRowSize(True)
        self.m_current_course_list_grid.SetRowLabelSize(30)
        self.m_current_course_list_grid.SetRowLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # Label Appearance
        self.m_current_course_list_grid.SetLabelFont(
            wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體"))

        # Cell Defaults
        self.m_current_course_list_grid.SetDefaultCellFont(
            wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體"))
        self.m_current_course_list_grid.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        self.m_current_course_list_grid.SetMinSize(wx.Size(-1, 150))
        self.m_current_course_list_grid.SetMaxSize(wx.Size(-1, 150))

        current_course_list_sizer.Add(self.m_current_course_list_grid, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(current_course_list_sizer, 1, wx.EXPAND, 5)

        help_course_list_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"輔助課程清單"), wx.VERTICAL)

        help_course_list_sizer_inside1 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_help_course_list = wx.ListBox(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition,
                                             wx.DefaultSize, m_help_course_listChoices, 0)
        self.m_help_course_list.SetMinSize(wx.Size(130, -1))
        self.m_help_course_list.SetMaxSize(wx.Size(130, -1))

        help_course_list_sizer_inside1.Add(self.m_help_course_list, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        help_course_list_sizer_inside1_1 = wx.BoxSizer(wx.VERTICAL)

        self.m_help_course_up_btn = wx.Button(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"↑",
                                              wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_help_course_up_btn.SetMinSize(wx.Size(100, -1))
        self.m_help_course_up_btn.SetMaxSize(wx.Size(100, -1))

        help_course_list_sizer_inside1_1.Add(self.m_help_course_up_btn, 0, wx.ALL, 5)

        self.m_help_course_down_btn = wx.Button(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"↓",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_help_course_down_btn.SetMinSize(wx.Size(100, -1))
        self.m_help_course_down_btn.SetMaxSize(wx.Size(100, -1))

        help_course_list_sizer_inside1_1.Add(self.m_help_course_down_btn, 0, wx.ALL, 5)

        self.m_add_help_course_btn = wx.Button(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"新增課程",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_add_help_course_btn.SetMinSize(wx.Size(100, -1))
        self.m_add_help_course_btn.SetMaxSize(wx.Size(100, -1))

        help_course_list_sizer_inside1_1.Add(self.m_add_help_course_btn, 0, wx.ALL, 5)

        self.m_delete_help_course_btn = wx.Button(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"刪除課程",
                                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_delete_help_course_btn.SetMinSize(wx.Size(100, -1))
        self.m_delete_help_course_btn.SetMaxSize(wx.Size(100, -1))

        help_course_list_sizer_inside1_1.Add(self.m_delete_help_course_btn, 0, wx.ALL, 5)

        self.m_import_trace_course_list_btn = wx.Button(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"從追蹤清單匯入",
                                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_import_trace_course_list_btn.SetMinSize(wx.Size(100, -1))
        self.m_import_trace_course_list_btn.SetMaxSize(wx.Size(100, -1))

        help_course_list_sizer_inside1_1.Add(self.m_import_trace_course_list_btn, 0, wx.ALL, 5)

        self.m_verify_course_list_btn = wx.Button(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"驗證清單",
                                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_verify_course_list_btn.SetMinSize(wx.Size(100, -1))
        self.m_verify_course_list_btn.SetMaxSize(wx.Size(100, -1))

        help_course_list_sizer_inside1_1.Add(self.m_verify_course_list_btn, 0, wx.ALL, 5)

        help_course_list_sizer_inside1.Add(help_course_list_sizer_inside1_1, 1, wx.EXPAND, 5)

        help_course_list_sizer_inside1_2 = wx.BoxSizer(wx.VERTICAL)

        help_course_list_sizer_inside1_2_1 = wx.BoxSizer(wx.VERTICAL)

        self.m_custom_time_text = wx.StaticText(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"輔助時間(單位:ms)",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_custom_time_text.Wrap(-1)

        help_course_list_sizer_inside1_2_1.Add(self.m_custom_time_text, 0, wx.ALL, 2)

        self.m_help_custom_time = wx.SpinCtrlDouble(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"100",
                                                    wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 10, 10000, 100,
                                                    1)
        self.m_help_custom_time.SetDigits(0)
        self.m_help_custom_time.SetMinSize(wx.Size(120, -1))
        self.m_help_custom_time.SetMaxSize(wx.Size(120, -1))

        help_course_list_sizer_inside1_2_1.Add(self.m_help_custom_time, 0, wx.ALL, 3)

        help_course_list_sizer_inside1_2.Add(help_course_list_sizer_inside1_2_1, 1, wx.EXPAND, 5)

        help_course_list_sizer_inside1_2_2 = wx.BoxSizer(wx.VERTICAL)

        self.m_help_mode_text = wx.StaticText(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"輔助模式",
                                              wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_help_mode_text.Wrap(-1)

        help_course_list_sizer_inside1_2_2.Add(self.m_help_mode_text, 0, wx.ALL, 2)

        m_help_mode_choiceChoices = ["加選", "新增登記", "新增追蹤", "退選", "取消登記", "刪除追蹤", "取消遞補"]
        self.m_help_mode_choice = wx.Choice(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition,
                                            wx.DefaultSize, m_help_mode_choiceChoices, 0)
        self.m_help_mode_choice.SetSelection(0)
        self.m_help_mode_choice.SetMinSize(wx.Size(120, 15))
        self.m_help_mode_choice.SetMaxSize(wx.Size(120, 15))
        help_course_list_sizer_inside1_2_2.Add(self.m_help_mode_choice, 0, wx.ALL | wx.EXPAND, 3)

        help_course_list_sizer_inside1_2.Add(help_course_list_sizer_inside1_2_2, 1, wx.EXPAND, 5)

        help_course_list_sizer_inside1_2_3 = wx.BoxSizer(wx.VERTICAL)

        self.m_help_times_text = wx.StaticText(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"輔助循環次數",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_help_times_text.Wrap(-1)

        help_course_list_sizer_inside1_2_3.Add(self.m_help_times_text, 0, wx.BOTTOM | wx.RIGHT | wx.LEFT, 2)

        self.m_help_times_ctrl = wx.SpinCtrl(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"1", wx.DefaultPosition,
                                             wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 10000, 1)
        self.m_help_times_ctrl.SetMinSize(wx.Size(120, -1))
        self.m_help_times_ctrl.SetMaxSize(wx.Size(120, -1))

        help_course_list_sizer_inside1_2_3.Add(self.m_help_times_ctrl, 0, wx.RIGHT | wx.LEFT, 3)

        self.m_help_times_infinity_checkbox = wx.CheckBox(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"無限循環",
                                                          wx.DefaultPosition, wx.DefaultSize, 0)
        help_course_list_sizer_inside1_2_3.Add(self.m_help_times_infinity_checkbox, 0, wx.TOP | wx.RIGHT | wx.LEFT, 5)

        help_course_list_sizer_inside1_2.Add(help_course_list_sizer_inside1_2_3, 1, wx.EXPAND, 5)

        help_course_list_sizer_inside1.Add(help_course_list_sizer_inside1_2, 1, wx.EXPAND, 5)

        help_course_list_sizer_inside1_3 = wx.BoxSizer(wx.VERTICAL)

        help_course_list_sizer_inside1_3_1 = wx.BoxSizer(wx.VERTICAL)

        help_course_list_sizer_inside1_3_1_1 = wx.BoxSizer(wx.VERTICAL)

        self.m_schedule_checkbox = wx.CheckBox(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"設定排程時間",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        help_course_list_sizer_inside1_3_1_1.Add(self.m_schedule_checkbox, 0, wx.ALL, 5)

        self.m_schedule_text = wx.StaticText(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"\n\n\n\n",
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_schedule_text.Wrap(-1)

        help_course_list_sizer_inside1_3_1_1.Add(self.m_schedule_text, 0, wx.ALL, 5)

        help_course_list_sizer_inside1_3_1.Add(help_course_list_sizer_inside1_3_1_1, 1, wx.EXPAND, 5)

        help_course_list_sizer_inside1_3_1_2 = wx.BoxSizer(wx.VERTICAL)

        self.m_nothing_text_1 = wx.StaticText(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                              wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_nothing_text_1.Wrap(-1)

        help_course_list_sizer_inside1_3_1_2.Add(self.m_nothing_text_1, 0, wx.RIGHT | wx.LEFT, 5)

        self.m_nothing_text_2 = wx.StaticText(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                              wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_nothing_text_2.Wrap(-1)

        help_course_list_sizer_inside1_3_1_2.Add(self.m_nothing_text_2, 0, wx.RIGHT | wx.LEFT, 5)

        self.m_start_help_btn = wx.Button(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"開始輔助",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_start_help_btn.SetMinSize(wx.Size(120, -1))
        self.m_start_help_btn.SetMaxSize(wx.Size(120, -1))

        help_course_list_sizer_inside1_3_1_2.Add(self.m_start_help_btn, 0, wx.ALL, 5)

        self.m_stop_help_btn = wx.Button(help_course_list_sizer.GetStaticBox(), wx.ID_ANY, u"停止輔助",
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_stop_help_btn.SetMinSize(wx.Size(120, -1))
        self.m_stop_help_btn.SetMaxSize(wx.Size(120, -1))
        self.m_stop_help_btn.Enable(False)

        help_course_list_sizer_inside1_3_1_2.Add(self.m_stop_help_btn, 0, wx.ALL, 5)

        help_course_list_sizer_inside1_3_1.Add(help_course_list_sizer_inside1_3_1_2, 1, wx.EXPAND, 5)

        help_course_list_sizer_inside1_3.Add(help_course_list_sizer_inside1_3_1, 1, wx.EXPAND, 5)

        help_course_list_sizer_inside1.Add(help_course_list_sizer_inside1_3, 1, wx.EXPAND, 5)

        help_course_list_sizer.Add(help_course_list_sizer_inside1, 1, wx.EXPAND, 1)

        main_sizer.Add(help_course_list_sizer, 1, wx.EXPAND, 5)

        system_status_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"狀態列"), wx.VERTICAL)
        system_status_sizer.SetMinSize(wx.Size(-1, 300))

        self.m_system_status_text = wx.TextCtrl(system_status_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                wx.DefaultPosition, wx.Size(-1, 200),
                                                wx.TE_AUTO_URL | wx.TE_MULTILINE | wx.TE_READONLY)
        self.m_system_status_text.SetFont(
            wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "新細明體"))
        self.m_system_status_text.SetForegroundColour(wx.Colour(0, 255, 0))
        self.m_system_status_text.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.m_system_status_text.SetMinSize(wx.Size(-1, 300))
        self.m_system_status_text.SetMaxSize(wx.Size(-1, 300))

        system_status_sizer.Add(self.m_system_status_text, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(system_status_sizer, 1, wx.EXPAND, 5)

        self.SetSizer(main_sizer)
        self.Layout()
        self.m_menubar1 = wx.MenuBar(0)
        self.m_system_menu = wx.Menu()

        self.m_check_version = wx.MenuItem(self.m_system_menu, wx.ID_ANY, u"檢查更新", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_system_menu.Append(self.m_check_version)

        self.m_system_menu.AppendSeparator()

        self.m_user_manager = wx.MenuItem(self.m_system_menu, wx.ID_ANY, u"帳號管理", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_system_menu.Append(self.m_user_manager)

        self.m_system_menu.AppendSeparator()

        self.m_login = wx.MenuItem(self.m_system_menu, wx.ID_ANY, u"登入", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_system_menu.Append(self.m_login)

        self.m_logout = wx.MenuItem(self.m_system_menu, wx.ID_ANY, u"登出", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_system_menu.Append(self.m_logout)
        self.m_logout.Enable(False)

        self.m_menubar1.Append(self.m_system_menu, u"系統選單")

        self.m_menu3 = wx.Menu()
        self.m_save_help_course_setting = wx.MenuItem(self.m_menu3, wx.ID_ANY, u"保存清單", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.m_save_help_course_setting)

        self.m_load_help_course_setting = wx.MenuItem(self.m_menu3, wx.ID_ANY, u"讀取清單", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu3.Append(self.m_load_help_course_setting)

        self.m_menubar1.Append(self.m_menu3, u"輔助課程清單管理")

        self.m_debug_menu = wx.Menu()
        self.m_change_id = wx.MenuItem(self.m_debug_menu, wx.ID_ANY, u"更改學號", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_debug_menu.Append(self.m_change_id)

        #

        self.SetMenuBar(self.m_menubar1)

        self.m_status_bar = self.CreateStatusBar(4, wx.STB_SIZEGRIP, wx.ID_ANY)
        self.m_status_bar.SetStatusWidths([-1, -3, -1, -3])
        self.m_status_bar.SetStatusText("目前使用者", 0)
        self.m_status_bar.SetStatusText("系統狀態", 2)

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_current_course_enrollment_radiobtn.Bind(wx.EVT_RADIOBUTTON,
                                                       self.current_course_enrollment_course_radiobtn_selected)
        self.m_help_times_infinity_checkbox.Bind(wx.EVT_CHECKBOX, self.do_help_times_infinity)
        self.m_trace_course_radiobtn.Bind(wx.EVT_RADIOBUTTON, self.trace_course_radiobtn_selected)
        self.m_reg_select_course_radiobtn.Bind(wx.EVT_RADIOBUTTON, self.reg_course_radiobtn_selected)
        self.m_append_course_radiobtn.Bind(wx.EVT_RADIOBUTTON, self.append_course_radiobtn_selected)
        self.m_export_course_list_btn.Bind(wx.EVT_BUTTON, self.do_export_course_list)
        self.m_help_course_up_btn.Bind(wx.EVT_BUTTON, self.help_course_up)
        self.m_help_course_down_btn.Bind(wx.EVT_BUTTON, self.help_course_down)
        self.m_add_help_course_btn.Bind(wx.EVT_BUTTON, self.add_help_course)
        self.m_delete_help_course_btn.Bind(wx.EVT_BUTTON, self.delete_help_course)
        self.m_import_trace_course_list_btn.Bind(wx.EVT_BUTTON, self.import_trace_course_list)
        self.Bind(wx.EVT_MENU, self.on_user_manager, id=self.m_user_manager.GetId())
        self.Bind(wx.EVT_MENU, self.do_login, id=self.m_login.GetId())
        self.Bind(wx.EVT_MENU, self.do_logout, id=self.m_logout.GetId())
        self.Bind(wx.EVT_MENU, self.on_save_help_course_setting, id=self.m_save_help_course_setting.GetId())
        self.Bind(wx.EVT_MENU, self.on_load_help_course_setting, id=self.m_load_help_course_setting.GetId())
        self.Bind(wx.EVT_MENU, self.on_change_id, id=self.m_change_id.GetId())
        self.m_start_help_btn.Bind(wx.EVT_BUTTON, self.do_help_timer_start)
        self.m_stop_help_btn.Bind(wx.EVT_BUTTON, self.do_help_timer_stop)
        self.m_course_time_btn.Bind(wx.EVT_BUTTON, self.course_time_btn_selected)
        self.m_get_user_all_course_data_btn.Bind(wx.EVT_BUTTON, self.do_get_user_all_course_data)
        self.m_verify_course_list_btn.Bind(wx.EVT_BUTTON, self.verify_course_list)
        self.m_schedule_checkbox.Bind(wx.EVT_CHECKBOX, self.do_set_schedule)
        if len(google_doc_id) != 0:
            self.Bind(wx.EVT_MENU, self.do_check_version, id=self.m_check_version.GetId())
        self.m_help_mode_choice.Bind(wx.EVT_CHOICE, self.change_help_mode)
        self.Bind(wx.EVT_CLOSE, self.do_close)

        # Timer
        self.m_schedule_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.do_schedule_ontimer, self.m_schedule_timer)
        self.m_help_course_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.do_help_timer_ontimer, self.m_help_course_timer)
        self.m_auto_retry_login_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.do_retry_login_ontimer, self.m_auto_retry_login_timer)

        self.app_version_check()
        self.do_load_help_course_list()
        self.app_init = False

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def do_close(self, event):
        if self.student_login.login_status:
            self.do_logout(event)

        self.Destroy()
        event.Skip()

    def app_version_check(self):
        online_version_list = requests.get('https://docs.google.com/spreadsheets/d/' +google_doc_id + '/export?format=csv').text.split('\r\n')
        self.m_system_status_text.AppendText(u"目前版本: " + self.app_version + "\t 最新版本: ")
        if len(online_version_list) == 2:
            self.m_system_status_text.AppendText(online_version_list[0] + u" \n")
            if not online_version_list[0] == self.app_version:
                self.m_system_status_text.AppendText(u"發現新版本!請到 " + online_version_list[1] + " 下載!\n")
        else:
            self.m_system_status_text.AppendText(u"Unknown Version \n")

    def do_check_version(self, event):
        self.app_version_check()
        event.Skip()

    def verify_course_list_old(self, event):
        if self.student_login.login_status:
            for i in range(self.m_help_course_list.GetCount()-1, -1, -1):
                tmp = self.course_request.search_course(
                    self.m_help_course_list.GetString(i))
                if tmp.status_code == 200:
                    if tmp.json()['totalRows'] == 0:
                        self.m_help_course_list.Delete(i)
                else:
                    self.do_login(event)
                    i -= 1

            self.on_save_help_course_setting(event)
        else:
            self.m_system_status_text.AppendText("請先登入，在使用驗證課程之功能!!\n")
        event.Skip()

    def do_get_course_list_from_course_query_system(self):
        try:
            if not self.app_init:
                self.m_system_status_text.AppendText("取得開課系統資料中，請稍後......\n")
        except AttributeError:
            pass
        headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / ' + str(random.uniform(500, 600))[
                                                                                        0:6]
                          + '(KHTML, like Gecko) '
                            'Chrome / ' + str(random.uniform(61, 68))[0:5] + '.' + str(random.uniform(0, 9999))[0:8] +
                          'Safari / ' + str(random.uniform(500, 600))[0:6],
        }
        r = requests.post('https://itouch.cycu.edu.tw/active_system/CourseQuerySystem/GetYearTerm.jsp',
                          headers=headers)
        now_term = r.text.split('@')[1].split('|')[1]
        # print(now_term)

        r = requests.post('https://itouch.cycu.edu.tw/active_system/CourseQuerySystem/GetCourses.jsp?yearTerm='
                          + now_term, headers=headers)

        course_list_raw = r.text.split('@@')

        for i in range(1, len(course_list_raw), 1):
            self.online_course_data[course_list_raw[i].split('|')[6]] = course_list_raw[i].split('|')[11]

    def verify_course_list(self, event):
        # print(str(random.uniform(61, 68))[0:5]+'.'+str(random.uniform(0, 9999))[0:8])
        if len(self.online_course_data) == 0:
            self.do_get_course_list_from_course_query_system()

        for i in range(self.m_help_course_list.GetCount() - 1, -1, -1):
            if not self.online_course_data.get(self.m_help_course_list.GetString(i).split(' ')[0]):
                self.m_help_course_list.Delete(i)
            else:
                i -= 1

        self.on_save_help_course_setting(event)
        self.m_system_status_text.AppendText(u"輔助課程清單驗證完畢!並以自動保存!!\n")

        event.Skip()

    def do_help_times_infinity(self, event):
        if self.m_help_times_infinity_checkbox.GetValue():
            self.m_help_times_ctrl.Enable(False)
        else:
            self.m_help_times_ctrl.Enable(True)

        event.Skip()

    def do_retry_login_ontimer(self, event):
        # self.m_auto_retry_login_timer.StartOnce(0)

        print(self.help_times)
        self.m_system_status_text.AppendText(u"自動嘗試登入中......可透過停止輔助來取消!!\n")
        self.do_login(event)
        self.help_times -= 1

        if self.student_login.login_status:
            self.m_auto_retry_login_timer.Stop()
            self.do_help_timer_start(event)
        else:
            if self.m_help_times_infinity_checkbox.GetValue():
                self.help_times = self.m_help_times_ctrl.GetValue()
            elif self.help_times == 0:
                self.do_help_timer_stop(event)


    def do_help_timer_start_btn_switcher(self):
        self.m_stop_help_btn.Enable(True)
        self.m_help_custom_time.Enable(False)
        self.m_help_mode_choice.Enable(False)
        self.m_start_help_btn.Enable(False)
        self.m_help_times_ctrl.Enable(False)
        self.m_help_times_infinity_checkbox.Enable(False)
        self.m_help_times_ctrl.Enable(False)
        self.help_times = self.m_help_times_ctrl.GetValue()

    def do_help_timer_start(self, event):
        if not self.course_request:
            self.m_system_status_text.AppendText(u"將自動嘗試登入直到成功為止!!可透過停止輔助來取消!!\n")
            self.do_help_timer_start_btn_switcher()
            self.m_auto_retry_login_timer.Start(int(self.m_help_custom_time.GetValue()))

        if self.course_request:
            self.verify_course_list(event)
            verify_session = self.course_request.view_trace_list()
            if not verify_session.status_code == 200:
                self.do_logout(event)
                self.do_login(event)

            if self.student_login.login_status:
                self.help_course_list = self.m_help_course_list.GetItems()
                self.help_course_mode = self.m_help_mode_choice.GetString(self.m_help_mode_choice.GetSelection())
                self.help_delay_time = int(self.m_help_custom_time.GetValue())

                self.m_system_status_text.AppendText(u"已開始課程輔助功能!!\n")
                self.do_help_timer_start_btn_switcher()
                self.m_help_course_timer.StartOnce(0)
            else:
                self.m_system_status_text.AppendText(u"目前處於登出狀態沒辦法進行輔助功能!!將自動嘗試登入直到成功為止!!可透過停止"
                                                     u"輔助來取消!!\n")
                self.do_help_timer_start_btn_switcher()
                self.m_auto_retry_login_timer.Start(int(self.m_help_custom_time.GetValue()))
        else:
            pass
            # self.m_system_status_text.AppendText(u"請確認已經登入再進行輔助功能!!\n")

        event.Skip()

    def do_help_timer_stop(self, event):
        self.m_help_course_timer.Stop()
        self.m_auto_retry_login_timer.Stop()
        self.m_system_status_text.AppendText("已停止課程輔助功能!!\n")
        self.m_help_custom_time.Enable(True)
        self.m_help_mode_choice.Enable(True)
        self.m_start_help_btn.Enable(True)
        self.m_stop_help_btn.Enable(False)
        self.m_help_times_infinity_checkbox.Enable(True)
        self.do_help_times_infinity(event)
        event.Skip()

    def do_help_timer_ontimer(self, event):
        # print(datetime.now())
        if self.help_course_mode == u'新增追蹤':
            tmp = self.course_request.add_trace(self.help_course_list[self.help_list_index].split(' ')[0])
            if tmp.status_code == 200:
                tmp = tmp.json()
                self.m_system_status_text.AppendText(self.help_course_list[self.help_list_index] + u" 新增追蹤成功！\n")
            elif tmp.status_code == 400:
                self.m_system_status_text.AppendText(self.help_course_list[self.help_list_index] + u" 已經追蹤不需再追蹤！\n")
            else:
                self.do_logout(event)
                self.do_login(event)
                self.help_list_index -= 1

        elif self.help_course_mode == u'刪除追蹤':
            tmp = self.course_request.delete_trace(self.help_course_list[self.help_list_index].split(' ')[0])
            if tmp.status_code == 200:
                tmp = tmp.json()
                # print(tmp)
                if tmp['result']:
                    self.m_system_status_text.AppendText(self.help_course_list[self.help_list_index] + u" 刪除追蹤成功！\n")
                else:
                    self.m_system_status_text.AppendText(self.help_course_list[self.help_list_index]
                                                         + u" 已經刪除追蹤不需再刪除追蹤！\n")
            else:
                self.do_logout(event)
                self.do_login(event)
                self.help_list_index -= 1

        elif self.help_course_mode == u'新增登記':
            tmp = self.course_request.add_register(self.help_course_list[self.help_list_index].split(' ')[0])
            if tmp.status_code == 200 or tmp.status_code == 400:
                tmp = tmp.json()
                if tmp['result']:
                    self.m_system_status_text.AppendText(self.help_course_list[self.help_list_index] + u" 新增登記成功！\n")
                else:
                    self.m_system_status_text.AppendText(self.help_course_list[self.help_list_index] + u" 新增登記失敗！"
                                                         + tmp['message'] + "\n")
            else:
                self.do_logout(event)
                self.do_login(event)
                self.help_list_index -= 1

        elif self.help_course_mode == u'取消登記':
            tmp = self.course_request.delete_register(self.help_course_list[self.help_list_index].split(' ')[0])
            if tmp.status_code == 200 or tmp.status_code == 400:
                tmp = tmp.json()
                if tmp['result']:
                    self.m_system_status_text.AppendText(self.help_course_list[self.help_list_index] + u" 取消登記成功！\n")
                else:
                    self.m_system_status_text.AppendText(self.help_course_list[self.help_list_index] + u" 取消登記失敗！"
                                                         + tmp['message'] + "\n")
            else:
                self.do_logout(event)
                self.do_login(event)
                self.help_list_index -= 1

        elif self.help_course_mode == u'加選':
            #if self.student_id not in self.allowed_user_list:
            #    self.m_system_status_text.AppendText(u"非認可使用者無法使用加選功能！\n")
            #    self.help_list_index = 0
            #    self.do_help_timer_stop(event)
            #else:
            tmp = self.course_request.add_selection(self.help_course_list[self.help_list_index].split(' ')[0])
            if tmp.status_code == 200 or tmp.status_code == 400:
                tmp = tmp.json()
                if tmp['result']:
                    self.m_system_status_text.AppendText(self.help_course_list[self.help_list_index] + u" 加選成功！\n")
                else:
                    self.m_system_status_text.AppendText(self.help_course_list[self.help_list_index] + u" 加選失敗！"
                                                         + tmp['message'] + "\n")
            else:
                self.do_logout(event)
                self.do_login(event)
                self.help_list_index -= 1

        #elif self.help_course_mode == u'退選':
        #    tmp = self.course_request.delete_selection(self.help_course_list[self.help_list_index].split(' ')[0])
        #    if tmp.status_code == 200 or tmp.status_code == 400:
        #        tmp = tmp.json()
        #        if tmp['result']:
        #            self.m_system_status_text.AppendText(self.help_course_list[self.help_list_index] + u" 退選成功！\n")
        #        else:
        #            self.m_system_status_text.AppendText(self.help_course_list[self.help_list_index] + u" 退選失敗！"
        #                                                 + tmp['message'] + "\n")
        #    else:
        #        self.do_logout(event)
        #        self.do_login(event)
        #        self.help_list_index -= 1

        else:
            self.m_system_status_text.AppendText(self.help_course_mode + u"功能尚未實裝! 敬請期待!\n")
            self.do_help_timer_stop(event)

        self.help_list_index += 1

        if self.help_list_index == len(self.help_course_list):
            self.help_list_index = 0
            if self.m_help_times_infinity_checkbox.GetValue():
                pass
            elif self.help_times == 1:
                self.do_help_timer_stop(event)
            else:
                self.help_times -= 1
        else:
            self.m_help_course_timer.Start(self.help_delay_time*0.6)
        event.Skip()

    def do_get_user_all_course_data(self, event):
        if self.course_request:
            self.user_current_course_enrollment_list = self.course_request.view_reg_list(sn_status=">0")
            if self.user_current_course_enrollment_list.status_code == 200:
                # self.user_current_course_enrollment_list = self.user_current_course_enrollment_list.json()
                pass
            else:
                self.do_logout(event)
                self.do_login(event)

            if self.student_login.login_status:
                self.user_current_course_enrollment_list = self.course_request.view_reg_list(sn_status=">0").json()
                self.user_trace_course_list = self.course_request.view_trace_list().json()
                self.user_register_course_list = self.course_request.view_reg_list(sn_status="=-200").json()
                self.user_append_course_list = self.course_request.view_reg_list(sn_status="=-400").json()
                self.user_course_time_list = self.course_request.view_course_time().json()
                # print(self.user_course_time_list)
                self.m_get_user_all_course_data_btn.SetLabel(u'重新取得')
                self.m_system_status_text.AppendText(u"取得所有目前課程清單成功!!\n")
                self.m_export_course_list_btn.Enable(True)
                if self.m_current_course_enrollment_radiobtn.GetValue():
                    self.current_course_enrollment_course_radiobtn_selected(event)
                elif self.m_reg_select_course_radiobtn.GetValue():
                    self.reg_course_radiobtn_selected(event)
                elif self.m_trace_course_radiobtn.GetValue():
                    self.trace_course_radiobtn_selected(event)
                elif self.m_append_course_radiobtn.GetValue():
                    self.append_course_radiobtn_selected(event)
            else:
                self.m_get_user_all_course_data_btn.SetLabel(u'取得資料')
                self.m_system_status_text.AppendText(u"目前處於登出狀態沒辦法取得所有目前課程清單!!\n")
        else:
            if not self.app_init:
                self.m_system_status_text.AppendText(u"請先登入!!\n")
        event.Skip()

    def current_course_enrollment_course_radiobtn_selected(self, event):
        if not self.user_current_course_enrollment_list:
            self.do_get_user_all_course_data(event)
        else:
            pass
        self.do_change_grid(mode='current_course_enrollment')
        event.Skip()

    def append_course_radiobtn_selected(self, event):
        if not self.user_append_course_list:
            self.do_get_user_all_course_data(event)
        else:
            pass
        self.do_change_grid(mode='append')
        event.Skip()

    def trace_course_radiobtn_selected(self, event):
        if not self.user_trace_course_list:
            self.do_get_user_all_course_data(event)
        else:
            pass
        self.do_change_grid(mode='trace')
        event.Skip()

    def reg_course_radiobtn_selected(self, event):
        if not self.user_register_course_list:
            self.do_get_user_all_course_data(event)
        else:
            pass
        self.do_change_grid(mode='reg')
        event.Skip()

    def course_time_btn_selected(self, event):
        if not self.user_course_time_list:
            self.do_get_user_all_course_data(event)
            if self.user_course_time_list:
                course_time_dialog = gui_dialog.CourseTimeDialog(self)
                course_time_dialog.ShowModal()
        else:
            course_time_dialog = gui_dialog.CourseTimeDialog(self)
            course_time_dialog.ShowModal()
        event.Skip()

    def do_change_grid(self, **kwargs):
        if self.course_request:
            course_list = None
            if not self.m_current_course_list_grid.GetNumberRows() == 0:
                self.m_current_course_list_grid.DeleteRows(0, self.m_current_course_list_grid.GetNumberRows())
            if kwargs.get('mode') == 'current_course_enrollment':
                course_list = self.user_current_course_enrollment_list

            elif kwargs.get('mode') == 'trace':
                course_list = self.user_trace_course_list

            elif kwargs.get('mode') == 'reg':
                course_list = self.user_register_course_list
                # print(self.user_register_course_list)
            elif kwargs.get('mode') == 'append':
                course_list = self.user_append_course_list
                # print(self.user_append_course_list)

            for i in range(0, course_list['totalRows'], 1):
                self.m_current_course_list_grid.AppendRows()
                self.m_current_course_list_grid.SetCellValue(i, 0, course_list['datas'][i]['op_code'])
                self.m_current_course_list_grid.SetCellValue(i, 1, course_list['datas'][i]['cname'])
                self.m_current_course_list_grid.SetCellValue(i, 2, course_list['datas'][i]['op_stdy']+'-' +
                                                             course_list['datas'][i]['op_quality'])
                self.m_current_course_list_grid.SetCellValue(i, 3, course_list['datas'][i]['dept_name'] if
                course_list['datas'][i]['dept_name'] else "")
                self.m_current_course_list_grid.SetCellValue(i, 4, str(course_list['datas'][i]['op_credit'])[:-2])
                self.m_current_course_list_grid.SetCellValue(i, 5, course_list['datas'][i]['teacher'] if
                course_list['datas'][i]['teacher'] else "")
                self.m_current_course_list_grid.SetCellValue(i, 6, course_list['datas'][i]['op_time_1'] if
                course_list['datas'][i]['op_time_1'] else "")
                self.m_current_course_list_grid.SetCellValue(i, 7, course_list['datas'][i]['op_rm_name_1'] if
                course_list['datas'][i]['op_rm_name_1'] else "")
                self.m_current_course_list_grid.SetCellValue(i, 8, course_list['datas'][i]['op_time_2'] if
                course_list['datas'][i]['op_time_2'] else "")
                self.m_current_course_list_grid.SetCellValue(i, 9, course_list['datas'][i]['op_rm_name_2'] if
                course_list['datas'][i]['op_rm_name_2'] else "")
                self.m_current_course_list_grid.SetCellValue(i, 10, course_list['datas'][i]['op_time_3'] if
                course_list['datas'][i]['op_time_3'] else "")
                self.m_current_course_list_grid.SetCellValue(i, 11, course_list['datas'][i]['op_rm_name_3'] if
                course_list['datas'][i]['op_rm_name_3'] else "")
                if kwargs.get('mode') == 'append':
                    self.m_current_course_list_grid.SetCellValue(i, 12, "遞補順位: " + course_list['datas'][i]['ord'] +
                                                                        " 。" + course_list['datas'][i]['memo1'] if
                                                                        course_list['datas'][i]['memo1'] else "")
                else:
                    self.m_current_course_list_grid.SetCellValue(i, 12, course_list['datas'][i]['memo1'] if
                                                                        course_list['datas'][i]['memo1'] else "")

            course_list = None
            self.m_current_course_list_grid.AutoSizeRows()
            self.m_current_course_list_grid.AutoSizeColumns()

    def do_export_course_list(self, event):
        # self.user_current_course_enrollment_list = None
        # self.user_trace_course_list = None
        # self.user_register_course_list = None
        csv_header = ['代碼', '名稱', '類別', '開課班級', '學分', '老師', '時間-1', '教室-1', '時間-2', '教室-2', '時間-3', '教室-3', '備註']
        if self.user_trace_course_list['datas']:
            try:
                with open(self.student_id+'_追蹤清單.csv', 'w+', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(csv_header)
                    for i in self.user_trace_course_list['datas']:
                        writer.writerow([i['op_code'], i['cname'], i['op_stdy'] + '-' + i['op_quality'], i['dept_name'],
                                         str(i['op_credit'])[:-2], i['teacher'], i['op_time_1'], i['op_rm_name_1'],
                                         i['op_time_2'], i['op_rm_name_2'], i['op_time_3'], i['op_rm_name_3'], i['memo1']])
            except TypeError:
                pass
        else:
            pass

        if self.user_register_course_list['datas']:
            try:
                with open(self.course_request.student_id+'_登記(加選)清單.csv', 'w+', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(csv_header)
                    for i in self.user_register_course_list['datas']:
                        writer.writerow([i['op_code'], i['cname'], i['op_stdy']+'-'+i['op_quality'], i['dept_name'],
                                         str(i['op_credit'])[:-2], i['teacher'], i['op_time_1'], i['op_rm_name_1'],
                                         i['op_time_2'], i['op_rm_name_2'], i['op_time_3'], i['op_rm_name_3'], i['memo1']])
            except TypeError:
                pass
        else:
            pass

        if self.user_current_course_enrollment_list['datas']:
            try:
                with open(self.course_request.student_id+'_修課清單.csv', 'w+', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(csv_header)
                    for i in self.user_current_course_enrollment_list['datas']:
                        writer.writerow([i['op_code'], i['cname'], i['op_stdy'] + '-' + i['op_quality'], i['dept_name'],
                                         str(i['op_credit'])[:-2], i['teacher'], i['op_time_1'], i['op_rm_name_1'],
                                         i['op_time_2'], i['op_rm_name_2'], i['op_time_3'], i['op_rm_name_3'], i['memo1']])
            except TypeError:
                pass
        else:
            pass

        if self.user_append_course_list['datas']:
            try:
                with open(self.course_request.student_id+'_遞補清單.csv', 'w+', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(csv_header)
                    for i in self.user_append_course_list['datas']:
                        writer.writerow([i['op_code'], i['cname'], i['op_stdy'] + '-' + i['op_quality'], i['dept_name'],
                                         str(i['op_credit'])[:-2], i['teacher'], i['op_time_1'], i['op_rm_name_1'],
                                         i['op_time_2'], i['op_rm_name_2'], i['op_time_3'], i['op_rm_name_3'], "遞補順位: " +
                                         i['ord'] + " 。" + i['memo1']])
            except TypeError:
                pass
        else:
            pass

        self.m_system_status_text.AppendText("所有目前課程清單均已匯出完成!!\n")
        event.Skip()

    def on_user_manager(self, event):
        user_manager_dialog = gui_dialog.UserManagerDialog(self)
        if user_manager_dialog.ShowModal() == wx.ID_OK:
            self.student_id = user_manager_dialog.m_student_id_textctrl.GetValue()
            self.student_pw = user_manager_dialog.m_student_pw_textctrl.GetValue()
        else:
            pass
        event.Skip()

    def do_login(self, event):
        login_init_package = self.student_login.login_init()
        if login_init_package['result']:
            if not (self.student_id and self.student_pw):
                self.on_user_manager(event)
            if self.student_id and self.student_pw:
                package_json = self.student_login.login(self.student_id, self.student_pw)
                if self.student_login.login_status:
                    self.course_request = Course(self.student_login.login_setting, self.student_login.get_session(),
                                                 self.student_id)
                    self.m_status_bar.SetStatusText(u'選課系統開放中!', 3)
                    self.m_system_status_text.AppendText(self.student_id+u" 登入成功!!\n")
                    if not self.student_login.allowed_id:
                        self.m_help_mode_choice.SetItems(["新增登記", "新增追蹤", "退選", "取消登記", "刪除追蹤", "取消遞補"])
                        if not self.user_select_help_mode == u'加選':
                            self.m_help_mode_choice.SetSelection(
                                self.m_help_mode_choice.FindString(self.user_select_help_mode))
                        else:
                            self.m_help_mode_choice.SetSelection(0)
                            self.user_select_help_mode = self.m_help_mode_choice.GetString(
                                self.m_help_mode_choice.GetSelection())

                    # print(self.user_select_help_mode)
                    if self.student_id == debug_id and self.m_menubar1.FindMenu('Debug') == -1:
                        self.m_menubar1.Append(self.m_debug_menu, "Debug")
                    self.m_status_bar.SetStatusText(self.student_id, 1)
                    self.m_login.Enable(False)
                    self.m_logout.Enable(True)

                else:
                    self.m_system_status_text.AppendText(package_json['message']+"\n")
                    self.m_status_bar.SetStatusText(package_json['message'], 1)
            else:
                self.m_system_status_text.AppendText(u"請重新到帳號管理或是直接點選登入並正確填寫學號及密碼，方可登入，謝謝!!\n")
        else:


            self.m_status_bar.SetStatusText(login_init_package['message'], 3)
            self.m_system_status_text.AppendText(login_init_package['message']+"\n")
        event.Skip()

    def do_logout(self, event):
        if self.student_login.check_status():
            self.m_system_status_text.AppendText(self.student_id + u" 登出成功!!\n")
            self.m_status_bar.SetStatusText(u'使用者已登出!', 3)
            if self.student_id == debug_id and self.m_menubar1.FindMenu('Debug') == 2:
                self.m_menubar1.Remove(2)
            self.m_help_mode_choice.SetItems(["加選", "新增登記", "新增追蹤", "退選", "取消登記", "刪除追蹤", "取消遞補"])
            # print(self.user_select_help_mode)
            self.m_help_mode_choice.SetSelection(self.m_help_mode_choice.FindString(self.user_select_help_mode))
            self.m_status_bar.SetStatusText("", 1)
            self.student_login.logout()
            self.course_request = None
            self.m_login.Enable(True)
            self.m_logout.Enable(False)
            self.user_select_help_mode = u'加選'
        else:
            pass

        event.Skip()

    def on_save_help_course_setting(self, event):
        help_course_list_output = {}
        for i in range(0, self.m_help_course_list.GetCount(), 1):
            tmp = 'course_' + str(i+1)
            help_course_list_output[tmp] = self.m_help_course_list.GetString(i).split(' ')[0]
            # print(type(self.m_help_course_list.GetString(i)))

        with open('help_course.json', 'w+') as f:
            json.dump(help_course_list_output, f)
        self.m_system_status_text.AppendText(u"輔助課程清單保存成功!!\n")
        event.Skip()

    def do_load_help_course_list(self):
        try:
            with open('help_course.json', 'r+') as f:
                while True:
                    if self.m_help_course_list.GetCount() > 0:
                        self.m_help_course_list.Delete(self.m_help_course_list.GetCount()-1)
                    else:
                        break
                try:
                    tmp = json.load(f)
                    if len(self.online_course_data) == 0:
                        self.do_get_course_list_from_course_query_system()

                    for i in tmp.values():
                        if self.online_course_data.get(i):
                            self.m_help_course_list.Append(i + ' ' + self.online_course_data.get(i))

                    self.m_system_status_text.AppendText(u"輔助課程清單讀取成功!!\n")
                    # self.m_help_course_list.Unbind(wx.EVT_SIZE)
                except ValueError:
                    self.m_system_status_text.AppendText(u"輔助課程清單損毀!!請刪除help_course.json後再重新製作!!\n")
        except FileNotFoundError:
            self.m_system_status_text.AppendText(u"輔助課程清單讀取失敗!!\n")
            self.help_course_list_found = False

    def on_load_help_course_setting(self, event):
        self.do_load_help_course_list()
        event.Skip()

    def on_change_id(self, event):
        change_id_dialog = gui_dialog.ChangeIdDialog(self)
        if change_id_dialog.ShowModal() == wx.ID_OK:
            if len(change_id_dialog.m_change_id_textctrl.GetValue().replace(" ", "").replace("\t", "")) > 0:
                self.course_request.student_id = change_id_dialog.m_change_id_textctrl.GetValue()\
                    .replace(" ", "").replace("\t", "")
                self.m_system_status_text.AppendText(u"學號已更換成"+self.course_request.student_id+"\n")
        else:
            self.m_system_status_text.AppendText(u"學號沒有更換!!\n")
        event.Skip()

    def do_set_schedule(self, event):
        if self.m_schedule_checkbox.GetValue():
            set_schedule = gui_dialog.SetScheduleDialog(self)
            if set_schedule.ShowModal() == wx.ID_OK:
                self.schedule = datetime.strptime(str(set_schedule.m_schedule_start_date_picker.GetValue().FormatISODate())
                                                  + " " +
                                                  str(set_schedule.m_schedule_start_time_picker.GetValue().FormatISOTime()),
                                                  '%Y-%m-%d %H:%M:%S')
                self.m_schedule_text.SetLabel('將於\n' +
                                              str(set_schedule.m_schedule_start_date_picker.GetValue().FormatISODate()) +
                                              '\n' +
                                              str(set_schedule.m_schedule_start_time_picker.GetValue().FormatISOTime()) +
                                              '\n' + '自動開始進行輔助')
                self.m_help_times_ctrl.SetValue(self.m_help_times_ctrl.GetValue()+10)
                self.m_schedule_timer.Start(0)
            else:
                # print(set_schedule.ShowModal())
                self.m_schedule_checkbox.SetValue(False)

        else:
            self.m_schedule_timer.Stop()
            self.m_help_times_ctrl.SetValue(1)
            self.m_schedule_text.SetLabel('\n\n\n\n')

        event.Skip()

    def do_schedule_ontimer(self, event):
        if (self.schedule-datetime.now()).total_seconds() < 0.2:
            self.m_schedule_timer.Stop()
            self.do_help_timer_start(event)
            self.m_help_times_ctrl.SetValue(1)
            self.m_schedule_text.SetLabel('\n\n\n\n')
            self.m_schedule_checkbox.SetValue(False)
            # print(datetime.now())

        event.Skip()

    def help_course_up(self, event):
        if self.m_help_course_list.GetSelection() > 0:
            tmp = self.m_help_course_list.GetString(self.m_help_course_list.GetSelection())
            self.m_help_course_list.SetString(self.m_help_course_list.GetSelection(),
                                              self.m_help_course_list.GetString(
                                                  self.m_help_course_list.GetSelection()-1))
            self.m_help_course_list.SetString(self.m_help_course_list.GetSelection()-1, tmp)
            self.m_help_course_list.SetSelection(self.m_help_course_list.GetSelection()-1)
        else:
            self.m_system_status_text.AppendText(u"課程上移失敗，請先選取要移動的課程!!\n")

        event.Skip()

    def help_course_down(self, event):
        if self.m_help_course_list.GetSelection() < self.m_help_course_list.GetCount()-1 and \
                self.m_help_course_list.GetSelection() != -1:
            tmp = self.m_help_course_list.GetString(self.m_help_course_list.GetSelection())
            self.m_help_course_list.SetString(self.m_help_course_list.GetSelection(),
                                              self.m_help_course_list.GetString(
                                                  self.m_help_course_list.GetSelection()+1))
            self.m_help_course_list.SetString(self.m_help_course_list.GetSelection()+1, tmp)
            self.m_help_course_list.SetSelection(self.m_help_course_list.GetSelection()+1)

        else:
            self.m_system_status_text.AppendText(u"課程下移失敗，請先選取要移動的課程!!\n")
        event.Skip()

    def add_course_to_help_list(self, _op_code):
        if len(self.online_course_data) == 0:
            self.do_get_course_list_from_course_query_system()

        if self.online_course_data.get(_op_code):
            tmp = _op_code + ' ' + self.online_course_data.get(_op_code)
            self.m_help_course_list.Append(tmp)
            self.m_system_status_text.AppendText(tmp + u" 已成功新增!!\n")
        else:
            self.m_system_status_text.AppendText(u"課程代碼 " + _op_code + u" 不存在開課系統裡面!!\n")

    def do_import_trace_course(self):
        for i in self.user_trace_course_list['datas']:
            self.add_course_to_help_list(i['op_code'])
            # print(i)

    def add_help_course(self, event):
        add_help_course_dialog = gui_dialog.AddCourseDialog(self)
        if add_help_course_dialog.ShowModal() == wx.ID_OK:
            tmp = add_help_course_dialog.m_add_course_textctrl.GetValue().replace(" ", "").replace("\t", "")
            if len(tmp) > 0:
                self.add_course_to_help_list(tmp)
            else:
                self.m_system_status_text.AppendText(u"請檢查輸入是否有誤!!\n")
        else:
            add_help_course_dialog.Destroy()
        event.Skip()

    def delete_help_course(self, event):
        if self.m_help_course_list.GetSelection() >= 0:
            tmp = self.m_help_course_list.GetString(self.m_help_course_list.GetSelection())
            self.m_help_course_list.Delete(self.m_help_course_list.GetSelection())
            self.m_system_status_text.AppendText(tmp+u" 已成功刪除!!\n")
            # print("課程 "+tmp+" 已成功刪除!!")
            tmp = None
        else:
            self.m_system_status_text.AppendText(u"課程刪除失敗，請先選取要刪除的課程!!\n")
            # print("課程刪除失敗，請先選取要刪除的課程!!")
        event.Skip()

    def import_trace_course_list(self, event):
        if not self.user_trace_course_list:
            self.do_get_user_all_course_data(event)
            if self.user_trace_course_list:
                self.do_import_trace_course()
        else:
            self.do_import_trace_course()
        event.Skip()

    def change_help_mode(self, event):
        self.user_select_help_mode = self.m_help_mode_choice.GetString(self.m_help_mode_choice.GetSelection())
        # print(self.user_select_help_mode)
        event.Skip()


if __name__ == '__main__':
    app = wx.App(False)
    csys_helper = MainGui(None)
    csys_helper.Show(True)
    app.MainLoop()
