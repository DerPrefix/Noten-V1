import datetime
import time
import tkinter as tk
from tkinter import *
from tkinter import Menubutton, simpledialog, messagebox, PhotoImage

from tkinter.ttk import Combobox, Progressbar
import mysql.connector
import requests
from ttkbootstrap import Style, Notebook
import json
import random
import string
import os
from ttkbootstrap.dialogs import Messagebox
import tkinter.scrolledtext as tb
import PySimpleGUI as sg
from tkinter import ttk
import sys
import subprocess
import ttkbootstrap as tb

import threading






with open("theme.txt", "r") as file:
    theme = file.read()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Notenprogramm")
        self.master.geometry("600x400")
        self.master.resizable(False, False)
        self.style = Style(theme=theme)  # Choose your preferred theme
        self.create_widgets()
        
        try:
            self.check_for_new_grades()
        except Exception as e:
            pass
            
        try:
            self.load_grades()
        except Exception as e:
            pass
        try:
            self.generate_lizenz()
        except Exception as e:
            pass
        try:
            self.load_notes_from_database()
        except Exception as e:
            pass
        

    def check_for_new_grades(self):
        # Lade die Lizenz aus der "lizenz.txt"-Datei

        try:
            with open("lizenz.txt", "r") as file:
                lizenz = file.read()

                db = mysql.connector.connect(
                    host="database.snbz.services",
                    user="Nicklas-Public",
                    password="E5$03tb@5k?vfZc#xsB",
                    database="App_Nicklas",
                    port="3306")
                    
                cursor = db.cursor()
                cursor.execute("SELECT * FROM Lizenzen")
                result = cursor.fetchall()


                
                # Daten aus der Datenbank herunterladen
                cursor.execute("SELECT Note FROM Lizenzen WHERE Lizenz = %s", (lizenz,))
                result = cursor.fetchone()
                grades = result[0]

                # Daten in die grades.json Datei schreiben
                with open("grades.json", "w") as file:
                    file.write(grades)

                
                

                with open("timestamp.txt", "w") as file:
                        
                    # reinschreiben wann die noten heruntergeladen wurden
                    timestamp = datetime.datetime.now().strftime("%d.%m %H:%M:%S")
                    file.write(timestamp)

                    sync = f"Zuletzt synchronisiert: {timestamp}"
                    self.sync_label.config(text=sync)

                # listbox aktualisieren
                
                self.update_subject_listbox()

        except FileNotFoundError:
            pass
            
    def load_grades(self):
        time.sleep(1)
        try:
            with open("grades.json", "r") as file:
                self.grades = json.load(file)

                # Update subject listbox
                self.update_subject_listbox()
        except FileNotFoundError:
            pass

    
    def generate_lizenz(self):

        if not os.path.isfile("lizenz.txt"):
            with open("lizenz.txt", "w") as file:
                pass

        with open("lizenz.txt", "r") as file:
            lizenz = file.read()

            if lizenz == "":

                num_letters = 10  # Anzahl der gewünschten Buchstaben
                random_letters = ''.join(random.choice(string.ascii_letters) for _ in range(num_letters))
                with open("lizenz.txt", "w") as file:

                    file.write(random_letters)

                db = mysql.connector.connect(
                    host="database.snbz.services",
                    user="Nicklas-Public",
                    password="E5$03tb@5k?vfZc#xsB",
                    database="App_Nicklas",
                    port="3306"
                )

                cursor = db.cursor()

                 
                with open("lizenz.txt", "r") as file:
                    lizenz = file.read()

                # get the pc username
                username = os.getlogin()


                # schreib es in die Datenbank
                cursor.execute("INSERT INTO Lizenzen (Lizenz, User, Note) VALUES (%s,%s,%s)", (lizenz, username, "{}"))
                db.commit()

            else:
                pass

        

    def create_widgets(self):
        notebook = Notebook(self.master)
        notebook.pack(expand=1, fill="both")

        tab0 = tk.Frame(notebook)
        tab1 = tk.Frame(notebook)

        tab2 = tk.Frame(notebook)
        tab3 = tk.Frame(notebook)

        tab4 = tk.Frame(notebook)  
        tab5 = tk.Frame(notebook)
        tab6 = tk.Frame(notebook)

        notebook.add(tab0, text="Home")
        notebook.add(tab1, text="Noten")
        notebook.add(tab2, text="Stundenplan")
        notebook.add(tab3, text="Notizen")
        notebook.add(tab5, text="Kalender")
        notebook.add(tab6, text="Tipps")
        
        notebook.add(tab4, text="Einstellungen")
        

        self.create_home(tab0)
        self.create_noten_tab(tab1)
        self.create_stundenplan_tab(tab2)
        self.create_notizen_tab(tab3)
        self.create_einstellungen_tab(tab4)
        self.create_kalender_tab(tab5)
        self.create_tipps_tab(tab6)
        
        

        

        # disable the tabs
        notebook.tab(2, state="disabled")



    def upload_edit_grades():
        try:
            with open("lizenz.txt", "r") as file:
                lizenz = file.read()

            with mysql.connector.connect(
                    host="database.snbz.services",
                    user="Nicklas-Public",
                    password="E5$03tb@5k?vfZc#xsB",
                    database="App_Nicklas",
                    port="3306") as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM Lizenzen")
                result = cursor.fetchall()

                with open("grades.json", "r") as file:
                    grades = file.read()

                # Daten in die Datenbank hochladen
                timestamp = datetime.datetime.now().strftime("%d.%m %H:%M:%S")

                try:
                    cursor.execute("INSERT INTO Lizenzen (Lizenz, Note) VALUES (%s, %s)", (lizenz, grades))
                    db.commit()
                    print("Die Noten wurden hochgeladen!")
                except mysql.connector.errors.IntegrityError as e:
                    cursor.execute("UPDATE Lizenzen SET Note = %s WHERE Lizenz = %s", (grades, lizenz))
                    db.commit()
                    print("Die Noten wurden aktualisiert!")

                with open("timestamp.txt", "w") as file:
                    file.write(timestamp)
        except Exception as e:
            print(f"An error occurred: {e}")


    def create_home(self, tab):
        # Your code for the "Home" ta

        self.home_label = tk.Label(tab, text="Willkommen!", font=("Arial", 15))
        self.home_label.pack()

        # Die Aktuelle Uhrzeit soll angezeigt werden und sich jede Sekunde aktualisieren
        self.clock_label = tk.Label(tab, font=("Arial", 15))
        self.clock_label.pack()

        def update_clock():
            self.clock_label.config(text=datetime.datetime.now().strftime("%H:%M:%S"))
            self.clock_label.after(1000, update_clock)

        update_clock()

        
        self.date_label = tk.Label(tab, font=("Arial", 15))
        self.date_label.pack()
        self.date_label.place(x=0, y=330)

        def update_date():
            self.date_label.config(text=datetime.datetime.now().strftime("%d.%m.%Y"))
            self.date_label.after(1000, update_date)

        update_date()#

        # update RPC 

        

        



        # Rest of the code for the "Home" tab

    def create_noten_tab(self, tab):
        self.subject_label = tk.Label(tab, text="Fach", font=("Arial", 15))
        self.subject_label.place(x=3, y=10)

        self.subject_entry = tk.Entry(tab, font=("Arial", 13))
        self.subject_entry.place(x=80, y=10)

        self.grade_label = tk.Label(tab, text="Note:", font=("Arial", 15))
        self.grade_label.place(x=3, y=50)

        self.grade_entry = tk.Entry(tab, font=("Arial", 13))
        self.grade_entry.place(x=80, y=50)

    
        self.save_button = tk.Button(tab, text="Note speichern", font=("Arial", 15),bg="green", command=self.save_grade)
        self.save_button.place(x=50, y=90)

        self.result_label = tk.Label(tab, text="", font=("Arial", 12))
        self.result_label.place(x=30, y=160)

        self.sync_label = tk.Label(tab, text="Keine Synchronisierung vorhanden", font=("Arial", 15))
        self.sync_label.place(x=210, y=310)

        self.subject_listbox = tk.Listbox(tab, font=("Arial", 13), selectmode=tk.SINGLE)
        self.subject_listbox.place(x=280, y=10, width=150, height=300, anchor="nw")

        self.subject_listbox.bind("<<ListboxSelect>>", self.select_subject)
        self.subject_listbox.bind("<Button-3>", self.handle_right_click)

    def calculate_average(self):
        subject = self.subject_entry.get()
        
        if subject in self.grades:
            subject_grades = self.grades[subject]

            if subject_grades:
                # Calculate the average grade for the subject
                average = sum(subject_grades) / len(subject_grades)

                # Display the result
                self.result_label.config(text=f"Aktueller Durchschnitt für {subject}:\n {average:.2f}")

                if average >= 5:
                    # pack den tipps button aus
                    msg = messagebox.showwarning("Schlechte Noten", "Du hast schlechte Noten!\n\nKlicke auf den Reiter 'Extras', um Tipps zu bekommen!")

                # Send webhook notification
                

            else:
                self.result_label.config(text=f"Keine Noten für {subject} vorhanden")

        else:
            self.result_label.config(text=f"Keine Noten vorhanden")


    def select_subject(self, event):
        if self.subject_listbox.curselection():
            grade = self.grades[self.subject_listbox.get(self.subject_listbox.curselection())][-1]
            selected_subject = self.subject_listbox.get(self.subject_listbox.curselection())
            self.subject_entry.delete(0, tk.END)
            self.subject_entry.insert(0, selected_subject)
            self.calculate_average()

    def remove_grade(self):
        # Das Fach was ausgewählt ist
        selected_subject = self.subject_listbox.get(self.subject_listbox.curselection())

        # Noten für das Fach abfragen
        subject_grades = self.grades[selected_subject]

        # Noten in einem String zusammenfügen
        grades_string = ", ".join([str(grade) for grade in subject_grades])

        # Noten anzeigen
        

        grade = simpledialog.askstring("Noten entfernen", f"Welche Note möchtest du entfernen?\n\nNoten: {grades_string}")

    

        if grade:
            try:
                # Note in ein float umwandeln
                grade = float(grade)

                # Note aus dem Fach entfernen
                self.grades[selected_subject].remove(grade)

                # Speichern der Änderungen
                self.save_grades()

                # Noten aktualisieren
                self.calculate_average()

                if not self.grades[selected_subject]:
                    self.delete_subject(selected_subject)

                # Listbox aktualisieren
                self.update_subject_listbox()
            except ValueError:
                mb = Messagebox.show_error(title="Fehler", message="Bitte gib eine vorhandene Zahl an!")

    def handle_right_click(self, event):
        # Prüfen, ob ein Element in der Listbox ausgewählt ist
        if self.subject_listbox.curselection():
            selected_subject = self.subject_listbox.get(self.subject_listbox.curselection())

            # Kontextmenü erstellen
            context_menu = tk.Menu(self, tearoff=0)
            context_menu.add_command(label="Noten anzeigen", command=lambda: self.show_grades())
            context_menu.add_separator()
            context_menu.add_command(label="Noten entfernen", command=lambda: self.remove_grade())
            context_menu.add_separator()
            context_menu.add_command(label="Fach bearbeiten", command=lambda: self.edit_subject(selected_subject))
            context_menu.add_separator()
            context_menu.add_command(label="Fach löschen", command=lambda: self.delete_subject(selected_subject))
            

            # Position des Kontextmenüs anzeigen
            context_menu.post(event.x_root, event.y_root)

    def edit_subject(self, subject):
        # bearbeitetes Fach abfragen
        new_subject = simpledialog.askstring("Fach bearbeiten", "Wie soll das Fach heißen?", initialvalue=subject)

        # Prüfen, ob ein Fach eingegeben wurde
        if new_subject:
            # Prüfen, ob das Fach bereits vorhanden ist
            if new_subject in self.grades:
                messagebox.showerror("Fach bereits vorhanden", f"Das Fach '{new_subject}' ist bereits vorhanden.")
            else:
                # Fach umbenennen
                self.grades[new_subject] = self.grades[subject]
                del self.grades[subject]
                self.update_subject_listbox()
                self.save_grades()#

                
                sync_status = f"Zuletzt synchronisiert: {datetime.datetime.now().strftime('%d.%m %H:%M:%S')}"
                self.sync_label.config(text=sync_status)
                self.upload_edit_grades()

    def show_grades(self):
        # Das Fach was ausgewählt ist
        selected_subject = self.subject_listbox.get(self.subject_listbox.curselection())

        # Noten für das Fach abfragen
        subject_grades = self.grades[selected_subject]

        # Noten in einem String zusammenfügen
        grades_string = ", ".join([str(grade) for grade in subject_grades])

        # Noten anzeigen
        messagebox.showinfo(f"{selected_subject}", grades_string)

        pass

    def delete_subject(self, subject):
        # Bestätigungsmeldung anzeigen
        if messagebox.askyesno("Fach löschen", f"Möchtest du das Fach '{subject}' wirklich löschen?"):
            # Fach aus dem Dictionary entfernen
            del self.grades[subject]
            # Listbox aktualisieren
            self.update_subject_listbox()
            self.subject_entry.delete(0, tk.END)
            # Speichern der Änderungen
            self.save_grades()

            self.upload_edit_grades()
            sync_status = f"Zuletzt synchronisiert: {datetime.datetime.now().strftime('%d.%m %H:%M:%S')}"
            self.sync_label.config(text=sync_status)
     
    def save_grades(self):
        with open("grades.json", "w") as file:
            json.dump(self.grades, file)

        db = mysql.connector.connect(
                host="database.snbz.services",
                user="Nicklas-Public",
                password="E5$03tb@5k?vfZc#xsB",
                database="App_Nicklas",
                port="3306"
            )
        

        cursor = db.cursor()

        with open("lizenz.txt", "r") as file:
            lizenz = file.read()

        
                
        

        # Er soll die grades.json so wie sie ist hochladen
        with open("grades.json", "r") as file:
            grades = file.read()

        
            # Daten in die Datenbank hochladen
        try:
            cursor.execute("INSERT INTO Lizenzen (Lizenz, Note) VALUES (%s, %s)", (lizenz, grades))
            
            db.commit()
        except mysql.connector.errors.IntegrityError as e:
            if e.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                cursor.execute("UPDATE Lizenzen SET Note = %s WHERE Lizenz = %s", (grades, lizenz))
                
                db.commit()
            else:
                raise e

    def update_subject_listbox(self):
        self.subject_listbox.delete(0, tk.END)
        self.subject_listbox.insert(tk.END, *self.grades.keys())

    def save_grade(self):

        with open("grades.json", "r") as file:
            self.grades = json.load(file)

        try:
            # Get the subject and grade from the entry fields
            subject = self.subject_entry.get()
            grade = float(self.grade_entry.get())

            # if grade is not between 1 and 6, raise ValueError
            if grade < 1 or grade > 6:
                raise ValueError

            # Save the grade to the dictionary
            if subject in self.grades:
                # Check if it's a list, if not, convert it to a list
                if not isinstance(self.grades[subject], list):
                    self.grades[subject] = [self.grades[subject]]
                self.grades[subject].append(grade)
            else:
                self.grades[subject] = [grade]

            # Clear the entry fields
            # self.subject_entry.delete(0, tk.END)
            self.grade_entry.delete(0, tk.END)

            # Save the updated grades to the JSON file
            self.save_grades()

            # Update subject listbox
            self.update_subject_listbox()
            # Emojis springen nach dem Speichern auf
            if grade == 1:
                self.result_label.config(text="Sehr gut, weiter so! 😃", fg="green")
            elif grade == 2:
                self.result_label.config(text="Gut, weiter so! 😊", fg="green")
            elif grade == 3:
                self.result_label.config(text="Nicht schlecht, weiter so! 🙂", fg="green")
            elif grade == 4:
                self.result_label.config(text="Naja, das geht besser! 😐", fg="orange")
            elif grade == 5:
                self.result_label.config(text="Schlecht, das muss besser werden! 😕", fg="orange")
            elif grade == 6:
                self.result_label.config(text="Sehr schlecht, das muss besser werden! 😞", fg="red")

        except ValueError:
            self.result_label.config(text="Bitte gib eine Zahl zwischen 1 und 6 ein!", fg="red")
                                
    
    def create_stundenplan_tab(self, tab):




        # mach den tab größer
        tab.config(width=800, height=800)

        menu = Menu(tab)
        

        filemenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Datei", menu=filemenu)
        #filemenu.add_command(label="Vertretungsplan", command=self.open_vertretungsplan)
        #filemenu.add_command(label="Notizen", command=self.text_editor)
        #filemenu.add_command(label="Stundenplan herunterladen", command=self.install_timetable)
        #filemenu.add_command(label="QR-Code", command=self.qr_code)
        #filemenu.add_command(label="Beenden", command=self.close_window)

        helpmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Hilfe", menu=helpmenu)
        #helpmenu.add_command(label="Über", command=self.dev_infos)

        minispiel = Menu(menu, tearoff=0)
        menu.add_cascade(label="Minispiel", menu=minispiel)
        #minispiel.add_command(label="Snake", command=self.snake)

       
        werbung = Menu(menu, tearoff=0)
        menu.add_cascade(label="Werbung", menu=werbung)
        #werbung.add_command(label="shutdown app", command=self.werbung)
        #werbung.add_command(label="YouTube Downloader", command=self.msg_for_yt)

        # accelerator = shortcut
        try:
            db = mysql.connector.connect(
                host="database.snbz.services",
                user="Nicklas-Public",
                password="E5$03tb@5k?vfZc#xsB",
                database="App_Nicklas",
                port="3306"
            )
            cursor = db.cursor()

            quarder = tk.PhotoImage(file='images/quarder1.png')
            Stundenplan = tk.Label(tab, image=quarder)
            Stundenplan.image = quarder
            Stundenplan.grid(row=0, column=0, padx=10, pady=10)  # Passende Spalte für das Bild
            # Rechts neben dem Bild
            label = tk.Label(tab, text="©Nicklas", fg="Black",bg="white", font=("Arial", 10, "bold")).place(x=500, y=75)
            
            

            days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]

            # Tagesnamen nebeneinander anzeigen
            for day_idx, day in enumerate(days):
                label = tk.Label(tab, text=day, fg="Black", font=("Arial", 12, "bold")).place(x=day_idx * 130 + 10, y=110)
                
            
            # unter den tagen ein strich
            label = tk.Label(tab, text="____________________________________________________________________________________________________________________", fg="Black", font=("Arial", 15, "bold")).place(x=0, y=130)
            
            # Montag
            cursor.execute("SELECT * FROM montag")
            result = cursor.fetchall()

            # Alle Fächer durchgehen
            def show_text1(event):
                text_label.config(text="7:30-8:15")
            
            def show_text2(event):
                text_label.config(text="8:15-9:00")

            def show_text3(event):
                text_label.config(text="9:20-10:05")

            def show_text4(event):
                text_label.config(text="10:15-11:00")

            def show_text5(event):
                text_label.config(text="11:10-11:55")

            def show_text6(event):
                text_label.config(text="12:15-13:00")
              
                
            





            for subject_idx, subject in enumerate(result):
                label1 = tk.Label(tab, text=subject[0], width=7, height=2, fg="black", font=("Arial", 9, "bold"))
                label1.place(x=10, y=subject_idx * 50 + 175)
                label1.bind("<Enter>", show_text1)
                text_label = tk.Label(tab, text="", bg="white", fg="black", font=("Arial", 12, "bold"))
                text_label.place(x=260, y=75)

                label1.bind("<Leave>", lambda event: text_label.config(text=""))
         

                label2 = tk.Label(tab, text=subject[1], width=7, height=2, fg="black", font=("Arial", 9, "bold"))
                label2.place(x=10, y=subject_idx * 50 + 225)
                label2.bind("<Enter>", show_text2)
                text_label = tk.Label(tab, text="", bg="white", fg="black", font=("Arial", 12, "bold"))
                text_label.place(x=260, y=75)

                label2.bind("<Leave>", lambda event: text_label.config(text=""))
                

                label3 = tk.Label(tab, text=subject[2], width=7, height=2, fg="black", font=("Arial", 9, "bold"))
                label3.place(x=10, y=subject_idx * 50 + 275)
                label3.bind("<Enter>", show_text3)
                text_label = tk.Label(tab, text="", bg="white", fg="black", font=("Arial", 12, "bold"))
                text_label.place(x=260, y=75)

                label3.bind("<Leave>", lambda event: text_label.config(text=""))

                label4 = tk.Label(tab, text=subject[3], width=7, height=2, fg="black", font=("Arial", 12, "bold"))
                label4.place(x=10, y=subject_idx * 50 + 325)
                label4.bind("<Enter>", show_text4)
                text_label = tk.Label(tab, text="", bg="white", fg="black", font=("Arial", 12, "bold"))
                text_label.place(x=260, y=75)

                label4.bind("<Leave>", lambda event: text_label.config(text=""))

                label5 = tk.Label(tab, text=subject[4], width=7, height=2, fg="black", font=("Arial", 12, "bold"))
                label5.place(x=10, y=subject_idx * 50 + 375)
                label5.bind("<Enter>", show_text5)
                text_label = tk.Label(tab, text="", bg="white", fg="black", font=("Arial", 12, "bold"))
                text_label.place(x=260, y=75)

                label5.bind("<Leave>", lambda event: text_label.config(text=""))

                label6 = tk.Label(tab, text=subject[5], width=7, height=2, fg="black", font=("Arial", 12, "bold"))
                label6.place(x=10, y=subject_idx * 50 + 425)
                label6.bind("<Enter>", show_text6)
                text_label = tk.Label(tab, text="", bg="white", fg="black", font=("Arial", 12, "bold"))
                text_label.place(x=260, y=75)

                label6.bind("<Leave>", lambda event: text_label.config(text=""))


          

            


        
            


        except Exception as e:
            print(f"An error occurred: {e}")
    



    def create_einstellungen_tab(self, tab):
        # hide 
        # Your code for the "Einstellungen" tab
        self.settings_label = tk.Label(tab, text="Einstellungen", font=("Arial", 15))
        self.settings_label.pack()

        def show_lizenz():
            with open("lizenz.txt", "r") as file:
                lizenz = file.read()

                self.leer_label.config(text=f"{lizenz}\nIn Zwischenablage kopiert!") 
                # delete after 5 seconds
                self.master.after(5000, lambda: self.leer_label.config(text="")) 
             
                self.master.clipboard_clear()
                self.master.clipboard_append(lizenz)
                self.master.update()


        def new_lizenz():
            entry = tk.Entry(tab, font=("Arial", 13))
            entry.pack()
            entry.place(x=40, y=150)
            
            self.master.after(30000, lambda: entry.destroy())

            button = tk.Button(tab, text="Lizenz speichern", font=("Arial", 13), command=lambda: save_lizenz(entry.get()))
            button.pack()
            self.master.after(30000, lambda: button.destroy())

            button.place(x=40, y=200)

            def save_lizenz(lizenz):
                

                db = mysql.connector.connect(
                    host="database.snbz.services",
                    user="Nicklas-Public",
                    password="E5$03tb@5k?vfZc#xsB",
                    database="App_Nicklas",
                    port="3306"
                )

                cursor = db.cursor()

    
             
                cursor.execute("SELECT Note FROM Lizenzen WHERE Lizenz = %s", (lizenz,))
                result = cursor.fetchone()

                if result is None:
                    Messagebox.show_error("Fehler", "Diese Lizenz ist nicht vorhanden!")

                else:
                    messagebox.showinfo("Lizenz", "Die Lizenz wurde erfolgreich gespeichert!")
                    with open("lizenz.txt", "w") as file:
                        file.write(lizenz)
                    self.check_for_new_grades()
                    self.load_grades()


            
                

        # button 
        self.button = tk.Button(tab, text="Lizenz anzeigen", font=("Arial", 13), command=show_lizenz)
        self.button.pack()
      
        self.button.place(x=40, y=40)

        self.leer_label = tk.Label(tab, text="", font=("Arial", 15))
        self.leer_label.pack()

        self.leer_label.place(x=330, y=37)

        self.button = tk.Button(tab, text="Vorhandene Lizenz eingeben", font=("Arial", 13), command=new_lizenz)
        self.button.pack()

        self.button.place(x=40, y=100)
        
        self.combobox = Combobox(tab, values=["darkly", "flatly", "cosmo", "superhero", "solar", "cyborg", "vapor"], font=("Arial", 13), state="readonly")
        # text im combobox
        self.combobox.set("Design auswählen")
        self.combobox.place(x=40, y=250)
 
        # search for notes files 
        notes_files = [file for file in os.listdir() if file.startswith("notes")]
        # Create Combobox with individual files as values
        self.notizen_löschen = Combobox(tab, values=notes_files, font=("Arial", 13), state="readonly")
        self.notizen_löschen.set("Notizen löschen")

        
        self.notizen_löschen.place(x=350, y=100)

        def delete_note():	
            db = mysql.connector.connect(
                host="database.snbz.services",
                user="Nicklas-Public",
                password="E5$03tb@5k?vfZc#xsB",
                database="App_Nicklas",
                port="3306"
            )

            cursor = db.cursor()

            
            selected_file = self.notizen_löschen.get()
            file = selected_file.replace("notes_", "").replace(".txt", "")
            cursor.execute("DELETE FROM Notes WHERE `key` = %s", (file,))
            db.commit()
            os.remove(selected_file)
            messagebox.showinfo("Notiz", "Die Notiz wurde erfolgreich gelöscht!")

            # update the combobox
            notes_files = [file for file in os.listdir() if file.startswith("notes")]
            self.notizen_löschen.config(values=notes_files)
            self.notizen_löschen.set("Notizen löschen")

            

            

        

        self.button_delete = tk.Button(tab, text="Notiz löschen", font=("Arial", 13), command=delete_note)
        self.button_delete.pack()
        self.button_delete.place(x=350, y=150)

        
            

        def key_enter():
            entry = tk.Entry(tab, font=("Arial", 13))
            entry.pack()
            entry.place(x=350, y=250)

            self.master.after(30000, lambda: entry.destroy())

            def save_key():
                # wenn der eingegeben Key in der datenbank vorhanden ist, notiz laden
                db = mysql.connector.connect(
                    host="database.snbz.services",
                    user="Nicklas-Public",
                    password="E5$03tb@5k?vfZc#xsB",
                    database="App_Nicklas",
                    port="3306"
                )

                cursor = db.cursor()

                cursor.execute("SELECT * FROM Notes")

                result = cursor.fetchall()

                for row in result:
                    if row[0] == entry.get():
                        with open(f"notes_{entry.get()}.txt", "w") as file:
                            file.write(row[1])
                        messagebox.showinfo("Notiz", "Die Notiz wurde erfolgreich geladen! \n\nDie App wird neu gestartet!")
                        # restart the app

                        # Neustart der App ohne CMD-Fenster
                        current_file = os.path.abspath(__file__)
                        python_executable = sys.executable
                        subprocess.Popen([python_executable, current_file])
                        sys.exit()
                        
                        




                        # update the combobox
                        

                        return

                messagebox.showerror("Fehler", "Dieser Schlüssel ist nicht vorhanden!")

            button = tk.Button(tab, text="Schlüssel speichern", font=("Arial", 13), command=save_key)
            button.pack()

            button.place(x=350, y=300)


        self.button_key = tk.Button(tab, text="Notiz laden", font=("Arial", 13), command=key_enter)
        self.button_key.pack()
        self.button_key.place(x=350, y=200)

        



        
            

        def save_theme():

            if self.combobox.get() != "darkly" and self.combobox.get() != "flatly" and self.combobox.get() != "cosmo" and self.combobox.get() != "superhero" and self.combobox.get() != "solar" and self.combobox.get() != "cyborg" and self.combobox.get() != "vapor":
                messagebox.showerror("Fehler", "Dieses Design ist nicht vorhanden!")
                return

            with open("theme.txt", "w") as file:
                file.write(self.combobox.get())

            messagebox.showinfo("Design", "Das Design wurde erfolgreich gespeichert!")

            # Neustart der App ohne CMD-Fenster
            current_file = os.path.abspath(__file__)
            python_executable = sys.executable
            subprocess.Popen([python_executable, current_file])
            sys.exit()
                        

        self.button = tk.Button(tab, text="Design speichern", font=("Arial", 13), command=save_theme)
        self.button.pack()

        self.button.place(x=40, y=300)

    def load_notes_from_database(self):
        db = mysql.connector.connect(
            host="database.snbz.services",
            user="Nicklas-Public",
            password="E5$03tb@5k?vfZc#xsB",
            database="App_Nicklas",
            port="3306"
        )

        cursor = db.cursor()

        cursor.execute("SELECT * FROM Notes")
        result = cursor.fetchall()

        # Durchlaufe die Datenbankergebnismenge
        for row in result:
            # Extrahiere den Dateinamen aus der Datenbankergebnismenge (Annahme: Der Dateiname befindet sich in Spalte mit Index 1)
            db_filename = row[0]
            db_filename = f"notes_{db_filename}.txt"
            file = db_filename.replace("notes_", "").replace(".txt", "")


            # Überprüfe, ob die Datei im Ordner vorhanden ist
            if os.path.isfile(db_filename):
                # Wenn die Datei im Ordner vorhanden ist, lade die Notiz aus der Datenbank
                with open(db_filename, "w") as file:
                    file.write(row[1])
            else:
                # Andernfalls zeige eine Meldung oder führe eine andere Aktion durch
                print(f"File {db_filename} not found in the folder.")

    def create_notizen_tab(self, tab):
        
        self.notizen_label = tk.Label(tab, text="Notizen", font=("Arial", 15))
        self.notizen_label.pack()



        def create_note():
            db = mysql.connector.connect(
                host="database.snbz.services",
                user="Nicklas-Public",
                password="E5$03tb@5k?vfZc#xsB",
                database="App_Nicklas",
                port="3306"
            ) 

            cursor = db.cursor()

            
            num_letters = 5  
            random_letters = ''.join(random.choice(string.ascii_letters) for _ in range(num_letters))
            leer_label.config(text=f"{random_letters}")

            cursor.execute("INSERT INTO Notes (`key`, notes) VALUES (%s, %s)", (random_letters, ""))
            db.commit()


            self.master.after(30000, lambda: leer_label.config(text=""))

            # create a new file
            with open(f"notes_{random_letters}.txt", "w") as file:
                file.write("")

            # update the combobox
            notes_files = [file for file in os.listdir() if file.startswith("notes")]
            box.config(values=notes_files)
            box.set(f"notes_{random_letters}.txt")
            
            self.notizen_löschen.config(values=notes_files)
            self.notizen_löschen.set("Notizen löschen")

            # feld leeren
            self.notes_entry.delete("1.0", tk.END)





            

            
            



        self.button = tk.Button(tab, text="Notiz erstellen", font=("Arial", 13), command=create_note)
        self.button.pack()
        self.button.place(x=40, y=330)

        leer_label = tk.Label(tab, text="", font=("Arial", 12))
        leer_label.pack()
        leer_label.place(x=480, y=330)

        

        # Text widget for entering notes
        self.notes_entry = tk.Text(tab, wrap=tk.WORD, height=18, width=80)
        self.notes_entry.pack(pady=10)

        # Load existing notes from file
        notes_files = [file for file in os.listdir() if file.startswith("notes")]

        print(notes_files)

        box = ttk.Combobox(tab, values=notes_files, font=("Arial", 13), state="readonly")
        box.set("Notizen auswählen")
        box.pack()

        def load_notes(event):
            selected_file = box.get()
            with open(selected_file, "r") as file:
                notes = file.read()

            self.notes_entry.delete("1.0", tk.END)
            self.notes_entry.insert("1.0", notes)

        box.bind("<<ComboboxSelected>>", load_notes)
       
        
        #self.idmessage = tk.Label(tab, text="ID: ", font=("Arial", 13))

        def save_notes(event=None):
            selected_file = box.get()
            with open(selected_file, "w") as file:
                file.write(self.notes_entry.get("1.0", tk.END))
            
            db = mysql.connector.connect(
                    host="database.snbz.services",
                    user="Nicklas-Public",
                    password="E5$03tb@5k?vfZc#xsB",
                    database="App_Nicklas",
                    port="3306"
                )

            cursor = db.cursor()


            file = selected_file.replace("notes_", "").replace(".txt", "")
            print(file)

            cursor.execute("UPDATE Notes SET notes = %s WHERE `key` = %s", (self.notes_entry.get("1.0", tk.END), file))
            db.commit()


        # Bind Ctrl+s to save_notes
        self.notes_entry.bind("<Control-s>", save_notes)
          
        
    

    def create_kalender_tab(self, tab):
        # Your code for the "Kalender" tab
        self.kalender_label = tk.Label(tab, text="Kalender", font=("Arial", 15))
        self.kalender_label.pack()

        my_date = tb.DateEntry(tab, bootstyle="normal")
        my_date.pack(pady=10)

        my_label = tk.Label(tab, text="")
        my_label.pack(pady=20)

        # text für das datum 

        
        

        
        
    def create_tipps_tab(self, tab):
        # Zeige hier die fächer an, die schlechter als 3 sind
        # Your code for the "Tipps" tab
        self.tipps_label = tk.Label(tab, text="Tipps", font=("Arial", 15))
        self.tipps_label.pack()

        with open("grades.json", "r") as file:
            self.grades = json.load(file)


        for subject, grades in self.grades.items():
            average = sum(grades) / len(grades)
            if average >= 3.5:
    
                #überschrift ist das fach
                self.subject_label = tk.Label(tab, text=subject, font=("Arial", 20, "bold"))        
                self.subject_label.pack()
                
                # wenn schlechter als 5, dann mach den durchschnitt rot
                if average >= 5:
                    self.grade_label = tk.Label(tab, text=f"Durchschnitt: {average:.2f}", font=("Arial", 15), fg="red")
                    self.grade_label.pack()
                    
                    
                elif average >= 3.5:
                    self.grade_label = tk.Label(tab, text=f"Durchschnitt: {average:.2f}", font=("Arial", 15), fg="orange")
                    self.grade_label.pack()



# wenn die App geschlossen wird soll der RPC auch geschlossen werden
                    


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    