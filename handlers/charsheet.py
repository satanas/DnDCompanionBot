import requests

SHEETS_JSON_URL = "https://gist.githubusercontent.com/satanas/0d38dad2f1eae87143a4cd10206eece5/raw/b4bdf85be78e5e15f3a65c7c7474862a2477dc48/character_dnd.json"

def handler(bot, update, command, txt_args):
    username = update.message.text.strip().replace('/charsheet', '').strip()
    if username == '' or username == ' ':
        username = update.message.from_user.username

    print(f"{username} is requesting charsheet")

    link = get_charsheet_link(username)

    bot.send_message(chat_id=update.message.chat_id, text=link, parse_mode="Markdown", disable_web_page_preview=True)


def get_charsheet_link(username):
    r = requests.get(SHEETS_JSON_URL)
    sheet = r.json()

    link = f"{username} has no character sheet registered"
    if username in sheet.keys():
        print(username, sheet)
        if sheet[username] != '':
            link = sheet[username]

    return link
