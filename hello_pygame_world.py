print("Hello World") # Intro
print("Welcome to Pygame World")
import random as rnd # Says that we will be doing things with the variable "random".
for i in range(rnd.randint(1,10)): # Picks a number and repeats the "Question, Answer" part of the code.
     question = input("Ask magic 8 ball a question Important!! **Only 10 allowed**: ")
     if "?" not in question: # Makes sure there is a question mark in the question.
          print("That is not a question!!\nGO AWAY!!")     
     else:
          answer = rnd.randint(21, 21) # Picks a number 1 through 22 for the answers.
          if answer == 1:
              print("It is certain") 
          elif answer == 2:
              print("Outlook good")
          elif answer == 3:
              print("You may rely on it")
          elif answer == 4:
              print("Ask again later")
          elif answer == 5:
              print("Concentrate and ask again")
          elif answer == 6:
              print("Beause why not?")
          elif answer == 7:
              print("My reply is NO!!")
          elif answer == 8:
              print("My sources say NO!!")
          elif answer == 9:
              print("I am too lazy to answer you")
          elif answer == 10:
              print("I am too lazy to answer you")
          elif answer == 11:
              print("There is no way to explain")
          elif answer == 12:
              print("Elephants don't like big brains") 
          elif answer == 13:
              print("I don't care.\nJust go away!!")
          elif answer == 14:
              print("Baby...\nCan't do it your self?")
          elif answer == 15:
              print("A dog could answer that")
          elif answer == 16:
              print("These brainless people")
          elif answer == 17:
              print("DAD!\nTHEY'RE ANNOYING ME ")
          elif answer == 18:
              print("yES")
          elif answer == 19:
              print("I'M AT SCHOOL!")
          elif answer == 20:
              print("Beeeee")
          elif answer == 21:
              print("I'm ea...\nting...\nmy...\ncookie")
          elif answer == 22:
              print("Hey!\n I wonder why I am getting spam calls!?")
print("The end") # Finalizes the game.
