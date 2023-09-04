import asyncio
from copy import copy

import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, List

from madi_api.data_containers.lesson import Lesson
from madi_api.data_containers.schedule import Schedule
from madi_api.data_containers.workday import WorkDay
from madi_api.group_id_loader import GroupIdLoader
from madi_api.request_data.schedule_request_data import *

weekdays = {
    'Понедельник': 0,
    'Вторник': 1,
    'Среда': 2,
    'Четверг': 3,
    'Пятница': 4,
    'Суббота': 5,
    'Полнодневные занятия': 7
}

class NetworkScheduleLoader:
    def __init__(self, group: str):
        self.group = group

    @classmethod
    async def load_schedule_by_group(cls, group) -> Schedule:
        schedule = await NetworkScheduleLoader(group).load_schedule()
        return schedule

    async def load_schedule(self) -> Schedule:
        result = None
        while result is None:
            try:
                result = await self.get_html()
            except:
                print('Caught error, restarting...')
                await asyncio.sleep(3)

        soup = BeautifulSoup(result, features='html.parser')
        trs = soup.find_all('tr')
        #if len(trs) == 0:
        #    await asyncio.sleep(1)
        #    return await self.load_schedule()
        started = False
        lessons = []
        workdays = {}
        for wd in weekdays.keys():
            workdays[weekdays[wd]] = WorkDay([])

        weekday = None
        for i in range(len(trs)):
            tds = [td.text for td in trs[i].find_all('td')]
            th = trs[i].find('th')
            if th is not None and th.text in weekdays.keys():
                weekday = weekdays[th.text]
            '''if len(tds) < 6 and started:
                print(lessons)
                workday = WorkDay(copy(lessons))
                workdays[weekday] = copy(workday)
                lessons.clear()'''
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
                workdays[weekday].lessons.append(lesson)
                #lessons.append(lesson)
            #if th is not None and th.text == 'Полнодневные занятия':
            #    continue
        return copy(Schedule(workdays))

    async def get_html(self) -> str:
        group_id = await GroupIdLoader(self.group).get_group_id()
        data = copy(request_data)
        data['gp_name'] = self.group
        data['gp_id'] = group_id
        async with aiohttp.ClientSession() as session:
            async with session.post('https://raspisanie.madi.ru/tplan/tasks/tableFiller.php',
                                    data=data,
                                    cookies=cookies,
                                    headers=headers) as response:
                html = await response.text()
        return html

    @classmethod
    async def load_all_schedules(cls, tasks_per_time=3) -> dict:
        groups = await GroupIdLoader.get_all_groups()
        result = {}
        tasks = {}
        for i in range(0, len(groups), tasks_per_time):
            slice = await cls.__load_part_schedules(list(groups.keys()), i, tasks_per_time)
            for key in slice.keys():
                result[key] = slice[key]
        # for group in groups.keys():
        #    result[group] = await ScheduleLoader.load_schedule_by_group(group)
        return result

    @classmethod
    async def __load_part_schedules(cls, groups: List[str], start, tasks_amount) -> Dict[str, Schedule]:
        #await asyncio.sleep(2)
        print(f'Loading... {start}/{len(groups)}')
        end = start + tasks_amount
        if end > len(groups):
            end = len(groups)
        keys = groups[start:end]
        tasks = []
        result = {}
        i = 0
        for i in range(len(keys)):
            tasks.append(asyncio.create_task(NetworkScheduleLoader.load_schedule_by_group(keys[i])))
        await asyncio.gather(*tasks)
        for i in range(len(keys)):
            result[keys[i]] = tasks[i].result()
        return result
