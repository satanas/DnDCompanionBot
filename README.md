# Dungeons and Dragons Companion Bot
`DnDCompanionBot` is a telegram bot to play Dungeons and Dragons. In the future, this bot should be able to track
campaigns, character sheets and help the DM with management tasks.

## Commands
Command | Action
--------|-------
/start | Starts the `DnDCompanionBot`
/roll [expression1,expression2,...] | Rolls the dice using the [dice notation](https://en.wikipedia.org/wiki/Dice_notation)
/help | Prints the help message

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


## Notes
AWS credentials saved on your machine at ~/.aws/credentials.
