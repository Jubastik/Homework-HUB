from tgbot.entities.stage import Stage


class Mode:
    STAGES = {
        "entry_stage": Stage,  # entry_stage is required
    }
    STAGES_NUM_TO_NAME = {0: "entry_stage"}
    STAGES_NAME_TO_NUM = {"entry_stage": 0}
    STAGES_LEN = len(STAGES)

    def __init__(self, user):
        self.user = user
        self.stages = {}  # {"stage_name": Stage()}
        self.current_stage: Stage = self.STAGES["entry_stage"](self)
        self.stage_num: int = self.STAGES_NAME_TO_NUM["entry_stage"]
        self.data = {}  # data for stages

    async def set_stage(self, stage: str | int) -> int:
        if isinstance(stage, int):
            stage = min(self.STAGES_LEN - 1, max(0, stage))
            stage = self.STAGES_NUM_TO_NAME[stage]
            
        if stage in self.stages:
            self.current_stage = self.stages[stage]
        else:
            self.stages[stage] = self.current_stage = self.STAGES[stage](self)
        main_msg_id = await self.stages[stage].activate()
        return main_msg_id

    async def handle_callback(self, call) -> bool:
        return await self.current_stage.handle_callback(call)

    async def handle_message(self, msg) -> bool:
        return await self.current_stage.handle_message(msg)

    def handle_api_error(self, error) -> bool:
        return False
