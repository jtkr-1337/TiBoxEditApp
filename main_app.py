import datetime
import json

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QTreeWidgetItem
from pydantic import ValidationError

from api_connector import API_Connector
from main_logic import Logic, Row, ListWidgetItem
from error_dialog import ErrorDialog


def getListName(arr):
    name = []
    for i in arr:
        name.append(i['name'])
    return name


def getLessonId(arr):
    id = []
    for i in arr:
        id.append(i['id_lesson'])
    return id


def getTeacherId(arr):
    id = []
    for i in arr:
        id.append(i['id_teacher'])
    return id


def get_week_type_id(name):
    if name == Logic.WeekType.up.value["name"]:
        return Logic.WeekType.up.value["id"]
    elif name == Logic.WeekType.down.value["name"]:
        return Logic.WeekType.down.value["id"]
    elif name == Logic.WeekType.any.value["name"]:
        return Logic.WeekType.any.value["id"]
    else:
        print("Error get_week_type_id()")
        return "error"


def get_time(name):
    if name == Logic.Time.fst.value["name"]:
        return Logic.Time.fst.value
    elif name == Logic.Time.snd.value["name"]:
        return Logic.Time.snd.value
    elif name == Logic.Time.trd.value["name"]:
        return Logic.Time.trd.value
    elif name == Logic.Time.frth.value["name"]:
        return Logic.Time.frth.value
    elif name == Logic.Time.ffth.value["name"]:
        return Logic.Time.ffth.value
    else:
        print("error get_time()")
        return {"name": "error", "up_date": "", "delta": ""}


def get_time_index(time):
    if time == Logic.Time.fst.value["up_date"]:
        return Logic.Time.fst.value["id"]
    if time == Logic.Time.snd.value["up_date"]:
        return Logic.Time.snd.value["id"]
    if time == Logic.Time.trd.value["up_date"]:
        return Logic.Time.trd.value["id"]
    if time == Logic.Time.frth.value["up_date"]:
        return Logic.Time.frth.value["id"]
    if time == Logic.Time.ffth.value["up_date"]:
        return Logic.Time.ffth.value["id"]
    if time == Logic.Time.none.value["up_date"]:
        return Logic.Time.none.value["id"]


def valid_row(data: dict):
    try:
        row = Row(**data)
        return row
    except ValidationError as e:
        print("error valid_row(): " + str(e))
        return False


class MainApp:
    def __init__(self):
        self.added_days_name = []
        self.rows = []
        self.lesson_id = None
        self.lesson_name = None
        self.teacher_id = None
        self.teacher_name = None
        self.win = uic.loadUi("ui/main_gui.ui")
        self.api = API_Connector()
        self.group = ''
        self.lessons = []
        self.teachers = []
        self.error_dialog = ErrorDialog()
        self.start_date = None
        self.date_now = self.win.end_calendar.selectedDate()

    def show(self, group):
        self.group = group
        self.api_requests()
        self.lesson_id = getLessonId(self.lessons)
        self.lesson_name = getListName(self.lessons)
        self.teacher_id = getTeacherId(self.teachers)
        self.teacher_name = getListName(self.teachers)

        self.fill_widgets()
        self.connect_widgets()

        self.win.show()

    def api_requests(self):
        self.lessons = self.api.get_lessons(self.group['id'])
        self.teachers = self.api.get_teachers(self.group['id'])

    def fill_widgets(self):
        self.win.group_label.setText(self.group['text'])
        self.win.subject_name_lw.addItems(self.lesson_name)
        self.win.subject_time_cb.addItems([Logic.Time.fst.value['name'], Logic.Time.snd.value['name'],
                                           Logic.Time.trd.value['name'], Logic.Time.frth.value['name'],
                                           Logic.Time.ffth.value['name'], Logic.Time.none.value['name']])
        self.win.subject_teacher_cb.addItems(self.teacher_name)
        self.win.subject_type_cb.addItems([Logic.Type.lecture.value, Logic.Type.practice.value,
                                           Logic.Type.session.value, Logic.Type.none.value])
        self.win.subject_week_number_cb.addItems([Logic.WeekType.up.value['name'],
                                                  Logic.WeekType.down.value['name'],
                                                  Logic.WeekType.any.value['name']])

        date = self.date_now
        if date.month() < 8:
            date.setDate(date.year(), 1, 1)
        else:
            date.setDate(date.year(), 9, 1)

        self.win.start_calendar.setSelectedDate(date)
        self.start_date = date
        root = self.win.day_tw.invisibleRootItem()
        root.child(0).setExpanded(True)
        root.child(1).setExpanded(True)
        root.child(0).child(0).setSelected(True)

    def connect_widgets(self):
        # todo добавить проверку кастомного времени
        self.win.subject_name_le.textChanged.connect(self.filter_list)
        self.win.checkBox.stateChanged.connect(self.change_state_tab)

        self.win.day_tw.itemSelectionChanged.connect(self.day_selected)
        self.win.subject_list.itemClicked.connect(self.subject_selected)

        self.win.subjectAddButton.clicked.connect(self.create_lesson)
        self.win.subjectEditButton.clicked.connect(self.edit_lesson)

        self.win.SaveFileButton.clicked.connect(self.save_file)
        self.win.LoadFileButton.clicked.connect(self.load_file)

    def save_file(self):
        # todo добавить выбор места сохранения
        data = """{"rows":["""
        for i in self.rows:
            data += json.dumps(i.model_dump(), default=str, ensure_ascii=False) + ","
        data = data[:-1]
        data += """]}"""
        with open("timetable.json", "w", encoding='utf8') as f:
            f.write(data)
            print("file saved")

    def load_file(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self.win, "Choose file", "./",
                                                     "JSON files (*.json)")
        with open(path[0], "r", encoding='utf8') as f:
            data = f.read()
            data = json.loads(data)
            data = data["rows"]
            self.clear_all()
            # for i in data:
            #     row = valid_row(row)
            #     if row:
            #         self.rows.append(row)
            #         item = ListWidgetItem(self.generate_title(row), row.gid)
            #         self.win.subject_list.addItem(item)
            #         self.win.subject_list.item(len(self.rows)-1).setSelected(True)
            #         self.create_day()
    #         todo доделать

    def clear_all(self):
        root = self.win.day_tw.invisibleRootItem()
        self.win.day_tw.takeTopLevelItem(1)
        day = QTreeWidgetItem(root)
        day.setText(0, "Added days")

        self.win.subject_list.clear()

        self.rows = []

    def create_lesson(self):
        if len(self.win.subject_name_lw.selectedItems()) > 0:
            row = dict()
            row["id_lesson"] = int(
                self.lesson_id[self.lesson_name.index(self.win.subject_name_lw.selectedItems()[0].text())])
            row["id_group"] = self.group["id"]
            row["id_teacher"] = int(self.teacher_id[self.teacher_name.index(self.win.subject_teacher_cb.currentText())])
            row["date"] = self.get_date()
            time = get_time(self.win.subject_time_cb.currentText())
            row["up_date"] = time["up_date"]
            row["delta"] = time["delta"]

            if self.win.checkBox.isChecked():
                row["date_end"] = self.win.end_calendar.selectedDate().toPyDate()

            if len(self.win.subject_description_tb.toPlainText()) > 0:
                row["info"] = self.win.subject_description_tb.toPlainText()

            row["addiction"] = self.win.subject_type_cb.currentText()
            row["date_start"] = self.win.start_calendar.selectedDate().toPyDate()

            row = valid_row(row)
            if row:
                self.rows.append(row)
                item = ListWidgetItem(self.generate_title(row), row.gid)
                self.win.subject_list.addItem(item)
                self.win.subject_list.item(len(self.rows)-1).setSelected(True)
                self.create_day()
        else:
            self.error_dialog.show()

    def edit_lesson(self):
        lesson = self.win.subject_list.selectedItems()[0]
        for i in range(len(self.rows)):
            new_row = self.rows[i]
            self.win.subject_list.takeItem(self.win.subject_list.row(lesson))
            if new_row.gid == lesson.gid:
                if len(self.win.subject_name_lw.selectedItems()) > 0:
                    new_row = dict()
                    new_row["gid"] = lesson.gid
                    new_row["id_lesson"] = int(
                        self.lesson_id[self.lesson_name.index(self.win.subject_name_lw.selectedItems()[0].text())])
                    new_row["id_group"] = self.group["id"]
                    new_row["id_teacher"] = int(
                        self.teacher_id[self.teacher_name.index(self.win.subject_teacher_cb.currentText())])
                    new_row["date"] = self.get_date()
                    time = get_time(self.win.subject_time_cb.currentText())
                    new_row["up_date"] = time["up_date"]
                    new_row["delta"] = time["delta"]

                    if self.win.checkBox.isChecked():
                        new_row["date_end"] = self.win.end_calendar.selectedDate().toPyDate()

                    if len(self.win.subject_description_tb.toPlainText()) > 0:
                        new_row["info"] = self.win.subject_description_tb.toPlainText()

                    new_row["addiction"] = self.win.subject_type_cb.currentText()
                    new_row["date_start"] = self.win.start_calendar.selectedDate().toPyDate()

                    new_row = valid_row(new_row)
                    if new_row:
                        self.rows[i] = new_row
                        item = ListWidgetItem(self.generate_title(new_row), new_row.gid)
                        # self.win.subject_list.insertItem(i, item)
                        self.win.subject_list.addItem(item)
                        self.win.subject_list.item(len(self.rows)-1).setSelected(True)
                        self.create_day()
                else:
                    self.error_dialog.show()

    def get_date(self):
        date = self.win.start_calendar.selectedDate().toPyDate()
        if self.start_date.toPyDate() < date:
            return date
        else:
            day = self.win.day_tw.selectedItems()[0].text(0)
            if day in Logic.WeekDay.array_num.value:
                return datetime.date(year=1,
                                     month=int(get_week_type_id(self.win.subject_week_number_cb.currentText())),
                                     day=int(
                                         Logic.WeekDay.array_num.value.index(day)))
            else:
                return datetime.date(year=1,
                                     month=int(day[5:7]),
                                     day=int(day[8:10]))

    def create_day(self):
        date = self.win.day_tw.selectedItems()[0].text(0)
        if date in Logic.WeekDay.array_num.value:
            # todo перепроверить даты, тк тут изменил формат создания
            date = self.get_date().strftime("%Y-%m-%d")
        if not self.check_day_exists(date):
            self.added_days_name.append(date)
            root = self.win.day_tw.invisibleRootItem()
            day = QTreeWidgetItem(root.child(1))
            day.setText(0, date)

    def change_state_tab(self):
        if self.win.checkBox.isChecked():
            self.win.tab_2.setEnabled(True)
            self.win.end_calendar.setEnabled(True)
        else:
            self.win.end_calendar.showToday()
            self.win.end_calendar.setSelectedDate(self.date_now)
            self.win.tab_2.setEnabled(False)
            self.win.end_calendar.setEnabled(False)

    def day_selected(self):
        day = self.win.day_tw.selectedItems()[0]
        match day.text(0):
            case Logic.WeekDay.mon.value:
                self.fill_args_day(1, True)
            case Logic.WeekDay.tue.value:
                self.fill_args_day(2, True)
            case Logic.WeekDay.wed.value:
                self.fill_args_day(3, True)
            case Logic.WeekDay.thu.value:
                self.fill_args_day(4, True)
            case Logic.WeekDay.fri.value:
                self.fill_args_day(5, True)
            case Logic.WeekDay.sat.value:
                self.fill_args_day(6, True)
            case Logic.WeekDay.sun.value:
                self.fill_args_day(7, True)
            case _:
                if day.text(0) in self.added_days_name:
                    self.fill_args_day(day.text(0), False)

    def subject_selected(self, item):
        gid = item.gid
        for row in self.rows:
            if row.gid == gid:
                self.fill_args_lesson(row)
                break

    def fill_args_day(self, index, flag):
        self.clear_args()
        if not flag:
            y = int(index[:4])
            m = int(index[5:7])
            d = int(index[8:10])
            date = datetime.date(year=y, month=m, day=d)
            fst = True
            for i in self.rows:
                if date == i.date:
                    item = ListWidgetItem(self.generate_title(i), i.gid)
                    self.win.subject_list.addItem(item)
                    if fst:
                        self.fill_args_lesson(i)
                        self.win.subject_list.item(0).setSelected(True)
                        fst = False

    def generate_title(self, i):
        time = datetime.timedelta(hours=i.up_date.hour, minutes=i.up_date.minute)
        time += datetime.timedelta(hours=i.delta.hour, minutes=i.delta.minute)
        title = (str(i.up_date)[:5] + "-" + str(time)[:5] + " | " +
                 self.lesson_name[self.lesson_id.index(i.id_lesson)])
        return title

    def fill_args_lesson(self, i):
        self.win.subject_name_le.setText(self.lesson_name[self.lesson_id.index(i.id_lesson)])
        self.filter_list()
        self.win.subject_name_lw.item(0).setSelected(True)

        self.win.subject_time_cb.setCurrentIndex(get_time_index(i.up_date))
        self.win.subject_teacher_cb.setCurrentIndex(self.teacher_id.index(i.id_teacher))
        self.win.subject_type_cb.setCurrentIndex(Logic.Type.array_index.value.index(i.addiction))
        self.win.subject_week_number_cb.setCurrentIndex(3 - int(i.date.month))

        if len(i.info) > 0:
            self.win.subject_description_tb.setPlainText(i.info)

        date = i.date_start
        new_date = self.win.start_calendar.selectedDate()
        new_date.setDate(date.year, date.month, date.day)
        self.win.start_calendar.setSelectedDate(new_date)

        if i.date_end is not None:
            self.win.checkBox.setChecked(True)
            date = i.date_end
            new_date = self.win.start_calendar.selectedDate()
            new_date.setDate(date.year, date.month, date.day)
            self.win.start_calendar.setSelectedDate(new_date)

    def clear_args(self):
        self.win.subject_name_le.setText("")

        self.win.subject_name_lw.clear()
        self.win.subject_name_lw.addItems(self.lesson_name)

        self.win.subject_time_cb.setCurrentIndex(0)
        self.win.subject_teacher_cb.setCurrentIndex(0)
        self.win.subject_type_cb.setCurrentIndex(0)
        self.win.subject_week_number_cb.setCurrentIndex(0)
        self.win.subject_description_tb.setPlainText("")
        self.win.start_calendar.setSelectedDate(self.start_date)
        self.win.checkBox.setChecked(False)
        self.win.tab_2.setEnabled(False)
        self.win.end_calendar.showToday()
        self.win.end_calendar.setSelectedDate(self.date_now)
        self.win.subject_list.clear()

    def filter_list(self):
        search_text = self.win.subject_name_le.text().lower()
        self.win.subject_name_lw.clear()
        for item in self.lesson_name:
            if search_text in item.lower():
                self.win.subject_name_lw.addItem(item)

    def check_day_exists(self, date):
        if date in self.added_days_name:
            return True
        else:
            return False
