import wx
import wx.xrc
import json
import setting
from login import Login


class GuiLogin(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Login", pos=wx.DefaultPosition, size=wx.Size(296, 300),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.user_setting_found = True
        try:
            with open('user.json', 'r+') as f:
                self.user_setting = json.load(f)
        except FileNotFoundError:
            self.user_setting_found = False

        self.app_setting = setting.init_setting()
        self.console_login = Login(self.app_setting)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微軟正黑體"))
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTIONTEXT))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        gSizer2 = wx.GridSizer(4, 2, 0, 0)

        self.m_id_label = wx.StaticText(self, wx.ID_ANY, u"學號", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_id_label.Wrap(-1)

        gSizer2.Add(self.m_id_label, 0, wx.ALL, 5)

        self.m_id_textctrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.m_id_textctrl, 0, wx.ALL, 5)

        self.m_pw_label = wx.StaticText(self, wx.ID_ANY, u"密碼", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_pw_label.Wrap(-1)

        gSizer2.Add(self.m_pw_label, 0, wx.ALL, 5)

        self.m_pw_textctrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                         wx.TE_PASSWORD)
        gSizer2.Add(self.m_pw_textctrl, 0, wx.ALL, 5)

        self.m_remember_id_checkbox = wx.CheckBox(self, wx.ID_ANY, u"記住學號", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_remember_id_checkbox.SetValue(True)
        gSizer2.Add(self.m_remember_id_checkbox, 0, wx.ALL, 5)

        self.m_remember_all_checkbox = wx.CheckBox(self, wx.ID_ANY, u"記住學號/密碼", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.m_remember_all_checkbox, 0, wx.ALL, 5)

        self.m_reset_button = wx.Button(self, wx.ID_ANY, u"清除重填", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.m_reset_button, 0, wx.ALL, 5)

        self.m_login_button = wx.Button(self, wx.ID_ANY, u"登入", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_login_button.Enable(False)

        gSizer2.Add(self.m_login_button, 0, wx.ALL, 5)

        self.SetSizer(gSizer2)
        self.Layout()
        self.m_login_init_statusbar = self.CreateStatusBar(2, wx.STB_SIZEGRIP, wx.ID_ANY)
        self.m_login_init_statusbar.SetStatusWidths([-1, -3])
        self.m_login_init_statusbar.SetStatusText("系統狀態", 0)
        # self.m_login_init_statusbar.SetStatusText(self.login_init(), 1)
        self.Centre(wx.BOTH)

        # Connect Events
        self.m_id_textctrl.Bind(wx.EVT_TEXT, self.id_pw_written)
        self.m_pw_textctrl.Bind(wx.EVT_TEXT, self.id_pw_written)
        self.m_remember_all_checkbox.Bind(wx.EVT_CHECKBOX, self.remember_all)
        self.m_reset_button.Bind(wx.EVT_BUTTON, self.reset_all)
        self.m_login_button.Bind(wx.EVT_BUTTON, self.login)
        self.m_login_init_statusbar.Bind(wx.EVT_PAINT, self.server_status_timer_start)

        self.server_status_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.server_status_timer_ontimer, self.server_status_timer)

        self.load_user_setting()

    def __del__(self):
        pass

        # Virtual event handlers, overide them in your derived class

    def load_user_setting(self):
        if self.user_setting_found:
            self.m_id_textctrl.SetValue(self.user_setting['id'])
            self.m_pw_textctrl.SetValue(self.user_setting['pw'])
            self.m_remember_id_checkbox.SetValue(self.user_setting['remember_id'])
            self.m_remember_all_checkbox.SetValue(self.user_setting['remember_all'])
        else:
            pass

    def server_status_timer_start(self, event):
        self.server_status_timer.Start(1000)  # 設定時間間隔為1000毫秒,並啟動定時器
        event.Skip()

    def server_status_timer_stop(self, event):
        self.server_status_timer.Stop()
        event.Skip()

    def server_status_timer_ontimer(self, event):  # 顯示時間事件處理函數
        self.console_login.login_init()
        if self.console_login.check_status():
            self.server_status_timer_stop(event)
            print(self.console_login.init_message)
            self.m_login_init_statusbar.SetStatusText('選課系統開放中!', 1)
        else:
            print(self.console_login.init_message)
            self.m_login_init_statusbar.SetStatusText(self.console_login.init_message, 1)
        event.Skip()

    def id_pw_written(self, event):
        # print(self.m_id_textctrl.GetValue())
        # print(self.m_pw_textctrl.GetValue())
        if len(self.m_id_textctrl.GetValue()) > 0 and len(self.m_pw_textctrl.GetValue()) > 0 and \
               self.console_login.check_status():
            self.m_login_button.Enable()
        else:
            self.m_login_button.Enable(False)
        event.Skip()

    def remember_all(self, event):
        if self.m_remember_all_checkbox.GetValue():
            self.m_remember_id_checkbox.SetValue(True)
            self.m_remember_id_checkbox.Enable(False)
        else:
            self.m_remember_id_checkbox.Enable(True)
        event.Skip()

    def reset_all(self, event):
        self.m_id_textctrl.SetValue("")
        self.m_pw_textctrl.SetValue("")
        self.m_remember_id_checkbox.SetValue(False)
        self.m_remember_all_checkbox.SetValue(False)
        event.Skip()

    def login(self, event):
        self.console_login.login_init()
        if self.console_login.check_status():
            # self.console_login.login(self.m_id_textctrl.GetValue(), self.m_pw_textctrl.GetValue())
            self.user_setting = {
                'id': self.m_id_textctrl.GetValue(),
                'pw': self.m_pw_textctrl.GetValue(),
                'remember_id': self.m_remember_id_checkbox.GetValue(),
                'remember_all': self.m_remember_all_checkbox.GetValue(),
            }
            with open('user.json', 'w+') as f:
                json.dump(self.user_setting, f)
        else:
            self.server_status_timer_start(event)
        event.Skip()


if __name__ == '__main__':
    app = wx.App(False)
    test = GuiLogin(None)
    test.Show(True)
    app.MainLoop()