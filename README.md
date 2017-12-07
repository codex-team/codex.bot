# [@codex_bot](https://ifmo.su/bot)
Platform for services integration into messengers. It's simple. Applications written with [our SDK](https://github.com/codex-bot/sdk-python) will be available in all supported messengers.

## Messengers
Currently we support these messengers. We will add several ones soon.

- Telegram
- Slack

## How to use

Add `@codex_bot` in your chat and type `/apps` to view list of available applications.

### How to create own application

Our [Python SDK](https://github.com/codex-bot/sdk-python) and Guide for creation an app will help you.

## Available applications
Everyone can write own application with our SDK. Thats we've got now.

### GitHub
https://github.com/codex-bot/github

Useful integration with github.com. Provides notifications about
- Opened/closed issues
- Assigned issues
- Opened/closes pull requests
- Code review
- Branch updates
- Commits

#### Usage
Type `/github_start` and follow instructions to add a new repository.

![](https://capella.pics/de15cea7-d234-4ddb-9923-c76fa0ec803a)

### Yandex.Metrica
https://github.com/codex-bot/metrika

Get regular or instant reports with analytics data from Yandex.

#### Usage
- `/metrika` — shows application menu
- `/metrika_add` — add new counter
- `/metrika_subscriptions` — setting up a regular daily reports
- `/metrika_stop` — disable counter
- `/metrika_counters` — list of added counters
- `/metrika_access` — remove user from the chat

![](https://capella.pics/52a46a39-4573-4597-a0a1-9ac6d7e87120)

### Webhooks
https://github.com/codex-bot/Webhooks

Easy-to-setup notifications scheme. You will get special link that allows to send messages via simple POST requests.

#### Usage
- `/notify_start` — get webhook URL for sending request
- Send POST request for given URL with `message` field

Example:
```bash
curl -X POST https://notify.bot.ifmo.su/u/ABCD1234 -d "message=Hello world"
```

![demo](https://user-images.githubusercontent.com/15448200/29435981-1c1e223e-83b2-11e7-8ee0-a3568b40ed7b.gif "You'll get message Hello world in telegram chat")

### RSS Parser
https://github.com/codex-bot/rssparser

Subscribe to your favorite feeds and get notifications with updates.

#### Usage
- `/rssparser` — help message with a list of commands
- `/rssparser_list` — show list of your subscriptions
- `/rssparser_add <URL>` — subscribe to the feed
- `/rssparser_get` — check your feed for updates
- `/rssparser_remove <URL>` — unsubscribe from the feed

![](https://capella.pics/0f595425-82e6-4793-a342-875b189f05d8)

### Weather
https://github.com/codex-bot/weather

Allow you to be informed about weather conditions in your region via Telegram chat.

#### Usage
- `/city <CITY_ID>` — setting up your location
- `/cities` — view cities list
- `/weather` — get current weather conditions

![](https://capella.pics/3ee93508-ef47-4c61-9c2f-988e2e6d9b93)

## Issues and improvements

Ask a question or report a bug on the [create issue page](https://github.com/codex-team/codex.bot/issues/new).

Know how to improve platform? [Fork it](https://github.com/codex-team/codex.bot) and send a pull request.

## About CodeX

We are small team of passionate web-developers consisting of IFMO University students and graduates located in St. Petersburg, Russia. Fell free to give us a feedback on  [team@ifmo.su](mailto:team@ifmo.su)
