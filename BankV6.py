import json
import os
import sys
import uuid
from random import randint
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget


# Константа для количества зарабатываемых/переводимых снежинок
snowmoney_AMOUNT = 1000

# Минимальная и максимальная длина логинов и паролей
MIN_LOGIN_LENGTH = 3
MAX_LOGIN_LENGTH = 20
MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 30

# Проверка логина
def validate_login(login):
    if MIN_LOGIN_LENGTH <= len(login) <= MAX_LOGIN_LENGTH:
        return True
    return False

# Проверка пароля
def validate_password(password):
    if MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
        return True
    return False

# Класс для хранения данных пользователя
class UserData:
    def __init__(self, users=[]):
        self.users = users

    @staticmethod
    def load_from_file(filename="BankV2LoginHash.json"):
        """Загрузка данных из файла"""
        if not os.path.exists(filename):
            # Если файл не существует, создаем его с начальными данными
            initial_data = {
                "users": [
                    {
                        "login": "Br0k3n_",
                        "password": "lollollol",
                        "group": "UwU",
                        "snowmoney": 0
                    }
                ]
            }
            with open(filename, "w") as file:
                json.dump(initial_data, file, indent=4)

        # Загружаем данные из файла
        try:
            with open(filename, "r") as file:
                return UserData(json.load(file)["users"])
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            return UserData()

    def save_to_file(self, filename="BankV2LoginHash.json"):
        """Сохранение данных в файл"""
        try:
            with open(filename, "w") as file:
                json.dump({"users": self.users}, file, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")

    def find_user_by_login(self, login):
        """Поиск пользователя по логину"""
        for user in self.users:
            if user["login"] == login:
                return user
        return None

    def add_user(self, login, password):
        """Добавление нового пользователя"""
        new_user = {
            "login": login,
            "password": password,
            "group": "UwU",
            'snowmoney': 0
        }
        self.users.append(new_user)
        return new_user

    def update_snowmoney(self, login, amount):
        """Обновление баланса снежинок пользователя"""
        user = self.find_user_by_login(login)
        if user is not None:
            user['snowmoney'] += amount
            return True
        return False

# Создание полей ввода
def create_input_field(label_text, placeholder_text=""):
    label = QLabel(label_text)
    input_field = QLineEdit()
    input_field.setPlaceholderText(placeholder_text)
    hbox = QHBoxLayout()
    hbox.addWidget(label)
    hbox.addWidget(input_field)
    return hbox, input_field

class RegWin(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.main_layout = QVBoxLayout()
        self.setWindowTitle("Регистрация")
        
        # Никнейм
        nickname_hbox, self.nickname_input = create_input_field("НикНейм:", "Введите никнейм")
        self.main_layout.addLayout(nickname_hbox)

        # Пароль
        password_hbox, self.password_input = create_input_field("Пароль:", "Введите пароль")
        self.main_layout.addLayout(password_hbox)

        # Повтор пароля
        repeat_password_hbox, self.repeat_password_input = create_input_field("Повторите пароль:", "Повторите пароль")
        self.main_layout.addLayout(repeat_password_hbox)

        # Кнопка создания аккаунта
        self.create_button = QPushButton("Создать")
        self.create_button.clicked.connect(self.register_user)
        self.main_layout.addWidget(self.create_button)

        # Кнопка возврата
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.go_back)
        self.main_layout.addWidget(self.back_button)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def go_back(self):
        self.hide()
        self.parent.show()

    def register_user(self):
        login = self.nickname_input.text().strip()
        password1 = self.password_input.text().strip()
        password2 = self.repeat_password_input.text().strip()

        if not login or not password1 or not password2:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        if password1 != password2:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")

        if not validate_login(login):
            QMessageBox.warning(self, "Ошибка", "Логин должен содержать от 3 до 20 символов.")
            return

        if not validate_password(password1):
            QMessageBox.warning(self, "Ошибка", "Пароль должен содержать от 6 до 30 символов.")
            return

        userdata = UserData.load_from_file()
        if userdata.find_user_by_login(login) is not None:
            QMessageBox.warning(self, "Ошибка", f"Пользователь с логином '{login}' уже существует.")
            return

        new_user = userdata.add_user(login, password1)
        userdata.save_to_file()

        QMessageBox.information(self, "Успех", "Пользователь успешно создан!")
        self.go_back()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.userdata = UserData.load_from_file()
        self.main_layout = QVBoxLayout()
        self.setWindowTitle("Вход в SnF Bank")

        # Логин
        login_hbox, self.login_input = create_input_field("Логин:", "Введите ваш логин")
        self.main_layout.addLayout(login_hbox)

        # Пароль
        password_hbox, self.password_input = create_input_field("Пароль:", "Введите ваш пароль")
        self.main_layout.addLayout(password_hbox)

        # Кнопка входа
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.authenticate)
        self.main_layout.addWidget(self.login_button)

        # Кнопка регистрации
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.open_registration_window)
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

        user = self.userdata.find_user_by_login(login)
        if user is None:
            QMessageBox.warning(self, "Ошибка", "Пользователя с таким логином не существует.")
            return

        QMessageBox.information(self, "Успех", "Вы вошли в систему!")
        self.w = Bank(user["login"], self.userdata)
        self.w.show()
        self.hide()

    def open_registration_window(self):
        self.registration_window = RegWin(parent=self)
        self.registration_window.show()
        self.hide()


class Bank(QDialog):
    def __init__(self, username, userdata):
        super().__init__()
        self.username = username
        self.userdata = userdata
        self.initUI()

    def initUI(self):
        self.setWindowTitle("snowmoney Bank")
        message = QLabel(f"Привет, {self.username}! Добро пожаловать в систему.")

        button = QPushButton("Заработать")
        button.clicked.connect(self.EarnMoney)

        button2 = QPushButton("Перевести")
        button2.clicked.connect(self.TransferMoney)

        layout = QVBoxLayout()
        layout.addWidget(message)
        layout.addWidget(button)
        layout.addWidget(button2)

        self.setLayout(layout)

    def EarnMoney(self):
        self.label = QLabel("Сумма:")
        self.Input = QLineEdit()
        box = QHBoxLayout()
        box.addWidget(self.label)
        box.addWidget(self.Input)
        success = self.userdata.update_snowmoney(self.username, snowmoney_AMOUNT)
        if success:
            QMessageBox.information(self, "Успешно!", f"Вы заработали {snowmoney_AMOUNT} снежинок!")
        else:
            QMessageBox.warning(self, "Ошибка", "Что-то пошло не так. Попробуйте еще раз.")

    def TransferMoney(self):
        user = self.userdata.find_user_by_login(self.username)
        if user['snowmoney'] < snowmoney_AMOUNT:
            QMessageBox.warning(self, "Недостаточно средств", "На вашем счету недостаточно снежинок для этой операции.")
            return

        success = self.userdata.update_snowmoney(self.username, -snowmoney_AMOUNT)
        if success:
            QMessageBox.information(self, "Успешно!", f"Вы перевели {snowmoney_AMOUNT} снежинок.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())