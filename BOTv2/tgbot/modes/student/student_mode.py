from asyncio import sleep

from tgbot.modes.student.stages import MenuStage
from tgbot.entities.mode import Mode

class StudentMode(Mode):
    STAGES = {
        "entry_stage": MenuStage,
    }
    STAGES_NUM_TO_NAME = {i: name for i, name in enumerate(STAGES)}
    STAGES_NAME_TO_NUM = {name: i for i, name in enumerate(STAGES)}
    STAGES_LEN = len(STAGES)

    async def handle_callback(self, call) -> bool:
        return False
    
    async def handle_message(self, msg) -> bool:
        if msg.text == "/start":
            msg_id = await self.reset()
            self.user.set_main_msg_id(msg_id)
            await sleep(0.5)
            await msg.delete()
            return True
        handled = await self.current_stage.handle_message(msg) if self.current_stage else False
        if handled:
            return True
        return False