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

        for i in range(len(self.lessons)):
            result += f'<b>Пара {i + 1}</b>\n'
            result += str(self.lessons[i]) + '\n\n'
        return result

    def add_lesson(self, lesson: Lesson):
        self.lessons.append(lesson)