import re
import tkinter as tk

root = tk.Tk()
root.title("Калькулятор")
root.resizable(False, False)

expression = ""
display = tk.StringVar(value="0")

entry = tk.Entry(root, textvariable=display, font=("Arial", 24), justify="right",
                 state="readonly", readonlybackground="white", width=14, bd=8)
entry.grid(row=0, column=0, columnspan=4, padx=6, pady=6)


def press(value):
    global expression
    expression += value
    display.set(expression)


def clear():
    global expression
    expression = ""
    display.set("0")


def backspace():
    global expression
    expression = expression[:-1]
    display.set(expression or "0")


def calculate():
    global expression
    # разрешены только цифры и знаки + - * / . ( )
    if not expression or not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        return
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        expression = str(result)
        display.set(expression)
    except ZeroDivisionError:
        expression = ""
        display.set("Деление на 0")
    except Exception:
        expression = ""
        display.set("Ошибка")


buttons = [
    ("C", clear), ("⌫", backspace), ("(", lambda: press("(")), (")", lambda: press(")")),
    ("7", lambda: press("7")), ("8", lambda: press("8")), ("9", lambda: press("9")), ("/", lambda: press("/")),
    ("4", lambda: press("4")), ("5", lambda: press("5")), ("6", lambda: press("6")), ("*", lambda: press("*")),
    ("1", lambda: press("1")), ("2", lambda: press("2")), ("3", lambda: press("3")), ("-", lambda: press("-")),
    ("0", lambda: press("0")), (".", lambda: press(".")), ("=", calculate), ("+", lambda: press("+")),
]

for i, (text, command) in enumerate(buttons):
    tk.Button(root, text=text, font=("Arial", 18), width=4, height=2,
              command=command).grid(row=1 + i // 4, column=i % 4, padx=3, pady=3)

# управление с клавиатуры
root.bind("<Return>", lambda e: calculate())
root.bind("<BackSpace>", lambda e: backspace())
root.bind("<Escape>", lambda e: clear())
root.bind("<Key>", lambda e: press(e.char) if e.char and e.char in "0123456789+-*/.()" else None)

root.mainloop()