def normalized_username(username):
    return username.replace('@', '').strip()

def to_snake_case(text):
    text = text.lower()
    text = text.replace(' ', '-')
    return text
