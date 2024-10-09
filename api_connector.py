from requests import get


class API_Connector:
    def __init__(self):
        self.url = "http://api.arefaste.ru/"
        self.id_app = "3"
        self.secret_key = "41572e69-51f6-4639-9994-100e8ee5b9f6"
        # убрать юзер токен
        self.user_token = '9f9bfb39-784d-4de6-bb1a-52bd3dff0e94'

    def get_groups(self):
        response = get(self.url + "system.getApp_data?"+"id_app="+self.id_app+"&secret_key="+self.secret_key)
        result = response.json()
        print("get_groups: " + str(response))
        groups = result['response']['groups']['3'] # 3 - это айди института
        return groups

    def get_lessons(self, group):
        response = get(self.url + "timetable.getLesson?"+"user_token="+self.user_token)
        result = response.json()
        print("get_lessons: " + str(response))
        lessons = result['response']['rows']
        return lessons

    def get_teachers(self, group):
        response = get(self.url + "timetable.getTeacher?"+"user_token="+self.user_token)
        result = response.json()
        print("get_teachers: " + str(response))
        teachers = result['response']['rows']
        return teachers


