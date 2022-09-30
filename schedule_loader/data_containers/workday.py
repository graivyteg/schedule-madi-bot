from dataclasses import dataclass
from typing import List
from schedule_loader.data_containers.lesson import Lesson


@dataclass
class WorkDay:
    lessons: List[Lesson]

    def __str__(self):
        result = 'УЧЕБНЫЙ ДЕНЬ: \n'
        for lesson in self.lessons:
            result += str(lesson) + '\n'
        return result