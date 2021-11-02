from dns.rdatatype import NULL


class Items():
    def __init__(self, db, name, barcode, amount, buyprice, sellprice, experation_date, category, unit_of_measurment,
                 supplier_name):
        self.db = db
        self.mycursor = self.db.cursor()
        self.name = name
        self.barcode = barcode
        self.amount = amount
        self.buyprice = buyprice
        self.sellprice = sellprice
        self.experation_date = experation_date
        self.category = category
        self.unit_of_measurment = unit_of_measurment
        self.supplier_name = supplier_name

    # GET ALL ITEMS
    def get_items(self):
        self.mycursor.execute(
            "SELECT * from items ORDER BY status DESC, experation_date, supplier_name")
        data = self.mycursor.fetchall()
        return data

    # GET ALL ITEMS OF A SPECIFIC SUPPLIER
    def get_items_by_supplier(self, supplier_name):
        self.mycursor.execute(
            "SELECT * from items WHERE supplier_name = '" + supplier_name + "'")
        data = self.mycursor.fetchall()
        return data

    # GET ALL ITEMS BY ID
    def get_items_by_id(self, item_id):
        self.mycursor.execute(
            "SELECT * from items WHERE item_id = '" + item_id + "'")
        data = self.mycursor.fetchall()
        return data

    # ADD ITEM TO THE DB
    def add_item(self):
        self.mycursor.execute(
            "SELECT item_name from items")
        data = self.mycursor.fetchall()
        names = [name for n in data for name in n]
        if self.name in names:
            return False
        self.mycursor.execute(
            "INSERT INTO items(catalogue_number, item_name, amount, buy_price, sell_price, experation_date, category, unit_of_measurment, supplier_name) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (self.barcode, self.name, self.amount, self.buyprice, self.sellprice, self.experation_date, self.category,
             self.unit_of_measurment, self.supplier_name))
        self.db.commit()
        return True

    # EDIT AN ITEM
    def edit_item(self, id):
        self.mycursor.execute("UPDATE items SET item_name = %s, catalogue_number = %s, amount = %s, buy_price = %s, sell_price = %s, supplier_name = %s, experation_date = %s, category = %s, unit_of_measurment = %s WHERE item_id = %s",
                              (self.name, self.barcode, self.amount, self.buyprice, self.sellprice, self.supplier_name, self.experation_date, self.category, self.unit_of_measurment, id))
        self.db.commit()

    # GET ALL EXPIRED ITEMS
    def show_expired_items(self):
        self.mycursor.execute(
            "SELECT * FROM items WHERE status = 1 AND experation_date <= CURRENT_DATE() AND amount > 0 ORDER BY supplier_name")
        data = self.mycursor.fetchall()
        return data

    # CHANGE ITEM STATUS, ACTIVE OR INACTIVE
    def change_item_status(self, id, status):
        self.mycursor.execute(
            "UPDATE items SET status = %s WHERE item_id = %s", (status, id))
        self.db.commit()

#-----------------------------pdf-------------------------------#

    def print_expired_items_in_pdf(self, start_date, end_date):
        if start_date and end_date:
            self.mycursor.execute("SELECT item_id,item_name,catalogue_number,amount,supplier_name FROM items WHERE status = 1 AND experation_date >= '" +
                                  start_date + "' AND experation_date <= '" + end_date + "' AND amount > 0 ORDER BY item_id")
        elif not start_date and not end_date:
            print(start_date)
            print(end_date)
            self.mycursor.execute(
                "SELECT item_id,item_name,catalogue_number,amount,supplier_name FROM items WHERE status = 1 AND amount > 0 AND experation_date < CURRENT_DATE() OR (experation_date = CURRENT_DATE() AND experation_date <= CURRENT_TIME()) ORDER BY item_id")
        data = self.mycursor.fetchall()
        return data

    # PRINT ALL ITEMS TO PDF
    def print_all_items_in_pdf(self):
        self.mycursor.execute(
            "SELECT item_id,item_name,catalogue_number,amount,supplier_name from items WHERE status = 1 ORDER BY item_id")
        data = self.mycursor.fetchall()
        return data

        # GET THE QUANTITY OF THE EXPIRED ITEMS THAT ARE ACTIVE ///pdf number 3

    def print_all_ItemsAmount_in_pdf(self, amount):
        self.mycursor.execute(
            "SELECT item_id,item_name,catalogue_number,amount,supplier_name from items WHERE amount <= '" + amount + "' ")
        data = self.mycursor.fetchall()
        return data

    def get_quntity_of_ItemsAmount(self, amount):
        self.mycursor.execute(
            "SELECT count(amount) from items WHERE amount <= '" + amount + "'")
        data = self.mycursor.fetchall()
        return data

    # ----------------------------------------------------------------------------------

    # GET THE QUANTITY OF THE EXPIRED ITEMS THAT ARE ACTIVE ///pdf number 2
    def get_quntity_of_expired_items(self, start_date, end_date):
        if start_date and end_date:
            self.mycursor.execute(
                "SELECT count(amount) from items WHERE experation_date >= '" + start_date + "' AND experation_date <= '" + end_date + "' ")
        elif not start_date and not end_date:
            self.mycursor.execute(
                "SELECT count(amount) from items WHERE experation_date <= CURRENT_DATE() ")
        data = self.mycursor.fetchall()
        return data

    # GET THE QUANTITY OF ALL ITEMS THAT ARE ACTIVE //pdf number 1
    def items_quantity(self):
        self.mycursor.execute("SELECT sum(amount) from items WHERE status = 1")
        data = self.mycursor.fetchall()
        return data
