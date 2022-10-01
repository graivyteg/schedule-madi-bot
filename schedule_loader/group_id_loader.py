import aiohttp
from bs4 import BeautifulSoup, ResultSet

from schedule_loader.request_data.group_id_request_data import *


class GroupIdLoader:
    def __init__(self, group):
        self.group = group

    @classmethod
    async def get_html(cls) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://www.madi.ru/tplan/tasks/task3,7_fastview.php',
                                    data=data,
                                    cookies=cookies,
                                    headers=headers) as response:
                return await response.text()

    @classmethod
    async def get_groups_html(cls) -> ResultSet:
        html = await cls.get_html()
        soup = BeautifulSoup(html, features='html.parser')
        groups = soup.find_all('li')
        return groups

    async def get_group_id(self) -> str:
        groups = await self.get_groups_html()
        for li in groups:
            if li.text == self.group:
                return li['value']
        return ''

    @classmethod
    async def get_all_groups(cls) -> dict:
        groups = await cls.get_groups_html()
        result = {}
        for li in groups:
            result[li.text.replace(' ', '')] = li['value']
        return result
