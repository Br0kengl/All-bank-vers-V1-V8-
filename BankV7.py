import json
import os
import sys
from os import path
from random import randint
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
#from unidecode import unidecode



# Константа для количества зарабатываемых/переводимых снежинок
SNOWFLAKE_AMOUNT = 1000

# Класс для хранения данных пользователя
class UserData:
    def __init__(self, users):
        self.users = users

    @staticmethod
    def load_from_file(filename = "BankV2LoginHash.json"):
        """Загрузка данных из файла"""
        if not os.path.exists(filename):
            # Если файл не существует, создаем его с начальными данными
            initial_data = {
                "users": [
                    {
                        "login": "admin",
                        "password": "takethel",
                        'group': 'UwU',
                        "snowmoney": 0
                    },
                    {
                        "login": "Br0k3n_",
                        "password": "lollollol",
                        'group': 'UwU',
                        "snowmoney": 0
                    },
                    {
                        "login": "lol",
                        "password": "lol",
                        'group': 'UwU',
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

    def update_snowflake(self, login, amount):
        """Обновление баланса снежинок пользователя"""
        user = self.find_user_by_login(login)
        if user is not None:
            user['snowmoney'] += amount
            return True
        return False


class RegWin(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.main_layout = QVBoxLayout()
        self.setWindowTitle("Регистрация")
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
        login = self.nickname_input.text().strip()
        password1 = self.password_input.text().strip()
        password2 = self.repeat_password_input.text().strip()

        if not login or not password1 or not password2:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        if password1 != password2:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают.")
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

        user = self.userdata.find_user_by_login(login)
        if user is None:
            QMessageBox.warning(self, "Ошибка", "Пользователя с таким логином не существует.")
            return

        if user["password"] != password:
            QMessageBox.warning(self, "Ошибка", "Неверный пароль.")
            return

        QMessageBox.information(self, "Успех", "Вы вошли в систему!")
        self.w = Bank(user["login"], self.userdata)
        self.w.show()
        self.hide()
    
    def closeEvent(self, event):
        # Спрашиваем подтверждение перед закрытием
        confirmation = QMessageBox.question(self, "Закрыть?", "Хочешь закрыть прогу(твои снежинки не будут сохраться)?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            err()
            event.ignore()  # Закрываем приложение
        else:
            event.ignore()
    
    def open_registration_window(self):
        self.registration_window = RegWin(parent=self)
        self.registration_window.show()
        self.hide()

class Bank(QDialog):
    def __init__(self, username, userdata):
        super().__init__()
        self.username = username
        self.userdata = userdata
        self.user = self.userdata.find_user_by_login(username)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Snowflake Bank")
        message = QLabel(f"""
Привет, {self.username}! Добро пожаловать в систему.
""")
        balance_message = QLabel(f"""Текущий баланс: {self.user['snowmoney']} снежинок
                                 """)

        button = QPushButton("Заработать")
        button.clicked.connect(self.EarnMoney)

        button2 = QPushButton("Перевести")
        button2.clicked.connect(self.TransferMoney)

        layout = QVBoxLayout()
        layout.addWidget(message)
        layout.addWidget(balance_message)
        layout.addWidget(button)
        layout.addWidget(button2)

        self.setLayout(layout)

    def EarnMoney(self, login):
        self.label = QLabel("Сумма:")
        self.Input = QLineEdit()
        box = QHBoxLayout()
        box.addWidget(self.label)
        box.addWidget(self.Input)

        def on_accept():
            try:
                amount = int(self.Input.text())
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной.")
                
                success = self.userdata.update_snowflake(self.username, amount)
                if success:
                    QMessageBox.information(self, "Успешно!", f"Вы заработали {amount} снежинок!")
                    UserData.update_snowflake(self, login, amount)
                else:
                    QMessageBox.warning(self, "Ошибка", "Что-то пошло не так. Попробуйте еще раз.")
            
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", str(e))

        accept_button = QPushButton("Подтвердить")
        accept_button.clicked.connect(on_accept)
        box.addWidget(accept_button)

        self.layout().addLayout(box)

    def TransferMoney(self):
        recipient_label = QLabel("Получатель:")
        recipient_input = QLineEdit()
        amount_label = QLabel("Сумма:")
        amount_input = QLineEdit()

        def on_transfer():
            recipient = recipient_input.text().strip()
            try:
                amount = int(amount_input.text())
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной.")
                
                sender = self.userdata.find_user_by_login(self.username)
                if sender['snowmoney'] < amount:
                    QMessageBox.warning(self, "Недостаточно средств", "На вашем счету недостаточно снежинок для этой операции.")
                    return

                recipient_user = self.userdata.find_user_by_login(recipient)
                if recipient_user is None:
                    QMessageBox.warning(self, "Ошибка", f"Пользователь '{recipient}' не найден.")
                    return

                sender_success = self.userdata.update_snowflake(self.username, -amount)
                recipient_success = self.userdata.update_snowflake(recipient, amount)

                if sender_success and recipient_success:
                    QMessageBox.information(self, "Успешно!", f"Вы перевели {amount} снежинок пользователю '{recipient}'.")
                else:
                    QMessageBox.warning(self, "Ошибка", "Что-то пошло не так. Попробуйте еще раз.")
            
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", str(e))
        
        transfer_button = QPushButton("Перевести")
        transfer_button.clicked.connect(on_transfer)

        layout = QGridLayout()
        layout.addWidget(recipient_label, 0, 0)
        layout.addWidget(recipient_input, 0, 1)
        layout.addWidget(amount_label, 1, 0)
        layout.addWidget(amount_input, 1, 1)
        layout.addWidget(transfer_button, 2, 0, 1, 2)

        self.layout().addLayout(layout)

    def closeEvent(self, event):
        # Спрашиваем подтверждение перед закрытием
        confirmation = QMessageBox.question(self, "Закрыть?", "Хочешь закрыть прогу(твои снежинки не будут сохраться)?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            QMessageBox.warning(self, "Ну ладно", "Ну ладно... как хочешь)")
            os.startfile("e:/Сергей л/Bank project/fakeVirus.py")
            event.accept()  # Закрываем приложение
        else:
            event.ignore()

    def update_balance(self):
        self.user = self.userdata.find_user_by_login(self.username)
        balance_message = self.findChild(QLabel, "balance_message")
        balance_message.setText(f"Текущий баланс: {self.user['snowmoney']} снежинок")

class err(QWidget):
    def __init__(self):
        super().__init__()

        # Настройка интерфейса
        self.show_error()

    def show_error(self):

        # Создаем всплывающее окно с ошибкой
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)  # Иконка ошибки
        error_box.setWindowTitle('Ошибка')  # Заголовок окна
        error_box.setText('Произошла ошибка!')  # Основной текст
        error_box.button = QPushButton('ok', self)
        self.button.clicked.connect(self.go_back)  # Кнопка "ОК"

        error_box.exec_()

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def go_back(self):
        self.hide()
        self.parent.show()
        # Показываем окно
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())