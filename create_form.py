from tkinter import messagebox
import tkinter as tk
from create_album import create_album

categories = ["Постільна білизна", "Ковдри", "Подушки", "Покривала"]

bedding_urls = {
    "Постільна білизна": {
        "Постільна білизна": "https://www.asorti.store/?path=33",
        "Бязь Голд": "https://www.asorti.store/?path=33_59",
        "В ліжечко": "https://www.asorti.store/?path=33_74",
        "Дитяча постільна білизна": "https://www.asorti.store/?path=33_62",
        "Страйп Сатин": "https://www.asorti.store/?path=33_72",
        "Батерфляй": "https://www.asorti.store/?path=33_63",
        "Байка": "https://www.asorti.store/?path=33_65",
        "Зимова тепла (плюш, велюр) постільна білизна": "https://www.asorti.store/?path=33_68"
    },
    "Ковдри": {
        "Ковдри": "https://www.asorti.store/?path=20",
        "Літні ковдри ОДА": "https://www.asorti.store/?path=20_84",
        "Ковдри ОДА мікрофібра холофайбер 500грм м2": "https://www.asorti.store/?path=20_61",
        "Ковдри Соти Екопух": "https://www.asorti.store/?path=20_69",
        "Ковдри Принт холофайбер 500грм м2": "https://www.asorti.store/?path=20_73",
        "Ковдра довгий ворс Травка холофайбер": "https://www.asorti.store/?path=20_66"
    },
    "Подушки": {
        "Подушки": "https://www.asorti.store/?path=18"
    },
    "Покривала": {
        "Покривала": "https://www.asorti.store/?path=25",
        "Вафельне покривало": "https://www.asorti.store/?path=25_70",
        "Велюрові покривала": "https://www.asorti.store/?path=25_80",
        "Дитячі пледики": "https://www.asorti.store/?path=25_75",
        "Плед - покривало Норка": "https://www.asorti.store/?path=25_77",
        "Плед-Покривало Шарпей Клітинки": "https://www.asorti.store/?path=25_64",
        "Покривала Кролик": "https://www.asorti.store/?path=25_76",
        "Стібана Клітинка": "https://www.asorti.store/?path=25_78",
        "Шарпей": "https://www.asorti.store/?path=25_67",
        "Шарпей Полуторка": "https://www.asorti.store/?path=25_82"
    }
}

first_category = {
    "Постільна білизна",
    "Бязь Голд",
    "Дитяча постільна білизна",
    "Страйп Сатин",
    "Батерфляй",
    "Байка",
    "Зимова тепла (плюш, велюр) постільна білизна",
    "Ковдри",
    "Літні ковдри ОДА",
    "Ковдри ОДА мікрофібра холофайбер 500грм м2",
    "Ковдри Соти Екопух",
    "Ковдри Принт холофайбер 500грм м2",
    "Ковдра довгий ворс Травка холофайбер",
    "Покривала",
    "Вафельне покривало",
    "Велюрові покривала",
    "Плед - покривало Норка",
    "Плед-Покривало Шарпей Клітинки",
    "Покривала Кролик",
    "Стібана Клітинка",
    "Шарпей",
    "Шарпей Полуторка"
}

podyshky = "Подушки"

v_lizhechko = "В ліжечко"

dityachi_plediki = "Дитячі пледики"


class CreateForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_album_button = None
        self.item_menu = None
        self.item_var = None
        self.category_menu = None
        self.category_var = None
        self.checkboxes = []
        self.checkboxes_vars = []
        self.create_widgets()

    def create_widgets(self):
        self.category_var = tk.StringVar(self)
        self.category_var.set(categories[0])  # Set the default category
        self.category_menu = tk.OptionMenu(self, self.category_var, *categories)
        self.category_menu.pack(pady=20, padx=20)
        self.category_var.trace('w', self.on_category_change)

        items = list(bedding_urls[categories[0]].keys())
        self.item_var = tk.StringVar(self)
        self.item_var.set(items[1])
        self.item_menu = tk.OptionMenu(self, self.item_var, *items)
        self.item_menu.pack(pady=20, padx=20)
        self.item_var.trace('w', self.create_checkboxes)

        self.create_checkboxes()

        self.create_album_button = tk.Button(self, text="Зробити Скріншоти", command=self.create)
        self.create_album_button.pack(pady=20, padx=20, side=tk.BOTTOM)

    def create_checkboxes(self, *args):
        for checkbox in self.checkboxes:
            checkbox.destroy()

        self.checkboxes = []
        self.checkboxes_vars = []

        selected_category = self.item_var.get()
        if selected_category in first_category:
            checkbox_names = [
                "Півтораспальний", "Двохспальний", "Євро", "Сімейний", "Прост. 220х250"
            ]
        elif selected_category == podyshky:
            checkbox_names = [
                "50/70", "70/70"
            ]
        else:
            checkbox_names = []

        for name in checkbox_names:
            checkbox_var = tk.BooleanVar(self)
            checkbox_var.set(True)
            self.checkboxes_vars.append(checkbox_var)
            checkbox = tk.Checkbutton(self, text=name, variable=checkbox_var)
            checkbox.pack()
            self.checkboxes.append(checkbox)

    def create(self):
        selected_category = self.category_var.get()
        selected_item = self.item_var.get()
        selected_checkboxes = [checkbox.cget('text') for checkbox in self.checkboxes if self.checkboxes_vars[self.checkboxes.index(checkbox)].get()]

        if selected_category in bedding_urls and selected_item in bedding_urls[selected_category]:
            url = bedding_urls[selected_category][selected_item]
            create_album(url, selected_item, selected_checkboxes)
            messagebox.showinfo("Створення Скріншотів", "Скріншоти успішно створені!")
        else:
            messagebox.showerror("Помилка", "Виберіть категорію та елемент")

    def on_category_change(self, *args):

        selected_category = self.category_var.get()
        items = list(bedding_urls[selected_category].keys())
        self.item_var.set(items[0])
        self.item_menu['menu'].delete(0, 'end')
        for item in items:
            self.item_menu['menu'].add_command(label=item, command=tk._setit(self.item_var, item))
