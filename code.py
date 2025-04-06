import tkinter as tk
from tkinter import colorchooser
from tkinter import simpledialog

# --- Глобальные переменные ---
last_x, last_y = None, None  # Координаты последней точки
current_color = "black"      # Текущий цвет рисования
current_width = 2          # Текущая толщина линии

# --- Функции ---

def start_draw(event):
    """Вызывается при нажатии кнопки мыши. Запоминает начальные координаты."""
    global last_x, last_y
    last_x, last_y = event.x, event.y
    # Начинаем рисовать точку сразу при клике
    canvas.create_oval(event.x - current_width/2, event.y - current_width/2,
                       event.x + current_width/2, event.y + current_width/2,
                       fill=current_color, outline=current_color, width=0)


def draw(event):
    """Вызывается при движении мыши с зажатой кнопкой. Рисует линию."""
    global last_x, last_y
    if last_x is not None and last_y is not None:
        # Рисуем линию от последней точки до текущей
        canvas.create_line(last_x, last_y, event.x, event.y,
                           fill=current_color, width=current_width,
                           capstyle=tk.ROUND, smooth=tk.TRUE)
        # Обновляем последнюю точку
        last_x, last_y = event.x, event.y

def stop_draw(event):
    """Вызывается при отпускании кнопки мыши. Сбрасывает координаты."""
    global last_x, last_y
    last_x, last_y = None, None

def choose_color():
    """Открывает диалог выбора цвета и устанавливает выбранный цвет."""
    global current_color
    # askcolor возвращает кортеж ((R, G, B), '#rrggbb') или (None, None) если отмена
    color_code = colorchooser.askcolor(title="Выбери цвет для Humming Paint")
    if color_code[1]: # Если цвет выбран (не None)
        current_color = color_code[1]
        # Можно добавить визуальный индикатор текущего цвета
        color_button.config(bg=current_color, activebackground=current_color)
        # Сделаем текст кнопки видимым на темном фоне
        try:
            # Простая проверка яркости цвета
            r, g, b = root.winfo_rgb(current_color) # Возвращает значения 0-65535
            brightness = (r + g + b) / 3 / 65535
            if brightness < 0.5:
                color_button.config(fg='white', activeforeground='white')
            else:
                color_button.config(fg='black', activeforeground='black')
        except: # На случай, если не удастся определить цвет (редко)
             color_button.config(fg='black', activeforeground='black')


def set_width(size):
    """Устанавливает толщину линии."""
    global current_width
    current_width = size
    print(f"Толщина кисти установлена на: {current_width}") # Для отладки

def clear_canvas():
    """Очищает весь холст."""
    canvas.delete("all") # Удаляет все элементы с тегом "all" (т.е. все)

# --- Настройка GUI ---

# 1. Создание главного окна
root = tk.Tk()
root.title("Humming Paint v0.1")

# 2. Создание рамки для кнопок управления
controls_frame = tk.Frame(root, bd=2, relief=tk.RAISED)
controls_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

# 3. Кнопки управления
color_button = tk.Button(controls_frame, text="Цвет", width=10, command=choose_color, bg=current_color, fg='white', activebackground=current_color, activeforeground='white')
color_button.pack(side=tk.LEFT, padx=5, pady=2)

# Кнопки для толщины кисти
width_btn_frame = tk.Frame(controls_frame) # Вложенная рамка для кнопок толщины
width_btn_frame.pack(side=tk.LEFT, padx=5)

tk.Button(width_btn_frame, text="Тонко", width=6, command=lambda: set_width(2)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="Средне", width=6, command=lambda: set_width(5)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="Толсто", width=6, command=lambda: set_width(10)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="Своя", width=6, command=lambda: set_width(simpledialog.askinteger("Толщина кисти", "Введите толщину (пиксели):", parent=root, minvalue=1, maxvalue=50, initialvalue=current_width) or current_width)).pack(side=tk.LEFT) # Кнопка для своей толщины


clear_button = tk.Button(controls_frame, text="Очистить", width=10, command=clear_canvas)
clear_button.pack(side=tk.RIGHT, padx=5, pady=2) # Размещаем справа

# 4. Создание холста для рисования
canvas = tk.Canvas(root, bg="white", cursor="pencil") # Устанавливаем белый фон и курсор-карандаш
canvas.pack(fill=tk.BOTH, expand=True) # Растягиваем холст на все доступное пространство

# 5. Привязка событий мыши к функциям
canvas.bind("<Button-1>", start_draw)       # Нажатие левой кнопки мыши
canvas.bind("<B1-Motion>", draw)          # Движение мыши с зажатой левой кнопкой
canvas.bind("<ButtonRelease-1>", stop_draw) # Отпускание левой кнопки мыши

# --- Запуск главного цикла приложения ---
root.mainloop()