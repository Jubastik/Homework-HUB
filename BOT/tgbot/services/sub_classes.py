class SheduleData:
    def __init__(self):
        # fmt: off
        self.shedule = {
            0: {
                "day_name": "monday",
                "shedule": {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: ""},
            },
            1: {
                "day_name": "tuesday",
                "shedule": {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: ""},
            },
            2: {
                "day_name": "wednesday",
                "shedule": {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: ""},
            },
            3: {
                "day_name": "thursday",
                "shedule": {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: ""},
            },
            4: {
                "day_name": "friday",
                "shedule": {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: ""},
            },
            5: {
                "day_name": "saturday",
                "shedule": {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: ""},
            },
        }  # self.shedule = {day_id: {day_name: "day_name", {lesson: "name"}}}
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
                item["shedule"][pos[1]] = item["shedule"][pos[1]].ljust(20) + "⬅️"
            res[item["day_name"]] = "\n".join(
                [f"<code>{k + 1})</code> {i}" for k, i in item["shedule"].items()]
            )
        return res

    def load_shedule(self, shedule):
        # Мб пригодится, когда будем делать блок студента
        pass


class RestErorr:
    def __init__(self, response):
        self.status_code = response.status_code
        self.error_message = response.json()["error"]
