import sys, os, shutil
from random import randint
import json
import time
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget


def load_data():
    """Загрузка данных из файла"""
    filename = "BankV2LoginHash.json"
    if not os.path.exists(filename):
        # Если файл не существует, создаем его с начальными данными
        initial_data = {
            "users": [
                {
                    "login": "admin",
                    "password": "takethel",
                    "group": "admin"
                },
                {
                    "login": "Br0k3n_",
                    "password": "lollollol",
                    "group": "UwU"
                }
            ]
        }
        with open(filename, "w") as file:
            json.dump(initial_data, file, indent=4)
    
    # Загружаем данные из файла
    try:
        with open(filename, "r") as file:
            return json.load(file)["users"]
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        return []


class RegWin(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.main_layout = QVBoxLayout()

        # Никнейм
        self.nickname_label = QLabel("НикНейм:")
        self.nickname_input = QLineEdit()
        nickname_box = QHBoxLayout()
        nickname_box.addWidget(self.nickname_label)
        nickname_box.addWidget(self.nickname_input)

        # Пароль
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        password_box = QHBoxLayout()
        password_box.addWidget(self.password_label)
        password_box.addWidget(self.password_input)

        # Повтор пароля
        self.repeat_password_label = QLabel("Повторите пароль:")
        self.repeat_password_input = QLineEdit()
        repeat_password_box = QHBoxLayout()
        repeat_password_box.addWidget(self.repeat_password_label)
        repeat_password_box.addWidget(self.repeat_password_input)

        # Кнопка создания аккаунта
        self.create_button = QPushButton("Создать")
        self.create_button.clicked.connect(self.register_user)

        # Кнопка возврата
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)

        # Добавляем все элементы в основной layout
        self.main_layout.addLayout(nickname_box)
        self.main_layout.addLayout(password_box)
        self.main_layout.addLayout(repeat_password_box)
        self.main_layout.addWidget(self.create_button)
        self.main_layout.addWidget(self.back_button)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def go_back(self):
        self.hide()
        self.parent.show()

    def register_user(self):
        global data
        login = self.nickname_input.text().strip()
        password1 = self.password_input.text().strip()
        password2 = self.repeat_password_input.text().strip()

        if not login or not password1 or not password2:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        if password1 != password2:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают.")
            return

        if any(user["login"] == login for user in data):
            QMessageBox.warning(self, "Ошибка", f"Пользователь с логином '{login}' уже существует.")
            return

        new_user = {
            "login": login,
            "password": password1,
            "group": "UwU"
        }
        data.append(new_user)

        # Сохраняем изменения в файл
        with open("BankV2LoginHash.json", "w") as file:
            json.dump({"users": data}, file, indent=4)

        QMessageBox.information(self, "Успех", "Пользователь успешно создан!")
        self.go_back()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()

        # Логин
        self.login_label = QLabel("Логин:")
        self.login_input = QLineEdit()
        login_box = QHBoxLayout()
        login_box.addWidget(self.login_label)
        login_box.addWidget(self.login_input)

        # Пароль
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        password_box = QHBoxLayout()
        password_box.addWidget(self.password_label)
        password_box.addWidget(self.password_input)

        # Кнопка входа
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.authenticate)

        # Кнопка регистрации
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.open_registration_window)

        # Добавляем все элементы в основной layout
        self.main_layout.addLayout(login_box)
        self.main_layout.addLayout(password_box)
        self.main_layout.addWidget(self.login_button)
        self.main_layout.addWidget(self.register_button)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def authenticate(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля.")
            return

        for user in data:
            if user["login"] == login and user["password"] == password:
                QMessageBox.information(self, "Успех", "Вы вошли в систему!")
                self.w = BankMSG(login)
                self.w.show()
                self.hide()
                break
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль.")

    def open_registration_window(self):
        self.registration_window = RegWin(parent=self)
        self.registration_window.show()
        self.hide()


class BankMSG(QDialog):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Приветствие")
        message = QLabel(f"Привет, {self.username}! Добро пожаловать в систему.")
        button = QPushButton("Продолжить")
        button.clicked.connect(self.BankEnter)

        layout = QVBoxLayout()
        layout.addWidget(message)
        layout.addWidget(button)

        self.setLayout(layout)

    def BankEnter(self):
        self.bank_window = Bank(self.username)
        self.bank_window.show()
        self.hide()


class Bank(QDialog):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.initUI()
        Snowflake = 0

    def initUI(self):
        self.setWindowTitle("Snowflake Bank")
        message = QLabel(f"""
                
Привет, {self.username}! Добро пожаловать в SFBank(snowflake).

""")
        button = QPushButton("""Заработать
(Это игровая валюта и она бесконечна)""")
        button.clicked.connect(self.EarnMoney)
        
        button = QPushButton("Перевод")
        button.clicked.connect(self.Transaktion)



        layout = QVBoxLayout()
        layout.addWidget(message)
        layout.addWidget(button)

        self.setLayout(layout)

    def EarnMoney(self):
        self.Snow_input = QLineEdit()
        box = QHBoxLayout()
        box.addWidget(self.Snow_input)
        Snowflake = Snowflake + self.Snow_input
    def Transaktion(self):
        self.Snow_Output = QLineEdit()
        box = QHBoxLayout()
        box.addWidget(self.Snow_Output)
    




data = load_data()
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())