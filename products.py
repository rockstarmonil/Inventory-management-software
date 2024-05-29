from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

class Product:

    def is_entry_empty(self, *args):
        """Check if any of the given Entry fields are empty."""
        for var in args:
            if var.get() == "":
                return True
        return False
    
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x550+150+50")
        self.root.title("Products")
        self.root.config(bg="white")
        self.root.focus_force()
        
        # Define StringVar variables for entry fields
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_quantity = StringVar()
        self.var_status = StringVar()
        self.var_supplier=StringVar()
        self.var_category=StringVar()

        # Create the frame instance and then place it
        self.product_frame = Frame(self.root, bd=2, relief=RIDGE, background="white")
        self.product_frame.place(x=5, y=5, width=550, height=540)

        # Use the frame as the parent for the label
        self.title_lbl = Label(self.product_frame, text="Manage Product Details", font=("Times New Roman", 20), background="#009688")
        self.title_lbl.pack(side=TOP, fill=X)
        
        self.category_lbl = Label(self.product_frame, text="Category", font=("Times New Roman", 20), background="white").place(x=50, y=70)
        self.supplier_lbl = Label(self.product_frame, text="Supplier", font=("Times New Roman", 20), background="white").place(x=50, y=130)
        self.name_lbl = Label(self.product_frame, text="Name", font=("Times New Roman", 20), background="white").place(x=50, y=190)
        self.price_lbl = Label(self.product_frame, text="Price", font=("Times New Roman", 20), background="white").place(x=50, y=250)
        self.qty_lbl = Label(self.product_frame, text="Quantity", font=("Times New Roman", 20), background="white").place(x=50, y=310)
        self.status_lbl = Label(self.product_frame, text="Status", font=("Times New Roman", 20), background="white").place(x=50, y=370)

        # Create comboboxes for category and supplier
        self.supplier_combobox = ttk.Combobox(self.product_frame,textvariable=self.var_supplier, font=("Times New Roman", 20), background="lightyellow")
        self.supplier_combobox.place(x=200, y=130)

        self.category_combobox = ttk.Combobox(self.product_frame,textvariable=self.var_category, font=("Times New Roman", 20), background="lightyellow")
        self.category_combobox.place(x=200, y=70)

        self.name_entry = Entry(self.product_frame, textvariable=self.var_name, font=("Times New Roman", 20), background="lightyellow")
        self.name_entry.place(x=200, y=190)
        self.price_entry = Entry(self.product_frame, textvariable=self.var_price, font=("Times New Roman", 20), background="lightyellow")
        self.price_entry.place(x=200, y=250)
        self.qty_entry = Entry(self.product_frame, textvariable=self.var_quantity, font=("Times New Roman", 20), background="lightyellow")
        self.qty_entry.place(x=200, y=310)
        self.status_combox = ttk.Combobox(self.product_frame, textvariable=self.var_status, font=("Times New Roman", 20), background="lightyellow",values=("Select","Active","Inactive"),state='readonly')
        self.status_combox.place(x=200, y=370)
        self.status_combox.current(0)

        self.btn_save = Button(self.product_frame, text="Save",command=self.save_data, font=("goudy old style", 15), bg="#78281F", fg="white", cursor="hand2").place(x=50, y=450, width=100, height=30)
        self.btn_Update = Button(self.product_frame, text="Update",command=self.update_data, font=("goudy old style", 15), bg="#78281F", fg="white", cursor="hand2").place(x=170, y=450, width=100, height=30)
        self.btn_delete = Button(self.product_frame, text="Delete",command=self.delete_data, font=("goudy old style", 15), bg="#78281F", fg="white", cursor="hand2").place(x=290, y=450, width=100, height=30)
        self.btn_clear = Button(self.product_frame, text="Clear",command=self.clear_fields, font=("goudy old style", 15), bg="#78281F", fg="white", cursor="hand2").place(x=410, y=450, width=100, height=30)
        
        self.populate_comboboxes()

        product_frames = Frame(self.root, bd=3, relief=RIDGE)
        product_frames.place(x=560, y=10, width=540, height=540)

        scrolly = Scrollbar(product_frames, orient=VERTICAL, width=20)
        scrollx = Scrollbar(product_frames, orient=HORIZONTAL, width=20)

        # Create the Treeview widget
        self.producttable = ttk.Treeview(product_frames, columns=("P_id","category","supplier","name", "price", "quantity", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        # Bind the on_treeview_click function to the Treeview click event
        self.producttable.bind("<ButtonRelease-1>", self.on_treeview_click)

        # Set up column headings
        self.producttable.heading("P_id",text="P_id")
        self.producttable.heading("category", text="Category")
        self.producttable.heading("supplier", text="Supplier")
        self.producttable.heading("name", text="Name")
        self.producttable.heading("price", text="Price")
        self.producttable.heading("quantity", text="Quantity")
        self.producttable.heading("status", text="Status")


        # Set up column widths
        self.producttable.column("#0", width=0)  # Hide the first column
        self.producttable.column("P_id",width=20)
        self.producttable.column("category", width=50)
        self.producttable.column("supplier", width=50)
        self.producttable.column("name", width=50)
        self.producttable.column("price", width=50)
        self.producttable.column("quantity", width=50)
        self.producttable.column("status", width=50)

        # Attach scrollbars
        scrolly.config(command=self.producttable.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.producttable.xview)
        scrollx.pack(side=BOTTOM, fill=X)

        # Pack the Treeview widget
        self.producttable.pack(fill=BOTH, expand=1)

        #Call the fetch_data method to populate the Treeview initially
        self.fetch_data()

    def populate_comboboxes(self):

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="company"
        )
        cursor = connection.cursor()

        # Fetch data for suppliers from the database
        cursor.execute("SELECT name FROM supplier")
        suppliers = cursor.fetchall()
        supplier_names = [supplier[0] for supplier in suppliers]

        # Fetch data for categories from the database
        cursor.execute("SELECT name FROM category")
        categories = cursor.fetchall()
        category_names = [category[0] for category in categories]

        # Set the values for the comboboxes
        self.supplier_combobox['values'] = supplier_names
        self.category_combobox['values'] = category_names

    def on_treeview_click(self, event):
        try:
         # Get the selected item
         selected_item = self.producttable.selection()[0]

         # Retrieve details of the selected row
         details = self.producttable.item(selected_item, "values")

         # Fill entry fields with details
         self.var_supplier.set(details[1])  #supplier
         self.var_category.set(details[2]) #category
         self.var_name.set(details[3])  # Name
         self.var_price.set(details[4])  # Price
         self.var_quantity.set(details[5])  # Quantity
         self.var_status.set(details[6])  # Status
        except IndexError:
         # Show error message if no item is selected
         messagebox.showerror("Error", "Please select a product.")


    def save_data(self):
        try:
         # Check if any entry field is empty
         if self.is_entry_empty(self.var_name, self.var_price, self.var_quantity, self.var_status):
            # Show error message if any field is empty
            messagebox.showerror("Error", "Please fill in all fields.")
            return

         # Open connection to the database
         connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="company"
         )

         cursor = connection.cursor()

         # Retrieve data from Tkinter variables
         name = self.var_name.get()
         price = self.var_price.get()
         quantity = self.var_quantity.get()
         status = self.var_status.get()

         # Fetch supplier and category information
         supplier = self.supplier_combobox.get()
         category = self.category_combobox.get()

         # Execute SQL INSERT query without p_id column
         query = "INSERT INTO product (supplier, category, name, price, quantity, status) VALUES (%s, %s, %s, %s, %s, %s)"
         values = (supplier, category, name, price, quantity, status)
         cursor.execute(query, values)

         # Commit the transaction
         connection.commit()

         # Show success message
         messagebox.showinfo("Success", "Product data saved successfully!")

         # Clear all data fields
         self.clear_fields()
         self.fetch_data()
         self.root.focus_force()

        except Exception as e:
         # Show error message if there's an exception
         messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def clear_fields(self):
        # Clear entry fields
        self.var_name.set("")
        self.var_price.set("")
        self.var_quantity.set("")
        self.var_status.set("")

        # Clear comboboxes
        self.supplier_combobox.set("")  # Reset the selection
        self.category_combobox.set("")  # Reset the selection
    
    def fetch_data(self):
        try:
            # Establish a connection to the database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="company"
            )
            cursor = connection.cursor()

            # Execute SQL SELECT query to fetch data from the product table
            cursor.execute("SELECT * FROM product")
            products = cursor.fetchall()

            # Clear the existing data in the Treeview
            self.producttable.delete(*self.producttable.get_children())

            # Insert the fetched data into the Treeview
            for product in products:
                self.producttable.insert("", END, values=product)

            # Commit the transaction and close the cursor and connection
            connection.commit()
            cursor.close()
            connection.close()

        except Exception as e:
            # Show error message if there's an exception
            messagebox.showerror("Error", f"Error occurred: {str(e)}")
    
    def delete_data(self):
        try:
            # Get the selected item from the Treeview
            selected_item = self.producttable.selection()[0]

            # Retrieve the ID of the selected item
            selected_id = self.producttable.item(selected_item, "values")[0]

            # Confirm deletion with the user
            confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this product?")

            if confirm:
                # Establish a connection to the database
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="company"
                )
                cursor = connection.cursor()

                # Execute SQL DELETE query to delete the selected product
                cursor.execute("DELETE FROM product WHERE p_id = %s", (selected_id,))

                # Commit the transaction and close the cursor and connection
                connection.commit()
                cursor.close()
                connection.close()

                # Show success message
                messagebox.showinfo("Success", "Product deleted successfully!")

                # Refresh the data in the Treeview
                self.fetch_data()
                self.clear_fields()

        except IndexError:
            # Show error message if no item is selected
            messagebox.showerror("Error", "Please select a product to delete.")

        except Exception as e:
            # Show error message if there's an exception
            messagebox.showerror("Error", f"Error occurred: {str(e)}")
    
    def update_data(self):
        try:
            # Get the selected item from the Treeview
            selected_item = self.producttable.selection()[0]

            # Retrieve the ID of the selected item
            selected_id = self.producttable.item(selected_item, "values")[0]

            # Confirm update with the user
            confirm = messagebox.askyesno("Confirmation", "Are you sure you want to update this product?")

            if confirm:
                # Establish a connection to the database
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="company"
                )
                cursor = connection.cursor()

                # Retrieve updated data from entry fields
                name = self.var_name.get()
                price = self.var_price.get()
                quantity = self.var_quantity.get()
                status = self.var_status.get()

                # Fetch supplier and category information
                supplier = self.supplier_combobox.get()
                category = self.category_combobox.get()

                # Execute SQL UPDATE query to update the selected product
                query = "UPDATE product SET supplier = %s, category = %s, name = %s, price = %s, quantity = %s, status = %s WHERE p_id = %s"
                values = (supplier, category, name, price, quantity, status, selected_id)
                cursor.execute(query, values)

                # Commit the transaction and close the cursor and connection
                connection.commit()
                cursor.close()
                connection.close()

                # Show success message
                messagebox.showinfo("Success", "Product updated successfully!")

                # Refresh the data in the Treeview
                self.fetch_data()

        except IndexError:
            # Show error message if no item is selected
            messagebox.showerror("Error", "Please select a product to update.")

        except Exception as e:
            # Show error message if there's an exception
            messagebox.showerror("Error", f"Error occurred: {str(e)}")



if __name__ == "__main__":
    root = Tk()
    obj = Product(root)
    root.mainloop()

