import tkinter as tk
from create_form import CreateForm

root = tk.Tk()
root.title("Створення Скріншотів")

create_form = CreateForm(root)
create_form.pack()

root.mainloop()
