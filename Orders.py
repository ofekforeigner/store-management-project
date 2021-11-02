import re
import datetime


class Orders():
    def __init__(self, db):
        self.db = db
        self.mycursor = self.db.cursor()

    # GET A SPECIFIC ORDER INFO BY SUPPLIER NAME FROM THE DB
    def get_orders_by_supplier_name(self, name):
        self.mycursor.execute(
            "SELECT * from orders where supplier = '" + name + "'")
        data = self.mycursor.fetchall()
        return data

    # GET A SPECIFIC ORDER INFO BY ID FROM THE DB
    def get_order_info_by_id(self, id):
        self.mycursor.execute(
            "SELECT * from orders where order_id = '" + id + "'")
        data = self.mycursor.fetchall()
        return data

    # GET ALL ORDERS INFO FOR THE REPORTS
    def get_orders_to_reports(self):
        self.mycursor.execute(
            "SELECT order_id,supplier,order_type,price from orders ORDER BY order_date DESC")
        data = self.mycursor.fetchall()
        return data

    # GET ALL ORDERS FROM THE DB
    def get_orders(self):
        self.mycursor.execute(
            "SELECT * from orders ORDER BY order_checked, order_date DESC")
        data = self.mycursor.fetchall()
        return data

    # GET ALL ORDERS FROM THE DB
    def get_orders_by_supplier(self):
        self.mycursor.execute("SELECT * from orders ORDER BY supplier")
        data = self.mycursor.fetchall()
        return data

    # GET THE NUMBER OF ORDERS
    def get_orders_count(self):
        self.mycursor.execute(
            "SELECT count(*) from orders ORDER BY order_date DESC")
        data = self.mycursor.fetchall()
        return data

    # GET A SPECIFIC ORDER ITEMS INFO BY ID FROM THE DB
    def show_order_info_by_id(self, id):
        self.mycursor.execute(
            "SELECT * from ordersItems where order_id = '" + str(id) + "'")
        data = self.mycursor.fetchall()
        return data

    def show_order_name_and_quantity_by_id(self, id):
        self.mycursor.execute(
            "SELECT item_name,item_code,quantity from ordersItems where order_id = '" + str(id) + "'")
        data = self.mycursor.fetchall()
        out = [name for n in data for name in n]  # PLACE THE NAMES IN A LIST
        return out

    def show_order_quantity_by_id(self, orders_id):
        for order in orders_id:
            self.mycursor.execute(
                "SELECT item_code,quantity from ordersItems where order_id = '" + str(order) + "'")  # get items by id
            data = self.mycursor.fetchall()
            for info in data:
                self.mycursor.execute("UPDATE items SET amount = amount + " + str(
                    info[1]) + " WHERE catalogue_number = '" + str(info[0]) + "'")  # update amount items by barcode

    def close_order_by_type(self, orders_id):
        for order in orders_id:
            self.mycursor.execute(
                "UPDATE orders SET order_checked = 2 WHERE order_id= '" + str(order) + "'")
            self.db.commit()

    def close_expired_orders(self, orders_id):
        for order in orders_id:
            self.mycursor.execute(
                "UPDATE orders SET order_checked = 3 WHERE order_id= '" + str(order) + "'")
            self.db.commit()

    # CLOSE ORDER

    def close_order(self, orders_id):
        self.mycursor.execute(
            "SELECT item_code,quantity FROM ordersItems WHERE order_id = '" + str(orders_id) + "'")  # get items by id
        data = self.mycursor.fetchall()
        self.mycursor.execute(
            "SELECT order_type FROM orders WHERE order_id = '" + str(orders_id) + "'")
        order_type = self.mycursor.fetchall()[0][0]
        for info in data:
            if order_type == 'הזמנה מספק':
                self.mycursor.execute("UPDATE items SET amount = amount + " + str(
                    info[1]) + " WHERE catalogue_number = '" + str(info[0]) + "'")  # update amount items by barcode
        self.mycursor.execute(
            "UPDATE orders SET order_checked = 2 WHERE order_id= '" + str(orders_id) + "'")
        self.db.commit()

    def show_order_info_by_id_to_report(self, id):
        self.mycursor.execute(
            "SELECT item_name, item_code, quantity, piece_price, price from ordersItems where order_id = '" + str(id) + "'")
        data = self.mycursor.fetchall()
        return data

    def item_exist_by_barcode_in_specific_order(self, orderid, barcode):
        item_is_exist = False
        self.mycursor.execute(
            "SELECT * from ordersItems where order_id = '" + str(orderid) + "' AND item_code = '" + str(barcode) + "'")
        data = self.mycursor.fetchall()
        if data:
            item_is_exist = True
        return item_is_exist

    def get_order_checked_status(self, ordernumber):
        self.mycursor.execute(
            "SELECT order_checked FROM orders WHERE order_id = '" + str(ordernumber) + "'")
        data = self.mycursor.fetchall()
        return data[0][0]

    def show_order_info_by_id_report(self, id):
        self.mycursor.execute(
            "SELECT  * from ordersItems where order_id = '" + str(id) + "'")
        data = self.mycursor.fetchall()
        return data

    def get_orders_number_by_order_checked_status(self):
        self.mycursor.execute(
            "SELECT order_id FROM orders WHERE order_checked = '1' and order_date = CURDATE() AND order_type = 'הזמנה מספק'")
        data = self.mycursor.fetchall()
        data = [name for n in data for name in n]
        return data

    def get_orders_number_by_order_checked_status_expired_items(self):
        self.mycursor.execute(
            "SELECT order_id FROM orders WHERE order_checked = '1' and order_date = CURDATE() AND order_type = 'החזרת סחורה לספק'")
        data = self.mycursor.fetchall()
        data = [name for n in data for name in n]
        return data

    def get_expired_orders_number(self):
        self.mycursor.execute(
            "SELECT * FROM orders WHERE order_checked = '0' or  order_checked = '1'")
        data = self.mycursor.fetchall()
        orders = []
        for order in data:
            if order[5] < datetime.date.today():
                orders.append(order[0])
        return orders

    # ADD NEW ORDER TO THE DB, CHECKS IF THE ORDER HAS QUANTITY AND EXECUTE THR RIGHT QUERY

    def add_new_order(self, supplier_name, supplier_mail, order_date, order_type, quantity):
        if int(quantity) > 0:
            self.mycursor.execute(
                "INSERT INTO orders(supplier,supplier_mail,order_type, order_date, amount) VALUES(%s,%s,%s,%s,%s)", (supplier_name, supplier_mail, order_type, order_date, 0))
            self.db.commit()
        else:
            self.mycursor.execute(
                "INSERT INTO orders(supplier,supplier_mail,order_type, order_date, amount) VALUES(%s,%s,%s,%s,%s)", (supplier_name, supplier_mail, order_type, order_date, 0))
            self.db.commit()

    # ADD NEW ORDER FROM THE MANAGER HOME PAGE TO THE DB
    def add_order_from_home_page(self, supplier_name, order_date, order_type):
        self.mycursor.execute(
            "INSERT INTO orders(supplier,order_type, order_date, amount) VALUES(%s,%s,%s,%s)", (supplier_name, order_type, order_date, 0))
        self.mycursor.execute("INSERT INTO orders(supplier,order_type, order_date, amount) VALUES(%s,%s,%s,%s)",
                              (supplier_name, order_type, order_date, 0))
        self.db.commit()

    # CHECK IF THE ORDER IS EMPTY
    def order_is_empty(self, id):
        items_in_order = False
        self.mycursor.execute(
            "SELECT * FROM ordersitems WHERE order_id = '" + str(id) + "'")
        items = self.mycursor.fetchall()
        if items:
            items_in_order = True
        return items_in_order

# UPDATE ITEMS QUANTITY IN A SPECIFIC ORDER AFTER ADDING ITEMS
    def update_order_amount_after_adding_item(self, id):
        if self.order_is_empty(id):
            self.mycursor.execute(
                "UPDATE orders INNER JOIN ordersitems ON orders.order_id = ordersitems.order_id SET orders.amount =(SELECT COUNT(ordersitems.item_name) FROM ordersitems WHERE ordersitems.order_id=orders.order_id)")
        else:
            self.mycursor.execute(
                "UPDATE orders SET amount = 0 WHERE order_id = " + str(id))
        self.db.commit()

    # ADD EXPIRED ITEM TO A SPECIFIC ORDER BY ORDER NUMBER
    def add_item_into_order_by_order_number(self, item, ordernumber, quantity):
        if "<" in str(ordernumber):
            # SPLIT THE ORDER NUMER BECAUSE IT COMES WITH < >, WE USE REGEX TO GET ONLY THE NUMBER AND THEN WE CAN TAKE INDEX 1
            ordernumber = re.split("[<>]", ordernumber)
            if self.item_exist_by_barcode_in_specific_order(ordernumber[1], item[0][1]):
                self.mycursor.execute(
                    "UPDATE ordersitems SET quantity = quantity+ " + quantity + " WHERE order_id = '" + ordernumber[1] + "' AND item_code = '" + str(item[0][1]) + "'")
                self.update_order_sum_after_adding_item()
                self.update_order_amount_after_adding_item(ordernumber[1])
            else:
                self.mycursor.execute("INSERT INTO ordersitems(order_id,item_name,item_code,quantity,piece_price,price) VALUES(%s,%s,%s,%s,%s,%s)",
                                      (ordernumber[1], item[0][2], item[0][1], quantity, item[0][4], float(quantity)*float(item[0][4])))
                self.update_order_sum_after_adding_item()
                self.update_order_amount_after_adding_item(ordernumber[1])
        else:
            if self.item_exist_by_barcode_in_specific_order(ordernumber, item[0][1]):
                self.mycursor.execute(
                    "UPDATE ordersitems SET quantity = quantity+ " + quantity + " WHERE order_id = '" + ordernumber + "' AND item_code = '" + str(item[0][1]) + "'")
                self.update_order_sum_after_adding_item()
                self.update_order_amount_after_adding_item(ordernumber)
            else:
                self.mycursor.execute("INSERT INTO ordersitems(order_id,item_name,item_code,quantity,piece_price,price) VALUES(%s,%s,%s,%s,%s,%s)",
                                      (ordernumber, item[0][2], item[0][1], quantity, item[0][4], float(quantity)*float(item[0][4])))
                self.update_order_sum_after_adding_item()
                self.update_order_amount_after_adding_item(ordernumber)

    # ADD OUT OF STOCK ITEM TO A SPECIFIC ORDER BY ORDER NUMBER

    def add_oos_item_into_order_by_order_number(self, item, ordernumber, quantity):
        self.mycursor.execute("INSERT INTO ordersitems(order_id,item_name,item_code,quantity,piece_price,price) VALUES(%s,%s,%s,%s,%s,%s)",
                              (ordernumber, item[0][2], item[0][1], quantity, item[0][4], float(quantity)*float(item[0][4])))
        self.update_order_sum_after_adding_item()
        self.update_order_amount_after_adding_item(ordernumber)

    # UPDATE ORDER SUM AFTER ADDING ITEMS
    def update_order_sum_after_adding_item(self):
        self.mycursor.execute(
            "UPDATE orders SET orders.price=(SELECT SUM(ordersitems.price) FROM ordersitems WHERE ordersitems.order_id=orders.order_id)")
        self.db.commit()

    # REMOVE ITEMS FROM ORDER

    def get_item_from_order_by_item_id(self, id, itemid):
        self.mycursor.execute(
            "SELECT * from ordersitems WHERE ordersitems_id = '" + str(itemid) + "' AND order_id = '" + id + "'")
        data = self.mycursor.fetchall()
        return data

    def check_order_type(self, id):
        self.mycursor.execute(
            "SELECT order_type from orders where order_id = '" + id + "'")
        data = self.mycursor.fetchall()
        return data

    def update_stock_quantity_after_delete_item_from_order(self, quantity, barcode):
        self.mycursor.execute("UPDATE items SET amount = amount+ " + str(
            quantity) + "  WHERE catalogue_number = '" + str(barcode) + "'")
        self.db.commit()

    def remove_item_from_order(self, id, itemid):
        # before update stock check order type.
        if len(self.check_order_type(id)[0][0]) == 16:
            item_quantity = self.get_item_from_order_by_item_id(
                id, itemid)[0][4]  # get qunatity of this item
            barcode = self.get_item_from_order_by_item_id(id, itemid)[0][3]
            self.update_stock_quantity_after_delete_item_from_order(
                item_quantity, barcode)  # update the stock

        # delete item from order:
        self.mycursor.execute(
            "DELETE FROM ordersitems WHERE ordersitems_id = '" + str(itemid) + "' AND order_id = '" + id + "'")

        self.update_order_sum_after_adding_item()
        self.update_order_amount_after_adding_item(id)
        self.db.commit()

    # DELETE AN ORDER

    def delete_order(self, id):
        self.mycursor.execute(
            "DELETE FROM ordersitems WHERE order_id = '" + id + "'")
        self.mycursor.execute(
            "DELETE FROM orders WHERE order_id = '" + id + "'")
        self.db.commit()

    def approve_order_chekced_status(self, ordernumber):
        self.mycursor.execute(
            "UPDATE orders SET order_checked = 1 WHERE order_id = '" + ordernumber + "'")
        self.db.commit()

    def cancel_order_chekced_status(self, ordernumber):
        self.mycursor.execute(
            "UPDATE orders SET order_checked = 0 WHERE order_id = '" + ordernumber + "'")
        self.db.commit()

    # GET ALL EXPIRED ITEMS BY A SPECIFIC SUPPLIER

    def show_expired_items_by_supplier(self, supplier_name):
        self.mycursor.execute(
            "SELECT * from items WHERE supplier_name = '" + supplier_name + "' AND status = 1 AND experation_date <= CURRENT_DATE() AND amount > 0")
        data = self.mycursor.fetchall()
        if data:
            return data
        return False

    # GET ALL ITEMS BY A SPECIFIC SUPPLIER
    def show_items_by_supplier(self, supplier_name):
        self.mycursor.execute(
            "SELECT * from items WHERE supplier_name = '" + supplier_name + "' AND status = 1")
        data = self.mycursor.fetchall()
        if data:
            return data
        return False

    def get_supplier_mail_by_supplier_name(self, supplier_name):
        self.mycursor.execute(
            "SELECT email FROM suppliers WHERE supplier_name = '" + supplier_name + "'")
        data = self.mycursor.fetchall()
        if data:
            return data[0][0]
        return False

    # RESET ITEMS QUANTITY AFTER WE CREATE AN ORDER TO RETURN ITEMS TO THE SUPPLIER

    def reset_items_quantity_after_return_to_supplier(self, item_ids):
        if type(item_ids) == list:
            for item_id in item_ids:
                self.mycursor.execute(
                    "UPDATE items SET amount = 0 WHERE item_id = " + str(item_id))
                self.db.commit()
        else:
            self.mycursor.execute(
                "UPDATE items SET amount = 0  WHERE item_id = " + str(item_ids))
            self.db.commit()

    # GET THE LAST ORDER WE CREATED
    def get_last_inserted_order_id(self):
        self.mycursor.execute("SELECT MAX(order_id) FROM orders")
        data = self.mycursor.fetchall()
        return data

    # ADD EXPIRED ITEMS TO ORDER BY THIER BARCODE
    def add_item_to_order_by_barcode(self, barcodes, order_number):
        for barcode in barcodes:
            self.mycursor.execute(
                "SELECT * from items WHERE catalogue_number = '" + barcode + "'")
            item = self.mycursor.fetchall()
            self.add_item_into_order_by_order_number(
                item, order_number, item[0][3])

    # ADD OUT OF STOCK ITEMS TO ORDER BY THIER BARCODE
    def add_oos_item_to_order_by_barcode(self, barcodes, order_number, quantity):
        for barcode in barcodes:
            self.mycursor.execute(
                "SELECT * from items WHERE catalogue_number = '" + barcode + "'")
            item = self.mycursor.fetchall()
            self.add_oos_item_into_order_by_order_number(
                item, order_number, quantity)

    # GET THE TOP SOLD ITEMS FOR THE REPORT
    def get_top_5_sold_items_report(self, start_date, end_date):
        if start_date and end_date:
            self.mycursor.execute("SELECT SUM(ordersitems.quantity),ordersitems.item_name,ordersitems.item_code FROM ordersitems where order_id IN ( SELECT order_id FROM orders WHERE order_checked = 2 AND order_date >= '" +
                                  start_date + "' AND order_date <='"+end_date+"') GROUP by ordersitems.item_code  ORDER BY SUM(ordersitems.quantity) DESC LIMIT 5")
            data = self.mycursor.fetchall()
        elif not start_date and not end_date:
            self.mycursor.execute(
                "SELECT SUM(ordersitems.quantity),ordersitems.item_name,ordersitems.item_code FROM ordersitems where order_id IN ( SELECT order_id FROM orders WHERE order_checked = 2) GROUP by ordersitems.item_code  ORDER BY SUM(ordersitems.quantity) DESC LIMIT 5")
            data = self.mycursor.fetchall()
        print(data)
        return data

    def count_checked_orders(self):
        self.mycursor.execute(
            "SELECT COUNT(order_id) FROM orders WHERE order_checked = 0")
        data = self.mycursor.fetchall()
        return data[0][0]
