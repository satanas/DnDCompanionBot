[![Build Status](https://travis-ci.com/satanas/DnDCompanionBot.svg?branch=master)](https://travis-ci.com/satanas/DnDCompanionBot)

# Dungeons and Dragons Companion Bot
`DnDCompanionBot` is a telegram bot to play Dungeons and Dragons. In the future, this bot should be able to track
campaigns, character sheets and help the DM with management tasks.

## Commands
General commands | Action
--------|-------
/start | starts the DnDCompanionBot
/roll \<expression\> | rolls the dice using the [dice notation](https://en.wikipedia.org/wiki/Dice_notation)
/charsheet \<username\> | returns the character sheet associated with username
/help | shows this help message

Campaign commands | Action
--------|-------
/start_campaign | starts a new campaign in the invoked group
/close_campaign | closes an active campaign
/set_turns \<username1\>, ..., \<usernameN\> | creates a list with the order of players for a given round
/turn | shows the current player in the turns list
/next_turn | moves to the next player in the turns list
/set_dm \<username\> | sets the username of the DM for the current campaign
/dm | shows the DM for the current campaign

Character commands | Action
--------|-------
/import_char \<url\> | imports the JSON data of a character from a URL
/link_char \<char\_id\>, (username) | links character to target username or self username
/status \<username\|character\> | shows the list of weapons of a character
/weapons \<username\|character\> | shows the list of weapons of a character
/attack_roll \<character\>, \<weapon\>, \<melee\|range\>, (distance), (adv\|disadv) | performs an attack roll on a character
/initiative_roll \<character\> | performs an initiative roll for a character
/short_rest_roll \<username\|character\> | performs an short rest roll for a character
/talk \<message\> | prints a message using in-game conversation format
/say \<message\> | prints a normal message using in-game conversation format
/whisper \<message\> | prints a whisper message using in-game conversation format
/yell \<message\> | prints a yell message using in-game conversation format


## What do I need?
- A AWS key configured locally, see [here](https://serverless.com/framework/docs/providers/aws/guide/credentials/).
- NodeJS >= v8.9.0.
- A Telegram account.

## Installing
```
# Install the Serverless Framework
$ npm install serverless -g

# Install the necessary plugins
$ npm install

# Get a bot from Telegram, sending this message to @BotFather
$ /newbot

# Put the token received into a file called serverless.env.yml, along with your Firebase configuration details. Like this:
# file: serverless.env.yml
TELEGRAM_TOKEN: <your_token>
FIREBASE_DB_URL: <your_firebase_realtime_database_url>
FIREBASE_API_SECRET: <your_firebase_realtime_database_secret>

# Deploy it!
$ serverless deploy

# With the URL returned in the output, configure the Webhook
$ curl -X POST https://<your_url>.amazonaws.com/dev/set_webhook
```

## Installing locally

Define the following ENV variables for your OS:
```
TELEGRAM_TOKEN: <your_telegram_bot_token>
FIREBASE_DB_URL: <your_firebase_realtime_database_url>
FIREBASE_API_SECRET: <your_firebase_realtime_database_secret>
```

Then, make sure you use pip and all tools for Python 3 and install all dependencies:
```
$ pip3 install virtualenv
$ virtualenv venv
$ source venv/bin/activate

$ pip3 install -r requirements.txt
```

## Running the bot locally

Follow the instructions from the section [Installing locally](#installing-locally), and then run the bot:

```
$ python local.py
```

## Running tests locally

Follow the instructions from the section [Installing locally](#installing-locally), and then run the tests:

```
$ nose2 -v
```

## Notes
AWS credentials saved on your machine at ~/.aws/credentials.

## References
* https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/README.md
* https://github.com/treetrnk/rollem-telegram-bot/blob/master/bot.py
