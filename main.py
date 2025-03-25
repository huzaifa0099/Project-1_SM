from tkinter import *
from tkinter import messagebox
import os

class AuthSystem:
    def __init__(self):
        self.root = Tk()
        self.root.title("Auth System")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        self.current_user = None
        self.create_main_screen()

    # -------------------- Authentication Functions -------------------- #
    def create_main_screen(self):
        # Header
        Label(self.root, text="PhoneBook Pro", font=("Helvetica", 24, "bold"), 
              bg="#2c3e50", fg="white").pack(pady=40)
        
        # Auth Card
        self.auth_card = Frame(self.root, bg="#ecf0f1", padx=20, pady=30)
        self.auth_card.pack(pady=20, padx=20)
        
        # Auth Buttons
        Button(self.auth_card, text="Login", bg="#3498db", fg="white",
               command=self.show_login, width=15).pack(pady=10)
        Button(self.auth_card, text="Register", bg="#3498db", fg="white",
               command=self.show_register, width=15).pack(pady=10)

    def show_login(self):
        self.clear_card()
        self.create_form("Login", self.login_user)

    def show_register(self):
        self.clear_card()
        self.create_form("Register", self.register_user)

    def create_form(self, title, command):
        Label(self.auth_card, text=title, font=("Helvetica", 18), 
              bg="#ecf0f1").pack(pady=10)
        
        # Username
        Label(self.auth_card, text="Username:", bg="#ecf0f1").pack()
        self.username = Entry(self.auth_card)
        self.username.pack(pady=5)
        
        # Password
        Label(self.auth_card, text="Password:", bg="#ecf0f1").pack()
        self.password = Entry(self.auth_card, show="*")
        self.password.pack(pady=5)
        
        # Submit Button
        Button(self.auth_card, text=title, bg="#2ecc71", fg="white",
               command=command).pack(pady=20)

    def register_user(self):
        username = self.username.get()
        password = self.password.get()
        
        if os.path.exists(username):
            messagebox.showerror("Error", "Username already exists!")
            return
            
        with open(username, "w") as f:
            f.write(f"{username}\n{password}")
            messagebox.showinfo("Success", "Registration Successful!")
            self.show_login()

    def login_user(self):
        username = self.username.get()
        password = self.password.get()
        
        if not os.path.exists(username):
            messagebox.showerror("Error", "User not found!")
            return
            
        with open(username, "r") as f:
            stored_password = f.read().splitlines()[1]
            if password == stored_password:
                self.current_user = username
                self.show_phonebook()
            else:
                messagebox.showerror("Error", "Incorrect password!")

    # -------------------- Phonebook Functions -------------------- #
    def show_phonebook(self):
        self.root.destroy()  # Close auth window
        
        # Create new phonebook window
        self.phonebook = Tk()
        self.phonebook.title("PhoneBook")
        self.phonebook.geometry("800x600")
        
        # Create UI elements
        self.create_phonebook_ui()
        self.load_contacts()

    def create_phonebook_ui(self):
        # Input Frame
        input_frame = Frame(self.phonebook)
        input_frame.pack(pady=20)
        
        # Name Input
        Label(input_frame, text="Name:").grid(row=0, column=0)
        self.name_entry = Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10)
        
        # Number Input
        Label(input_frame, text="Number:").grid(row=0, column=2)
        self.number_entry = Entry(input_frame, width=20)
        self.number_entry.grid(row=0, column=3, padx=10)
        
        # Buttons
        Button(input_frame, text="Add", bg="#2ecc71", fg="white",
               command=self.add_contact).grid(row=0, column=4, padx=5)
        Button(input_frame, text="Delete", bg="#e74c3c", fg="white",
               command=self.delete_contact).grid(row=0, column=5, padx=5)
        
        # Search
        Label(input_frame, text="Search:").grid(row=1, column=0, pady=10)
        self.search_entry = Entry(input_frame)
        self.search_entry.grid(row=1, column=1, pady=10)
        Button(input_frame, text="Search", 
               command=self.search_contact).grid(row=1, column=2)
        
        # Contact List
        self.contact_list = Listbox(self.phonebook, width=60, height=20)
        self.contact_list.pack(pady=20)
        
        # Logout Button
        Button(self.phonebook, text="Logout", bg="#3498db", fg="white",
               command=self.logout).pack()

    def add_contact(self):
        name = self.name_entry.get()
        number = self.number_entry.get()
        
        if name and number:
            with open(f"{self.current_user}_contacts.txt", "a") as f:
                f.write(f"{name},{number}\n")
            self.load_contacts()
            self.clear_entries()
        else:
            messagebox.showwarning("Warning", "Please fill both fields!")

    def delete_contact(self):
        try:
            index = self.contact_list.curselection()[0]
            contact = self.contact_list.get(index)
            
            with open(f"{self.current_user}_contacts.txt", "r") as f:
                lines = f.readlines()
                
            with open(f"{self.current_user}_contacts.txt", "w") as f:
                for line in lines:
                    if line.strip() != contact:
                        f.write(line)
            
            self.load_contacts()
        except:
            messagebox.showwarning("Warning", "Please select a contact!")

    def search_contact(self):
        search_term = self.search_entry.get().lower()
        self.contact_list.delete(0, END)
        
        if os.path.exists(f"{self.current_user}_contacts.txt"):
            with open(f"{self.current_user}_contacts.txt", "r") as f:
                contacts = f.readlines()
                for contact in contacts:
                    if search_term in contact.lower():
                        self.contact_list.insert(END, contact.strip())

    def load_contacts(self):
        self.contact_list.delete(0, END)
        if os.path.exists(f"{self.current_user}_contacts.txt"):
            with open(f"{self.current_user}_contacts.txt", "r") as f:
                contacts = f.readlines()
                for contact in contacts:
                    self.contact_list.insert(END, contact.strip())

    def clear_entries(self):
        self.name_entry.delete(0, END)
        self.number_entry.delete(0, END)

    def logout(self):
        self.phonebook.destroy()
        self.__init__()  # Restart the application

    def clear_card(self):
        for widget in self.auth_card.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AuthSystem()
    app.run()