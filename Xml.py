import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
import datetime


class Xml:
    def __init__(self):
        self.filename = 'settings.xml'
        self.xmlTree = ET.parse(self.filename)
        self.root_element = self.xmlTree.getroot()
        self.business_details_list = []

    def sound_set(self, sound):
        # this function set from xml file the task boolean value.
        for value in self.root_element.findall('sound'):
            if sound == "1":
                value.find('soundValue').text = "True"
            else:
                value.find('soundValue').text = ""
        self.xmlTree.write(self.filename, encoding='UTF-8',
                           xml_declaration=True)

    def sound_get(self):
        for value in self.root_element.findall('sound'):
            self.flag_value = value.find('soundValue').text
        return self.flag_value

    def tasks_get(self):
        # this function get from xml file the task boolean value.
        for value in self.root_element.findall('Alerts'):
            self.flag_value = value.find('Tasks').text
        return self.flag_value

    def tasks_set(self, flag_value):
        # this function set from xml file the task boolean value.
        for value in self.root_element.findall('Alerts'):
            if flag_value == "1":
                value.find('Tasks').text = "True"
            else:
                value.find('Tasks').text = ""
        self.xmlTree.write(self.filename, encoding='UTF-8',
                           xml_declaration=True)

    def task_alert(self, db):
        """
        this function get tasks date and check if date time is today return the mission
        :return:
        """
        mycursor = db.cursor()
        mycursor.execute("SELECT * from tasks")
        # makes a list of tuples, every tuple is a row in the database
        data = mycursor.fetchall()
        tasks_to_display = []
        for task in data:  # runing each row
            # check if task date is today (task[3]= task date)
            if task[3] <= datetime.date.today():
                tasks_to_display.append(task)  # save tasks in list
        return tasks_to_display  # send tasks with date today.

    def advert_get(self):
        # this function get from xml file the advert boolean value.
        for value in self.root_element.findall('Alerts'):
            self.flag_value = value.find('Advert').text
        return self.flag_value

    def advert_set(self, flag_value):
        # this function set from xml file the advert boolean value.
        for value in self.root_element.findall('Alerts'):
            if flag_value == "1":
                value.find('Advert').text = "True"
            else:
                value.find('Advert').text = ""
        self.xmlTree.write(self.filename, encoding='UTF-8',
                           xml_declaration=True)

    ########################items date alert################################

    def items_get(self):
        # this function get from xml file the advert boolean value.
        for value in self.root_element.findall('Alerts'):
            self.flag_value = value.find('Items').text
        return self.flag_value

    def items_set(self, flag_value):
        # this function set from xml file the advert boolean value.
        for value in self.root_element.findall('Alerts'):
            if flag_value == "1":
                value.find('Items').text = "True"
            else:
                value.find('Items').text = ""
        self.xmlTree.write(self.filename, encoding='UTF-8',
                           xml_declaration=True)

    def items_date_alert(self, db):
        mycursor = db.cursor()
        mycursor.execute(
            "SELECT * from items WHERE status = 1 AND amount <> 0 ORDER BY supplier_name")
        data = mycursor.fetchall()
        item_to_display = []
        for item in data:
            if item[6] <= datetime.date.today():
                item_to_display.append(item)
        return item_to_display

    ##########################################################################

    ########################items amount alert################################

    # set and get amount:
    def items_amount_get(self):
        # this function get from xml file the advert boolean value.
        for value in self.root_element.findall('Alerts'):
            self.flag_value = value.find('ItemsAmount').text
        return self.flag_value

        # set and get alert value:

    def items_value_amount_get(self):
        # this function get from xml file the advert boolean value.
        for value in self.root_element.findall('Alerts'):
            self.flag_value = value.find('ItemsAmountValue').text
        return self.flag_value

    def items_amount_set(self, flag_value, amount):
        # this function set from xml file the advert boolean value.
        for value in self.root_element.findall('Alerts'):
            if flag_value == "1":
                value.find('ItemsAmountValue').text = "True"
            else:
                value.find('ItemsAmountValue').text = ""
            self.xmlTree.write(
                self.filename, encoding='UTF-8', xml_declaration=True)

            if amount:
                value.find('ItemsAmount').text = amount
            self.xmlTree.write(self.filename, encoding='UTF-8',
                               xml_declaration=True)

    def items_amount_alert(self, db):
        mycursor = db.cursor()
        mycursor.execute(
            "SELECT * from items WHERE status = 1 AND experation_date >= CURRENT_DATE() OR status = 1 AND experation_date < CURRENT_DATE() AND amount = 0  ORDER BY supplier_name")
        data = mycursor.fetchall()
        item_to_display = []
        for item in data:
            if int(item[3]) <= int(self.items_amount_get()):
                item_to_display.append(item)
        return item_to_display

        ##########################################################################

    def email_get(self):
        # this function get from xml file the email string value.
        for value in self.root_element.findall('mail'):
            self.flag_value = value.find('email').text
        return self.flag_value

    def pass_get(self):
        # this function get from xml file the email pass value.
        for value in self.root_element.findall('mail'):
            self.flag_value = value.find('pass').text
        return self.flag_value

    def email_set(self, email, password):
        # this function set from xml file the email and pass Details.
        for value in self.root_element.findall('mail'):
            if email:
                value.find('email').text = email
            if password:
                value.find('pass').text = password
        self.xmlTree.write(self.filename, encoding='UTF-8',
                           xml_declaration=True)

    def business_details_get(self):
        # this function get from xml file the BusinessDetails.
        for value in self.root_element.findall('BusinessDetails'):
            self.business_details_list.append(value.find('name').text)
            self.business_details_list.append(value.find('address').text)
            self.business_details_list.append(value.find('Bn').text)
            self.business_details_list.append(value.find('phone').text)
            self.business_details_list.append(value.find('email').text)
        return self.business_details_list

    def task_alert(self, db):
        """
        this function get tasks date and check if date time is today return the mission
        :return:
        """
        mycursor = db.cursor()
        mycursor.execute("SELECT * from tasks")
        # makes a list of tuples, every tuple is a row in the database
        data = mycursor.fetchall()
        mission_to_display = []
        for mission in data:  # runing each row
            # check if mission date is today (mission[3]= mission date)
            if mission[3] <= datetime.date.today():
                mission_to_display.append(mission)  # save mission in list
        return mission_to_display  # send missions with date today.
