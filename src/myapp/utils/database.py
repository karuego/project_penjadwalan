import os
from .waktu_util import TimeSlotManager
from .schedule_generator import ScheduleGenerator
from .database_manager import DatabaseManager


class Database:
    DB_FILE: str = "database.sqlite3.db"

    def __init__(self):
        self.db_manager: DatabaseManager = DatabaseManager(self.DB_FILE)

        is_exist = False
        if not os.path.exists(self.DB_FILE):
            self.db_manager.init_database()
            is_exist = True

        self.timeslot_manager: TimeSlotManager = TimeSlotManager(self.db_manager)
        self.schedule_generator: ScheduleGenerator = ScheduleGenerator(
            self.timeslot_manager
        )

        if is_exist:
            # total_generated, results = self.schedule_generator.generate_schedule()
            _ = self.schedule_generator.generate_schedule()
