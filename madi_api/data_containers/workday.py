from copy import copy
from dataclasses import dataclass
from typing import List
from madi_api.data_containers.lesson import Lesson
from madi_api.even_odd_loader import EvenOddLoader


@dataclass
class WorkDay:
    lessons: List[Lesson]

    def __str__(self):
        #print([l.subject for l in self.lessons])
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
        result_lessons = []
        for lesson in temp_lessons:
            if (lesson.week == 'Числитель' and is_odd) or \
                    (lesson.week == 'Знаменатель' and not is_odd) or \
                    (lesson.week == 'Еженедельно'):
                result_lessons.append(lesson)
        if len(result_lessons) == 0:
            return '🍺 <b>Кажется, это выходной!</b>'
        for i in range(len(result_lessons)):
            result += f'📕 {str(result_lessons[i])}\n'
        return result


    def add_lesson(self, lesson: Lesson):
        self.lessons.append(lesson)