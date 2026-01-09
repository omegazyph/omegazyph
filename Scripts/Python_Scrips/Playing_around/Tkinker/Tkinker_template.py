import tkinter as tk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Application")
        self.geometry("400x300")  # Set the initial size of the window

        # Create widgets
        self.label = tk.Label(self, text="Hello, Tkinter!", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.button = tk.Button(self, text="Click Me!", command=self.on_button_click)
        self.button.pack()

    def on_button_click(self):
        self.label.config(text="Button clicked!")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
