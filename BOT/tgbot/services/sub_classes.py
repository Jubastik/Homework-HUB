class SheduleData:
    def __init__(self):
        # fmt: off
        self.shedule = {
            0: {
                "day_name": "Понедельник",
                "day_tag": "monday",
                "shedule": {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: ""},
            },
            1: {
                "day_name": "Вторник",
                "day_tag": "tuesday",
                "shedule": {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: ""},
            },
            2: {
                "day_name": "Среда",
                "day_tag": "wednesday",
                "shedule": {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: ""},
            },
            3: {
                "day_name": "Четверг",
                "day_tag": "thursday",
                "shedule": {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: ""},
            },
            4: {
                "day_name": "Пятница",
                "day_tag": "friday",
                "shedule": {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: ""},
            },
            5: {
                "day_name": "Суббота",
                "day_tag": "saturday",
                "shedule": {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: ""},
            },
        }  # self.shedule = {day_id: {day_name: "day_name", day_tag: "day_tag", {lesson: "name"}}}
        # fmt: on

    def add_lesson(self, name, pos):
        pos = [pos // 8, pos % 8]
        self.shedule[pos[0]]["shedule"][pos[1]] = name

    def delete_lesson(self, day_id, pos):
        pos = [pos // 8, pos % 8]
        self.shedule[day_id]["shedule"][pos] = ""

    def get_shedule(self):
        return self.shedule

    def get_formatted_shedule(self, pos=None):
        res = {}
        if pos is not None:
            pos = [pos // 8, pos % 8]
        for key, item in self.shedule.items():
            if pos is not None and key == pos[0]:
                txt = f"<code>{pos[1] + 1})</code> {item['shedule'][pos[1]].ljust(20) + '⬅️'}"
                data = []
                for k, i in item["shedule"].items():
                    if k == pos[1]:
                        data.append(txt)
                    else:
                        data.append(f"<code>{k + 1})</code> {i}")
                res[item["day_tag"]] = "\n".join(data)
            else:
                if all([k == "" for k in item["shedule"].values()]) and pos is None:
                    continue
                res[item["day_tag"]] = "\n".join(
                    [f"<code>{k + 1})</code> {i}" for k, i in item["shedule"].items()]
                )
        return res

    def load_shedule(self, shedule):
        translate = {
            "понедельник": 0,
            "вторник": 1,
            "среда": 2,
            "четверг": 3,
            "пятница": 4,
            "суббота": 5,
        }
        for lesson in shedule["data"]:
            self.shedule[translate[lesson["day"]["name"]]]["shedule"][
                int(lesson["slot"]["number_of_lesson"]) - 1
            ] = lesson["lesson"]["name"]


class RestErorr:
    def __init__(self, response):
        self.status_code = response.status_code
        self.error_message = response.json()["error"]
