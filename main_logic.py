import datetime
import enum
import uuid
from typing import Optional

from PyQt5.QtWidgets import QListWidgetItem
from pydantic import BaseModel, Field


class Logic:

    class Time(enum.Enum):
        fst = {"name": "Первая пара", "up_date": datetime.time(hour=9), "delta": datetime.time(hour=1, minute=30), "id": 0}
        snd = {"name": "Вторая пара", "up_date": datetime.time(hour=10, minute=40), "delta": datetime.time(hour=1, minute=30), "id": 1}
        trd = {"name": "Третья пара", "up_date": datetime.time(hour=12, minute=10), "delta": datetime.time(hour=1, minute=30), "id": 2}
        frth = {"name": "Четвертая пара", "up_date": datetime.time(hour=14, minute=20), "delta": datetime.time(hour=1, minute=30), "id": 3}
        ffth = {"name": "Пятая пара", "up_date": datetime.time(hour=16), "delta": datetime.time(hour=1, minute=30), "id": 4}
        none = {"name": "Кастомное время", "up_date": datetime.time(), "delta": datetime.time(), "id": 5}

    class Type(enum.Enum):
        lecture = "ЛК"
        practice = "лаб"
        session = "сессия"
        none = "---"
        array_index = [lecture, practice, session, none]

    class WeekType(enum.Enum):
        up = {"id": "3", "name": "Верхняя"}
        down = {"id": "2", "name": "Нижняя"}
        any = {"id": "1", "name": "Любая"}

    class WeekDay(enum.Enum):
        mon = "Monday"
        tue = "Tuesday"
        wed = "Wednesday"
        thu = "Thursday"
        fri = "Friday"
        sat = "Saturday"
        sun = "Sunday"
        array_num = [0, mon, tue, wed, thu, fri, sat, sun]


class Row(BaseModel):
    gid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    id_lesson: int
    id_group: int
    # todo добавить возможность добавлять нескольких преподавателей
    id_teacher: int
    date: datetime.date = Field(default=..., description="Стандартная дата, определяющая день и неделю, вида:" 
                                                         "\t0001-XX-YY\n\tXX:\t01 - any,\n\t\t02 - down,\n\t\t03 - up"
                                                         "\n\tYY:\t01 - mon,\n\t\t...\n\t\t07 - sun")
    up_date: datetime.time = Field(default=..., description="Время начала пары")
    delta: datetime.time = Field(default=datetime.time(hour=1, minute=30), description="Продолжительность пары")
    date_end: Optional[datetime.date] = Field(default=None, description="Опциональный параметр для определения даты "
                                                                       "окончания для пары")
    info: Optional[str] = Field(default="", description="Параметр для информации, например для номера аудитории")
    addiction: Optional[str] = Field(default="NULL::character varying", max_length=50,
                                     description="Параметр для доп. информации, например тип пары (ЛК, лаб, сессия)")
    date_start: datetime.date = Field(default=..., description="Дата начала проведения пары")


class ListWidgetItem(QListWidgetItem):
    def __init__(self, text, gid):
        super().__init__(text)
        self.gid = gid
