class Tasks:
    def __init__(self, db, name, task, task_date, taskId):
        self.db = db
        self.name = name
        self.task_date = task_date
        self.task = task
        self.mycursor = self.db.cursor()
        self.taskId = taskId

    # GET ALL TASKS
    def get_all_tasks(self):
        self.mycursor.execute("SELECT * from tasks ORDER BY completed")
        data = self.mycursor.fetchall()
        return data

    # ADD NEW TASK
    def add_task(self):
        self.mycursor.execute(
            "INSERT INTO tasks(employee_name, task, task_date)  VALUES(%s,%s,%s)", (self.name, self.task, self.task_date))
        self.db.commit()

    # DELETE TASK
    def delete_task(self):
        sql = "DELETE FROM tasks WHERE task_id =%s"
        adr = (self.taskId,)
        self.mycursor.execute(sql, adr)
        self.db.commit()




    # DELETE ALL TASKS
    def delete_all_tasks(self):
        self.mycursor.execute("DELETE FROM tasks")
        self.db.commit()

    # CHANGE STATUS OF A SPECIFIC TASK TO COMPLETETD IN THE DB
    def completed_tasks(self):
        self.mycursor.execute(
            "UPDATE tasks SET completed=%s WHERE task_id=%s", (True, self.taskId))
        self.db.commit()

    # GET THE NUMBER OF COMPLETED TASKS FOR THE DASHBOARD
    def count_completed_tasks_for_dashboard(self):
        self.mycursor.execute(
            "SELECT COUNT(completed) FROM tasks WHERE completed = TRUE")
        data = self.mycursor.fetchall()
        all_tasks = self.get_all_tasks()
        if len(all_tasks) > 0:
            # FOR THE TASKS LINE IN THE DASHBOARD, CT = COMPLETED TASKS
            ct = int(data[0][0] / len(all_tasks) * 100)
            arr = [data[0][0], len(all_tasks), ct]
        else:
            arr = [0, 0, 0]  # IF THERE ARE NO TASKS
        return arr
