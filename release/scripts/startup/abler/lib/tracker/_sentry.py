import os
import time

import bpy
import sentry_sdk

from ._tracker import Tracker


release_version = "abler@" + bpy.app.build_hash.decode("ascii")


class SentryTracker(Tracker):
    def __init__(self):
        super().__init__()
        with open(os.path.join(os.path.dirname(__file__), "sentry_dsn")) as f:
            sentry_dsn = f.readline()
            sentry_sdk.init(
                sentry_dsn,
                release=release_version,
            )

    def _enqueue_event(self, event_name: str):
        sentry_sdk.add_breadcrumb(
            category="event", message=event_name, timestamp=time.time()
        )

    def _enqueue_email_update(self, email: str):
        sentry_sdk.set_user({"email": email})
