from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from PIL import Image,ImageTk

class Supplier:
     
    def is_entry_empty(self, *args):
        """Check if any of the given Entry fields are empty."""
        for var in args:
            if var.get() == "":
                return True
        return False
    
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x550+150+50")
        self.root.title("Supplier Details")
        self.root.config(bg="white")
        self.root.focus_force()
        

        # Making Variables
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_supp_id = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        self.txt_desc = StringVar()

        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Supplier", bg="white", font=("goudy old style", 15))
        SearchFrame.place(x=250, y=20, width=600, height=70)

        cmb_search = ttk.Combobox(SearchFrame,textvariable=self.var_searchby, values=("supp_id"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame,textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=200, y=10)

        btn_search = Button(SearchFrame, text="Search",command=self.search_data, font=("goudy old style", 15), bg="#78281F", fg="white", cursor="hand2").place(x=430, y=9, width=150, height=30)
                
        # Title
        title = Label(self.root, text="Supplier Details", font=("goudy old style", 15), bg="#4caf50", fg="white")
        title.place(x=50, y=100, width=1000)
         
        # Open the image file using PIL
        self.image = Image.open("Images\icon3.jpg")
        # Resize the image
        self.image = self.image.resize((400, 180))  # Adjust the dimensions as needed
        # Convert the PIL image to a PhotoImage object
        self.photo1 = ImageTk.PhotoImage(self.image)
        # Create a Label and display the image
        lbl_image1 = Label(self.root, image=self.photo1)
        lbl_image1.place(x=600, y=140) 
        
        lbl_supplier = Label(self.root, text="Supp. Id", font=("goudy old style", 15)).place(x=50, y=150)
        supplier_entry = Entry(self.root,textvariable=self.var_supp_id, font=("goudy old style", 15), bg="lightyellow")
        supplier_entry.place(x=170, y=150, width=200)

        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15)).place(x=50, y=200)
        name_entry = Entry(self.root,textvariable=self.var_name,font=("goudy old style", 15), bg="lightyellow")
        name_entry.place(x=170, y=200, width=200)

        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15)).place(x=50, y=250)
        contact_entry = Entry(self.root,textvariable=self.var_contact,font=("goudy old style", 15), bg="lightyellow")
        contact_entry.place(x=170, y=250, width=200)

        lbl_desc = Label(self.root, text="Description", font=("goudy old style", 15)).place(x=50, y=300)
        address_entry = Entry(self.root,textvariable=self.txt_desc, font=("goudy old style", 15), bg="lightyellow")
        address_entry.place(x=170, y=300, width=350, height=50)
    
        btn_save = Button(self.root, text="Save",command=self.save_data,font=("goudy old style",15), bg="#78281F", fg="white", cursor="hand2").place(x=550, y=330, width=100, height=30)

        btn_Update = Button(self.root, text="Update",command=self.update_data, font=("goudy old style", 15), bg="#78281F", fg="white", cursor="hand2").place(x=670, y=330, width=100, height=30)

        btn_delete = Button(self.root, text="Delete",command=self.delete_data, font=("goudy old style", 15), bg="#78281F", fg="white", cursor="hand2").place(x=790, y=330, width=100, height=30)

        btn_clear = Button(self.root, text="Clear",command=self.clear_fields,font=("goudy old style", 15), bg="#78281F", fg="white", cursor="hand2").place(x=910, y=330, width=100, height=30)
        
        #------Supplier Details-----
        supp_frame = Frame(self.root, bd=3, relief=RIDGE)
        supp_frame.place(x=0, y=370, width=1080, height=180)
    
        scrolly = Scrollbar(self.root, orient=VERTICAL,width=20)
        scrollx = Scrollbar(self.root, orient=HORIZONTAL,width=20)

        # Create the Treeview widget
        self.SupplierTable = ttk.Treeview(supp_frame, columns=("Supp_id", "name", "contact", "Description"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    
        # Bind the on_treeview_click function to the Treeview click event
        self.SupplierTable.bind("<ButtonRelease-1>", self.on_treeview_click)

        # Set up column headings
        self.SupplierTable.heading("Supp_id", text="Supp Id")
        self.SupplierTable.heading("name", text="Name")
        self.SupplierTable.heading("contact", text="Contact")
        self.SupplierTable.heading("Description", text="Description")
        

        # Set up column widths
        self.SupplierTable.column("#0", width=0)  # Hide the first column
        self.SupplierTable.column("Supp_id", width=50)
        self.SupplierTable.column("name", width=50)
        self.SupplierTable.column("contact", width=50)
        self.SupplierTable.column("Description", width=50)

        # Attach scrollbars
        scrolly.config(command=self.SupplierTable.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrollx.pack(side=BOTTOM, fill=X)

        # Pack the Treeview widget
        self.SupplierTable.pack(fill=BOTH,expand=1)   

        # Call the fetch_data method to populate the Treeview initially
        self.fetch_data()

    def on_treeview_click(self, event):
       # Get the selected item
        selected_item = self.SupplierTable.selection()[0]

       # Retrieve details of the selected row
        details = self.SupplierTable.item(selected_item, "values")

       # Fill entry fields with details
        self.var_supp_id.set(details[0])
        self.var_name.set(details[1])
        self.var_contact.set(details[2])
        self.txt_desc.set(details[3])

    def delete_data(self):
        try:
         connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="company")
         
         # Get the selected item
         selected_item = self.SupplierTable.selection()[0]

         # Get the employee ID from the selected row
         supp_id = self.SupplierTable.item(selected_item, 'values')[0]

         # Delete the selected row from the Treeview
         self.SupplierTable.delete(selected_item)

         # Create a cursor object to execute SQL queries
         cursor = connection.cursor()

         # Execute SQL DELETE query
         query = "DELETE FROM supplier WHERE supp_id = %s"
         cursor.execute(query, (supp_id,))

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
            cursor.execute("SELECT * FROM supplier")
            rows = cursor.fetchall()
            
            # Clear existing data in the Treeview
            for row in self.SupplierTable.get_children():
                self.SupplierTable.delete(row)

            # Insert fetched data into the Treeview
            for row in rows:
                self.SupplierTable.insert(parent="", index="end", values=(row))

            # Commit changes and close cursor
            connection.commit()
            cursor.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while fetching data: {str(e)}")

    def clear_fields(self):
    # Clear all entry fields
         self.var_supp_id.set("")
         self.var_name.set("")
         self.var_contact.set("")
         self.txt_desc.set("")
     
    
    def save_data(self):
        try:
         # Check if any entry field is empty
         if self.is_entry_empty(self.var_supp_id, self.var_name, self.var_contact, self.txt_desc):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
         # Establish a connection to the database
         connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="company"
         )

         # Create a cursor object to execute SQL queries
         cursor = connection.cursor()

         # Retrieve data from Tkinter variables
         supp_id = self.var_supp_id.get()
         name = self.var_name.get()
         contact = self.var_contact.get()
         description = self.txt_desc.get()

         # Execute SQL INSERT query
         query = "INSERT INTO supplier (supp_id, name, contact, description) VALUES (%s, %s, %s, %s)"
         values = (supp_id, name, contact, description)
         cursor.execute(query, values)

         # Commit the transaction
         connection.commit()

         # Show success message
         messagebox.showinfo("Success", "Supplier data saved successfully!")
         self.fetch_data()
         self.clear_fields()       
         self.root.focus_force() 

        except mysql.connector.Error as err:
         # Show error message if there's a MySQL-related error
         messagebox.showerror("MySQL Error", f"Error occurred: {err}")

        except Exception as e:
         # Show error message for other exceptions
         messagebox.showerror("Error", f"Error occurred: {e}")

        finally:
         # Close cursor and database connection
         if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


    def update_data(self):
        try:
         connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="company")
         
         # Retrieve updated details from entry fields
         name = self.var_name.get()
         contact = self.var_contact.get()
         description = self.txt_desc.get()
         supp_id = self.var_supp_id.get()

         # Update the selected row in the database
         cursor = connection.cursor()
         query = """
            UPDATE supplier 
            SET name = %s, contact = %s, 
                description = %s
            WHERE supp_id = %s
         """
         values = (name,contact,description,supp_id)
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

         if search_query == "":
            messagebox.showerror("Error", "Search input should be required", parent=self.root)
            return

         else:
             # Execute SQL SELECT query to search for the row
             query = f"SELECT * FROM supplier WHERE {self.var_searchby.get()} LIKE %s"
             cursor.execute(query, ('%' + search_query + '%',))
             rows = cursor.fetchall()

            # Check if the row is found
             if rows:
                # Clear existing data in the Treeview
                for item in self.SupplierTable.get_children():
                    self.SupplierTable.delete(item)
                
                # Insert the fetched row(s) into the Treeview
                for row in rows:
                    self.SupplierTable.insert(parent="", index="end", values=row)
             else:
                messagebox.showinfo("Information", "No matching record found.")

            # Commit changes and close cursor
             connection.commit()
             cursor.close()

     except Exception as e:
         messagebox.showerror("Error", f"Error occurred while searching data: {str(e)}")
     
     
     
if __name__ == "__main__":
    root = Tk()
    obj = Supplier(root)
    root.mainloop()
