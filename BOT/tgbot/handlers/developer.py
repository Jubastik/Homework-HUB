from asyncio import sleep
from aiogram.types import Message, CallbackQuery

from bot import dp, bot
from tgbot.filters.developer_filter import DeveloperFilter
from tgbot.FSM.states import Developer
from tgbot.services.restapi.restapi import get_all_users
from tgbot.keyboards.inline.markup import (
    markup_developer_menu,
    markup_developer_mailingcheck,
    markup_developer_deny,
)


@dp.message_handler(DeveloperFilter(), commands=["dev_panel"], state="*")
async def dev_panel(msg: Message):
    await Developer.Panel.set()
    await msg.answer("Developer panel", reply_markup=markup_developer_menu)


@dp.callback_query_handler(DeveloperFilter(), state=Developer.Panel, text="mailing")
async def query_mailing_get_text(callback: CallbackQuery):
    await callback.answer()
    await Developer.MailingGetText.set()
    await callback.message.answer(
        "Отправьте текст рассылки.", reply_markup=markup_developer_deny
    )


@dp.message_handler(DeveloperFilter(), state=Developer.MailingGetText)
async def handler_add_time(msg: Message):
    FSMContext = dp.current_state(user=msg.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        FSMdata["txt"] = msg.text
    await Developer.MailingCheck.set()
    await msg.answer(
        f'Текст рассылки:\n"{msg.text}"\n\nНачать рассылку?',
        reply_markup=markup_developer_mailingcheck,
    )


@dp.callback_query_handler(
    DeveloperFilter(), state=Developer.MailingCheck, text="start_mailing"
)
async def query_mailing_get_text(callback: CallbackQuery):
    await callback.answer()
    users = await get_all_users()
    await callback.message.answer(
        f"Начинаю рассылку. Это может занять некоторое время (≈{len(users) * 0.4} секунд)"
    )
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        counter = 0
        for user in users:
            try:
                await bot.send_message(user, FSMdata["txt"])
                await sleep(0.3)
                counter += 1
            except Exception:
                pass
    await callback.message.answer(
        f"Рассылка завершена. Отправлено {counter} из {len(users)} сообщений."
    )
    await FSMContext.reset_state()
    await Developer.Panel.set()
    await callback.message.answer("Developer panel", reply_markup=markup_developer_menu)


@dp.callback_query_handler(DeveloperFilter(), state="*", text="deny")
async def query_mailing_get_text(callback: CallbackQuery):
    await callback.answer()
    await Developer.Panel.set()
    await callback.message.answer("Developer panel", reply_markup=markup_developer_menu)
