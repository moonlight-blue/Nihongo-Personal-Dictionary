import sqlite3
import tkinter as tk
import customtkinter as ctk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders




ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

root = ctk.CTk()
root.title("Nihongo Personal Dictionary")
root.geometry("650x300") #(x,y)
root.wm_iconphoto(False,tk.PhotoImage(file="images/window_icon.png"))
font_data = ("Raleway",9)
status_label = ctk.CTkLabel(master=root, text="[STATUS]", text_font=font_data)
status_label.place(relx=0.5,y=20,anchor=tk.CENTER)

file_name="Nihongo_Personal_Dictionary"
status=""
clr_red="#ba0502"
clr_green="#02a12c"
sort_by_var=1 # 1=by English, 0=by Romaji

def sort_by_english_func():
    sort_by_var=1

def sort_by_romaji_func():
    sort_by_var=0

def display_status(status,color):
    if color=="g":
        text_clr=clr_green
    elif color=="r":
        text_clr=clr_red
    status_label.configure(text=status,text_color=text_clr)


try:
    sqliteConnection = sqlite3.connect('nihongo.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS words(english VARCHAR(20), romaji VARCHAR(50));")
    status="Connected to the database"
    display_status(status,"g")
except:
    status="Could not connect to the database"
    display_status(status,"r")


def sendEmail(): 
    try:
        write_file()
        fromaddr = "nihongopersonaldictionary@gmail.com"
        toaddr = "paramjangale@gmail.com"
        
        # instance of MIMEMultipart
        msg = MIMEMultipart()
        
        # storing the senders email address  
        msg['From'] = fromaddr
        
        # storing the receivers email address 
        msg['To'] = toaddr
        
        # storing the subject 
        msg['Subject'] = "Nihongo Personal Dictionary"
        
        
        # open the file to be sent 
        filename = "Japanese_Personal_Dictionary.txt"
        attachment = open("Japanese_Personal_Dictionary.txt", "rb")
        
        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')
        
        # To change the payload into encoded form
        p.set_payload((attachment).read())
        
        # encode into base64
        encoders.encode_base64(p)
        
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        
        # attach the instance 'p' to instance 'msg'
        msg.attach(p)
        
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        
        # start TLS for security
        s.starttls()
        
        # Authentication
        sending_status=s.login(fromaddr, "sxsvbulvkjeakjbo")
        
        # Converts the Multipart msg into a string
        text = msg.as_string()
        
        # sending the mail
        s.sendmail(fromaddr, toaddr, text)
        
        # terminating the session
        s.quit()
        if sending_status[0]==235:
            status="Sent successfully"
            display_status(status,"g")            
        else:
            status="Couldn't send Email"
            display_status(status,"r")

    except:
        status="Something went wrong"
        display_status(status,"r")


def addToDB():
    try:
        english_val=english_var.get()
        romaji_val=romaji_var.get()
        cursor.execute("Insert into words (english,romaji) values (?,?);",(english_val,romaji_val))
        sqliteConnection.commit()
        status="Word added successfully"
        display_status(status,"g")
        english_text.delete(0,"end")
        romaji_text.delete(0,"end")
        english_text.focus_set()
    except:
        status="Something went wrong"
        display_status(status,"r")

    

def clearDB():
    def clearDB_yes():
        cursor.execute("DELETE from words;")
        sqliteConnection.commit()
        confirm_window.destroy()
        status="Dictionary cleared successfully"
        display_status(status,"g")

    def clearDB_no():
        confirm_window.destroy()   

    confirm_window=ctk.CTkToplevel(root)
    confirm_window.geometry("300x120")
    confirm_window.title("Clear Dictionary?")
    confirm_window.wm_iconphoto(False,tk.PhotoImage(file="images/window_icon.png"))
    label=ctk.CTkLabel(master=confirm_window,text="Do you want to clear the dictionary?", text_font=font_data)
    label.place(relx=0.5,y=40,anchor=tk.CENTER)
    yes_btn = ctk.CTkButton( master=confirm_window,
                            text="Yes", 
                            compound=ctk.RIGHT,
                            command=clearDB_yes,
                            fg_color=clr_green,
                            height=30,
                            width=40)
    yes_btn.place(relx=0.4,y=80,anchor=tk.CENTER)
    no_btn = ctk.CTkButton( master=confirm_window,
                            text="No", 
                            compound=ctk.RIGHT,
                            command=clearDB_no,
                            fg_color=clr_red,
                            height=30,
                            width=40)
    no_btn.place(relx=0.6,y=80,anchor=tk.CENTER)

    

def write_file():
    try:
        with open (file_name+".txt",'w') as f:
            sort_by_val=sort_by.get()
            if sort_by_val:
                cursor.execute("SELECT * FROM words ORDER BY english;")
            else:
                cursor.execute("SELECT * FROM words ORDER BY romaji;")

            rows=cursor.fetchall()
            for row in rows:
                f.write(row[0].ljust(25)+"- "+row[1]+"\n")
        status="Added to file successfully"
        display_status(status,"g")
    except:
        status="Something went wrong"
        display_status(status,"r")
    
text_frame=ctk.CTkFrame(root,bg_color="#ba0502")        

romaji_label=ctk.CTkLabel(master=root,text="Romaji -", text_font=font_data)
romaji_label.place(relx=0.35,y=74,anchor=tk.CENTER)

english_label=ctk.CTkLabel(master=root,text="English -", text_font=font_data)
english_label.place(relx=0.35,y=47,anchor=tk.CENTER)

enter_btn = ctk.CTkButton( master=root,
                            text="Enter", 
                            compound=ctk.RIGHT,
                            command=addToDB,
                            height=30,
                            width=95 )
enter_btn.place(relx=0.5,y=130,anchor=tk.CENTER)

send_email_btn = ctk.CTkButton( master=root,
                            text="Send Email", 
                            compound=ctk.RIGHT,
                            command=sendEmail,
                            height=30,
                            width=120 )
send_email_btn.place(relx=0.5,y=170,anchor=tk.CENTER)

root.bind('<Return>', lambda e: addToDB())

clear_db_btn = ctk.CTkButton( master=root,
                            text="Clear Dictionary", 
                            compound=ctk.RIGHT,
                            command=clearDB,
                            height=30,
                            width=120 )
clear_db_btn.place(relx=0.7,y=130,anchor=tk.CENTER)

write_file_btn = ctk.CTkButton(master=root,
                            text="Add to File", 
                            compound=ctk.RIGHT,
                            command=write_file,
                            height=30,
                            width=120 )
write_file_btn.place(relx=0.3,y=130,anchor=tk.CENTER)

english_var=tk.StringVar()
english_text = tk.Entry(root, textvariable=english_var, width = 20)
english_text.place(relx=0.5,y=70,anchor=tk.CENTER)

romaji_var=tk.StringVar()
romaji_text = tk.Entry(root, textvariable=romaji_var, width = 20)
romaji_text.place(relx=0.5,y=110, anchor=tk.CENTER)

sort_by = tk.IntVar()
sort_by_english = ctk.CTkRadioButton(root, text='Sort by English words',variable=sort_by, value=1)
sort_by_romaji = ctk.CTkRadioButton(root, text='Sort by Romaji words', variable=sort_by, value=0)
sort_by_english.place(relx=0.15,y=200,anchor=tk.CENTER)
sort_by_romaji.place(relx=0.15,y=230,anchor=tk.CENTER)

root.mainloop()