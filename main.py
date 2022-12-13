import re

from config import *
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters, enums, idle

bot = Client("my_account", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

filter = filters.chat(CHANNEL_ID) & filters.incoming


@bot.on_message(filter)
@bot.on_edited_message(filter)
async def add_to_resume(_, message):
    text = (message.text or message.caption).split("\n")[0]

    if not text.startswith("☢"):
        return

    resume_message = (await bot.get_chat(CHANNEL_ID)).pinned_message

    sections = resume_message.text.markdown.split("\n❌")

    substring_to_search = re.search("(\(.{1,3}\))", text)[1]

    types_acronym = list(types.keys())

    position = (types_acronym.index(substring_to_search) + 1) if substring_to_search in types_acronym else -1

    extra = "\n" if position == -1 else ""

    sections[position] += f"{extra}[{text}]({message.link})\n"

    await resume_message.edit_text(text="\n❌".join(sections), parse_mode=enums.ParseMode.MARKDOWN,
                                   disable_web_page_preview=True)


async def create_new_resume():
    resume = "RESUMEN pvtos\n"
    for type in types.values():
        resume += f"\n❌{type}:\n"
    message = await bot.send_message(CHANNEL_ID, resume)
    await message.pin()


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(create_new_resume, 'cron', hour='7', timezone='utc',
                      next_run_time=datetime.now() + timedelta(seconds=10))
    bot.start()
    scheduler.start()
    idle()
