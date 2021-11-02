import itertools


class Contacts:
    def __init__(self, db, name, address, city, phone, mail, status):
        self.db = db
        self.name = name
        self.address = address
        self.city = city
        self.phone = phone
        self.mail = mail
        self.status = status
        self.mycursor = self.db.cursor()

    # GET ALL CONTACTS
    def get_contacts(self):
        self.mycursor.execute("SELECT * FROM contacts ORDER BY status DESC")
        data = self.mycursor.fetchall()
        return data

    # GET THE EMAIL OF THE CONTACT BY ITS NAME
    def get_contact_email(self):
        self.mycursor.execute(
            "SELECT email FROM contacts WHERE fullname = '" + self.name + "'")
        cdata = self.mycursor.fetchall()
        c_list = list(itertools.chain(*cdata))
        self.mycursor.execute(
            "SELECT email FROM suppliers WHERE supplier_name = '" + self.name + "'")
        sdata = self.mycursor.fetchall()
        s_list = list(itertools.chain(*sdata))
        return c_list+s_list

    # ADD NEW CONTACT TO THE DB
    def add_contact(self):
        self.mycursor.execute(
            "SELECT fullname from contacts")
        data = self.mycursor.fetchall()
        names = [name for n in data for name in n]
        if self.name in names:
            return False
        self.mycursor.execute("INSERT INTO contacts(email, fullname, phone, address,city, status) VALUES(%s,%s,%s,%s,%s,'1')",
                              (self.mail, self.name, self.phone, self.address, self.city))
        self.db.commit()
        return True

    # EDIT A CONTACT, CHECK WHICH PART THE USER INPUTED AND EDIT IT
    def edit_contact(self, id):
        self.mycursor.execute(
            "UPDATE contacts SET fullname = %s, address = %s, city = %s, phone = %s, email = %s WHERE contact_id = %s", (self.name, self.address, self.city, self.phone, self.mail, id))
        self.db.commit()

    # CHANGE CONTACT STATUS, ACCTIVE OR INACTIVE

    def change_contact_status(self, id, status):
        self.mycursor.execute(
            "UPDATE contacts SET status = %s WHERE contact_id = %s", (status, id))
        self.db.commit()

    def get_cities(self):
        self.mycursor.execute(
            "SELECT * FROM cities")
        data = self.mycursor.fetchall()
        cities = []
        for city in data:
            cities.append(city[1])
        return cities

    def get_streets(self):
        self.mycursor.execute(
            "SELECT * FROM streets")
        data = self.mycursor.fetchall()
        strrets = []
        for street in data:
            strrets.append(street[1])
        return strrets
