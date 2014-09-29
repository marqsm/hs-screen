LED Bot
=========

[![Documentation Status](https://readthedocs.org/projects/led-bot/badge/?version=latest)](https://readthedocs.org/projects/led-bot/?badge=latest)

![marquee](./docs/marquee.gif)

A LED application server. Stream images, messages, emoji and more to LEDs in
your home, office, hacker space.

Currently pipeline is working, supports these commands.

#### Zulip

| command                              | parameters         |
| ------------------------------------ | ------------------ |
| ```led-bot show-image <image-url>``` | An image url  |
| ```led-bot show-text <text>```       | maximum of [1000](https://github.com/marqsm/LED-bot/blob/master/textRenderer.py#L12) characters  |

#### HTTP API (POST)
| end point                            | parameters         |
| ------------------------------------ | ------------------ |
| ```http://host:4000/show-image/```    | url=image url  |
| ```http://host:4000/show-text/```     | message=your_text&r=100&g=0&b=0  |


At the moment LEDbot can accept input from
[Hacker School's](https://hackerschool.com) internal chat system, Zulip, a web API and fetch arbitrary JSON feeds, but it
shouldn't be difficult to add other types of input (SMS, IRC, Slack,
etc). [Take a look at the code](https://github.com/marqsm/LED-bot/blob/master/LEDBot/bot_scheduler.py#L252)
and write another listener!

Output is [Open Pixel Control](http://openpixelcontrol.org/).

LEDBot uses
[NYC Resistor's](http://www.nycresistor.com/2013/09/12/octoscroller/)
[LEDscape](https://github.com/osresearch/LEDscape) as our low-level interface.

## Installation instructions

The documentation for the project is on
[Read the docs](http://led-bot.readthedocs.org/en/latest/)

## Goals

This project aims to be AWESOME to contribute to, especially for new Hacker
Schoolers.  To begin contributing, look at the long list of
[issues](https://github.com/marqsm/LED-bot/issues) we have!

## Authors

Created at [Hacker School](https://hackerschool.com), Summer 2014
