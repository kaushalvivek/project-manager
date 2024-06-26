import os
import sys
import slack_bolt
import logging
sys.path.append(os.environ['PROJECT_PATH'])
from tasks.ticket import Ticketer
from models.slack import Message

app = slack_bolt.App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ticketer = Ticketer(logger=logger)

@app.event("message")
def handle_message_events(body):
    logger.info("Handling message event")
    logger.debug(f"Event: {body}")
    
    event_subtype = None
    if "subtype" in body["event"]:
        event_subtype = body["event"]["subtype"]
    if event_subtype and event_subtype in ["bot_message", "message_changed","message_deleted"]:
        return
    
    event = body["event"]
    message = Message.get_message_from_event(event)
    if ticketer.is_relevant(message):
        logger.info("Message is relevant")
        ticketer.trigger_ticket_creation(message)
    return

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))