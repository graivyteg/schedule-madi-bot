import time

import aiohttp
import asyncio

from bs4 import BeautifulSoup

from schedule_loader.data_containers.lesson import Lesson
from schedule_loader.data_containers.schedule import Schedule
from schedule_loader.data_containers.workday import WorkDay
from schedule_loader.group_id_loader import GroupIdLoader
from schedule_loader.network_loader import NetworkScheduleLoader
from schedule_loader.schedule_saver.saver import ScheduleDBM


async def f(time):
    await asyncio.sleep(time)
    print(time)

async def main():
    schedules = await NetworkScheduleLoader.load_all_schedules(100)
    print('RESULT:', schedules)
    saver = ScheduleDBM()
    saver.update_schedules(schedules)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())