from tkinter import *
from PIL import Image, ImageTk
from employee import employeeclass
from supplier import Supplier
from category import Category
from products import Product
from billing import Billing
from sales import sales
from customers import Customers
import time
import mysql.connector
from tkinter import messagebox
import os
import sys



class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x645+0+0")
        self.root.title("Business Development & Inventory Management Software | Developed By Monil & Sujal ")
        self.root.config(bg="white")
        self.bg_image = Image.open("Images\download1.jpg")  # Replace with your image path
        self.bg_image = self.bg_image.resize((1290, 645), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        label1 = Label( root, image =self.bg_photo) 
        label1.place(x = -5, y = 80) 

        # Maximize the window to fullscreen
        self.root.attributes("-fullscreen", True)

        #------Loading and Resize the Image------
        self.icon_title=Image.open("Images\cart1.png")
        self.icon_title=self.icon_title.resize((60,60),)
        self.icon_title=ImageTk.PhotoImage(self.icon_title)

        # Create the title label with resized image
        title = Label(self.root, text="Business Development & Inventory Management Software", font=("times new roman", 25, "bold"), bg="black", fg="white", anchor="w", padx=20, image=self.icon_title, compound=LEFT).place(x=0, y=0, relwidth=1, height=70)

        #----Button--Logout
        btn_logout = Button(self.root,command=self.logout, text="Logout", font=("times new roman", 15, "bold"), bg="yellow", cursor="hand2").place(x=1100, y=10, height=50, width=150)

        #------Clock----
        self.lbl_clock = Label(self.root, text="Welcome to Dashboard \t\t\t Date: DD-MM-YYYY \t\t\t Time: HH:MM:SS", font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        #------Left Menu------
        self.Menu_icon=Image.open("Images\icon2.png")
        self.Menu_icon=self.Menu_icon.resize((130,130),)
        self.Menu_icon=ImageTk.PhotoImage(self.Menu_icon)

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE,bg="white")
        LeftMenu.place(x=10, y=110, width=190, height=495)
        

        lbl_menuicon = Label(LeftMenu, image=self.Menu_icon)
        lbl_menuicon.pack(side=TOP, fill=X)


        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)

        self.icon_arrow=Image.open("Images/arrow.png")
        self.icon_arrow=self.icon_arrow.resize((35,35),)
        self.icon_arrow=ImageTk.PhotoImage(self.icon_arrow)

        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_arrow,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_arrow,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        btn_category=Button(LeftMenu,text="Category",command=self.category,image=self.icon_arrow,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        btn_product=Button(LeftMenu,text="Product",command=self.product, image=self.icon_arrow,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        btn_billing_panel=Button(LeftMenu,text="Billing",command=self.billing,image=self.icon_arrow,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        btn_sales=Button(LeftMenu,text="Sales",command=self.sales, image=self.icon_arrow,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        
        
      #------Content------
        
        self.lbl_employee=Label(self.root,text="Total Employee \n [0]",font=("times new roman",15),bd=5,bg="#FF70AB")
        self.lbl_employee.place(x=250,y=110,height=100,width=150)

        self.lbl_supplier=Label(self.root,text="Total Supplier \n [0]",font=("times new roman",15),bd=5,bg="#FFEB3B")
        self.lbl_supplier.place(x=450,y=110,height=100,width=150)

        self.lbl_category=Label(self.root,text="Total Category \n [0]",font=("times new roman",15),bd=5,bg="#3f51b5",fg='white')
        self.lbl_category.place(x=650,y=110,height=100,width=150)

        self.lbl_product=Label(self.root,text="Total Product \n [0]",font=("times new roman",15),bd=5,bg="#78909C")
        self.lbl_product.place(x=850,y=110,height=100,width=150)

        self.lbl_sales=Label(self.root,text="Total Sales \n [0]",font=("times new roman",15),bd=5,bg="#F4511E")
        self.lbl_sales.place(x=1050,y=110,height=100,width=150)

        btn_customer_details=Button(self.root,command=self.customers,text="Customer Details",font=("times new roman",15),bg="#009688",cursor="hand2")
        btn_customer_details.place(x=1090,y=300)


        self.update_date_time()
        self.update_content()
        
    #------Footer-------
        lbl_footer = Label(self.root,text="For Any Technical Isuue Contact: 8989669527", font=("times new roman", 12), bg="#4d636d", fg="white").pack(side=BOTTOM,fill=X)

    def employee(self):
     self.new_win=Toplevel(self.root)
     self.new_obj=employeeclass(self.new_win)

    def supplier(self):
     self.new_win=Toplevel(self.root)
     self.new_obj=Supplier(self.new_win)

    def category(self):
     self.new_win=Toplevel(self.root)
     self.new_obj=Category(self.new_win)

    def sales(self):
     self.new_win=Toplevel(self.root)
     self.new_obj=sales(self.new_win)

    def product(self):
     self.new_win=Toplevel(self.root)
     self.new_obj=Product(self.new_win) 

    def billing(self):
      self.new_win=Toplevel(self.root)
      self.new_obj=Billing(self.new_win)

    def customers(self):
      self.new_win=Toplevel(self.root)
      self.new_obj=Customers(self.new_win)

    def update_date_time(self):
      current_time = time.strftime("%I:%M:%S")
      current_date = time.strftime("%d-%m-%Y")
      self.lbl_clock.config(text=f"Welcome to Dashboard \t\t\t Date: {current_date} \t\t\t Time:{current_time}")

      self.lbl_clock.after(200, self.update_date_time)

    def update_content(self):
      connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="company"
            )
      cursor = connection.cursor()
      try:

        cursor.execute("select * from employee ")
        employee=cursor.fetchall()
        self.lbl_employee.config(text=f'Total Employee\n[{str(len(employee))}]')

        cursor.execute("select * from supplier")
        supplier=cursor.fetchall()
        self.lbl_supplier.config(text=f'Total Supplier\n[{str(len(supplier))}]')

        cursor.execute("select * from product")
        product=cursor.fetchall()
        self.lbl_product.config(text=f'Total Product\n[{str(len(product))}]')

        cursor.execute("select * from category")
        category=cursor.fetchall()
        self.lbl_category.config(text=f'Total Category\n[{str(len(category))}]')
        
        bill=len(os.listdir('bill'))
        self.lbl_sales.config(text=f"Total sales\n [{str(bill)}]")

        current_time = time.strftime("%I:%M:%S")
        current_date = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Dashboard \t\t\t Date: {current_date} \t\t\t Time:{current_time}")

        self.lbl_clock.after(200, self.update_content)

      except Exception as ex:
        messagebox.showerror('Error',f"Error due to : {str(ex)}",parent=self.root)

    def logout(self):
      if messagebox.askokcancel("Logout", "Are you sure you want to logout?"):
        root.destroy()
        sys.exit()   
     



if __name__=="__main__":   
 root = Tk()
 obj = IMS(root)
 root.mainloop()
