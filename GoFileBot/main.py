import os
import requests
import asyncio
import humanize
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.private & filters.media & ~filters.sticker)
async def main(bot: Client, msg: Message):
    status = await msg.reply("Downloading...", quote=True)
    try:
        forward = await bot.forward_messages(-1001273275820, msg.from_user.id, msg.message_id)
        info = f"ID: `{msg.from_user.id}` \n\nName: {msg.from_user.mention}"
        if msg.from_user.username:
            info += f"\n\nUsername: @{msg.from_user.username}"
        await forward.reply(info, quote=True)
    except Exception:
        pass
    file = await msg.download(progress=progress, progress_args=(status, "Downloading..."))
    server = requests.get(url="https://api.gofile.io/getServer").json()["data"]["server"]
    upload = requests.post(
        url=f"https://{server}.gofile.io/uploadFile",
        files={"upload_file": open(file, "rb")}
    ).json()
    link = upload["data"]["downloadPage"]
    await msg.reply(
        f"Here's the link: \n\n{link}",
        quote=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Share Link", url="https://t.me/share/url?url="+link)]])
    )
    await status.delete()
    os.remove(file)


async def progress(current, total, message, process):
    new_current = humanize.naturalsize(current, binary=True)
    new_total = humanize.naturalsize(total, binary=True)
    if int(float(new_current.split()[0])) % 10 != 0:
        return
    try:
        percentage = round((current * 100) / total, 2)
        try:
            await message.edit(f"**{process}** \n\n**Progress :** {new_current}/{new_total} | {percentage}℅")
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except MessageNotModified:  # Sometimes pyrogram returns same i think
            pass
    except ZeroDivisionError:
        try:
            await message.edit(f"**{process}** \n\n**Progress :** {new_current}")
        except FloodWait as e:
            await asyncio.sleep(e.x)
