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
 

#region Story1
def Story1(win):
  def final(tl: Toplevel, name, sports, City, playername, drinkname, snacks):
 
    text = f'''
       One day me and my friend {name} decided to play a {sports} game in {City}.
       We wanted to watch {playername}.
       We drank {drinkname} and also ate some {snacks} 
       We really enjoyed! We are looking forward to go again and enjoy '''
 
    tl.geometry(newGeometry='500x550')
 
    Label(tl, text='Story:',  wraplength=tl.winfo_width()).place(x=160, y=310)
    Label(tl, text=text,wraplength=tl.winfo_width()).place(x=0, y=330)
 
  NewScreen = Toplevel(win, bg='yellow')
  NewScreen.title("A memorable day")
  NewScreen.geometry('500x500')
  Label(NewScreen, text='Memorable Day').place(x=100, y=0)
  Label(NewScreen, text='Name:').place(x=0, y=35)
  Label(NewScreen, text='Enter a game:').place(x=0, y=70)
  Label(NewScreen, text='Enter a city:').place(x=0, y=110)
  Label(NewScreen, text='Enter the name of a player:').place(x=0, y=150)
  Label(NewScreen, text='Enter the name of a drink:').place(x=0, y=190)
  Label(NewScreen, text='Enter the name of a snack:').place(x=0, y=230)
  Name = Entry(NewScreen, width=17)
  Name.place(x=250, y=35)
  game = Entry(NewScreen, width=17)
  game.place(x=250, y=70)
  city = Entry(NewScreen, width=17)
  city.place(x=250, y=105)
  player = Entry(NewScreen, width=17)
  player.place(x=250, y=150)
  drink = Entry(NewScreen, width=17)
  drink.place(x=250, y=190)
  snack = Entry(NewScreen, width=17)
  snack.place(x=250, y=220)
  SubmitButton = Button(NewScreen, text="Submit", background="Blue", font=('Times', 12), command=lambda:final(NewScreen, Name.get(), game.get(), city.get(), player.get(), drink.get(), snack.get()))
  SubmitButton.place(x=150, y=270)
 
  NewScreen.mainloop()
#endregion






Screen.update()
Screen.mainloop()