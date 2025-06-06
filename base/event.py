import os
import urllib3
import logging

from abc import ABC, abstractmethod
from typing import Tuple, Any

logger = logging.getLogger("fastapi_cli")


class BaseEventFabric(ABC):
    def __init__(self):
        self.scheduler = os.environ.get(
            "SCH_SERVICE_NAME", None)

        if self.scheduler is None:
            self.debugging_mode = True
        else:
            self.debugging_mode = False

            if not self.scheduler.startswith("http://"):
                self.scheduler = f"http://{self.scheduler}"

            print(f"Relying on the scheduler at {self.scheduler}")
        super(BaseEventFabric, self).__init__()

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
        try:
            if self.debugging_mode:
                logger.info("Faux call to scheduler has happened!")
                return

            http = urllib3.PoolManager()
            res = http.request('POST', f"{self.scheduler}/api/event",
                               json=dict(name=evt_name, data=data), retries=urllib3.Retry(5))
            if res.status >= 300:
                print(
                    f"Failure to send EventRequest to the scheduler because {res.reason}")
        except Exception as err:
            print("Failure during request because:")
            print(err)


class ExampleEventFabric(BaseEventFabric):

    def __init__(self):
        super(ExampleEventFabric, self).__init__()

    def call(self, *args, **kwargs):
        logger.info("Called to event fabric")
        return "GenEvent", None
