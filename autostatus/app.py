from typing import Optional
from chalice import Chalice, Cron
import slack
import os
from datetime import datetime, timedelta

app = Chalice(app_name='autostatus')


def set_status(status_text: str, status_emoji: str = ":no_bell:",
               expiration_min: Optional[int] = None, dnd: bool = False) -> None:
    """Method to set your status programmatically

    Args:
        status_text: Message to set
        status_emoji: Emoji to use
        expiration_min: Minutes to keep the status before removing
        dnd: Set do not disturb when setting the status

    Returns:
        None
    """
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    if expiration_min:
        expiration_time = datetime.now() + timedelta(minutes=expiration_min)
        expiration_int = round(expiration_time.timestamp())
    else:
        expiration_int = 0

    status = {
        "status_text": status_text,
        "status_emoji": status_emoji,
        "status_expiration": expiration_int
    }

    response = client.users_profile_set(profile=status)
    print(response)

    if dnd:
        response = client.dnd_setSnooze(num_minutes=expiration_min)
        print(response)


@app.schedule(Cron(0, 22, '?', '*', 'MON-FRI', '*'))
def job1(event):
    """My "family time" job to

    Args:
        event:

    Returns:

    """
    set_status("family time", status_emoji=":no_bell:", expiration_min=3 * 60, dnd=True)
