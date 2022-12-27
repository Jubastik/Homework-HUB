from asyncio import sleep

from aiogram.types import CallbackQuery, Message
from tgbot.filters.developer_filter import DeveloperFilter
from tgbot.FSM.states import Developer
from tgbot.keyboards.inline.markup import (markup_developer_deny,
                                           markup_developer_mailingcheck,
                                           markup_developer_menu)
from tgbot.services.restapi.restapi import get_all_chats, get_all_users
from tgbot.services.sub_classes import RestErorr

from bot import bot, dp


@dp.message_handler(DeveloperFilter(), commands=["test"], state="*")
async def dev_panel(msg: Message):
    x = await get_all_chats(msg.from_user.id)
    print(msg.from_user.id)
    print(x)



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
    FSMContext = dp.current_state(user=callback.from_user.id)
    users = await get_all_users()
    if isinstance(users, RestErorr):
        await callback.message.answer(f"Ошибка сервера {users.error_message}")
        FSMContext.reset_state()
        return
    await callback.message.answer(
        f"Начинаю рассылку. Это может занять некоторое время (≈{len(users) * 0.4} секунд)"
    )
    chats = await get_all_chats(callback.from_user.id)
    chats = [i["tg_id"] for i in chats]
    if isinstance(chats, RestErorr):
        await callback.message.answer(f"Ошибка сервера {users.error_message}")
        FSMContext.reset_state()
        return
    data = chats + users
    async with FSMContext.proxy() as FSMdata:
        counter = 0
        for chat_id in data:
            try:
                await bot.send_message(chat_id, FSMdata["txt"])
                await sleep(0.3)
                counter += 1
            except Exception:
                pass
    await callback.message.answer(
        f"Рассылка завершена. Отправлено {counter} из {len(data)} сообщений."
    )
    await FSMContext.reset_state()
    await Developer.Panel.set()
    await callback.message.answer("Developer panel", reply_markup=markup_developer_menu)


@dp.callback_query_handler(DeveloperFilter(), state="*", text="deny")
async def deny_mailing(callback: CallbackQuery):
    await callback.answer()
    await Developer.Panel.set()
    await callback.message.answer("Developer panel", reply_markup=markup_developer_menu)


# | send_msg | send_msg | send_msg | send_msg | send_msg | send_msg | send_msg | send_msg |


@dp.callback_query_handler(DeveloperFilter(), state=Developer.Panel, text="mail_to")
async def get_msg_info(callback: CallbackQuery):
    await callback.answer()
    await Developer.MsgGetData.set()
    await callback.message.answer("send info in format: 'chat_id | text'")

@dp.message_handler(DeveloperFilter(), state=Developer.MsgGetData)
async def send_msg(msg: Message):
    try:
        chat_id, text = msg.text.split('|')
    except ValueError:
        await msg.answer('wrong format')
        return
    await bot.send_message(chat_id, text)
    await msg.answer("message sent")