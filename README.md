# slack-status-scheduler
Automatically set your Slack status on a schedule with Lambda

## Introduction
This is a simple Chalice app that lets you very easily manage Cron based Lambda functions to set your Slack status.
While moving to remote work, I noticed I had trouble unplugging at times. I was also surprised
that it was hard to schedule slack status changes, as this has become important for communicating with my team. 
The only real option I found was using Zapier, but they requested permissions 
to basically everything in your Slack org which is stupid.

This super simple app just needs scopes to write your status and DND state. It is more complicated than Zapier, and does require you 
create an app in your desired organization and install it for yourself, but is customizable and minimizes access to your
org.

## Usage

### Create a Slack app and get Oauth Creds

First create a new Slack app by visiting https://api.slack.com/apps.

Then go to OAuth and Permissions. Set the following scopes:
* dnd:write
* users.profile:write

Make sure you've installed the app into your workspace and then from the OAuth and Permissions page copy the OAuth token

### Configure Chalice
Copy `.chalice/config_template.json` to `.chalice/config.json` and enter your token where indicated. This file is untracked 
in git. By putting your token here, it'll set it as an env var in the lambda function. Not the most secure thing, but the 
simplest for this little app.


### Configure your desired statuses
The app currently has what I'm using, but its very easy to add more or modify. You simply create a function with the 
[`Cron` decorator](https://chalice.readthedocs.io/en/latest/api.html#Cron), setting the desired time in UTC
when the function should fire. 

In that function call `set_status` with your desired configuration. You can set the message, emoji, duration, and if do not 
disturb should also be set.

### Deploy
* Create a virtualenv
* run `pip install -r requirements.txt`
* run `chalice deploy`

You're now all set for automatic statuses. If you change something, just run deploy again. If you want to clean up, call
`chalice delete` and everything will be deleted from your AWS account. 
You can read more about how Chalice works here: https://chalice.readthedocs.io/en/latest/index.html