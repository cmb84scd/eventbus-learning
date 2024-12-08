"""Get an animal fact and put it onto the eventbus."""

import logging

import boto3
import requests
from decouple import config


class GetFactFunction:
    """Get an animal fact and put it onto the eventbus."""

    EVENT_BUS_ARN = config("EVENT_BUS_ARN")

    events_client = boto3.client("events")

    def __init__(self, event, context):
        """Store the event and context, and set up the logger."""
        self.context = context
        self.event = event
        self.logger = logging.getLogger().setLevel(logging.INFO)

    def execute(self):
        """Put the fact onto the eventbus."""
        try:
            fact = self.get_fact()
            event = {
                "Detail": str(fact),
                "DetailType": "fact.retrieved",
                "EventBusName": self.EVENT_BUS_ARN,
                "Source": "GetFactFunction",
            }
            self.logger.info("Sending fact to eventbus", event)
            self.events_client.put_events(Entries=[event])
        except Exception as e:
            self.logger.error("Failed to send event to eventbus", exception=e)

    def get_fact(self):
        """Get an animal fact and remove id from response."""
        try:
            response = requests.get("http://127.0.0.1:8000/facts", timeout=5)
            response.raise_for_status()
            res = response.json()
            res.pop("id")
            return res
        except requests.exceptions.ConnectionError as e:
            self.logger.error("Failed to connect to API", exception=e)
            raise e
        except requests.exceptions.HTTPError as e:
            self.logger.error(
                "No data returned",
                {"Status Code": response.status_code},
                exception=e,
            )
            raise e
        except requests.exceptions.RequestException as e:
            self.logger.error("Failed to get fact", exception=e)
            raise e


handler = GetFactFunction.execute
