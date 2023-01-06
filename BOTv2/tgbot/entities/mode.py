from tgbot.entities.stage import Stage

class Mode:
    STAGES = {
        "entry_stage": Stage,  # entry_stage is required
    }
    STAGES_NUM_TO_NAME = {0: "entry_stage"}

    def __init__(self, user):
        self.user = user
        self.stages = {}  # {"stage_name": Stage()}
        self.current_stage = None  # Stage()

    async def init(self, main_msg_id) -> int:
        if main_msg_id:
            main_msg_id = await self.current_stage.activate()
        else:  # if main_msg_id is None we send new message
            self.stage_num = 0
            main_msg_id = await self.set_stage("entry_stage")
        return main_msg_id

    async def set_stage(self, stage: str | int) -> int:
        if isinstance(stage, int):
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
