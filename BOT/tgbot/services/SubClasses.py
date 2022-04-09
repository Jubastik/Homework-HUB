class SheduleData:
    def __init__(self):
        # fmt: off
        self.shedule = {
            1: {
                "day_name": "Понедельник",
                "shedule": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-"},
            },
            2: {
                "day_name": "Вторник",
                "shedule": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-"},
            },
            3: {
                "day_name": "Среда",
                "shedule": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-"},
            },
            4: {
                "day_name": "Четверг",
                "shedule": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-"},
            },
            5: {
                "day_name": "Пятница",
                "shedule": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-"},
            },
            6: {
                "day_name": "Суббота",
                "shedule": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-"},
            },
        }  # self.shedule = {day_id: {day_name: "day_name", {lesson: "name"}}}
        # fmt: on

    def add_lesson(self, name, day_id, lesson_id):
        self.shedule[day_id]["shedule"][lesson_id] = name

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
                res.append(f'{lesson}) {day["shedule"][lesson]}')
        if current_id is not None:
            pass

    def load_shedule(self, shedule):
        # Мб пригодится, когда будем делать блок студента
        pass
