from copy import copy

import aiohttp
from bs4 import BeautifulSoup

from schedule_loader.data_containers.lesson import Lesson
from schedule_loader.data_containers.schedule import Schedule
from schedule_loader.data_containers.workday import WorkDay
from schedule_loader.group_id_loader import GroupIdLoader
from schedule_loader.request_data.schedule_request_data import *


class ScheduleLoader:
    def __init__(self, group: str):
        self.group = group

    async def load_schedule(self) -> Schedule:
        result = await self.get_html()
        soup = BeautifulSoup(result, features='html.parser')
        trs = soup.find_all('tr')
        started = False
        lessons = []
        workdays = []

        for i in range(len(trs)):
            tds = [td.text for td in trs[i].find_all('td')]
            if len(tds) < 6 and started:
                workday = WorkDay(copy(lessons))
                workdays.append(workday)
                lessons.clear()
                continue
            if len(tds) == 6 and not tds[0] == 'Время занятий':
                started = True
                lesson = Lesson(
                    time=tds[0],
                    subject=tds[1],
                    type=tds[2],
                    week=tds[3],
                    classroom=tds[4],
                    teacher=tds[5]
                )
                lessons.append(lesson)
        return Schedule(workdays)

    async def get_html(self) -> str:
        group_id = await GroupIdLoader(self.group).get_group_id()
        data = copy(request_data)
        data['gp_name'] = self.group
        data['gp_id'] = group_id
        async with aiohttp.ClientSession() as session:
            async with session.post('https://www.madi.ru/tplan/tasks/tableFiller.php',
                                    data=data,
                                    cookies=cookies,
                                    headers=headers) as response:
                html = await response.text()
        return html

