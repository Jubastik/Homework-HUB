import datetime
import json
import logging

import requests
from fastapi import Depends
from sentry_sdk import capture_exception
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
from schemas.parser_pdc import ParserCreate, ParserHomeworkReturn, ParserHomeworkInfoReturn
from service.CONSTANTS import day_id_to_weekday

ed_ses = requests.Session()


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
            r = ed_ses.get(
                "https://dnevnik2.petersburgedu.ru/api/journal/person/related-child-list",
                cookies=cookies,
                headers=self.headers,
            )
            logging.warning(f"Запрос на сервер в get_p_educations_and_p_group_ids. User id: {parser.student_id}")
            if r.status_code not in [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED]:
                capture_exception(
                    my_err.APIError(status.HTTP_500_INTERNAL_SERVER_ERROR, my_err.ParserAccessError, "Access error")
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

    def get_user_with_ed(self, student_id: int):
        if (
            self.session.query(Parser).filter(Parser.student_id == student_id, Parser.active == True).first()
            is not None
        ):
            return student_id

        my_class = self.session.query(Class).join(Student).filter(Student.id == student_id).first()
        students = [st.id for st in my_class.student]
        parser = self.session.query(Parser).filter(Parser.student_id.in_(students), Parser.active == True).first()
        if not parser:
            raise my_err.APIError(status.HTTP_400_BAD_REQUEST, my_err.ParserNotFound, "Class has no active parser")
        return parser.student_id

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
            r = ed_ses.post(
                "https://dnevnik2.petersburgedu.ru/api/user/auth/login",
                headers=self.headers,
                data=payload,
            )
            logging.warning(f"Запрос на сервер в create_parser. User id: {student_id}")
            if r.status_code == status.HTTP_400_BAD_REQUEST:
                raise my_err.APIError(status.HTTP_400_BAD_REQUEST, my_err.ParserLoginError, "Invalid mail or password")
            elif r.status_code != status.HTTP_200_OK:
                capture_exception(
                    my_err.APIError(status.HTTP_500_INTERNAL_SERVER_ERROR, my_err.ParserAccessError, "Access error")
                )
                raise my_err.APIError(status.HTTP_500_INTERNAL_SERVER_ERROR, my_err.ParserAccessError, "Access error")
            data = r.json()
            x_jwt_token = data["data"]["token"]
            parser = Parser(
                student_id=student_id,
                platform_id=parser_data.platform_id,
                x_jwt_token=x_jwt_token,
            )
            self.session.add(parser)
            self.session.commit()
            education_id, group_id = self.get_p_educations_and_p_group_ids(parser)
            parser.education_id = education_id
            parser.group_id = group_id
            self.session.commit()
            return parser
        raise my_err.APIError(status.HTTP_400_BAD_REQUEST, my_err.IN_DEVELOPMENT, "Unknown platform_id")

    def delete_parser(self, student_id, parser_type):
        parsers = (
            self.session.query(Parser).filter(Parser.student_id == student_id, Parser.platform_id == parser_type).all()
        )
        for parser in parsers:
            self.session.delete(parser)
        self.session.commit()
        return True

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

        return hwdate - datetime.timedelta(days=7), [_[1] for _ in schedules if _[0] == now]

    def _fetch_hw_from_ed(self, json_data, date_num) -> list[ParserHomeworkInfoReturn]:
        data = json_data["data"]["items"]
        return_data = []
        for ed_lesson in data:
            for db_lesson in date_num:
                if db_lesson[1] == ed_lesson["datetime_from"][0:10] and ed_lesson["number"] in db_lesson[2]:
                    all_hw = []
                    for hw in ed_lesson["tasks"]:
                        all_hw.append(hw["task_name"])
                    if len(all_hw) != 0:
                        return_data.append(
                            ParserHomeworkInfoReturn(
                                subject=ed_lesson["subject_name"],
                                date=ed_lesson["datetime_from"][0:10],
                                text="+".join(all_hw),
                            )
                        )
        return return_data

    def get_pars_homework(self, student_id, hwdate: datetime.date):
        weekday = day_id_to_weekday[hwdate.weekday()]
        student = self.session.query(Student).filter(Student.id == student_id).first()

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
            return ParserHomeworkReturn(author=student, homework=[])
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
        if parser.education_id is not None and parser.group_id is not None:
            education_id, group_id = parser.education_id, parser.group_id
        else:
            education_id, group_id = self.get_p_educations_and_p_group_ids(parser)
            if education_id == 0 or group_id == 0:
                raise my_err.APIError(status.HTTP_400_BAD_REQUEST, my_err.ParserLoginError, "Token expired")

        cookies = {"X-JWT-Token": parser.x_jwt_token}

        r = ed_ses.get(
            f"https://dnevnik2.petersburgedu.ru/api/journal/lesson/list-by-education?p_limit=3000&p_datetime_from={d_min}&p_datetime_to={d_max}&p_educations%5B%5D={education_id}&p_group_ids%5B%5D={group_id}",
            cookies=cookies,
            headers=self.headers,
        )
        logging.warning(f"Запрос на сервер в get_pars_homework. User id: {student_id}")
        if r.status_code != status.HTTP_200_OK:
            capture_exception(my_err.APIError(status.HTTP_400_BAD_REQUEST, my_err.ParserLoginError, "Token expired"))
            raise my_err.APIError(status.HTTP_400_BAD_REQUEST, my_err.ParserLoginError, "Token expired")
        parser.x_jwt_token = r.cookies["X-JWT-Token"]
        self.session.commit()
        return_data = self._fetch_hw_from_ed(r.json(), date_num)
        return_data = ParserHomeworkReturn(author=student, homework=return_data)
        return return_data
