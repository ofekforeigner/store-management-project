class Users:
    def __init__(self, db, username, name, isAdmin):
        self.db = db
        self.username = username
        self.name = name
        self.isAdmin = isAdmin
        self.mycursor = self.db.cursor()

        # GET EMPLOYEE NAME BY USERNAME
    def get_employee_name_by_username(self, username):
        self.mycursor.execute(
            "SELECT employee_name FROM employees WHERE employee_username = '" + username + "'")
        data = self.mycursor.fetchall()
        return data

    def get_employee_by_username(self, username) -> tuple:
        self.mycursor.execute(
            "SELECT * FROM employees WHERE employee_username = '" + username + "'")
        data = self.mycursor.fetchall()
        return data
    # ------------------edit------------------------

    # EDIT A SPECIFIC USER, CHECK WHICH PART THE USER INPUTED AND EDIT IT
    def edit_user(self, id):
        self.mycursor.execute(
            "UPDATE employees SET employee_name = %s, employee_username = %s WHERE employee_id = %s", (self.name, self.username, str(id)))
        self.db.commit()

    # -------------------login---------------------------------------------

    # GET EMPLOYEE USERNAME AND PASSWORD TO LOGIN
    # def user_login(self):
    #     return self.mycursor.execute(
    #         "SELECT * FROM employees WHERE employee_username = '" + self.username + "' AND employee_password = '" + self.password + "'")

    # -------------------------register----------------------------------------

    # GET ALL EMPLOYEES
    def get_employees(self):
        self.mycursor.execute("SELECT * from employees ORDER BY status DESC")
        data = self.mycursor.fetchall()
        return data

    # GET ALL EMPLOYEES NAMES
    def get_employees_names(self):
        self.mycursor.execute("SELECT employee_name from employees")
        data = self.mycursor.fetchall()
        return data

    # INSERT NEW EMPLOYEE TO THE EMPLOYEES TABLE (REGISTER)
    def user_register(self, password):
        self.mycursor.execute(
            "INSERT INTO employees(employee_username, employee_password, employee_name, employee_role) VALUES(%s,%s,%s,%s)",
            (self.username, password, self.name, self.isAdmin))
        self.db.commit()

    # GET AN EMPLOYEE BY USERNAME TO CHECK IF EXISTS IN EMPLOYEES TABLE
    # def check_user_Exists(self) -> tuple:
    #     return self.mycursor.execute("SELECT * FROM employees WHERE employee_username = '" + self.username + "'")

    # CHECK IF EXISTS IN EMPLOYEES TABLE
    def check_if_user_exists(self):
        self.mycursor.execute(
            "SELECT * FROM employees WHERE employee_username = '" + self.username + "'")
        data = self.mycursor.fetchall()
        if data == []:
            return True
        return False

    # CHECK IF EMPLOYEE LOGIN DATA ARE VALID
    # def check_user_login_vaildation(self):
    #     mycursor = self.db.cursor()
    #     self.user_login()
    #     data = mycursor.fetchall()
    #     if data != []:
    #         self.db.commit()
    #         mycursor.close()
    #         return True
    #     return False

    # CHEKC IF EMPLOYEE IS ADMIN OR NOT
    def is_admin(self):
        self.mycursor.execute(
            "SELECT employee_role FROM employees WHERE employee_username = '" + self.username + " '")
        data = self.mycursor.fetchall()
        return data

    # CHACNGE EMPLOYEE STATUS, ACTIVE OR INACTIVE
    def change_employee_status(self, id, status):
        self.mycursor.execute(
            "UPDATE employees SET status = %s WHERE employee_id = %s", (str(status), str(id)))
        self.db.commit()

        # def change_contact_status(self, id, status):
        # self.mycursor.execute(
        #     "UPDATE contacts SET status = %s WHERE contact_id = %s", (status, id))
        # self.db.commit()

    def count_employees(self):
        self.mycursor.execute(
            "SELECT COUNT(employee_id) FROM employees WHERE status=1")
        data = self.mycursor.fetchall()
        return data[0][0]
