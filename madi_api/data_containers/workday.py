from copy import copy
from dataclasses import dataclass
from typing import List
from madi_api.data_containers.lesson import Lesson
from madi_api.even_odd_loader import EvenOddLoader


@dataclass
class WorkDay:
    lessons: List[Lesson]

    def __str__(self):
        if len(self.lessons) == 0:
            return '🍺 <b>Кажется, это выходной!</b>'
        result = '📆 <b>УЧЕБНЫЙ ДЕНЬ:</b> \n\n'

        for i in range(len(self.lessons)):

            result += f'<b>📕 ПАРА {i + 1}</b>\n'
            result += str(self.lessons[i]) + '\n'
        return result

    def str_even_odd(self, is_odd) -> str:
        result = '📆 <b>УЧЕБНЫЙ ДЕНЬ ({})</b>\n\n'.format('Числитель' if is_odd else 'Знаменатель')

        temp_lessons = copy(self.lessons)
        for lesson in temp_lessons:
            if (lesson.week == 'Числитель' and not is_odd) or \
                    (lesson.week == 'Знаменатель' and is_odd):
                temp_lessons.remove(lesson)
        if len(temp_lessons) == 0:
            return '🍺 <b>Кажется, это выходной!</b>'
        for i in range(len(temp_lessons)):
            result += f'📕 <b>ПАРА {i + 1}</b>\n'
            result += str(temp_lessons[i]) + '\n'
        return result


    def add_lesson(self, lesson: Lesson):
        self.lessons.append(lesson)