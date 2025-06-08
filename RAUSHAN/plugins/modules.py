from config import *
from subprocess import getoutput as r
from pyrogram import Client
from RAUSHAN import *
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton

a = r("ls RAUSHAN/plugins").split('\n')
help_data = {}
help_names = []
for x in a:
    if x.endswith('.py') and not x.startswith('__pycache__'):
        try:
            module = __import__(f"RAUSHAN.plugins.{x.replace('.py', '')}", fromlist=["MOD_NAME", "MOD_HELP"])
            if hasattr(module, 'MOD_NAME') and hasattr(module, 'MOD_HELP'):
                help_data[module.MOD_NAME] = module.MOD_HELP
                help_names.append(module.MOD_NAME)
        except:
            pass
logging.info(f"{f'Loaded Modules: {a}' if a else 'No modules loaded'}")

async def page_help(page=1, per_page=10):
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(help_names) + per_page - 1) // per_page
    buttons = []
    row = []
    for cmd in help_names[start:end]:
        row.append(InlineKeyboardButton(cmd, callback_data=f"help:{cmd}:{page}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton("🔙 Back", callback_data=f"helppage:{page - 1}"))
    if end < len(help_names):
        nav_buttons.append(InlineKeyboardButton("Next 🔜", callback_data=f"helppage:{page + 1}"))
    if nav_buttons:
        buttons.append(nav_buttons)
    return InlineKeyboardMarkup(buttons), page, total_pages

@RAUSHANBot.on_inline_query(filters.regex('help'))
async def showcommands(_, query):
    reply_markup, current_page, total_pages = await page_help(page=1)
    result = InlineQueryResultArticle(
        title="Help",
        input_message_content=InputTextMessageContent(
            f"**Click buttons bellow to get the module info**\nPage {current_page}/{total_pages}"
        ),
        reply_markup=reply_markup
    )
    await query.answer([result])

@RAUSHANBot.on_callback_query(qfilter('help:'))
async def showhelpinfo(_, query):
    if query.from_user.id != OWNER_ID:
        return await query.answer('This is not for you!', show_alert=False)
    data = query.data.split(":")
    help_cmd = data[1]
    current_page = int(data[2]) if len(data) > 2 else 1
    if help_cmd in help_names:
        txt = f"**⚡ Help for the module: {help_cmd}**\n\n{help_data[help_cmd]}"
        button = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data=f"helppage:{current_page}")]])
        await query.edit_message_text(txt, reply_markup=button)

@RAUSHANBot.on_callback_query(qfilter('helppage:'))
async def page_callback(_, query):
    if query.from_user.id != OWNER_ID:
        return await query.answer('This is not for you!', show_alert=False)
    page = int(query.data.split(":")[1])
    reply_markup, current_page, total_pages = await page_help(page=page)
    await query.edit_message_text(
        f"**Click buttons bellow to get the module info**\nPage {current_page}/{total_pages}",
        reply_markup=reply_markup
    )
