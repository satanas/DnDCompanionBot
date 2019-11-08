[![Build Status](https://travis-ci.com/satanas/DnDCompanionBot.svg?branch=master)](https://travis-ci.com/satanas/DnDCompanionBot)

# Dungeons and Dragons Companion Bot
`DnDCompanionBot` is a telegram bot to play Dungeons and Dragons. In the future, this bot should be able to track
campaigns, character sheets and help the DM with management tasks.

## Commands
General commands | Action
--------|-------
/start | starts the DnDCompanionBot
/roll [expression] | rolls the dice using the [dice notation](https://en.wikipedia.org/wiki/Dice_notation)
/charsheeet [username] | returns the character sheet associated with username
/help | shows this help message

Campaign commands | Action
--------|-------
/start_campaign | starts a new campaign in the invoked group
/close_campaign | closes an active campaign
/import_char [json_url] | imports the JSON data of a character
/set_turns [p1],[p2]... | creates a list with the order of players in a combat
/turn | shows the current player in the combat order list
/next_turn | moves the turn to the next player in the combat order list
/set_dm [username] | sets the DM of the current campaign
/dm | shows the DM for the current campaign

Character commands | Action
--------|-------
/weapons [character] | shows the list of weapons of a character
/attack_roll [character] [weapon] [attack](melee|range) [distance] [adv|disadv] | performs an attack roll
/initiative_roll [character] | performs an initiative roll for the character
/talk [character] [message] | prints message using an in-game conversation format

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

# Put the token received into a file called serverless.env.yml, like this
$ cat serverless.env.yml
TELEGRAM_TOKEN: <your_token>

# Deploy it!
$ serverless deploy

# With the URL returned in the output, configure the Webhook
$ curl -X POST https://<your_url>.amazonaws.com/dev/set_webhook
```

## Testing locally

Make sure you use pip and all tools for Python 3, then install all dependencies:

```
$ pip3 install virtualenv
$ virtualenv venv
$ source venv/bin/activate

$ pip3 install -r requirements.txt
```

And finally, run the tests:
```
$ nose2 -v
```

## Notes
AWS credentials saved on your machine at ~/.aws/credentials.
