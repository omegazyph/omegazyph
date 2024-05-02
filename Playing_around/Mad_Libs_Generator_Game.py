from tkinter import *

Screen = Tk()
Screen.title("Mad Libs Generator")
Screen.geometry('400x400')
Screen.config(bg="Black")


#creating buttons
Story1Button = Button(Screen, 
                      text='A memorable day', 
                      font=("Times New Roman", 13),
                      command=lambda: Story1(Screen),
                      bg='lightblue')
Story1Button.place(x=140, y=90)

Story2Button = Button(Screen, 
                      text='Ambitions', 
                      font=("Times New Roman", 13),
                      command=lambda: Story2(Screen), 
                      bg='lightblue')
Story2Button.place(x=165, y=150)
 
Screen.update()
Screen.mainloop()