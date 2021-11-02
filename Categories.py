
class Categories():
    def __init__(self, db, category_name):
        self.db = db
        self.category_name = category_name
        self.mycursor = self.db.cursor()

    # GET ALL CATEGORIES
    def get_categories(self):
        self.mycursor.execute("SELECT * from categories ORDER BY status DESC")
        data = self.mycursor.fetchall()
        return data

    # GET CATEGORIES ID AND NAME FOR THE PDF REPORT
    def get_categories_to_pdf(self):
        self.mycursor.execute(
            "SELECT Category_id,Category_name from categories where status = 1 ORDER BY status DESC")
        data = self.mycursor.fetchall()
        return data

    # GET THE QUANTITY OF CATEGORIES WITH THE SAME NAME
    def get_quntity_of_categories(self):
        self.mycursor.execute(
            "SELECT count(Category_name) from categories where status = 1 ")
        data = self.mycursor.fetchall()
        return data

    # GET ALL CATEGORIES NAME
    def get_category_names(self):
        self.mycursor.execute("SELECT Category_name from categories")
        data = self.mycursor.fetchall()
        out = [name for n in data for name in n]  # PLACE THE NAMES IN A LIST
        return out

    # ADD CATEGORY TO THE DB
    def add_category(self):
        self.mycursor.execute(
            "INSERT INTO categories(Category_name,status) VALUES (%s,%s)", (self.category_name, 1))
        self.db.commit()

    # EDIT CATEGORY
    def edit_category(self, id):
        self.mycursor.execute(
            "UPDATE categories SET category_name = %s WHERE category_id = %s", (self.category_name, id))
        self.db.commit()

    # CHANGE CATEGORY STATUS, ACTIVE OR IN ACTIVE
    def change_category_status(self, id, status):
        self.mycursor.execute(
            "UPDATE categories SET status = %s WHERE Category_id = %s", (status, id))
        self.db.commit()
