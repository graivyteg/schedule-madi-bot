from dataclasses import dataclass
from typing import List
from schedule_loader.data_containers.lesson import Lesson


@dataclass
class WorkDay:
    lessons: List[Lesson]

    def __str__(self):
        if len(self.lessons) == 0:
            return '<b>Кажется, это выходной!</b>'
        result = '<b>УЧЕБНЫЙ ДЕНЬ:</b> \n'
        for lesson in self.lessons:
            result += str(lesson) + '\n\n'
        return result

    def add_lesson(self, lesson: Lesson):
        self.lessons.append(lesson)