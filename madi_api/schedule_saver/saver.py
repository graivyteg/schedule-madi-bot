from copy import copy
from typing import List

from databases.database_manager import DatabaseManager
from madi_api.data_containers.lesson import Lesson
from madi_api.data_containers.schedule import Schedule
from madi_api.data_containers.workday import WorkDay
from madi_api.network_loader import NetworkScheduleLoader


class ScheduleDBM(DatabaseManager):
    def __init__(self, database_name):
        super(ScheduleDBM, self).__init__(database_name)
        self.create_table()

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY,
            study_group TEXT,
            weekday INTEGER,
            time TEXT,
            subject TEXT,
            type TEXT,
            week TEXT,
            classroom TEXT,
            teacher TEXT
        )'''
        self.cur.execute(sql)
        self.conn.commit()

    def get_schedule_by_group(self, group) -> Schedule:
        sql = f'''SELECT * FROM schedules WHERE study_group = '{group}';'''
        self.cur.execute(sql)
        result = self.cur.fetchall()
        schedule = Schedule(workdays=[])
        for i in range(0, 6):
            schedule.workdays.append(WorkDay([]))
        for data in result:
            schedule.get_workday(data[2]).add_lesson(Lesson(
                time=data[3],
                subject=data[4],
                type=data[5],
                week=data[6],
                classroom=data[7],
                teacher=data[8]
            ))
        return schedule

    def update_schedules(self, schedules: dict):
        self.clear_table()
        id = 1
        for group in schedules.keys():
            for weekday in range(len(schedules[group].workdays)):
                workday = schedules[group].workdays[weekday]
                for lesson in workday.lessons:
                    sql = f'''INSERT INTO schedules 
                        (id, study_group, weekday, time, subject, type, week, classroom, teacher) VALUES 
                        ({id}, '{group}', {weekday}, '{lesson.time}', '{lesson.subject}', '{lesson.type}', 
                        '{lesson.week}', '{lesson.classroom}', '{lesson.teacher}');'''
                    self.cur.execute(sql)
                    id += 1
        self.conn.commit()

    async def load_and_save_schedules(self):
        schedules = await NetworkScheduleLoader.load_all_schedules(100)
        self.update_schedules(schedules)

    def clear_table(self):
        sql = f'''DELETE from schedules;'''
        self.cur.execute(sql)
        self.conn.commit()
