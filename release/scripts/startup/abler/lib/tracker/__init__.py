import os

from ._tracker import Tracker, DummyTracker
from ._mixpanel import MixpanelTracker


tracker: Tracker = (
    DummyTracker() if os.environ.get("DISABLE_TRACK") else MixpanelTracker()
)
