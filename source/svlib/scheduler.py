from datetime import datetime
from dateutil import tz, parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from typing import Callable

from svtools import SecureVisionTools as svt

#place to config
SV_TIME_ZONE = "Europe/Budapest"
SV_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S:.%f%z"


class Scheduler(object):
    def __init__(self, scheduler_type: str, num_workers: int = 1):
        self.scheduler = scheduler_type
        self.countdown_job = None

    @property
    def scheduler(self):
        return self._scheduler

    @scheduler.setter
    def scheduler(self, scheduler_type: str, num_workers: int = 1):
        if scheduler_type == 'BlockingScheduler':
            self._scheduler = BlockingScheduler()
        elif scheduler_type == 'BackgroundScheduler':
            self._scheduler = BackgroundScheduler(executors={
                'default': ThreadPoolExecutor(num_workers)
            })
        else:
            raise Exception('Unrecognized scheduler type!')

    @property
    def date_parts(self):
        return [
            'second', 'minute', 'hour', 'day', 'month', 'year',
            'day_of_week', 'week'
        ]

    def schedule(
        self,
        callback_func: Callable,
        cron_expression: str,
        misfire_grace_time: int = 2,
        job_name: str = ""
    ) -> None:
        """

        :param callback_func:
        :param cron_expression:
        :param misfire_grace_time:
        :param job_name:
        :return:
        """
        job_name = job_name if job_name else 'unknown'
        svt.log.info(
            f'Initialized scheduler job {} with cron expression: '
            f'{cron_expression}!'
        )
        ct = CronTrigger(
            name=job_name,
            misfire_grace_time=misfire_grace_time,
            **dict(zip(self.date_parts, cron_expression.split()))
        )
        self.scheduler.add_job(callback_func, ct)

    def start(self) -> None:
        self.scheduler.start()

    def shutdown(self, wait: bool = False) -> None:
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown(wait=wait)

    def countdown_timer(
        self,
        callback_func: Callable,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0
    ) -> None:
        pass

    @staticmethod
    def now(self):
        # replace to config read
        return datetime.now(tz.gettz(SV_TIME_ZONE))

    @staticmethod
    def now_as_str(self):
        # replace to config read
        return datetime.now(tz.gettz(SV_TIME_ZONE)).strftime(
            SV_DATE_TIME_FORMAT
        )

