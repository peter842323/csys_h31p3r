import random
###############################################################################################################
# Setting Class
###############################################################################################################
class Setting:
    def __init__(self):
        #######################################################################################################
        # Basic Setting
        #######################################################################################################

        self.headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / '+str(random.uniform(500, 600))[0:6]
                          + '(KHTML, like Gecko) '
                          'Chrome / '+str(random.uniform(61, 68))[0:5]+'.'+str(random.uniform(0, 9999))[0:8] +
                          'Safari / '+str(random.uniform(500, 600))[0:6],
        }
        self.delay_time = 0.5
        self.retry_time = 600

    def get_header(self):
        return self.headers

    def set_headers(self, _page_id):
        self.headers['Page-Id'] = _page_id


###############################################################################################################
# Static Method
###############################################################################################################
url = 'https://csys.cycu.edu.tw/student/'


def get_url(_referer):
    if _referer == 'login':
        return url + 'sso.srv'
    elif _referer == 'course_view':
        return url + 'student/op/StudentCourseView.srv'
    elif _referer == 'course_trace':
        return url + 'student/op/StudentCourseTrace.srv'
    elif _referer == 'course_time':
        return url + 'student/op/StudentCourseTime.srv'
    elif _referer == 'course_query':
        return url + 'student/op/CourseQuery.srv'


def get_payload(**kwargs):
    payload = {'cmd': kwargs.get('mode')}

    if payload['cmd'] == 'login_init' or payload['cmd'] == 'logout':
        pass

    elif payload['cmd'] == 'login':
        payload['userid'] = kwargs.get('userid')
        payload['hash'] = kwargs.get('hash')

    elif payload['cmd'] == 'selectJson':
        if kwargs.get('idcode'):
            # -200: 登記清單, >0: 修課清單
            if kwargs.get('sn_status') == '=-200' or kwargs.get('sn_status') == '>0' or \
                    kwargs.get('sn_status') == '=-400':
                payload['where'] = 'sn_status'+kwargs.get('sn_status')+' AND idcode=\''+kwargs.get('idcode')+'\''
                payload['orderby'] = 'sn_course_type,op_code' if kwargs.get('sn_status') == '>0' or kwargs.get(
                    'sn_status') == '=-400' else 'sn_course_type,ord,op_code'
            # 功課表
            else:
                payload['where'] = 'idcode=\'' + kwargs.get('idcode') + '\''

        elif kwargs.get('opcode'):
            # 搜尋課程
            payload['where'] = '(op_code=\''+kwargs.get('opcode')+'\') AND (op_type IN (\'一般\',\'人\',\'人哲\',\'公民\',' \
                                                                  '\'天\',\'文學\',\'我\',\'宗哲\',\'延通\',\'法政\',\'物\'' \
                                                                  ',\'科技\',\'科學\',\'英聽\',\'軍訓\',\'軍護\',\'修辭\',' \
                                                                  '\'僑生專班\',\'寫作\',\'學程\',\'歷史\',\'體育\'))'
            payload['orderby'] = 'dept_code,op_code'
            payload['length'] = '10'
        else:
            # 追蹤清單
            pass
    else:
        payload['op_code'] = kwargs.get('opcode')

    # print(payload)
    return payload


def reset_id_pw():
    while True:
        _id = input('Your Student ID: ')
        _pw = input('Your Student Password: ')
        _confirm = input('Do you want to save it? [Y]es/[N]o (default: Yes)\n> ')
        if _confirm == 'N' or _confirm == 'n':
            continue
        else:
            print('Save Successfully!')
            break

    return {'id': _id, 'pw': _pw}


def init_setting():
    _setting = Setting()
    return _setting

