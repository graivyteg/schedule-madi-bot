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
        result = f'<b>[{self.time}] {self.subject}</b> ({self.week})\n' +\
                 f'{self.type}\n'
        if len(self.classroom) > 0:
            result += f'Аудитория {self.classroom}\n'
        if len(self.teacher) > 0:
            result += f'Преподаватель {" ".join(self.teacher.split())}\n'
        return result

