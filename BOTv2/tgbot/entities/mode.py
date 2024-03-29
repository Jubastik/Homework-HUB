from tgbot.entities.stage import Stage


class Mode:
    STAGES = {
        "entry_stage": Stage,  # entry_stage is required
    }
    STAGES_NUM_TO_NAME = {i: name for i, name in enumerate(STAGES)}
    STAGES_NAME_TO_NUM = {name: i for i, name in enumerate(STAGES)}
    STAGES_LEN = len(STAGES)

    def __init__(self, user):
        self.user = user
        self.stages = {"entry_stage": self.STAGES["entry_stage"](self)}  # {"stage_name": Stage()}
        self.current_stage: Stage = self.stages["entry_stage"]
        self.stage_num: int = self.STAGES_NAME_TO_NUM["entry_stage"]
    
    async def send_entry(self):
        msg_id = await self.current_stage.new_message()
        return msg_id

    async def set_stage(self, stage: str | int) -> int:
        if isinstance(stage, int):
            stage = self.STAGES_NUM_TO_NAME[stage]

        if stage in self.stages:
            self.current_stage = self.stages[stage]
        else:
            self.stages[stage] = self.current_stage = self.STAGES[stage](self)
        main_msg_id = await self.stages[stage].activate()
        self.stage_num = self.STAGES_NAME_TO_NUM[stage]
        return main_msg_id
    
    def get_stage(self, stage: str | int) -> Stage:
        if isinstance(stage, int):
            stage = self.STAGES_NUM_TO_NAME[stage]
        if stage in self.stages:
            return self.stages[stage]
        else:
            self.stages[stage] = self.STAGES[stage](self)
            return self.stages[stage]

    async def handle_callback(self, call) -> bool:
        return await self.current_stage.handle_callback(call)

    async def handle_message(self, msg) -> bool:
        return await self.current_stage.handle_message(msg)

    async def handle_api_error(self, error) -> bool:
        handled = await self.user.handle_api_error(error)
        if handled:
            return True
        else:
            return False
