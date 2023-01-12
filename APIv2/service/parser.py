import datetime
import json
from pprint import pprint

import requests
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

import my_err
from database.classes import Class
from database.db_session import get_session
from database.lessons import Lesson
from database.parsers import Parser
from database.schedules import Schedule
from database.students import Student
from database.time_tables import TimeTable
from database.week_days import WeekDay
from schemas.parser_pdc import ParserCreate, ParserHomeworkReturn
from service.CONSTANTS import day_id_to_weekday


class ParserService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json",
        }

    def get_p_educations_and_p_group_ids(self, parser: Parser) -> tuple[int, int]:
        cookies = {"X-JWT-Token": parser.x_jwt_token}
        if parser.platform_id == 1:
            r = requests.get(
                "https://dnevnik2.petersburgedu.ru/api/journal/person/related-child-list",
                cookies=cookies,
                headers=self.headers,
            )
            if r.status_code != status.HTTP_200_OK:
                return 0, 0
            data = r.json()
            education_id = data["data"]["items"][0]["educations"][0]["education_id"]
            group_id = data["data"]["items"][0]["educations"][0]["group_id"]
            return education_id, group_id

    def clarify_parsers(self, student_id: int):
        parsers = self.session.query(Parser).filter(Parser.student_id == student_id).all()
        for parser in parsers:
            education_id, group_id = self.get_p_educations_and_p_group_ids(parser)
            if education_id == 0 or group_id == 0:
                parser.active = False
            elif parser.active is False:
                parser.active = True
        self.session.commit()
        return parsers

    def create_parser(self, student_id: int, parser_data: ParserCreate):
        parsers = (
            self.session.query(Parser)
            .filter(Parser.student_id == student_id, Parser.platform_id == parser_data.platform_id)
            .all()
        )
        for parser in parsers:
            self.session.delete(parser)
        self.session.commit()
        if parser_data.platform_id == 1:
            payload = json.dumps(
                {
                    "login": parser_data.login,
                    "password": parser_data.password,
                    "type": "email",
                    "_isEmpty": False,
                    "activation_code": None,
                }
            )
            r = requests.post(
                "https://dnevnik2.petersburgedu.ru/api/user/auth/login",
                headers=self.headers,
                data=payload,
            )
            if r.status_code != status.HTTP_200_OK:
                raise my_err.APIError(status.HTTP_400_BAD_REQUEST, my_err.LoginError, "Invalid mail or password")
            data = r.json()
            x_jwt_token = data["data"]["token"]
            parser = Parser(
                student_id=student_id,
                platform_id=parser_data.platform_id,
                x_jwt_token=x_jwt_token,
            )
            self.session.add(parser)
            self.session.commit()
            return parser
        raise my_err.APIError(status.HTTP_400_BAD_REQUEST, my_err.IN_DEVELOPMENT, "Unknown platform_id")

    def _get_day_and_number(self, student_id, name, hwdate: datetime.date):
        # Получает название урока, дату урока. Возвращает дату предыдущего урока и номер урока
        schedules = (
            self.session.query(Schedule.day_id, TimeTable.number_of_lesson)
            .join(Lesson)
            .join(TimeTable)
            .join(Class)
            .join(Student)
            .filter(Student.id == student_id, Lesson.name == name)
            .order_by(Schedule.day_id)
            .all()
        )
        days = [_[0] for _ in schedules]
        now = hwdate.weekday() + 1
        for i in range(now - 1, -1, -1):
            if i in days:
                return hwdate - datetime.timedelta(days=now - i), [_[1] for _ in schedules if _[0] == i]
        for i in range(6, now + 1, -1):
            if i in days:
                return hwdate - datetime.timedelta(days=now + (7 - i)), [_[1] for _ in schedules if _[0] == i]
        return hwdate - datetime.timedelta(days=7), [_[1] for _ in schedules if _[0] == i]

    def get_pars_homework(self, student_id, hwdate: datetime.date):
        weekday = day_id_to_weekday[hwdate.weekday()]

        lessons_in_day = (
            self.session.query(Schedule)
            .join(WeekDay)
            .join(Class)
            .join(Student)
            .filter(WeekDay.name == weekday, Student.id == student_id)
            .all()
        )
        lessons_name = list(set([lesson.lesson.name for lesson in lessons_in_day]))
        if len(lessons_name) == 0:
            return []
        date_num = []
        for name in lessons_name:
            date_num.append((name, *self._get_day_and_number(student_id, name, hwdate)))
        date_num = [(_[0], _[1].strftime("%d.%m.%Y"), _[2]) for _ in date_num]
        d_min, d_max = (
            min(date_num, key=lambda x: x[1])[1],
            max(date_num, key=lambda x: x[1])[1],
        )

        parser = self.session.query(Parser).filter(Parser.student_id == student_id, Parser.active == True).first()
        if parser is None:
            # временно
            raise my_err.APIError(status.HTTP_400_BAD_REQUEST, my_err.ParserNotFound, "No active parser")
        education_id, group_id = self.get_p_educations_and_p_group_ids(parser)
        if education_id == 0 or group_id == 0:
            raise my_err.APIError(status.HTTP_400_BAD_REQUEST, my_err.ParserNotFound, "Token expired")

        cookies = {"X-JWT-Token": parser.x_jwt_token}

        r = requests.get(
            f"https://dnevnik2.petersburgedu.ru/api/journal/lesson/list-by-education?p_limit=3000&p_datetime_from={d_min}&p_datetime_to={d_max}&p_educations%5B%5D={education_id}&p_group_ids%5B%5D={group_id}",
            cookies=cookies,
            headers=self.headers,
        )
        if r.status_code != status.HTTP_200_OK:
            raise my_err.APIError(status.HTTP_400_BAD_REQUEST, my_err.LoginError, "Token expired")
        data = r.json()["data"]["items"]
        return_data = []
        for ed_lesson in data:
            for db_lesson in date_num:
                if db_lesson[1] == ed_lesson["datetime_from"][0:10] and ed_lesson["number"] in db_lesson[2]:
                    all_hw = []
                    for hw in ed_lesson["tasks"]:
                        all_hw.append(hw["task_name"])
                    return_data.append(
                        ParserHomeworkReturn(
                            subject=ed_lesson["subject_name"],
                            date=ed_lesson["datetime_from"][0:10],
                            text="+".join(all_hw),
                        )
                    )

        return return_data
