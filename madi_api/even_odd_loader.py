import asyncio
import re
from datetime import datetime

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from typing import List

from madi_api.request_data.even_odd_request_data import cookies, headers, data

class DateMinMax:
    def __init__(self, min_date, max_date):
        self.min_date = min_date
        self.max_date = max_date

    def is_in(self, date: datetime):
        return self.min_date < date < self.max_date

    def __str__(self):
        return f'From {self.min_date.strftime("%d/%m/%Y")} to {self.max_date.strftime("%d/%m/%Y")}'


class EvenOddLoader:
    def __init__(self):
        pass

    async def load_html(self):
        url = 'https://www.madi.ru/tplan/tasks/print_calendar.php'
        async with ClientSession() as session:
            async with session.post(url,
                                    data=data,
                                    cookies=cookies,
                                    headers=headers) as response:
                html = await response.text()
        return html

    async def is_today_odd(self) -> bool:
        html = await self.load_html()
        soup = BeautifulSoup(html, features='html.parser')
        tds = soup.find_all('td')
        for td in tds:
            if td.has_attr('bgcolor') and len(td['bgcolor']) > 0:
                return td.text == 'Числитель'

    def _get_years(self, soup: BeautifulSoup) -> List[int]:
        return [int(year) for year in soup.find('p').text.split(' ')[0].split('-')]

    async def get_even_odd_schedule(self) -> dict:
        html = await self.load_html()
        soup = BeautifulSoup(html, features='html.parser')
        trs = soup.find_all('tr')
        temp_dict = {}
        for i in range(len(trs)):
            tds = trs[i].find_all('td')
            for j in range(len(tds)):
                if tds[j].text == 'Числитель' or tds[j].text == 'Знаменатель':
                    continue
                if i + 1 < len(trs) and len(trs[i + 1].find_all('td')) > 0:
                    temp_dict[tds[j].text] = trs[i + 1].find_all('td')[j].text

        years = self._get_years(soup)
        result = {}
        for key in temp_dict:
            splitted = re.split('[- .]', key)
            for i in range(len(splitted)):
                if '' in splitted:
                    splitted.remove('')
            splitted = [int(x) for x in splitted]
            if len(splitted) == 3:
                splitted.insert(1, splitted[2])
            min_date = datetime(years[0], splitted[1], splitted[0])
            max_date = datetime(years[0], splitted[3], splitted[2])
            minmax = DateMinMax(min_date, max_date)
            result[minmax] = temp_dict[key] == 'Числитель'
        return result

    async def is_date_odd(self, date: datetime):
        schedule = await self.get_even_odd_schedule()
        for minmax in schedule:
            if minmax.is_in(date):
                return schedule[minmax]
