class SheduleData:
    def __init__(self):
        # fmt: off
        self.shedule = {
            0: {
                "day_name": "Понедельник",
                "shedule": {0: "-", 1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-"},
            },
            1: {
                "day_name": "Вторник",
                "shedule": {0: "-", 1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-"},
            },
            2: {
                "day_name": "Среда",
                "shedule": {0: "-", 1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-"},
            },
            3: {
                "day_name": "Четверг",
                "shedule": {0: "-", 1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-"},
            },
            4: {
                "day_name": "Пятница",
                "shedule": {0: "-", 1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-"},
            },
            5: {
                "day_name": "Суббота",
                "shedule": {0: "-", 1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-"},
            },
        }  # self.shedule = {day_id: {day_name: "day_name", {lesson: "name"}}}
        # fmt: on

    def add_lesson(self, name, pos):
        self.shedule[pos[0]]["shedule"][pos[1]] = name

    def delete_lesson(self, day_id, lesson_id):
        self.shedule[day_id]["shedule"][lesson_id] = "-"

    def get_shedule(self):
        return self.shedule

    def get_readable_shedule(self, current_id=None):
        res = []
        for key in self.shedule.keys():
            day = self.shedule[key]
            res.append(f'{day["day_name"]}:')
            for lesson in day["shedule"].keys():
                res.append(f'{lesson + 1}) {day["shedule"][lesson]}')
        if current_id is not None:
            res_id = current_id[0] * 9 + current_id[1] + 1
            res[res_id] = res[res_id].ljust(20)
            res[res_id] += "⬅️"
        return res

    def load_shedule(self, shedule):
        # Мб пригодится, когда будем делать блок студента
        pass


class RestErorr:
    def __init__(self, response):
        self.status_code = response.status_code
        self.error_message = response.json()['error']