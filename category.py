from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

class Category:
    def is_entry_empty(self, *args):
        """Check if any of the given Entry fields are empty."""
        for var in args:
            if var.get() == "":
                return True
        return False
        
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x550+150+50")
        self.root.title("Category")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_C_Id = StringVar()
        self.var_name = StringVar()
    
        title = Label(self.root, text="Manage Product Category", font=("Times New Roman", 25, "bold"), bg="#4caf50", fg="white")
        title.place(x=50, y=20, width=1000, height=50)
        
        Heading = Label(self.root, text="Enter Category Name", font=("Times New Roman", 20), bg="white")
        Heading.place(x=50, y=100)
        
        category_entry = Entry(self.root, textvariable=self.var_name, font=("Times New Roman", 20), bg="lightyellow")
        category_entry.place(x=50, y=160)
        
        btn_add = Button(self.root, text="Add", command=self.save_data, font=("goudy old style", 15), bg="#78281F", fg="white", cursor="hand2")
        btn_add.place(x=350, y=160, width=100, height=35)

        btn_delete = Button(self.root, command=self.delete_data, text="Delete", font=("goudy old style", 15), bg="#78281F", fg="white", cursor="hand2")
        btn_delete.place(x=480, y=160, width=100, height=35)
         
        category_frame = Frame(self.root, bd=3, relief=RIDGE)
        category_frame.place(x=620, y=100, width=450, height=400)

        scrolly = Scrollbar(category_frame, orient=VERTICAL)
        scrollx = Scrollbar(category_frame, orient=HORIZONTAL)

        self.categorytable = ttk.Treeview(category_frame, columns=("C_Id", "name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        self.categorytable.heading("C_Id", text="C_Id")
        self.categorytable.heading("name", text="Name")
        self.categorytable.column("#0", width=0, stretch=NO)
        self.categorytable.column("C_Id", width=100)
        self.categorytable.column("name", width=200)

        scrolly.config(command=self.categorytable.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.categorytable.xview)
        scrollx.pack(side=BOTTOM, fill=X)

        self.categorytable.pack(fill=BOTH, expand=1)

        self.categorytable.bind("<ButtonRelease-1>", self.on_treeview_click)

        # Open the image file using PIL
        self.image = Image.open("Images\icon4.jpg")
        # Resize the image
        self.image = self.image.resize((530, 280))  # Adjust the dimensions as needed
        # Convert the PIL image to a PhotoImage object
        self.photo1 = ImageTk.PhotoImage(self.image)
        # Create a Label and display the image
        lbl_image1 = Label(self.root, image=self.photo1)
        lbl_image1.place(x=50, y=220)  

       

        self.fetch_data()

    def on_treeview_click(self, event):
        # Get the selected item
        selected_item = self.categorytable.selection()[0]

        # Retrieve details of the selected row
        details = self.categorytable.item(selected_item, "values")

        # Fill entry fields with details
        self.var_C_Id.set(details[0])
        self.var_name.set(details[1])
        

    def delete_data(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="company")
            
            # Get the selected item
            selected_item = self.categorytable.selection()[0]

            # Get the employee ID from the selected row
            C_Id = self.categorytable.item(selected_item, 'values')[0]

            # Delete the selected row from the Treeview
            self.categorytable.delete(selected_item)

            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Execute SQL DELETE query
            query = "DELETE FROM category WHERE C_Id = %s"
            cursor.execute(query, (C_Id,))

            # Commit the transaction
            connection.commit()
            
            # Show success message
            messagebox.showinfo("Success", "Category name deleted successfully!")
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
            cursor.execute("SELECT * FROM category")
            rows = cursor.fetchall()
            
            # Clear existing data in the Treeview
            for row in self.categorytable.get_children():
                self.categorytable.delete(row)

            # Insert fetched data into the Treeview
            for row in rows:
                self.categorytable.insert(parent="", index="end", values=(row))

            # Commit changes and close cursor
            connection.commit()
            cursor.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while fetching data: {str(e)}")

    def clear_fields(self):
        # Clear all entry fields
        self.var_C_Id.set("")
        self.var_name.set("")
         
    
    def save_data(self):
        try:
            # Check if any entry field is empty
            if self.is_entry_empty(self.var_name):
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
            name = self.var_name.get()

            # Execute SQL INSERT query
            query = "INSERT INTO category (name) VALUES (%s)"
            values = (name,)
            cursor.execute(query, values)

            # Commit the transaction
            connection.commit()

            # Show success message
            messagebox.showinfo("Success", "Category name saved successfully!")
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

if __name__ == "__main__":
    root = Tk()
    obj = Category(root)
    root.mainloop()
