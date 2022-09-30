import time

import aiohttp
import asyncio

from bs4 import BeautifulSoup

from schedule_loader.data_containers.lesson import Lesson
from schedule_loader.data_containers.schedule import Schedule
from schedule_loader.data_containers.workday import WorkDay
from schedule_loader.group_id_loader import GroupIdLoader
from schedule_loader.loader import ScheduleLoader


async def main():
    day = int(input())
    loader = ScheduleLoader('1бАСУ1')
    schedule = await loader.load_schedule()
    print(str(schedule.get_schedule(day)))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())