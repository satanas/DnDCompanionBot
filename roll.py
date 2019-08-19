import re
import random

DICE_ROLL_PATTERN = re.compile('(\d+?d\d{1,3}|\d+?d%)([+-])*(\d+)*')

# Method to be invoked by telegram
def handler(bot, update, **args):
    print(update)
    print(args)
    username = f"@{update.message.from_user.username}" if update.message.from_user.username else update.message.from_user.first_name

    expression = update.message.text.strip().replace('/roll ', '')
    results = roll(expression)

    bot.send_message(chat_id=update.message.chat_id, text=response(username, results), parse_mode="Markdown")

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
        raise Exception('Request was not a valid equation!')

    for i in range(0, len(equation)):
        parts = equation[i]
        results[''.join(parts)] = process_notation(parts[0], parts[1], parts[2])

    #print(results)
    return results

def process_notation(notation, sign, modifier_amount):
    results = []

    modifier = 0
    if sign != '' and modifier != '':
        modifier = int(sign + modifier_amount)

    dice_num = int(notation.split('d')[0])
    sides = notation.split('d')[1]
    for n in range(0, dice_num):
        if sides == '100' or sides == '%':
            results.append(roll_percentile())
        else:
            results.append(roll_one(sides, modifier))

    return results

def roll_one(sides, mod=0):
    return random.randint(1, int(sides)) + mod

def roll_percentile():
    return random.randint(1, 100)

def response(username, results):
    rolls = ''
    for key in results:
        rolls += f"\r\n *{key}*: {results[key]}"

    return f"{username} rolled:{rolls}"

if __name__ == "__main__":
    print(response('wil', roll('1d20,1d6')))
