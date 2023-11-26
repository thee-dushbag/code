import tkinter
from tkinter import ttk

window = tkinter.Tk()
window.title("Hello world app")
window.geometry("300x300")

_counter = 0

count_label = ttk.Label(
    window,
    text='Click the button.',
    font=("monospace", 15, 'bold')
)

def say_hello():
    global _counter
    _counter += 1
    print(f"{_counter}: Hello there!")
    count_label.config(text=f'You clicked {_counter} time(s)')

count_label.pack()

hello_button = ttk.Button(window, text="Say hello", command=say_hello)
hello_button.pack()

window.mainloop()
