import setting


class Course:
    def __init__(self, _setting, _session, _student_id):
        self.course_setting = _setting
        self.course_session = _session
        self.student_id = _student_id

    def view_reg_list(self, **kwargs):
        # kwargs : mode = 登記、修課
        # 1-1. get user's id
        payload_data = setting.get_payload(mode='selectJson', idcode=self.student_id, sn_status=kwargs.get('sn_status'))
        # 1-2. get other user's id
        if kwargs.get('id'):
            payload_data = setting.get_payload(mode='selectJson', idcode=kwargs.get('id'),
                                               sn_status=kwargs.get('sn_status'))

        # print(payload_data)
        package = self.course_session.post(setting.get_url('course_view'),
                                           data=payload_data,
                                           headers=self.course_setting.get_header())

        # Show raw json data. Need to make its format become beautifier
        # print(package.json())
        return package

    def view_trace_list(self):
        # kwargs : mode = 追蹤
        payload_data = setting.get_payload(mode='selectJson')

        package = self.course_session.post(setting.get_url('course_trace'),
                                           data=payload_data,
                                           headers=self.course_setting.get_header())

        # Show raw json data. Need to make its format become beautifier
        return package

    def view_course_time(self):
        # kwargs : mode = 功課表
        payload_data = setting.get_payload(mode='selectJson', idcode=self.student_id)

        package = self.course_session.post(setting.get_url('course_time'),
                                           data=payload_data,
                                           headers=self.course_setting.get_header())

        # Show raw json data. Need to make its format become beautifier
        return package

    def search_course(self, _op_code):
        payload_data = setting.get_payload(mode='selectJson', opcode=_op_code)
        package = self.course_session.post(setting.get_url('course_query'),
                                           data=payload_data,
                                           headers=self.course_setting.get_header())

        # Show raw json data. Need to make its format become beautifier
        return package

    # 新增追蹤
    def add_trace(self, _op_code):
        package = self.course_session.post(setting.get_url('course_trace'),
                                           data=setting.get_payload(mode='insert', opcode=_op_code),
                                           headers=self.course_setting.get_header())

        return package
        # if package.status_code == 200:
        #else:
        #    return {'result': False}

    # 刪除追蹤
    def delete_trace(self, _op_code):
        package = self.course_session.post(setting.get_url('course_trace'),
                                           data=setting.get_payload(mode='delete', opcode=_op_code),
                                           headers=self.course_setting.get_header())
        # print(package)
        # print(package.json())
        return package

    # 新增登記
    def add_register(self, _op_code):
        package = self.course_session.post(setting.get_url('course_view'),
                                           data=setting.get_payload(mode='addRegister', opcode=_op_code),
                                           headers=self.course_setting.get_header())
        # print(package.json())
        return package

    # 取消登記
    def delete_register(self, _op_code):
        package = self.course_session.post(setting.get_url('course_view'),
                                           data=setting.get_payload(mode='deleteRegister', opcode=_op_code),
                                           headers=self.course_setting.get_header())
        # print(package.json())
        return package

    # 加選
    def add_selection(self, _op_code):
        package = self.course_session.post(setting.get_url('course_view'),
                                           data=setting.get_payload(mode='addSelection', opcode=_op_code),
                                           headers=self.course_setting.get_header())
        return package

    # 退選
    def delete_selection(self, _op_code):
        package = self.course_session.post(setting.get_url('course_view'),
                                           data=setting.get_payload(mode='deleteSelection', opcode=_op_code),
                                           headers=self.course_setting.get_header())
        return package

    # 取消遞補
    def delete_append(self, _op_code):
        package = self.course_session.post(setting.get_url('course_view'),
                                           data=setting.get_payload(mode='deleteAppend', opcode=_op_code),
                                           headers=self.course_setting.get_header())
        return package
