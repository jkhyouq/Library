import json
from typing import List, Dict, Optional

# Файл для хранения данных библиотеки
LIBRARY_FILE = "library.json"


class Book:
    """Класс для представления книги."""
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict:
        """Преобразует объект книги в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Book':
        """Создает объект книги из словаря."""
        return Book(data["id"], data["title"], data["author"], data["year"], data["status"])


class Library:
    """Класс для управления библиотекой книг."""
    def __init__(self, filename: str):
        self.filename = filename
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Загружает данные из файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.books = [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def save_books(self):
        """Сохраняет данные в файл."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """Добавляет книгу в библиотеку."""
        new_id = max([book.id for book in self.books], default=0) + 1
        book = Book(new_id, title, author, year)
        self.books.append(book)
        self.save_books()

    def delete_book(self, book_id: int) -> bool:
        """Удаляет книгу по ID."""
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                return True
        return False

    def search_books(self, **kwargs) -> List[Book]:
        """Ищет книги по указанным полям."""
        results = self.books
        for key, value in kwargs.items():
            results = [book for book in results if getattr(book, key, "").lower() == str(value).lower()]
        return results

    def list_books(self) -> List[Book]:
        """Возвращает список всех книг."""
        return self.books

    def update_status(self, book_id: int, status: str) -> bool:
        """Обновляет статус книги."""
        for book in self.books:
            if book.id == book_id:
                book.status = status
                self.save_books()
                return True
        return False


def main():
    library = Library(LIBRARY_FILE)

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выход")
        choice = input("Введите номер действия: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            if year.isdigit():
                library.add_book(title, author, int(year))
                print("Книга успешно добавлена!")
            else:
                print("Некорректный год издания.")

        elif choice == "2":
            book_id = input("Введите ID книги для удаления: ")
            if book_id.isdigit() and library.delete_book(int(book_id)):
                print("Книга успешно удалена!")
            else:
                print("Книга с указанным ID не найдена.")

        elif choice == "3":
            field = input("Введите поле для поиска (title, author, year): ").lower()
            value = input("Введите значение для поиска: ")
            results = library.search_books(**{field: value})
            if results:
                print("Найдено книг:")
                for book in results:
                    print(book.to_dict())
            else:
                print("Книг по заданным параметрам не найдено.")

        elif choice == "4":
            books = library.list_books()
            if books:
                print("Список всех книг:")
                for book in books:
                    print(book.to_dict())
            else:
                print("Библиотека пуста.")

        elif choice == "5":
            book_id = input("Введите ID книги для изменения статуса: ")
            new_status = input("Введите новый статус (в наличии/выдана): ").strip()
            if book_id.isdigit() and new_status in ["в наличии", "выдана"]:
                if library.update_status(int(book_id), new_status):
                    print("Статус книги успешно обновлен!")
                else:
                    print("Книга с указанным ID не найдена.")
            else:
                print("Некорректный ввод.")

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
