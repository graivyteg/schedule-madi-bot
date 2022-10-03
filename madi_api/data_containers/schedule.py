from copy import copy
from dataclasses import dataclass
from typing import List, Dict
from madi_api.data_containers.workday import WorkDay


@dataclass
class Schedule:
    workdays: Dict[int, WorkDay]

    def __str__(self):
        return 'РАСПИСАНИЕ:\n' + str(self.workdays)

    def get_schedule_at_day(self, day=0) -> WorkDay:
        if day >= 6 or day not in self.workdays.keys():
            return WorkDay([])
        return copy(self.workdays[day])

    def get_workday(self, weekday=0) -> WorkDay:
        if weekday >= 6:
            return WorkDay([])
        return self.workdays[weekday]


