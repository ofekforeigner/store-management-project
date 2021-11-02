class Work_Schedule:
    def __init__(self, db):
        self.db = db
        self.mycursor = self.db.cursor()

    # ADD A NEW WORK SCHEDULE
    def add_work_schedule(self):
        self.mycursor.execute(
            "INSERT INTO work_schedule () VALUES ()")
        self.db.commit()

    # GET ALL WORK SCHEDULE
    def get_work_schedule(self):
        self.mycursor.execute("SELECT * FROM work_schedule ORDER BY id DESC")
        data = self.mycursor.fetchall()
        return data

    # GET A SPECIFIC WORK SCHEDULE BY ID
    def get_weekly_work_schedule_by_id(self, id):
        self.mycursor.execute(
            "SELECT * FROM weekly_work_schedule WHERE work_schedule_id = '" + str(id) + "'")
        data = self.mycursor.fetchall()
        return data
