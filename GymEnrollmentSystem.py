import sqlite3
import random
from tkinter import messagebox, Tk, Label, Entry, Button, Toplevel
from tkinter import ttk, Canvas, NS
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from PIL import Image, ImageTk

# Database initialization
connection = sqlite3.connect("gymfinal.db")
cursor = connection.cursor()

# Create members table if it doesn't exist
cursor.execute(
    """CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        email TEXT,
        duration TEXT,
        start_date TEXT,
        expiration_date TEXT
    )"""
)
connection.commit()


# Function to authenticate the user
def login(username, password):
    if username == "admin" and password == "admin123":
        global login_successful
        login_successful = True
        login_window.destroy()  # Destroy the login window
        create_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


# Function to create the login window
def create_login_window():
    global login_window  # Declare login_window as a global variable
    login_window = Tk()
    login_window.title("Gym Enrollment System")
    login_window.geometry("1160x820")
    login_window.resizable(False, False)
    login_window.config(bg="#071E22")  # Set light blue background
    c=Canvas(login_window,bg="#071E22",height="1160",width="820")
    c.pack()
    
    
    image = Image.open("C:\\Users\\raaaa\\OneDrive\\Desktop\\gymbg.jpg")
    photo = ImageTk.PhotoImage(image)
    
    background_label1 = Label(login_window, image=photo)
    background_label1.place(x=0, y=0, relwidth=1, relheight=1)
    
    icon = ImageTk.PhotoImage(Image.open("C:\\Users\\raaaa\\OneDrive\\Desktop\\gymicon.png"))
    login_window.iconphoto(False,icon)

    Label(login_window, text = "GYM ENROLLMENT",font="arial 30 bold",bg="#071E22",fg="#4dccbd").place (x=735,y=130)
    Label(login_window, text = "SYSTEM",font="arial 30 bold",bg="#071E22",fg="#4dccbd").place (x=840,y=175)

    # Username label and entry field
    Label(login_window, text = "USERNAME:",font="arial 17 bold",bg="#071E22",fg="#4dccbd").place (x=750,y=260)
    username_entry = Entry(login_window)
    username_entry.place(x=753,y=295,height=30,width=300)

    # Password label and entry field
    Label(login_window, text = "PASSWORD:",font="arial 17 bold",bg="#071E22",fg="#4dccbd").place (x=750,y=360)
    password_entry = Entry(login_window, show="*")
    password_entry.place(x=753,y=395,height=30,width=300)

    # Login button
    login_button = Button(login_window, text="Login",height=2,width=8,bd=1,font="arial 13 bold",bg="#4dccbd",fg="#071E22", command=lambda: login(username_entry.get(), password_entry.get()))
    login_button.place(x=860,y=560)

    login_window.mainloop()

  

# Function to add a member
def add_member_window():
    add_member_window = Toplevel()
    add_member_window.title("Add Member")
    add_member_window.geometry("800x600")
    add_member_window.config(bg="#4dccbd")  # Set light blue background
    
    icon = ImageTk.PhotoImage(Image.open("C:\\Users\\raaaa\\OneDrive\\Desktop\\gymicon.png"))
    add_member_window.iconphoto(False,icon)
    
    # Member details labels and entry fields
    Label(add_member_window, text="Name:",font="arial 15 bold",bg="#071E22",fg="#4dccbd").place (x=200,y=130)
    name_entry = Entry(add_member_window)
    name_entry.place (x=400, y=130,height=30,width=330)

    Label(add_member_window, text="Age:",font="arial 15 bold",bg="#071E22",fg="#4dccbd").place (x=200,y=170)
    age_entry = Entry(add_member_window)
    age_entry.place (x=400, y=170,height=30,width=330)

    Label(add_member_window, text="Email:",font="arial 15 bold",bg="#071E22",fg="#4dccbd").place (x=200,y=210)
    email_entry = Entry(add_member_window)
    email_entry.place (x=400, y=210,height=30,width=330)

    Label(add_member_window, text="Duration:",font="arial 15 bold",bg="#071E22",fg="#4dccbd").place (x=200,y=250)
    duration_combobox = ttk.Combobox(add_member_window, values=["1 Month", "3 Months", "6 Months", "1 Year"])
    duration_combobox.place (x=400, y=250,height=30,width=330)

    # Function to add member details to the database
    def add_member_to_db():
        name = name_entry.get()
        age = age_entry.get()
        email = email_entry.get()
        duration = duration_combobox.get()
        
        # Generate unique membership ID
        current_year = str(date.today().year)[-2:]
        random_digits = str(random.randint(100, 999))
        membership_id = current_year + random_digits
    
        if name and age and email and duration:
            start_date = date.today().strftime("%Y-%m-%d")
            
            if duration == "1 Month":
                expiration_date = (date.today() + relativedelta(months=+1)).strftime("%Y-%m-%d")
            elif duration == "3 Months":
                expiration_date = (date.today() + relativedelta(months=+3)).strftime("%Y-%m-%d")
            elif duration == "6 Months":
                expiration_date = (date.today() + relativedelta(months=+6)).strftime("%Y-%m-%d")
            elif duration == "1 Year":
                current_date = date.today()
                expiration_date = (current_date + timedelta(days=365)).strftime("%Y-%m-%d")
            
            
            cursor.execute("INSERT INTO members (ID, name, age, email, duration, start_date, expiration_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (membership_id, name, age, email, duration, start_date, expiration_date))
            connection.commit()
            messagebox.showinfo("Success", "Member added successfully.")
            clear_entry_fields()
        else:
            messagebox.showwarning("Incomplete Information", "Please enter all member details.")
    # Add member button
    add_button = Button(add_member_window, text="Add Member", font="arial 15 bold",bg="#071E22",fg="#4dccbd", command=add_member_to_db)
    add_button.place (x=400, y=290,height=30,width=330)

# Function to display the member list
def member_list_window():
    member_list_window = Toplevel()
    member_list_window.title("Member List")
    member_list_window.geometry("1160x820")
    member_list_window.config(bg="#B1EDE8")  # Set light blue background
    
    icon = ImageTk.PhotoImage(Image.open("C:\\Users\\raaaa\\OneDrive\\Desktop\\gymicon.png"))
    member_list_window.iconphoto(False,icon)
    

    # Search function
    def search_members():
        search_text = search_entry.get().lower()

        # Clear the treeview before performing the search
        treeview.delete(*treeview.get_children())

        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()
        for member in members:
            if search_text in str(member[0]).lower() or search_text in member[1].lower():
                treeview.insert("", "end", text="", values=member)

    # Member list table
    treeview = ttk.Treeview(member_list_window)
    treeview["columns"] = ("ID", "Name", "Age", "Email", "Duration", "Start Date", "Expiration Date")
    treeview.column("#0", width=0, stretch="NO")
    treeview.column("ID", anchor="center", width=50)
    treeview.column("Name", anchor="w", width=150)
    treeview.column("Age", anchor="center", width=50)
    treeview.column("Email", anchor="w", width=150)
    treeview.column("Duration", anchor="center", width=80)
    treeview.column("Start Date", anchor="center", width=100)
    treeview.column("Expiration Date", anchor="center", width=100)

    treeview.heading("#0", text="", anchor="w")
    treeview.heading("ID", text="ID", anchor="center")
    treeview.heading("Name", text="Name", anchor="w")
    treeview.heading("Age", text="Age", anchor="center")
    treeview.heading("Email", text="Email", anchor="w")
    treeview.heading("Duration", text="Duration", anchor="center")
    treeview.heading("Start Date", text="Start Date", anchor="center")
    treeview.heading("Expiration Date", text="Expiration Date", anchor="center")

    # Function to fetch member list from the database and display it in the treeview
    def fetch_member_list():
        # Clear the treeview before fetching the member list
        treeview.delete(*treeview.get_children())

        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()
        for member in members:
            treeview.insert("", "end", text="", values=member)

    fetch_member_list()
    treeview.pack(fill="both", expand=True)

    # Search entry and button
    search_frame = ttk.Frame(member_list_window)
    search_frame.pack(pady=10)

    Label(search_frame, text="Search:",bg="#071E22",fg="#4dccbd").grid(row=0, column=0)
    search_entry = ttk.Entry(search_frame)
    search_entry.grid(row=0, column=1)

    search_button = ttk.Button(search_frame, text="Search", command=search_members)
    search_button.grid(row=0, column=2)

    # Function to edit member details
    def edit_member():
        selected_item = treeview.focus()
        if selected_item:
            member_id = treeview.item(selected_item)["values"][0]
            member_details = cursor.execute("SELECT * FROM members WHERE id=?", (member_id,))
            member = cursor.fetchone()

            if member:
                edit_member_window = Toplevel()
                edit_member_window.title("Edit Member")
                edit_member_window.geometry("800x600")
                edit_member_window.config(bg="#4dccbd")
                
                icon = ImageTk.PhotoImage(Image.open("C:\\Users\\raaaa\\OneDrive\\Desktop\\gymicon.png"))
                edit_member_window.iconphoto(False,icon)

                # Member details labels and entry fields
                Label(edit_member_window, text="Name:", font="arial 15 bold",bg="#071E22",fg="#4dccbd").place (x=200,y=130)
                name_entry = Entry(edit_member_window)
                name_entry.place (x=400, y=130,height=30,width=330)
                name_entry.insert(0, member[1])

                Label(edit_member_window, text="Age:",font="arial 15 bold",bg="#071E22",fg="#4dccbd").place (x=200,y=170)
                age_entry = Entry(edit_member_window)
                age_entry.place (x=400, y=170,height=30,width=330)
                age_entry.insert(0, member[2])

                Label(edit_member_window, text="Email:",font="arial 15 bold",bg="#071E22",fg="#4dccbd").place (x=200,y=210)
                email_entry = Entry(edit_member_window)
                email_entry.place (x=400, y=210,height=30,width=330)
                email_entry.insert(0, member[3])

                Label(edit_member_window, text="Duration:",font="arial 15 bold",bg="#071E22",fg="#4dccbd").place (x=200,y=250)
                duration_combobox = ttk.Combobox(edit_member_window, values=["1 Month", "3 Months", "6 Months", "1 Year"])
                duration_combobox.place (x=400, y=250,height=30,width=330)
                duration_combobox.set(member[4])

                # Function to update member details in the database
                def update_member_in_db():
                    name = name_entry.get()
                    age = age_entry.get()
                    email = email_entry.get()
                    duration = duration_combobox.get()

                    if name and age and email and duration:
                        new_expiration_date = (
                                date.today() + relativedelta(months=+int(duration.split()[0]))).strftime("%Y-%m-%d")

                        cursor.execute(
                            "UPDATE members SET name=?, age=?, email=?, duration=?, expiration_date=? WHERE id=?",
                            (name, age, email, duration, new_expiration_date, member_id)
                        )
                        connection.commit()
                        messagebox.showinfo("Success", "Member details updated successfully.")
                        edit_member_window.destroy()
                        fetch_member_list()  # Refresh member list after updating the member
                    else:
                        messagebox.showwarning("Incomplete Information", "Please enter all member details.")

                
                update_button = Button(edit_member_window, text="Update", font="arial 15 bold",bg="#071E22",fg="#4dccbd", command=update_member_in_db)
                update_button.place (x=400, y=290,height=30,width=330)
            else:
                messagebox.showerror("Error", "Member not found.")
        else:
            messagebox.showwarning("No Member Selected", "Please select a member to edit.")

    # Edit Member button
    edit_button = Button(member_list_window, text="Edit Member",bg="#071E22",fg="#4dccbd", command=edit_member)
    edit_button.pack(pady=10)

    # Function to delete member from the database
    def delete_member():
        selected_item = treeview.focus()
        if selected_item:
            member_id = treeview.item(selected_item)["values"][0]
            member_details = cursor.execute("SELECT * FROM members WHERE id=?", (member_id,))
            member = cursor.fetchone()

            if member:
                confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this member?")
                if confirm:
                    cursor.execute("DELETE FROM members WHERE id=?", (member_id,))
                    connection.commit()
                    fetch_member_list()  # Refresh member list after deleting the member
                    messagebox.showinfo("Success", "Member deleted successfully.")
            else:
                messagebox.showerror("Error", "Member not found.")
        else:
            messagebox.showwarning("No Member Selected", "Please select a member to delete.")

    # Delete Member button
    delete_button = Button(member_list_window, text="Delete Member",bg="#071E22",fg="#4dccbd", command=delete_member)
    delete_button.pack(pady=10)

    member_list_window.mainloop()





# Function to create the main window
def create_main_window():
    main_window = Tk()
    main_window.title("Gym Enrollment System")
    main_window.geometry("1160x820")
    main_window.resizable(False, False)
    main_window.config(bg="#071E22")
    
    image = Image.open("C:\\Users\\raaaa\\OneDrive\\Desktop\\gymbg.jpg")
    photo = ImageTk.PhotoImage(image)
    
    icon = ImageTk.PhotoImage(Image.open("C:\\Users\\raaaa\\OneDrive\\Desktop\\gymicon.png"))
    main_window.iconphoto(False,icon)
    
    background_label = Label(main_window, image=photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Add Member button
    add_member_button = Button(main_window, text="Add Member",height=2,width=8,bd=1,font="arial 13 bold",bg="#4dccbd",fg="#071E22", command=add_member_window)
    add_member_button.place(x=753,y=295,height=30,width=300)

    # Member List button
    member_list_button = Button(main_window, text="Member List",height=2,width=8,bd=1,font="arial 13 bold",bg="#4dccbd",fg="#071E22", command=member_list_window)
    member_list_button.place(x=753,y=395,height=30,width=300)

    main_window.mainloop()

# Set the initial value of login_successful flag to False
login_successful = False

# Call the function to create the login window
create_login_window()

# Start the event loop and keep running until login is successful
while not login_successful:
    login_window.update()

# Once the login is successful, start the main event loop
Tk.mainloop()