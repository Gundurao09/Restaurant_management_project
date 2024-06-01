from database import database

class Queries:
    def __init__(self, database=database(), dbname=None):
        self.database = database
        self.text = database.get_connect()
        if dbname:
            self.create_database(dbname)
        else:
            print("Database Not exists provide it as Query parameter")
            exit(0)
        self.text.execute("""
            CREATE TABLE IF NOT EXISTS user (
                user_id INT PRIMARY KEY Auto_Increment,
                name VARCHAR(100),
                email VARCHAR(100) unique,
                password VARCHAR(100),
                city VARCHAR(50),
                phone_no VARCHAR(50)
            );""")
        self.text.execute("""
            CREATE TABLE IF NOT EXISTS item (
                item_id INT PRIMARY KEY Auto_Increment,
                name VARCHAR(100),
                item_amount DECIMAL(16,2),
                category VARCHAR(100)
            );""")
        self.text.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_no INTEGER PRIMARY KEY Auto_Increment,
                quantity INT,
                user_id INTEGER,
                item_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES user(user_id),
                FOREIGN KEY (item_id) REFERENCES item(item_id) 
            );""")
        self.text.execute("""
            CREATE TABLE IF NOT EXISTS Admin(
            admin_id int primary key Auto_increment,
            admin_name varchar(20),
            city VARCHAR(50),
            phone_no VARCHAR(50)
            );""")
        self.text.execute("""
        CREATE TABLE IF NOT EXISTS Bill(
        bill_id int Auto_increment,
        order_no int,
        primary key(bill_id,order_no),
        FOREIGN KEY (order_no) REFERENCES orders(order_no))
        
                          ;""")

    def insert(self, table_name, values, parameters=None):
        """
        returns int
        """
        data_to_insert = f"""
            INSERT INTO {table_name} {f"({parameters})" if parameters else ""} VALUES ({values})"""
        self.text.execute(data_to_insert)
        self.database.commit()
        return self.text.rowcount

    def create_database(self, dbname):
        self.text.execute(f"CREATE DATABASE IF NOT EXISTS {dbname};")
        self.text.execute(f"USE {dbname};")
    
    def check_login(self,email,password):
        self.text.execute(f"""
        select user_id from user where email = '{email}' and password = '{password}';""")
        return self.text.fetchall()
    
    def get_current_user_info(self,user_id):
        self.text.execute(f"""
        select name from user where user_id = {user_id};""")
        return self.text.fetchall()
    
    def get_items(self):
        self.text.execute(f"""
        select name,item_amount,category from item;""")
        return self.text.fetchall()
    
    def check_item(self,item_name):
        self.text.execute(f"""
        select name from item where name = '{item_name}';""")
        return self.text.fetchall()
    
    def delete_database(self,dbname):
        self.text.execute(f"drop database if exists {dbname};")
    
    def select(self,table):
        self.text.execute(f"""
        select * from {table};""")
        a = self.text.fetchall()
        print(a)
    def northern_food(self):
            self.text.execute(f"""
        SELECT name, item_amount FROM item WHERE category = 'northern_food';""")
            return self.text.fetchall()
    def southern_food(self):
        self.text.execute(f"""
        SELECT name, item_amount FROM item WHERE category = 'southern_food';""")
        return self.text.fetchall()
    def snacks(self):
        self.text.execute(f"""
        SELECT name, item_amount FROM item WHERE category = 'snacks';""")
        return self.text.fetchall()
    def chect_item_id(self, name):
        self.text.execute(f"""
            SELECT item_id FROM item WHERE name = '{name}';
        """)
        return self.text.fetchall()
    def check_user_id(self, email):
        self.text.execute(f"""
            SELECT user_id FROM user WHERE email = '{email}';
        """)
        return self.text.fetchall()
    def insert_order(self,item_id,user_id,quantity):
        """
        returns int
        """
        data_to_insert = f"""
           INSERT INTO ORDERS (item_id,user_id,quantity) values ({item_id},{user_id},{quantity});
        """
        self.text.execute(data_to_insert)
        self.database.commit()
        return self.text.rowcount
    def order_details_north(self):
            self.text.execute(f"""
select o.ORDER_NO,i.name,c.name,c.phone_no,i.category,o.quantity
from  user c ,item i,orders o
where o.user_ID = c.user_ID and o.ITEM_ID=i.ITEM_ID and i.category='northern_food';
        """)
            return self.text.fetchall()
    def order_details_south(self):
            self.text.execute(f"""
select o.ORDER_NO,i.name,c.name,c.phone_no,i.category,o.quantity
from  user c ,item i,orders o
where o.user_ID = c.user_ID and o.ITEM_ID=i.ITEM_ID and i.category='southern_food';
        """)
            return self.text.fetchall()
    def order_details_(self):
            self.text.execute(f"""
select o.ORDER_NO,i.name,c.name,c.phone_no,i.category,o.quantity
from  user c ,item i,orders o
where o.user_ID = c.user_ID and o.ITEM_ID=i.ITEM_ID and i.category='snacks';
        """)
            return self.text.fetchall()
    def order_count(self):
            self.text.execute(f"""
        select count(order_no)
        from orders;
        """)
            return self.text.fetchall()
    def user_count(self):
            self.text.execute(f"""
        select count(user_id)
        from user;
        """)
            return self.text.fetchall()
    def item_count(self):
            self.text.execute(f"""
        select count(item_id)
        from item;
        """)
            return self.text.fetchall()
    def bill(self,user_id):
         self.text.execute(f"""
            SELECT o.order_no,u.name,i.name,o.quantity,i.item_amount,(o.quantity * i.item_amount) AS total_cost
            FROM Orders o
            JOIN  User u ON o.user_id = u.user_id
            JOIN Item i ON o.item_id = i.item_id;
            where u.user_id = {user_id}  """)
         return self.text.fetchall()
    def order_no_check(self):
        self.text.execute(f"""
        CREATE TRIGGER IF NOT EXISTS insert_order_into_bill
        AFTER INSERT
        ON Orders FOR EACH ROW

        BEGIN
        INSERT INTO Bill (order_no) VALUES (NEW.order_no);
        END;

        //

        DELIMITER ;                    
""")


        

        

    
    





    
