"""Get an animal fact and log it out."""

import logging

import requests


class GetFactFunction:
    """Get an animal fact and log it out."""

    def __init__(self, event, context):
        """Store the event and context, and set up the logger."""
        self.context = context
        self.event = event
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    # def execute(self):
    #     """Log out the fact."""
    #     pass

    def get_fact(self):
        """Get an animal fact and remove id from response."""
        response = requests.get("http://127.0.0.1:8000/facts")
        res = response.json()
        res.pop("id")
        return res
