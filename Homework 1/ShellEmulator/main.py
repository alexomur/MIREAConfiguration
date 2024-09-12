"""
I'll start with a preface that I really wanted to do the Homework in C# or something more interesting.
But then I read 2-4 assignments and realized that Python is my choice.
"""
import tkinter as tk

def load_window() -> tk.Tk:
    root = tk.Tk()
    root.title('ShellEmulator')
    root.geometry('1200x600')
    return root

def main() -> None:
    root = load_window()
    root.mainloop()

if __name__ == '__main__':
    main()
