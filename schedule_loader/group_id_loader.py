import aiohttp
from bs4 import BeautifulSoup

from schedule_loader.request_data.group_id_request_data import *


class GroupIdLoader:
    def __init__(self, group):
        self.group = group

    async def get_group_id(self) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://www.madi.ru/tplan/tasks/task3,7_fastview.php',
                                    data=data,
                                    cookies=cookies,
                                    headers=headers) as response:
                html = await response.text()
                soup = BeautifulSoup(html, features='html.parser')
                groups = soup.find_all('li')
                for li in groups:
                    if li.text == self.group:
                        return li['value']
                return ''