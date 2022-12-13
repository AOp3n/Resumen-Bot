import re

from config import *
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters, enums, idle

bot = Client("my_account", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

filter = filters.chat(CHANNEL_ID) & filters.incoming & filters.regex(r"[\u2622\uFE0F](\(\S{1,2}\)).+")


@bot.on_message(filter)
@bot.on_edited_message(filter)
async def add_to_resume(_, message):
    resume_message = (await bot.get_chat(CHANNEL_ID)).pinned_message
    resume_text = resume_message.text.markdown
    title = (message.text or message.caption).split('\n')[0]

    if message.link in resume_text:
        updated_resume = resume_text.replace(re.search(f"\[(.+)\]\({message.link}\)",
                                                       resume_text)[1], title)

        if updated_resume != resume_message:
            await resume_message.edit_text(text=updated_resume, parse_mode=enums.ParseMode.MARKDOWN,
                                       disable_web_page_preview=True)
        
        return

    sections = resume_text.split("\n❌")
    substring_to_search = message.matches[0].group(1)
    types_acronym = list(types.keys())

    position = (types_acronym.index(substring_to_search) + 1) if substring_to_search in types_acronym else -1

    extra = "\n" if position == -1 else ""

    sections[position] += f"{extra}[{title}]({message.link})\n"

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
    scheduler.add_job(create_new_resume, 'cron', hour='7', timezone='EST',
                      next_run_time=datetime.now() + timedelta(seconds=10))
    bot.start()
    scheduler.start()
    idle()
