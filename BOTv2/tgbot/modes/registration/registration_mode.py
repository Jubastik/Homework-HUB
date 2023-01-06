from tgbot.entities.mode import Mode

from tgbot.modes.registration import *


class RegistrationMode(Mode):
    STAGES = {
        "entry_stage": EntryStage,
        # "join_by_id_stage": JoinByIdStage,
        # "time_stage": TimeStage,
        # "subjects_stage": SubjectsStage,
        # "shedule_stage0": lambda *args, **kwargs: FirstSheduleStage(*args, **kwargs, day=0),
        # "shedule_stage1": lambda *args, **kwargs: SheduleStage(*args, **kwargs, day=1),
        # "shedule_stage2": lambda *args, **kwargs: SheduleStage(*args, **kwargs, day=2),
        # "shedule_stage3": lambda *args, **kwargs: SheduleStage(*args, **kwargs, day=3),
        # "shedule_stage4": lambda *args, **kwargs: SheduleStage(*args, **kwargs, day=4),
        # "shedule_stage5": lambda *args, **kwargs: LastSheduleStage(*args, **kwargs, day=5),
    }
    STAGES_NUM_TO_NAME = {
        0: "entry_stage",
        # 1: "join_by_id_stage",
        # 2: "time_stage",
        # 3: "subjects_stage",
        # 4: "shedule_stage0",
        # 5: "shedule_stage1",
        # 6: "shedule_stage2",
        # 7: "shedule_stage3",
        # 8: "shedule_stage4",
        # 9: "shedule_stage5",
    }
