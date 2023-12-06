from abc import ABC, abstractmethod
import sqlite3
import os
import time


def clear_console():
      os.system('cls')

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, values=None):
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        self.conn.commit()

    def fetch_data(self, query, values=None):
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

class User:
    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def save_to_db(self):
        db = Database('users.db')
        query = 'CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, password TEXT, role VARCHAR(20))'
        db.execute_query(query)
        query = 'INSERT INTO Users (name, email, password, role) VALUES (?, ?, ?, ?)'
        values = (self.name, self.email, self.password, self.role)
        db.execute_query(query, values)
        db.close()

class Product:
    def __init__(self, name, description, price, colvo, id):
        self.name = name
        self.description = description
        self.price = price
        self.colvo = colvo
        self.id = id

    def save_to_db(self):
        db = Database("products.db")
        query = 'CREATE TABLE IF NOT EXISTS Products (id INTEGER PRIMARY KEY, name TEXT, description TEXT, price REAL, colvo INT)'
        db.execute_query(query)
        query = 'INSERT INTO Products (name, description, price, colvo) VALUES (?, ?, ?, ?)'
        values = (self.name, self.description, self.price, self.colvo)
        db.execute_query(query, values)
        db.close()
        
    def update_db(self):
        db = Database("products.db")
        query = 'UPDATE Products SET name = ?, description = ?, price = ?, colvo = ? WHERE id = ?'
        values = (self.name, self.description, self.price, self.colvo, self.id)
        db.execute_query(query, values)
        db.close()
        
    def display_sorted_products(self):
        db = Database("products.db")
        query = 'SELECT * FROM Products ORDER BY name'
        products = db.execute_query(query)
        for product in products:
            print(product)
        db.close()
        

class Authentication(ABC):
    @abstractmethod
    def register(self, name, email, password, role):
        pass

    @abstractmethod
    def login(self, email, password, role):
        pass

class UserAuthentication:
    

    def register(self, name, email, password, role):
        user = User(name, email, password, role)
        user.save_to_db()
        print('Вы успешно зарегистрированы!')
        Main.vhod1(self, role)

    def login(self, email, password, role):
        db = Database('users.db')
        query = 'SELECT * FROM Users WHERE email=? AND password=? AND role=?'
        values = (email, password, role)
        result = db.fetch_data(query, values)
        db.close()
        if result:
            print('Вход выполнен успешно!')
            Main.vhod1(self, role)
        else:
            print('Неверный email, пароль или роль \n Система заблокирована, перезапустите')
       
class Korzina:
    def __init__(self, fio, id_tovara, adresdostavki, status, id):
        self.fio = fio
        self.id_tovara = id_tovara
        self.adresdostavki = adresdostavki
        self.status = status
        self.id = id
        
    def save_to_db(self):
        db = Database("zakaz.db")
        query = 'CREATE TABLE IF NOT EXISTS Zakaz (id INTEGER PRIMARY KEY, fio TEXT, id_tovara TEXT, adresdostavki TEXT, status TEXT)'
        db.execute_query(query)
        query = 'INSERT INTO Zakaz (fio, id_tovara, adresdostavki, status) VALUES (?, ?, ?,?)'
        values = (self.fio, self.id_tovara, self.adresdostavki, self.status)
        db.execute_query(query, values)
        db.close()
        
        # def update_db(self):
        # db = Database("products.db")
        # query = 'UPDATE Products SET name = ?, description = ?, price = ?, colvo = ? WHERE id = ?'
        # values = (self.name, self.description, self.price, self.colvo, self.id)
        # db.execute_query(query, values)
        # db.close()
        
    def update(self):
        db = Database("zakaz.db")
        query = 'UPDATE Zakaz SET status = ? WHERE id = ?'
        values = (self.status, self.id)
        db.execute_query(query, values)
        db.close()
         
class Main:
    def __init__(self):
        self.authentication = UserAuthentication()
      
        
        

    def display_menu(self):
        print("Добро пожаловать в магазин 'Istore'!")
        print("====================================")
        print("Выберите нужный Вам пункт: ")
        print(" ")
        print("1. Вход")
        print("2. Регистрация")
        print(" ")

    def handle_menu_choice(self, choice ):
        if choice == "1":
            clear_console()
            print("Выполните вход в систему! \n Для этого введите свои данные :)")
            print(" ")
            email = input("Введите email: ")
            password = input("Введите пароль: ")
            role = input("Введите вашу роль admin/client: ")
            self.authentication.login(email, password, role)
            
        elif choice == "2":
            clear_console()
            print("Мы рады, что Вы решились стать частичкой нашего магазина!!!\n Здесь Вам необходимо заполнить следующие данные ")
            print(" ")
            name = input("Введите имя: ")
            email = input("Введите email: ")
            password = input("Введите пароль: ")
            role = input("Введите свою роль admin/client: ")
            self.authentication.register(name, email, password, role)

    def vhod1(self, role):
       
        if role == "admin":
            clear_console()
            print("Вы вошли в меню администратора!!!")
            print("=================================")
            print("Выберите нужный пункт: ")
            print("1. Добавление нового товара")
            print("2. Обновление товара")
            print("3. Вывести все товары магазина")
            print("4. Вывести все заказы")
            print("5. Изменить статус заказа")
            print("6. Выйти")
            vib = input("Ваш выбор: ")
            if vib == "1":
                clear_console()
                name = input("Введите название товара: ")
                description = input("Введите описание товара: ")
                price = input("Введите цену товара: ")
                colvo = input("Введите количество: ")
                product = Product(name, description,  price, colvo, 0)
                product.save_to_db()
                print("Товар сохранён!!!")
                time.sleep(2)
                Main.vhod1(self, role)
            if vib == "2":
                clear_console()
                name = input("Измените имя товара: ")
                description = input("Измените описание товара: ")
                price = input("Измените цену товара: ")
                colvo = input("Измените количество: ")
                id = input("Введите id товара: ")
                update = Product(name, description,  price, colvo, id)
                update.update_db()
                print("Товар сохранён!!!")
                time.sleep(2)
                Main.vhod1(self, role)
            if vib == "3":
                clear_console()
                connection = sqlite3.connect('products.db')
                cursor = connection.cursor()
                products = cursor.execute("SELECT * FROM products").fetchall()
                spisok = list()
                print("id | name | description | price | colvo")
                for i in range(4):
                    for j in range(5):
                        spisok.append(products[i][j])
                    print(*spisok)
                    spisok = list()
                connection.close()
                time.sleep(2)
                Main.vhod1(self, role)
            if vib == "4":
                clear_console()
                connection = sqlite3.connect('zakaz.db')
                cursor = connection.cursor()
                products = cursor.execute("SELECT * FROM zakaz").fetchall()
                print("ID заказа, ФИО клиента, ID товара, Адрес доставки, Cтатус Доставки")
                for product in products:
                    print(*product)  
                    
                connection.close()
                time.sleep(10)
                Main.vhod1(self, role)
                
            if vib == "5":
                clear_console()
                id = input("Введите id заказа: ")
                status = input("Введите новый статус заказа: ")
                update1 = Korzina(None, None, None, status, id)
                update1.update()
                print("Статус сохранен!!!")
                time.sleep(2)
                Main.vhod1(self, role)
                
            if vib == "6":
                clear_console()
                print("До свидания! Перезапустите программу:)")
                
                
        else:
            clear_console()
            print("Вы вошли в меню клиента!!!")
            print("=================================")
            print("Выберите нужный пункт: ")
            print("1. Ассортимент товаров и выбор")
            print("2. Данные о заказах")
            print("3. Выйти")

            vib = input("Ваш выбор: ")

            if vib == "1":
                clear_console()
                print("Вот наш ассортимент: ")
                print("ID товара, Наименование, Описание, Цена, Количество")
                connection = sqlite3.connect('products.db')
                cursor = connection.cursor()
                products = cursor.execute("SELECT * FROM products").fetchall()
                spisok = list()
                for i in range(1):
                    for j in range(5):
                        spisok.append(products[i][j])
                    print(*spisok)
                    spisok = list()
                connection.close()
                print("=========================================================")
                fio = input("Введите своё ФИО: ")    
                id_tovara = input("Введите ID товара, который  хотите заказать: ")
                adresdostavki = input("Введити адрес доставки: ")
                status = input("Статус заказ (если вы клиент напишите '-'): ")
               
                zakaz = Korzina(fio, id_tovara, adresdostavki, status, 0)
                zakaz.save_to_db()
                print("Ваш заказ успешно сохранён!")
                time.sleep(2)
                Main.vhod1(self, role)
                
            if vib == "2":
                clear_console()
                connection = sqlite3.connect('zakaz.db')
                cursor = connection.cursor()
                products = cursor.execute("SELECT * FROM zakaz").fetchall()
                print("ID заказа, ФИО клиента, ID товара, Адрес доставки, Cтатус Доставки")
                for product in products:
                    print(*product)  # Assuming each row in 'zakaz' table has 5 columns
        
                connection.close()
                time.sleep(2)
                Main.vhod1(self, role)
                
            if vib == "3":
                clear_console()
                print("До свидания! Перезапустите программу:)")
                
                


if __name__ == "__main__":
    main = Main()
    main.display_menu()
    choice = input("Ваш выбор: ")
    main.handle_menu_choice(choice)
   
    
   
    
    
