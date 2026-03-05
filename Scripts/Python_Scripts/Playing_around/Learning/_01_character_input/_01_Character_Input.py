#Practice Python Exercise 1
#by Omegazyph 
#Started on 10/28/2018

#Create a program that asks the user to enter thier name and their age.  
#Print out a message addressed to them that tells them the year that they well turn 100 years old.


#askes for the name of the user
name = input("Give me your name: ")


#or more compact the code
age = int(input("Give me your age: "))
#age = input("Give me your Age: ")

#ask the user for the year
year = int(input("What is the year: ")) #did not have to put this in for the exercise


endyear = str((year - age) + 100)


#print out the name and the age
print(name + " will be 100 years in the year " + endyear )


