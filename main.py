import unittest
from unittest.mock import MagicMock
from parameterized import parameterized


# Завдання 1: Тестування виконання арифметичних операцій
class MathTool:
    @staticmethod
    def add(a, b):
        print(f"Додавання: {a} + {b} = {a + b}")
        return a + b

    @staticmethod
    def subtract(a, b):
        print(f"Віднімання: {a} - {b} = {a - b}")
        return a - b

    @staticmethod
    def multiply(a, b):
        print(f"Множення: {a} * {b} = {a * b}")
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            print("Помилка: ділення на нуль!")
            raise ValueError("Cannot divide by zero")
        print(f"Ділення: {a} / {b} = {a / b}")
        return a / b


# Тести для MathTool
class TestMathTool(unittest.TestCase):

    def test_add(self):
        print("Тестування додавання:")
        self.assertEqual(MathTool.add(3, 2), 5)

    def test_subtract(self):
        print("Тестування віднімання:")
        self.assertEqual(MathTool.subtract(3, 2), 1)

    def test_multiply(self):
        print("Тестування множення:")
        self.assertEqual(MathTool.multiply(3, 2), 6)

    def test_divide(self):
        print("Тестування ділення:")
        self.assertEqual(MathTool.divide(6, 2), 3)

    def test_divide_by_zero(self):
        print("Тестування ділення на нуль:")
        with self.assertRaises(ValueError):
            MathTool.divide(3, 0)


# Завдання 2: Тестування класу LibraryItem
class LibraryItem:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        print(f"Створено бібліотечний елемент: {self.title}, {self.author}, {self.year}")

    def details(self):
        details = f"Title: {self.title}, Author: {self.author}, Year: {self.year}"
        print(f"Виведення деталей: {details}")
        return details


# Тести для LibraryItem
class TestLibraryItem(unittest.TestCase):

    def test_details(self):
        print("Тестування деталей бібліотечного елементу:")
        book = LibraryItem("1984", "George Orwell", 1949)
        self.assertEqual(book.details(), "Title: 1984, Author: George Orwell, Year: 1949")

        book2 = LibraryItem("To Kill a Mockingbird", "Harper Lee", 1960)
        self.assertEqual(book2.details(), "Title: To Kill a Mockingbird, Author: Harper Lee, Year: 1960")


# Завдання 3: Тестування взаємодії класів з використанням mock
class NotificationService:
    def send(self, message, user):
        print(f"NotificationService: відправка повідомлення '{message}' користувачу {user}")


class UserManager:
    def __init__(self, notification_service):
        self.notification_service = notification_service
        print("UserManager: створено користувача менеджер сповіщень")

    def notify_user(self, user, message):
        print(f"UserManager: сповіщення користувача {user} з повідомленням '{message}'")
        self.notification_service.send(message, user)


# Тести для UserManager та NotificationService з mock
class TestUserManager(unittest.TestCase):

    def test_notify_user(self):
        print("Тестування UserManager notify_user:")
        mock_service = MagicMock()
        user_manager = UserManager(mock_service)

        user_manager.notify_user("user1", "Hello!")

        # Перевіряємо, що метод send був викликаний з правильними параметрами
        mock_service.send.assert_called_with("Hello!", "user1")


# Завдання 4: Параметризовані тести для парності числа
def check_even(number):
    print(f"Перевірка на парність числа: {number}")
    return number % 2 == 0


# Тести для check_even
class TestCheckEven(unittest.TestCase):

    @parameterized.expand([
        (2, True),  # Позитивне парне число
        (-2, True),  # Від'ємне парне число
        (0, True),  # Нуль
        (1, False),  # Непарне число
        (-1, False),  # Від'ємне непарне число
    ])
    def test_check_even(self, number, expected_result):
        print(f"Тест на парність числа {number}: очікуваний результат {expected_result}")
        self.assertEqual(check_even(number), expected_result)


# Головна функція для запуску всіх тестів
if __name__ == "__main__":
    unittest.main()
