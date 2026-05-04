import json
import os
from tkinter import *
from tkinter import ttk, messagebox

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker - Трекер прочитанных книг")
        self.root.geometry("900x600")
        
        # Файл для保存 данных
        self.data_file = "books.json"
        self.books = []
        
        # Создание интерфейса
        self.create_input_frame()
        self.create_filter_frame()
        self.create_table()
        self.create_button_frame()
        
        # Загрузка данных при запуске
        self.load_data()
        
    def create_input_frame(self):
        """Фрейм для ввода данных книги"""
        input_frame = LabelFrame(self.root, text="Добавление новой книги", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Название книги
        Label(input_frame, text="Название книги:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Автор
        Label(input_frame, text="Автор:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.author_entry = Entry(input_frame, width=30)
        self.author_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Жанр
        Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.genre_entry = Entry(input_frame, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Количество страниц
        Label(input_frame, text="Количество страниц:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.pages_entry = Entry(input_frame, width=30)
        self.pages_entry.grid(row=1, column=3, padx=5, pady=5)
        
    def create_filter_frame(self):
        """Фрейм для фильтрации"""
        filter_frame = LabelFrame(self.root, text="Фильтрация книг", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Фильтр по жанру
        Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky="w", padx=5)
        self.genre_filter_var = StringVar()
        self.genre_filter_var.set("Все")
        self.genre_filter_combo = ttk.Combobox(filter_frame, textvariable=self.genre_filter_var, width=27)
        self.genre_filter_combo.grid(row=0, column=1, padx=5)
        self.genre_filter_combo.bind("<<ComboboxSelected>>", self.apply_filters)
        
        # Фильтр по страницам
        Label(filter_frame, text="Страниц больше:").grid(row=0, column=2, sticky="w", padx=5)
        self.pages_filter_var = StringVar()
        self.pages_filter_var.set("0")
        self.pages_filter_entry = Entry(filter_frame, textvariable=self.pages_filter_var, width=10)
        self.pages_filter_entry.grid(row=0, column=3, padx=5)
        
        Button(filter_frame, text="Применить фильтр", command=self.apply_filters).grid(row=0, column=4, padx=10)
        Button(filter_frame, text="Сбросить фильтр", command=self.reset_filters).grid(row=0, column=5, padx=5)
        
    def create_table(self):
        """Таблица для отображения книг"""
        # Фрейм для таблицы с прокруткой
        table_frame = Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Создание таблицы
        columns = ("Название", "Автор", "Жанр", "Страницы")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Настройка колонок
        self.tree.heading("Название", text="Название книги")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Страницы", text="Страницы")
        
        self.tree.column("Название", width=250)
        self.tree.column("Автор", width=200)
        self.tree.column("Жанр", width=200)
        self.tree.column("Страницы", width=100)
        
        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_button_frame(self):
        """Фрейм с кнопками действий"""
        button_frame = Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        Button(button_frame, text="Добавить книгу", command=self.add_book, bg="#4CAF50", fg="white", 
               font=("Arial", 10, "bold"), padx=20, pady=5).pack(side="left", padx=5)
        
        Button(button_frame, text="Удалить выбранную книгу", command=self.delete_book, bg="#f44336", fg="white",
               font=("Arial", 10), padx=20, pady=5).pack(side="left", padx=5)
        
        Button(button_frame, text="Сохранить в JSON", command=self.save_data, bg="#2196F3", fg="white",
               font=("Arial", 10), padx=20, pady=5).pack(side="left", padx=5)
        
        Button(button_frame, text="Загрузить из JSON", command=self.load_data, bg="#FF9800", fg="white",
               font=("Arial", 10), padx=20, pady=5).pack(side="left", padx=5)
        
    def validate_input(self):
        """Проверка корректности ввода"""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()
        
        if not title:
            messagebox.showerror("Ошибка", "Название книги не может быть пустым!")
            return False
        if not author:
            messagebox.showerror("Ошибка", "Автор не может быть пустым!")
            return False
        if not genre:
            messagebox.showerror("Ошибка", "Жанр не может быть пустым!")
            return False
        if not pages:
            messagebox.showerror("Ошибка", "Количество страниц не может быть пустым!")
            return False
        
        try:
            pages_num = int(pages)
            if pages_num <= 0:
                messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return False
        
        return True
    
    def add_book(self):
        """Добавление книги в список"""
        if not self.validate_input():
            return
        
        book = {
            "title": self.title_entry.get().strip(),
            "author": self.author_entry.get().strip(),
            "genre": self.genre_entry.get().strip(),
            "pages": int(self.pages_entry.get().strip())
        }
        
        self.books.append(book)
        self.update_genre_filter()
        self.apply_filters()
        
        # Очистка полей
        self.title_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.genre_entry.delete(0, END)
        self.pages_entry.delete(0, END)
        
        messagebox.showinfo("Успех", f"Книга '{book['title']}' успешно добавлена!")
        
    def delete_book(self):
        """Удаление выбранной книги"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу для удаления!")
            return
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту книгу?"):
            # Получаем название книги из выделенной строки
            item = self.tree.item(selected[0])
            title_to_delete = item['values'][0]
            
            # Удаляем из списка
            self.books = [book for book in self.books if book['title'] != title_to_delete]
            
            # Обновляем отображение
            self.update_genre_filter()
            self.apply_filters()
            messagebox.showinfo("Успех", "Книга удалена!")
    
    def update_genre_filter(self):
        """Обновление списка жанров в фильтре"""
        genres = sorted(set(book['genre'] for book in self.books))
        genres.insert(0, "Все")
        self.genre_filter_combo['values'] = genres
        
        # Если текущий выбранный жанр не в списке, сбрасываем на "Все"
        if self.genre_filter_var.get() not in genres:
            self.genre_filter_var.set("Все")
    
    def apply_filters(self):
        """Применение фильтров и обновление таблицы"""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получаем параметры фильтрации
        selected_genre = self.genre_filter_var.get()
        try:
            pages_min = int(self.pages_filter_var.get())
        except ValueError:
            pages_min = 0
            self.pages_filter_var.set("0")
        
        # Фильтрация книг
        filtered_books = self.books
        if selected_genre != "Все":
            filtered_books = [book for book in filtered_books if book['genre'] == selected_genre]
        
        if pages_min > 0:
            filtered_books = [book for book in filtered_books if book['pages'] > pages_min]
        
        # Отображение книг в таблице
        for book in filtered_books:
            self.tree.insert("", END, values=(book['title'], book['author'], book['genre'], book['pages']))
    
    def reset_filters(self):
        """Сброс фильтров"""
        self.genre_filter_var.set("Все")
        self.pages_filter_var.set("0")
        self.apply_filters()
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", f"Данные успешно сохранены в файл {self.data_file}!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")
    
    def load_data(self):
        """Загрузка данных из JSON файла"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.books = json.load(f)
            self.update_genre_filter()
            self.apply_filters()
            messagebox.showinfo("Успех", f"Данные загружены из файла {self.data_file}!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = BookTracker(root)
    root.mainloop()
