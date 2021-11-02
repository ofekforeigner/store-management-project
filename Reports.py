
class Reports:
    def __init__(self, db):
        self.db = db
        self.mycursor = self.db.cursor()

    # SHOW ALL REPORT TYPES
    def show_reports_types(self):
        self.mycursor.execute("SELECT * from report_types")
        data = self.mycursor.fetchall()
        return data
