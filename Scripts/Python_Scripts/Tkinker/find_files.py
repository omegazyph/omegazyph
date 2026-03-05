# This is to find the path of the file on your computer 

from tkinter import filedialog as fb

path : str = fb.askopenfilename()
print(path)