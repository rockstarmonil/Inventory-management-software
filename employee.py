from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector


class employeeclass:

    def is_entry_empty(self, *args):
        """Check if any of the given Entry fields are empty."""
        for var in args:
            if var.get() == "":
                return True
        return False
        
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x550+150+50")
        self.root.title("Employee")
        self.root.config(bg="white")
        self.root.focus_force()

        #------All Variables-------
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_address=StringVar()
        self.var_salary=StringVar()

        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Employee", bg="white", font=("goudy old style", 15))
        SearchFrame.place(x=250, y=20, width=600, height=70)

        cmb_search = ttk.Combobox(SearchFrame,textvariable=self.var_searchby, values=("Select", "Name", "Email", "Contact"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame,textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=200, y=10)

        btn_search = Button(SearchFrame, text="Search",command=self.search_data, font=("goudy old style", 15), bg="#78281F", fg="white", cursor="hand2").place(x=430, y=9, width=150, height=30)

        # Title
        title = Label(self.root, text="Employee Details", font=("goudy old style", 15), bg="#4caf50", fg="white")
        title.place(x=50, y=100, width=1000)

        # Content
        lbl_employee = Label(self.root, text="Emp. Id", font=("goudy old style", 15)).place(x=50, y=140)
        employee_entry = Entry(self.root,textvariable=self.var_emp_id, font=("goudy old style", 15), bg="lightyellow")
        employee_entry.place(x=150, y=140, width=200)

        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15)).place(x=50, y=190)
        name_entry = Entry(self.root,textvariable=self.var_name,font=("goudy old style", 15), bg="lightyellow")
        name_entry.place(x=150, y=190, width=200)

        lbl_Email = Label(self.root, text="Email", font=("goudy old style", 15)).place(x=50, y=240)
        email_entry = Entry(self.root,textvariable=self.var_email,font=("goudy old style", 15), bg="lightyellow")
        email_entry.place(x=150, y=240, width=200)

        lbl_address = Label(self.root, text="Address", font=("goudy old style", 15)).place(x=50, y=290)
        address_entry = Entry(self.root,textvariable=self.var_address, font=("goudy old style", 15), bg="lightyellow")
        address_entry.place(x=150, y=290, width=350, height=50)

        lbl_Gender = Label(self.root, text="Gender", font=("goudy old style", 15))
        lbl_Gender.place(x=400, y=140)

        cmb_gender = ttk.Combobox(self.root,textvariable=self.var_gender, values=("Select", "Male", "Female"), font=("goudy old style", 15), state='readonly', justify=CENTER)
        cmb_gender.place(x=500, y=140, width=200)
        cmb_gender.current(0)

        lbl_DOB = Label(self.root, text="D.O.B.", font=("goudy old style", 15)).place(x=400, y=190)
        DOB_entry = Entry(self.root,textvariable=self.var_dob, font=("goudy old style", 15), bg="lightyellow")
        DOB_entry.place(x=500, y=190, width=200)

        lbl_password = Label(self.root, text="Password", font=("goudy old style", 15)).place(x=400, y=240)
        password_entry = Entry(self.root,textvariable=self.var_pass, font=("goudy old style", 15), bg="lightyellow")
        password_entry.place(x=500, y=240, width=200)

        lbl_contact = Label(self.root, text="Contact No.", font=("goudy old style", 15)).place(x=750, y=140)
        contact_entry = Entry(self.root,textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow")
        contact_entry.place(x=870, y=140, width=200)

        lbl_doj = Label(self.root, text="D.O.J.", font=("goudy old style", 15)).place(x=750, y=190)
        doj_entry = Entry(self.root,textvariable=self.var_doj, font=("goudy old style", 15), bg="lightyellow")
        doj_entry.place(x=870, y=190, width=200)

        lbl_usertype = Label(self.root, text="User Type", font=("goudy old style", 15)).place(x=750, y=240)
        cmb_usertype = ttk.Combobox(self.root,textvariable=self.var_utype, values=("Select", "Admin", "Employee"), font=("goudy old style", 15), state='readonly', justify=CENTER)
        cmb_usertype.place(x=870, y=240, width=200)
        cmb_usertype.current(0)

        lbl_salary = Label(self.root, text="Salary", font=("goudy old style", 15)).place(x=550, y=290)
        salary_entry = Entry(self.root,textvariable=self.var_salary, font=("goudy old style", 15), bg="lightyellow")
        salary_entry.place(x=650, y=290)

        btn_save = Button(self.root, text="Save",command=self.save_data ,font=("goudy old style",15), bg="#78281F", fg="white", cursor="hand2").place(x=550, y=330, width=100, height=30)

        btn_Update = Button(self.root, text="Update",command=self.update_data, font=("goudy old style", 15), bg="#78281F", fg="white", cursor="hand2").place(x=680, y=330, width=100, height=30)

        btn_delete = Button(self.root, text="Delete",command=self.delete_data, font=("goudy old style", 15), bg="#78281F", fg="white", cursor="hand2").place(x=810, y=330, width=100, height=30)

        btn_clear = Button(self.root, text="Clear",command=self.clear_fields ,font=("goudy old style", 15), bg="#78281F", fg="white", cursor="hand2").place(x=940, y=330, width=100, height=30)
        
    #------Employee Details-----
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=370, relwidth=1, height=180)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL,width=20)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL,width=20)

    # Create the Treeview widget
        self.EmployeeTable = ttk.Treeview(emp_frame,columns=("EmpId", "name", "email", "gender", "contact", "dob", "doj", "password", "utype", "address", "salary"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    
    # Bind the on_treeview_click function to the Treeview click event
        self.EmployeeTable.bind("<ButtonRelease-1>", self.on_treeview_click)

    # Set up column headings
        self.EmployeeTable.heading("EmpId", text="EmpId")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="DOB")
        self.EmployeeTable.heading("doj", text="DOJ")
        self.EmployeeTable.heading("password", text="Password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")

    # Set up column widths
        self.EmployeeTable.column("#0", width=0)  # Hide the first column
        self.EmployeeTable.column("EmpId", width=50)
        self.EmployeeTable.column("name", width=100)
        self.EmployeeTable.column("email", width=200)
        self.EmployeeTable.column("gender", width=100)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("dob", width=100)
        self.EmployeeTable.column("doj", width=100)
        self.EmployeeTable.column("password", width=100)
        self.EmployeeTable.column("utype", width=100)
        self.EmployeeTable.column("address", width=100)
        self.EmployeeTable.column("salary", width=100)

    # Attach scrollbars
        scrolly.config(command=self.EmployeeTable.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrollx.pack(side=BOTTOM, fill=X)

    # Pack the Treeview widget
        self.EmployeeTable.pack(fill=BOTH,expand=1)

    # Call the fetch_data method to populate the Treeview initially
        self.fetch_data()
#----------------------------------------------------------------------------------------------------
#Database-Backend-Working----------------------------------------------------------------------------
    def on_treeview_click(self, event):
       # Get the selected item
        selected_item = self.EmployeeTable.selection()[0]

       # Retrieve details of the selected row
        details = self.EmployeeTable.item(selected_item, "values")

       # Fill entry fields with details
        self.var_emp_id.set(details[0])
        self.var_name.set(details[1])
        self.var_email.set(details[2])
        self.var_gender.set(details[3])
        self.var_contact.set(details[4])
        self.var_dob.set(details[5])
        self.var_doj.set(details[6])
        self.var_pass.set(details[7])
        self.var_utype.set(details[8])
        self.var_address.set(details[9])
        self.var_salary.set(details[10])
    
    def delete_data(self):
        try:
         connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="company")
         # Get the selected item
         selected_item = self.EmployeeTable.selection()[0]

         # Get the employee ID from the selected row
         emp_id = self.EmployeeTable.item(selected_item, 'values')[0]

         # Delete the selected row from the Treeview
         self.EmployeeTable.delete(selected_item)

         # Create a cursor object to execute SQL queries
         cursor = connection.cursor()

         # Execute SQL DELETE query
         query = "DELETE FROM employee WHERE emp_id = %s"
         cursor.execute(query, (emp_id,))

         # Commit the transaction
         connection.commit()
         
         # Show success message
         messagebox.showinfo("Success", "Employee data deleted successfully!")
         self.clear_fields()
         self.fetch_data()
         self.root.focus_force()
         
        except IndexError:
        
         # Show error message if no row is selected
         messagebox.showerror("Error", "No row selected for deletion!")

        except Exception as e:
        
         # Show error message if there's an exception
         messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def fetch_data(self):
        try:
            connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="company")

            cursor = connection.cursor()

            # Execute SELECT query to fetch all employee data
            cursor.execute("SELECT * FROM employee")
            rows = cursor.fetchall()
            
            # Clear existing data in the Treeview
            for row in self.EmployeeTable.get_children():
                self.EmployeeTable.delete(row)

            # Insert fetched data into the Treeview
            for row in rows:
                self.EmployeeTable.insert(parent="", index="end", values=(row))

            # Commit changes and close cursor
            connection.commit()
            cursor.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while fetching data: {str(e)}")

    def clear_fields(self):
    # Clear all entry fields
         self.var_emp_id.set("")
         self.var_name.set("")
         self.var_email.set("")
         self.var_gender.set("")
         self.var_contact.set("")
         self.var_dob.set("")
         self.var_doj.set("")
         self.var_pass.set("")
         self.var_utype.set("")
         self.var_address.set("")
         self.var_salary.set("")
    
    def save_data(self):

        # Check if any entry field is empty
        if self.is_entry_empty(self.var_emp_id, self.var_name, self.var_email, self.var_gender, self.var_contact, self.var_dob, self.var_doj, self.var_pass, self.var_utype, self.var_address, self.var_salary):
        # Show error message if any field is empty
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        try:

            connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="company")

            cursor = connection.cursor()

            # Retrieve data from Tkinter variables
            emp_id = self.var_emp_id.get()
            name = self.var_name.get()
            email = self.var_email.get()
            gender = self.var_gender.get()
            contact = self.var_contact.get()
            dob = self.var_dob.get()
            doj = self.var_doj.get()
            password = self.var_pass.get()
            utype = self.var_utype.get()
            address = self.var_address.get()
            salary = self.var_salary.get()

            # Execute SQL INSERT query
            query = "INSERT INTO employee (emp_id,name, email, gender, contact, dob, doj, password, utype, address, salary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (emp_id,name, email, gender, contact, dob, doj, password, utype, address, salary)
            cursor.execute(query, values)


            # Commit the transaction
            connection.commit()

            # Show success message
            messagebox.showinfo("Success", "Employee data saved successfully!")

            # CLearing all data fields 
            self.clear_fields()
            self.fetch_data()
            self.root.focus_force()

        except Exception as e:
        # Show error message if there's an exception
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def update_data(self):
        try:
         connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="company")
         
         # Retrieve updated details from entry fields
         name = self.var_name.get()
         email = self.var_email.get()
         gender = self.var_gender.get()
         contact = self.var_contact.get()
         dob = self.var_dob.get()
         doj = self.var_doj.get()
         password = self.var_pass.get()
         utype = self.var_utype.get()
         address = self.var_address.get()
         salary = self.var_salary.get()
         emp_id = self.var_emp_id.get()

         # Update the selected row in the database
         cursor = connection.cursor()
         query = """
            UPDATE employee 
            SET name = %s, email = %s, gender = %s, contact = %s, 
                dob = %s, doj = %s, password = %s, utype = %s, 
                address = %s, salary = %s 
            WHERE emp_id = %s
         """
         values = (name, email, gender, contact, dob, doj, password, utype, address, salary,emp_id)
         cursor.execute(query, values)

         # Commit the transaction
         connection.commit()
         # Show success message
         messagebox.showinfo("Success", "Employee data updated successfully!")

         # CLearing all data fields
         self.clear_fields()
         self.fetch_data()
         self.root.focus_force()
        except Exception as e:
         # Show error message if there's an exception
         messagebox.showerror("Error", f"Error occurred: {str(e)}")
    
    def search_data(self):
     # Get the search query from the user
     search_query = self.var_searchtxt.get()

     try:
         connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="company")

         cursor = connection.cursor()

         if self.var_searchby.get() == "Select":
            messagebox.showerror("Error", "Select search by option", parent=self.root)
            return

         elif search_query == "":
            messagebox.showerror("Error", "Search input should be required", parent=self.root)
            return

         else:
             # Execute SQL SELECT query to search for the row
             query = f"SELECT * FROM employee WHERE {self.var_searchby.get()} LIKE %s"
             cursor.execute(query, ('%' + search_query + '%',))
             rows = cursor.fetchall()

            # Check if the row is found
             if rows:
                # Clear existing data in the Treeview
                for item in self.EmployeeTable.get_children():
                    self.EmployeeTable.delete(item)
                
                # Insert the fetched row(s) into the Treeview
                for row in rows:
                    self.EmployeeTable.insert(parent="", index="end", values=row)
             else:
                messagebox.showinfo("Information", "No matching record found.")

            # Commit changes and close cursor
             connection.commit()
             cursor.close()

     except Exception as e:
         messagebox.showerror("Error", f"Error occurred while searching data: {str(e)}")



if __name__ == "__main__":
    root = Tk()
    obj = employeeclass(root)
    root.mainloop()
