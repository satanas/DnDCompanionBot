import re
import random

DICE_ROLL_PATTERN = re.compile('(\d+?d\d{1,3}|\d+?d%)([+-])*(\d+)*')

# Method to be invoked by telegram
def handler(bot, update, command, expression):
    username = f"@{update.message.from_user.username}" if update.message.from_user.username else update.message.from_user.first_name

    try:
        results = roll(expression)
        resp = response(username, results)
    except Exception as e:
        resp = f"{username} {str(e)}"

    bot.send_message(chat_id=update.message.chat_id, text=resp, parse_mode="Markdown")

# Test cases
# 1d4,1d6
# 2d6+12,1d4-5
# 1d6-10
# 1d100
# 2d20
# 1d%
def roll(expression):
    equation = DICE_ROLL_PATTERN.findall(expression)
    results = {}

    if len(equation) <= 0:
        raise Exception('your request was not a valid equation! Please use the dice notation (for example: 1d6 to roll a die of 6 sides)')

    for i in range(0, len(equation)):
        parts = equation[i]
        key = ''.join(parts)
        roll_result = process_notation(parts[0], parts[1], parts[2])
        if key in results:
            results[key].append(roll_result)
        else:
            results[key] = [roll_result]

    return results

def process_notation(notation, sign, modifier_amount):
    result = 0

    modifier = 0
    if sign != '' and modifier != '':
        modifier = int(sign + modifier_amount)

    dice_num = int(notation.split('d')[0])
    sides = notation.split('d')[1]
    if sides == '100' and dice_num > 1:
        raise Exception('percentile roll doesn\'t support multiple dice')

    if sides == '100' or sides == '%':
        result = roll_one(100)
    else:
        for n in range(0, dice_num):
            result += roll_one(int(sides))
        result = max(1, result + modifier)

    return result

def roll_one(sides):
    return random.randint(1,sides)

def response(username, results):
    rolls = ''
    for key in results:
        rolls += f"\r\n *{key}*: {results[key]}"

    return f"{username} rolled:{rolls}"

