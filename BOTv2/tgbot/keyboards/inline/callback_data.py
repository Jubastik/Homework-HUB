from aiogram.utils.callback_data import CallbackData

SubjectData = CallbackData("subject", "name")
ArrowsData = CallbackData("up_or_down", "num")
CheckHomework = CallbackData("check_homework", "boolean")
DatesData = CallbackData("add_date", "date")

StudentsData = CallbackData("student_name", "tguser_id", "name")