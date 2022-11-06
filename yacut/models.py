""" Yacut models module """

from datetime import datetime
from urllib.parse import urljoin

from flask import request

from yacut import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False, unique=True)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def get_link_to_dict(self) -> dict:
        """Return dictionary for json output get_short_url"""
        return dict(url=self.original)

    def create_link_to_dict(self) -> dict:
        """Return dicrionary for json output created links"""

        return dict(url=self.original, short_link=urljoin(request.host_url, self.short))

    def from_dict(self, data):
        """redefining the dictionary keys at the input
        for model readably fields."""

        setattr(self, "original", data["url"])
        setattr(self, "short", data["custom_id"])
