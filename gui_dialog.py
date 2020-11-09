import wx
import wx.xrc
import wx.adv
import json
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
# from openpyxl import Workbook

encode_code = '9K0uDRXPQu96xQYvgzuczTCu22W'

class AddCourseDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"新增課程", pos=wx.DefaultPosition, size=wx.Size(200, 131),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(200, -1), wx.Size(200, -1))

        bSizer12 = wx.BoxSizer(wx.VERTICAL)

        self.m_add_course_text = wx.StaticText(self, wx.ID_ANY, u"請輸入課程代碼", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_add_course_text.Wrap(-1)

        self.m_add_course_text.SetFont(
            wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體"))
        self.m_add_course_text.SetMinSize(wx.Size(200, -1))

        bSizer12.Add(self.m_add_course_text, 0, wx.ALL, 5)

        self.m_add_course_textctrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_add_course_textctrl.SetMinSize(wx.Size(200, -1))
        self.m_add_course_textctrl.SetMaxSize(wx.Size(200, -1))

        bSizer12.Add(self.m_add_course_textctrl, 0, wx.ALL, 5)

        self.m_add_course_confirm_btn = wx.Button(self, wx.ID_OK, u"確定", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_add_course_confirm_btn.SetDefault()
        bSizer12.Add(self.m_add_course_confirm_btn, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_cancel_btn = wx.Button(self, wx.ID_CANCEL, u"取消")
        self.m_cancel_btn.SetId(wx.ID_CANCEL)
        self.m_cancel_btn.SetMinSize(wx.Size(0, 0))
        self.m_cancel_btn.SetMaxSize(wx.Size(0, 0))
        bSizer12.Add(self.m_cancel_btn, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(bSizer12)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_add_course_confirm_btn.Bind(wx.EVT_BUTTON, self.add_course_confirm)


    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def add_course_confirm(self, event):
        self.Destroy()
        event.Skip()


class CourseTimeDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"功課表", pos=wx.DefaultPosition, size=wx.DefaultSize,
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體"))

        bSizer20 = wx.BoxSizer(wx.VERTICAL)
        # bSizer20.SetMinSize(wx.Size(600, 800))
        self.m_course_time_grid = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), 0)


        # Grid
        self.m_course_time_grid.CreateGrid(15, 7)
        self.m_course_time_grid.EnableEditing(True)
        self.m_course_time_grid.EnableGridLines(True)
        self.m_course_time_grid.EnableDragGridSize(False)
        self.m_course_time_grid.SetMargins(0, 0)

        # Columns
        for i in range(0, 7, 1):
            self.m_course_time_grid.SetColSize(i, 80)
        self.m_course_time_grid.EnableDragColMove(False)
        self.m_course_time_grid.EnableDragColSize(True)
        self.m_course_time_grid.SetColLabelSize(30)
        self.m_course_time_grid.SetColLabelValue(0, u"週一")
        self.m_course_time_grid.SetColLabelValue(1, u"週二")
        self.m_course_time_grid.SetColLabelValue(2, u"週三")
        self.m_course_time_grid.SetColLabelValue(3, u"週四")
        self.m_course_time_grid.SetColLabelValue(4, u"週五")
        self.m_course_time_grid.SetColLabelValue(5, u"週六")
        self.m_course_time_grid.SetColLabelValue(6, u"週日")
        self.m_course_time_grid.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)


        # Rows
        for i in range(0, 15, 1):
            self.m_course_time_grid.SetRowSize(i, 80)
        self.m_course_time_grid.EnableDragRowSize(True)
        self.m_course_time_grid.SetRowLabelSize(50)
        self.m_course_time_grid.SetRowLabelValue(0, u"A\n07:10\n~\n08:00")
        self.m_course_time_grid.SetRowLabelValue(1, u"1\n08:10\n~\n09:00")
        self.m_course_time_grid.SetRowLabelValue(2, u"2\n09:10\n~\n10:00")
        self.m_course_time_grid.SetRowLabelValue(3, u"3\n10:10\n~\n11:00")
        self.m_course_time_grid.SetRowLabelValue(4, u"4\n11:10\n~\n12:00")
        self.m_course_time_grid.SetRowLabelValue(5, u"B\n12:10\n~\n13:00")
        self.m_course_time_grid.SetRowLabelValue(6, u"5\n13:10\n~\n14:00")
        self.m_course_time_grid.SetRowLabelValue(7, u"6\n14:10\n~\n15:00")
        self.m_course_time_grid.SetRowLabelValue(8, u"7\n15:10\n~\n16:00")
        self.m_course_time_grid.SetRowLabelValue(9, u"8\n16:10\n~\n17:00")
        self.m_course_time_grid.SetRowLabelValue(10, u"C\n17:05\n~\n17:55")
        self.m_course_time_grid.SetRowLabelValue(11, u"D\n18:00\n~\n18:50")
        self.m_course_time_grid.SetRowLabelValue(12, u"E\n18:55\n~\n19:45")
        self.m_course_time_grid.SetRowLabelValue(13, u"F\n19:50\n~\n20:40")
        self.m_course_time_grid.SetRowLabelValue(14, u"G\n20:45\n~\n21:35")
        self.m_course_time_grid.SetRowLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)


        # Label Appearance

        # Cell Defaults
        self.m_course_time_grid.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)
        self.m_course_time_grid.SetMinSize(wx.Size(-1, 750))
        self.m_course_time_grid.SetMaxSize(wx.Size(-1, 750))

        bSizer20.Add(self.m_course_time_grid, 0, wx.ALL| wx.EXPAND, 5)

        bSizer21 = wx.BoxSizer(wx.VERTICAL)

        self.m_course_time_export_btn = wx.Button(self, wx.ID_ANY, u"匯出(功能未建置完成)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_course_time_export_btn.SetFont(
            wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體"))

        bSizer21.Add(self.m_course_time_export_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.ALIGN_CENTER_HORIZONTAL,
                     5)

        bSizer20.Add(bSizer21, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer20)
        self.Layout()
        bSizer20.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_course_time_export_btn.Bind(wx.EVT_BUTTON, self.course_time_export)
        self.m_course_time_export_btn.Enable(False)

        self.course_time_list = parent.user_course_time_list['datas']
        for i in self.course_time_list:
            # print(i)
            col = int(i['week_day'])-1
            row = 0 if i['sess'] == 'A' else 1 if i['sess'] == '1' else 2 if i['sess'] == '2' else 3 if \
                i['sess'] == '3' else 4 if i['sess'] == '4' else 5 if i['sess'] == 'B' else 6 if \
                i['sess'] == '5' else 7 if i['sess'] == '6' else 8 if i['sess'] == '7' else 9 if \
                i['sess'] == '8' else 10 if i['sess'] == 'C' else 11 if i['sess'] == 'D' else 12 if \
                i['sess'] == 'E' else 13 if i['sess'] == 'F' else 14
            course_name = i['cname']+"\n"+i['op_code']+"\n"+i['room_name'] if i['room_name'] else ""
            self.m_course_time_grid.SetCellValue(row, col, course_name)

        self.student_id = parent.course_request.student_id

        # self.m_course_time_grid.AutoSizeRows()
        # self.m_course_time_grid.AutoSizeColumns()

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def course_time_export(self, event):
        """
        wb = Workbook()
        ws = wb.active
        ws.column_dimensions['A'].width = 10
        for i in range(1, 17, 1):
            ws.row_dimensions[i].height = 65
        ws.cell(row=1, column=1).value = "節"
        ws.cell(row=1, column=2).value = "週一"
        ws.cell(row=1, column=3).value = "週二"
        ws.cell(row=1, column=4).value = "週三"
        ws.cell(row=1, column=5).value = "週四"
        ws.cell(row=1, column=6).value = "週五"
        ws.cell(row=1, column=7).value = "週六"
        ws.cell(row=1, column=8).value = "週日"
        ws.cell(row=2, column=1).value = "A\n07:10\n~\n08:00"
        ws.cell(row=3, column=1).value = "1\n08:10\n~\n09:00"
        ws.cell(row=4, column=1).value = "2\n09:10\n~\n10:00"
        ws.cell(row=5, column=1).value = "3\n10:10\n~\n11:00"
        ws.cell(row=6, column=1).value = "4\n11:10\n~\n12:00"
        ws.cell(row=7, column=1).value = "B\n12:10\n~\n13:00"
        ws.cell(row=8, column=1).value = "5\n13:10\n~\n14:00"
        ws.cell(row=9, column=1).value = "6\n14:10\n~\n15:00"
        ws.cell(row=10, column=1).value = "7\n15:10\n~\n16:00"
        ws.cell(row=11, column=1).value = "8\n16:10\n~\n17:00"
        ws.cell(row=12, column=1).value = "C\n17:05\n~\n17:55"
        ws.cell(row=13, column=1).value = "D\n18:00\n~\n18:50"
        ws.cell(row=14, column=1).value = "E\n18:55\n~\n19:45"
        ws.cell(row=15, column=1).value = "F\n19:50\n~\n20:40"
        ws.cell(row=16, column=1).value = "G\n20:45\n~\n21:35"
        """

        """
        for i in self.course_time_list:
            # print(i)
            col = int(i['week_day'])-1
            row = 0 if i['sess'] == 'A' else 1 if i['sess'] == '1' else 2 if i['sess'] == '2' else 3 if \
                i['sess'] == '3' else 4 if i['sess'] == '4' else 5 if i['sess'] == 'B' else 6 if \
                i['sess'] == '5' else 7 if i['sess'] == '6' else 8 if i['sess'] == '7' else 9 if \
                i['sess'] == '8' else 10 if i['sess'] == 'C' else 11 if i['sess'] == 'D' else 12 if \
                i['sess'] == 'E' else 13 if i['sess'] == 'F' else 14
            course_name = i['cname']+"\n"+i['op_code']+"\n"+i['room_name']
            self.m_course_time_grid.SetCellValue(row, col, course_name)
        """
        #ws.title = self.student_id+'_CourseTime.xlsx'
        #wb.save(self.student_id+'_CourseTime.xlsx')
        #ws.title = '10327144_CourseTime.xlsx'
        #wb.save('10327144_CourseTime.xlsx')
        #export_ok_dialog = CourseTimeExportDialog(self)
        #export_ok_dialog.ShowModal()
        event.Skip()


class CourseTimeExportDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"功課表", pos=wx.DefaultPosition, size=wx.Size(300, 120),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(200, 120), wx.Size(200, 120))

        bSizer12 = wx.BoxSizer(wx.VERTICAL)

        bSizer12.SetMinSize(wx.Size(200, 120))
        self.m_course_time_export_text = wx.StaticText(self, wx.ID_ANY, u"功課表已成功匯出!!", wx.DefaultPosition,
                                                       wx.DefaultSize, 0)
        self.m_course_time_export_text.Wrap(-1)

        self.m_course_time_export_text.SetFont(
            wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體"))

        bSizer12.Add(self.m_course_time_export_text, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_export_ok_btn = wx.Button(self, wx.ID_OK, u"確定", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.m_export_ok_btn.SetDefault()
        bSizer12.Add(self.m_export_ok_btn, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(bSizer12)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_export_ok_btn.Bind(wx.EVT_BUTTON, self.export_ok)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def export_ok(self, event):
        self.Destroy()
        event.Skip()


class ChangeIdDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"更改學號", pos=wx.DefaultPosition, size=wx.Size(200, 131),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(200, -1), wx.Size(200, -1))

        bSizer19 = wx.BoxSizer(wx.VERTICAL)

        self.m_change_id_text = wx.StaticText(self, wx.ID_ANY, u"請輸入學號", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_change_id_text.Wrap(-1)

        self.m_change_id_text.SetFont(
            wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體"))
        self.m_change_id_text.SetMinSize(wx.Size(200, -1))

        bSizer19.Add(self.m_change_id_text, 0, wx.ALL, 5)

        self.m_change_id_textctrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_change_id_textctrl.SetMinSize(wx.Size(200, -1))
        self.m_change_id_textctrl.SetMaxSize(wx.Size(200, -1))

        bSizer19.Add(self.m_change_id_textctrl, 0, wx.ALL, 5)

        self.m_change_id_confirm_btn = wx.Button(self, wx.ID_OK, u"確定", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_change_id_confirm_btn.SetDefault()
        bSizer19.Add(self.m_change_id_confirm_btn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_cancel_btn = wx.Button(self, wx.ID_CANCEL, u"取消")
        self.m_cancel_btn.SetMinSize(wx.Size(0, 0))
        self.m_cancel_btn.SetMaxSize(wx.Size(0, 0))
        self.m_cancel_btn.SetId(wx.ID_CANCEL)
        bSizer19.Add(self.m_cancel_btn, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(bSizer19)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_change_id_confirm_btn.Bind(wx.EVT_BUTTON, self.change_id_confirm)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def change_id_confirm(self, event):
        self.Destroy()
        event.Skip()


class UserManagerDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"帳號管理", pos=wx.DefaultPosition, size=wx.Size(200, 450),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.user_setting_found = True
        try:
            with open('user.json', 'r+') as f:
                try:
                    self.user_setting = json.load(f)
                except ValueError:
                    self.user_setting_found = False
        except FileNotFoundError:
            self.user_setting_found = False

        self.SetSizeHints(wx.Size(200, -1), wx.Size(200, -1))
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        bSizer13 = wx.BoxSizer(wx.VERTICAL)

        bSizer13.SetMinSize(wx.Size(200, 200))
        bSizer14 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer14.SetMinSize(wx.Size(200, 20))
        self.m_student_id_text = wx.StaticText(self, wx.ID_ANY, u"   學    號 ", wx.DefaultPosition, wx.Size(50, 18), 0)
        self.m_student_id_text.Wrap(-1)

        self.m_student_id_text.SetMinSize(wx.Size(50, 18))
        self.m_student_id_text.SetMaxSize(wx.Size(50, 18))

        bSizer14.Add(self.m_student_id_text, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.m_student_id_textctrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1),
                                                 0)
        self.m_student_id_textctrl.SetMinSize(wx.Size(200, -1))
        self.m_student_id_textctrl.SetMaxSize(wx.Size(200, -1))

        bSizer14.Add(self.m_student_id_textctrl, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        bSizer13.Add(bSizer14, 1, wx.EXPAND, 5)

        bSizer15 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer15.SetMinSize(wx.Size(200, 20))
        self.m_student_pw_text = wx.StaticText(self, wx.ID_ANY, u"   密    碼", wx.DefaultPosition, wx.Size(50, -1), 0)
        self.m_student_pw_text.Wrap(-1)

        self.m_student_pw_text.SetMinSize(wx.Size(50, -1))
        self.m_student_pw_text.SetMaxSize(wx.Size(50, -1))

        bSizer15.Add(self.m_student_pw_text, 0, wx.ALL, 5)

        self.m_student_pw_textctrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1),
                                                 wx.TE_PASSWORD)
        self.m_student_pw_textctrl.SetMinSize(wx.Size(200, -1))
        self.m_student_pw_textctrl.SetMaxSize(wx.Size(200, -1))

        bSizer15.Add(self.m_student_pw_textctrl, 0, wx.ALL, 5)

        bSizer13.Add(bSizer15, 1, wx.EXPAND, 5)

        bSizer16 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer16.SetMinSize(wx.Size(200, 20))
        self.m_remember_id_checkbox = wx.CheckBox(self, wx.ID_ANY, u"記住學號", wx.DefaultPosition, wx.Size(-1, 20), 0)
        self.m_remember_id_checkbox.SetValue(True)
        self.m_remember_id_checkbox.SetMinSize(wx.Size(-1, 20))
        self.m_remember_id_checkbox.SetMaxSize(wx.Size(-1, 20))

        bSizer16.Add(self.m_remember_id_checkbox, 0, wx.ALL, 5)

        self.m_remember_all_checkbox = wx.CheckBox(self, wx.ID_ANY, u"記住學號密碼", wx.DefaultPosition, wx.Size(-1, 20), 0)
        self.m_remember_all_checkbox.SetMinSize(wx.Size(-1, 20))
        self.m_remember_all_checkbox.SetMaxSize(wx.Size(-1, 20))

        bSizer16.Add(self.m_remember_all_checkbox, 0, wx.ALL, 5)

        bSizer13.Add(bSizer16, 1, wx.EXPAND, 5)

        bSizer21 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_auto_help_checkbox = wx.CheckBox(self, wx.ID_ANY, u"自動輔助", wx.DefaultPosition, wx.Size(-1, 20), 0)
        self.m_auto_help_checkbox.Enable(False)
        self.m_auto_help_checkbox.SetMinSize(wx.Size(-1, 20))
        self.m_auto_help_checkbox.SetMaxSize(wx.Size(-1, 20))

        bSizer21.Add(self.m_auto_help_checkbox, 0, wx.ALL, 5)

        self.m_checkBox7 = wx.CheckBox(self, wx.ID_ANY, u"未知功能", wx.DefaultPosition, wx.Size(-1, 20), 0)
        self.m_checkBox7.Enable(False)
        self.m_checkBox7.SetMinSize(wx.Size(-1, 20))
        self.m_checkBox7.SetMaxSize(wx.Size(-1, 20))

        bSizer21.Add(self.m_checkBox7, 0, wx.ALL, 5)

        bSizer13.Add(bSizer21, 1, wx.EXPAND, 5)

        self.m_description_text = wx.TextCtrl(self, wx.ID_ANY,
                                              u"[特別注意]\n目前記住密碼事先將密碼加密再保存在跟本程式同個位置的user.json檔裡，"
                                              u"所以有一定的安全性在!如果會怕的話，還是建議使用完本程式後，自行把user.json檔刪除"
                                              u"，感謝~",
                                              wx.DefaultPosition, wx.Size(150, 200), wx.TE_MULTILINE | wx.TE_READONLY)
        self.m_description_text.SetFont(
            wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體"))
        self.m_description_text.SetMinSize(wx.Size(150, 200))
        self.m_description_text.SetMaxSize(wx.Size(150, 200))

        bSizer13.Add(self.m_description_text, 0, wx.ALL | wx.EXPAND, 5)

        bSizer18 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer18.SetMinSize(wx.Size(200, 10))
        bSizer20 = wx.BoxSizer(wx.VERTICAL)

        bSizer20.SetMinSize(wx.Size(100, 10))
        self.m_ok_btn = wx.Button(self, wx.ID_OK, u"確定", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_ok_btn.SetDefault()
        bSizer20.Add(self.m_ok_btn, 0, wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.m_cancel_btn = wx.Button(self, wx.ID_CANCEL, u"取消")
        self.m_cancel_btn.SetMinSize(wx.Size(0, 0))
        self.m_cancel_btn.SetMaxSize(wx.Size(0, 0))
        self.m_cancel_btn.SetId(wx.ID_CANCEL)
        bSizer20.Add(self.m_cancel_btn, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer18.Add(bSizer20, 1, wx.EXPAND, 5)

        bSizer13.Add(bSizer18, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer13)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_remember_all_checkbox.Bind(wx.EVT_CHECKBOX, self.remember_all)
        self.m_ok_btn.Bind(wx.EVT_BUTTON, self.user_setting_confirm)

        self.do_load_user_setting()

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def do_load_user_setting(self):
        if self.user_setting_found:
            try:
                self.m_student_id_textctrl.SetValue(self.user_setting['id'])
                self.m_remember_id_checkbox.SetValue(self.user_setting['remember_id'])
                self.m_remember_all_checkbox.SetValue(self.user_setting['remember_all'])
                if self.user_setting['remember_all']:
                    self.m_remember_id_checkbox.SetValue(True)
                    self.m_remember_id_checkbox.Enable(False)
                    new_id = self.m_student_id_textctrl.GetValue()
                    if len(new_id) < 8:
                        new_id = (new_id + 'e6rM39jz')[0:8]
                    elif len(new_id) > 8:
                        new_id = new_id[0:8]
                    try:
                        f = Fernet(str.encode(new_id+encode_code + new_id + "="))
                        self.m_student_pw_textctrl.SetValue(bytes.decode(f.decrypt(str.encode(self.user_setting['pw']))))
                    except InvalidToken:
                        pass
                else:
                    pass
            except KeyError:
                pass

        else:
            pass

    def remember_all(self, event):
        if self.m_remember_all_checkbox.GetValue():
            self.m_remember_id_checkbox.SetValue(True)
            self.m_remember_id_checkbox.Enable(False)
        else:
            self.m_remember_id_checkbox.Enable(True)
        event.Skip()

    def user_setting_confirm(self, event):
        if self.m_student_id_textctrl.GetValue().split(' ')[0]:
            # print(len(self.m_student_pw_textctrl.GetValue()))
            if self.m_remember_all_checkbox.GetValue() and len(self.m_student_pw_textctrl.GetValue())>0:
                new_id = self.m_student_id_textctrl.GetValue().split(' ')[0]

                if len(new_id) < 8:
                    new_id = (new_id + 'e6rM39jz')[0:8]
                elif len(new_id) > 8:
                    new_id = new_id[0:8]

                f = Fernet(str.encode(new_id + encode_code + new_id + "="))
                new_pw = f.encrypt(str.encode(self.m_student_pw_textctrl.GetValue()))
                self.user_setting = {
                    'id': self.m_student_id_textctrl.GetValue().split(' ')[0],
                    'pw': bytes.decode(new_pw),
                    'remember_id': True,
                    'remember_all': True,
                }
            else:
                self.user_setting = {
                    'id': self.m_student_id_textctrl.GetValue().split(' ')[0],
                    'pw': '',
                    'remember_id': True,
                    'remember_all': False,
                }
            with open('user.json', 'w+') as f:
                json.dump(self.user_setting, f)
        else:
            pass
        self.Destroy()
        event.Skip()


class SetScheduleDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"設定排程時間", pos=wx.DefaultPosition, size=wx.Size(260, 150),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體"))

        bSizer27 = wx.BoxSizer(wx.VERTICAL)

        bSizer28 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_schedule_start_date_text = wx.StaticText(self, wx.ID_ANY, u"設定開始日期", wx.DefaultPosition, wx.DefaultSize,
                                                        0)
        self.m_schedule_start_date_text.Wrap(-1)

        self.m_schedule_start_date_text.SetFont(
            wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體"))

        bSizer28.Add(self.m_schedule_start_date_text, 0, wx.ALL, 5)

        self.m_schedule_start_date_picker = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime,
                                                                  wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT)
        self.m_schedule_start_date_picker.SetMinSize(wx.Size(150, -1))
        self.m_schedule_start_date_picker.SetMaxSize(wx.Size(150, -1))

        bSizer28.Add(self.m_schedule_start_date_picker, 0, wx.ALL, 5)

        bSizer27.Add(bSizer28, 1, wx.EXPAND, 5)

        bSizer29 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_schedule_start_time_text = wx.StaticText(self, wx.ID_ANY, u"設定開始時間", wx.DefaultPosition, wx.DefaultSize,
                                                        0)
        self.m_schedule_start_time_text.Wrap(-1)

        self.m_schedule_start_time_text.SetFont(
            wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體"))

        bSizer29.Add(self.m_schedule_start_time_text, 0, wx.ALL, 5)

        self.m_schedule_start_time_picker = wx.adv.TimePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime,
                                                                  wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT)
        self.m_schedule_start_time_picker.SetMinSize(wx.Size(150, -1))
        self.m_schedule_start_time_picker.SetMaxSize(wx.Size(150, -1))

        bSizer29.Add(self.m_schedule_start_time_picker, 0, wx.ALL, 5)

        bSizer27.Add(bSizer29, 1, wx.EXPAND, 5)

        bSizer30 = wx.BoxSizer(wx.VERTICAL)
        bSizer30.SetMinSize(wx.Size(-1, 20))
        self.m_set_schedule_ok_btn = wx.Button(self, wx.ID_OK, u"確定", wx.Point(-1, 25), wx.DefaultSize, 0)
        self.m_set_schedule_ok_btn.SetDefault()
        bSizer30.Add(self.m_set_schedule_ok_btn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_cancel_btn = wx.Button(self, wx.ID_CANCEL, u"取消")
        self.m_cancel_btn.SetId(wx.ID_CANCEL)
        self.m_cancel_btn.SetMinSize(wx.Size(0, 0))
        self.m_cancel_btn.SetMaxSize(wx.Size(0, 0))
        bSizer30.Add(self.m_cancel_btn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer27.Add(bSizer30, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer27)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_set_schedule_ok_btn.Bind(wx.EVT_BUTTON, self.do_set_schedule_ok)


        # print(self.key_code)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def do_set_schedule_ok(self, event):
        self.Destroy()
        event.Skip()
