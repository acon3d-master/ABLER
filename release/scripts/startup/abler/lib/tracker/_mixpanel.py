import threading
from typing import Optional
import os
from uuid import uuid4

from mixpanel import Mixpanel, BufferedConsumer
import bpy
from ._tracker import Tracker

mixpanel_token_path = os.path.join(os.path.dirname(__file__), "mixpanel_token")
with open(mixpanel_token_path, "r") as f:
    _mixpanel_token = f.readline()


class MixpanelResource:
    mp: Mixpanel
    timer: threading.Timer
    # Tracking ID, 기기마다 유일한 것으로 기대됨
    tid: str

    _consumer: BufferedConsumer
    _flush_interval = 5  # seconds

    def __init__(self):
        self._consumer = BufferedConsumer()
        print(f"Initializing Mixpanel with token {_mixpanel_token}")
        self.mp = Mixpanel(_mixpanel_token, consumer=self._consumer)

        user_path = bpy.utils.resource_path("USER")
        tid_path = os.path.join(user_path, "abler_tid")
        # NOTE: 로그아웃 후 다른 이메일로 로그인하는 경우는 고려하지 않음
        try:
            if not os.path.exists(tid_path):
                with open(tid_path, "w") as f:
                    f.write(str(uuid4()))
            with open(tid_path, "r") as f:
                self.tid = f.read(36)
        except OSError:
            self.tid = "anonymous"

        self.flush_repeatedly()

    def flush_repeatedly(self):
        # 현재는 cleanup 로직을 두지 않음
        timer = threading.Timer(self._flush_interval, self.flush_repeatedly)
        timer.daemon = True
        timer.start()
        self.timer = timer

        self._consumer.flush()


class MixpanelTracker(Tracker):
    _r: Optional[MixpanelResource] = None

    def _ensure_resource(self):
        if self._r is None:
            self._r = MixpanelResource()

    def _send_event(self, event_name: str):
        self._ensure_resource()
        self._r.mp.track(self._r.tid, event_name)

    def _update_email(self, email: str):
        self._ensure_resource()
        self._r.mp.people_set_once(self._r.tid, {"$email": email})
