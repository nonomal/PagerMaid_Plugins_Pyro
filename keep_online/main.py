import contextlib

from pyrogram.raw.functions.account import UpdateStatus

from pagermaid.services import bot, scheduler
from pagermaid.utils.bot_utils import log


@scheduler.scheduled_job("interval", seconds=55, id="keep_online")
async def keep_online():
    try:
        await bot.invoke(UpdateStatus(offline=False))
    except Exception as e:
        with contextlib.suppress(Exception):
            await log(f"Keep online failed: {e}")
