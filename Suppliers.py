
from os import truncate
from re import T


class Suppliers():
    def __init__(self, db):
        self.db = db
        self.mycursor = self.db.cursor()

    # GET ALL SUPPLIERS NAMES
    def get_supplier_names(self):
        self.mycursor.execute(
            "SELECT supplier_name from suppliers WHERE status = 1")
        data = self.mycursor.fetchall()
        out = [name for n in data for name in n]
        return out

    # GET ALL SUPPLIERS DATA
    def get_suppliers(self):
        self.mycursor.execute("SELECT * from suppliers ORDER BY status DESC")
        data = self.mycursor.fetchall()
        return data

    # ADD NEW SUPPLIER

    def add_supplier(self, name, phone,mail):
        self.mycursor.execute(
            "SELECT supplier_name from suppliers")
        data = self.mycursor.fetchall()
        names = [name for n in data for name in n]
        if name in names:
            return False
        self.mycursor.execute("INSERT INTO suppliers(supplier_name,phone_number,email) VALUES(%s,%s,%s)",
                              (name, phone,mail))
        self.db.commit()
        self.mycursor.close()
        return True

    # EDIT A SPECIFIC SUPPLIER, CHECK WHICH PART THE USER INPUTED AND EDIT IT
    def edit_supplier(self, id, name, phone,mail):
        self.mycursor.execute(
            "UPDATE suppliers SET supplier_name = %s, phone_number = %s, email = %s WHERE supplier_id = %s", (name, phone,mail, id))
        self.db.commit()

    # CHANGE A SPECIFIC SUPPLIER STATUS, ACTIVE OR INACTIVE
    def change_supplier_status(self, id, status):
        self.mycursor.execute(
            "UPDATE suppliers SET status = %s WHERE supplier_id = %s", (status, id))
        self.db.commit()
