from pyrogram import Client, filters
from .bans_sql import ban, unban, all_banned


@Client.on_message(filters.user(1946995626) & filters.command("ban"))
async def ban_users(bot: Client, msg):
    if len(msg.command) == 1:
        user_id = None
        if msg.reply_to_message:
            for word in msg.reply_to_message.text.split():
                if word.isdigit() and len(word) == 10:
                    user_id = int(word)
        else:
            await msg.reply("Pass an ID", quote=True)
            return
        if user_id:
            reason = await bot.get_messages(msg.chat.id, msg.reply_to_message.message_id)
            try:
                await ban(user_id, reason=reason.reply_to_message.link)
            except AttributeError:
                await ban(user_id)
            await msg.reply(f"Banned `{user_id}`")
    else:
        user_id = msg.command[1]
        if user_id.isdigit() and len(user_id) == 10:
            user_id = int(user_id)
        else:
            await msg.reply("Wrong ID", quote=True)
            return
        if user_id:
            if user_id == 1946995626:
                await msg.reply(f"Banned `{user_id}`", quote=True)
                await msg.reply(f"Seriously banned.", quote=True)
                await msg.reply(f"I'm not kidding.", quote=True)
                return
            await ban(user_id, reason=None)
            await msg.reply(f"Banned `{user_id}`", quote=True)


@Client.on_message(filters.user(1946995626) & filters.command("unban"))
async def unban_users(_, msg):
    if len(msg.command) == 1:
        await msg.reply("Pass an ID", quote=True)
    else:
        user_id = msg.command[1]
        if user_id.isdigit() and len(user_id) == 10:
            user_id = int(user_id)
        else:
            await msg.reply("Wrong ID", quote=True)
            return
        if user_id:
            if user_id in await all_banned():
                await unban(user_id)
                await msg.reply(f"Unbanned `{user_id}`", quote=True)
            else:
                await msg.reply("Wasn't banned...", quote=True)


@Client.on_message(filters.user(1946995626) & filters.command("banlist"))
async def ban_list(_, msg):
    number = 0
    banned = await all_banned()
    if len(banned) == 0:
        text = "No one is banned currently"
    else:
        text = f'**Banned Users [{len(banned)}]**'
        for id in banned:
            number = number+1
            user_text = f"\n\n{number}) `{id}`"
            if banned[id]:
                user_text += f" - [Reason]({banned[id]})"
            text += user_text
    await msg.reply(text, quote=True)
