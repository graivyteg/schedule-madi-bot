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
        result = f'{self.time} | {self.subject} | {self.type} | {self.week}'
        if len(self.classroom) > 0:
            result += f' | {self.classroom}'
        if len(self.teacher) > 0:
            result += f' | {self.teacher}'
        return result

