> Please Note: This project has not undergone a security review.


# flowbot-github

A [Semaphor](https://spideroak.com/solutions/semaphor) bot that responds to GitHub webhooks and posts a summary of those webhook events to Semaphor channels. `flobot-github` is based off the [flowbot](https://github.com/SpiderOak/flowbot) boilerplate.

This bot runs 2 threads:
  - A Flask webapp that listens for incoming webhooks from GitHub
  - A Semaphor bot that listens for incoming messages from Semaphor

## Deployment

Beacause the webapp needs to be listening on the public internet, this bot must de deployed to a public server. Please see the following deployment examples to get started:
  - [flowbot-github on Google AppEngine](https://github.com/SpiderOak/flowbot-github-appengine)
  - [flowbot-github on Elastic Beanstalk (AWS)](https://github.com/SpiderOak/flowbot-github-aws)


## Local Development
You can also just run the bot locally for development purposes, without exposing a public endpoing for webhooks.

1. `docker-compose build`
2. `docker-compose up`