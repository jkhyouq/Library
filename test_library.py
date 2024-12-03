import unittest
from library import Library, Book

class TestLibrary(unittest.TestCase):
    def setUp(self):
        """
        Создает тестовую либу перед каждым тестом.
        """
        self.library = Library("test_library.json")
        self.library.books = []  # Очистка данных для тестирования

    def test_add_book(self):
        """
        Тестирует добавление книги.
        """
        self.library.add_book("Процесс", "Ф.Кафка", 1925)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Процесс")

    def test_delete_book(self):
        """
        Тестирует удаление книги.
        """
        self.library.add_book("Процесс", "Ф.Кафка", 1925)
        book_id = self.library.books[0].id
        self.library.delete_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_search_books(self):
        """
        Тестирует поиск книг.
        """
        self.library.add_book("Процесс", "Ф.Кафка", 1925)
        self.library.add_book("Лолита", "В.Набоков", 1955)
        results = self.library.search_books(title="Процесс")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Процесс")

    def test_update_status(self):
        """
        Тестирует обновление статуса книги.
        """
        self.library.add_book("Процесс", "Ф.Кафка", 1925)
        book_id = self.library.books[0].id
        self.library.update_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

    def tearDown(self):
        """
        Удаляет тест файл после того как тест закончен.
        """
        import os
        if os.path.exists("test_library.json"):
            os.remove("test_library.json")


if __name__ == "__main__":
    unittest.main()
