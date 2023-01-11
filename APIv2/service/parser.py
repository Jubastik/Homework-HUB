import json

import requests
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

import my_err
from database.db_session import get_session
from database.parsers import Parser
from schemas.parser_pdc import ParserCreate


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
