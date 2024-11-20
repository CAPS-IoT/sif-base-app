import os
import urllib3

from abc import ABC, abstractmethod
from typing import Tuple, Any


class BaseEvent(ABC):
    def __init__(self):
        self.scheduler = os.environ.get("SCH_SERVICE_NAME", "localhost:8080")
        print(f"Relying on the scheduler at {self.scheduler}")
        super(BaseEvent, self).__init__()

    @abstractmethod
    def call(self, *args, **kwargs) -> Tuple[str, Any]:
        """
        Custom implementation to handle event invocations. Each child event
        must adhere to this structure so events are properly propagated to the
        SIF-edge scheduler

        :returns: once the callback finished, it must return the event's name and corresponding data
        :rtype: Tuple[str, Any]
        """
        raise NotImplementedError("Implement the 'call' method in your class")

    def __call__(self, *args, **kwargs):
        evt_name, data = self.call(*args, **kwargs)
        http = urllib3.PoolManager()
        res = http.request('POST', self.scheduler,
                           json=dict(name=evt_name, data=data), retries=urllib3.Retry(5))
        if res.status >= 300:
            print(
                f"Failure to send EventRequest to the scheduler because {res.reason}")