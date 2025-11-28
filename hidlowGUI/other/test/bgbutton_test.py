from tkinter import *
from PIL import Image, ImageTk

root = Tk()

# Загружаем изображение
img = Image.open("bg3.jpg")

# При желании можно изменить размер
img = img.resize((150, 50))  # ширина x высота

# Преобразуем в формат, понятный tkinter
button_img = ImageTk.PhotoImage(img)

# Создаём кнопку с этой картинкой
btn = Button(root, text="click", fg="red", compound="center", image=button_img, borderwidth=0, highlightthickness=0)
btn.pack(pady=20)

root.mainloop()