from dataclasses import dataclass


@dataclass
class Lesson:
    time: str
    subject: str
    type: str
    week: str  # Нечетная - числитель, четная - знаменатель
    classroom: str
    teacher: str

    def __str__(self):
        result = f'[{self.time}] <i>{self.subject}</i> ({self.week})\n' +\
                 f'{self.type}'
        if len(self.classroom) > 0:
            result += f'Аудитория {self.classroom}\n'
        if len(self.teacher) > 0:
            result += f'Преподаватель {self.teacher}\n'
        return result

