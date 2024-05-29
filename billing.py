from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import mysql.connector
import time
import os
import tempfile



class Billing:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x645+0+0")
        self.root.title("Business Development & Inventory Management Software | Developed By Monil & Sujal ")
        self.root.config(bg="white")

        # Maximize the window to fullscreen
        #self.root.attributes("-fullscreen", True)

        #------Loading and Resize the Image------
        self.icon_title=Image.open("Images\cart1.png")
        self.icon_title=self.icon_title.resize((60,60),)
        self.icon_title=ImageTk.PhotoImage(self.icon_title)
        self.cart_list=[]
        self.chk_print=0

        # Create the title label with resized image
        title = Label(self.root, text="Business Development & Inventory Management Software", font=("times new roman", 25, "bold"), bg="black", fg="white", anchor="w", padx=20, image=self.icon_title, compound=LEFT).place(x=0, y=0, relwidth=1, height=70)

        #----Button--Logout
        btn_logout = Button(self.root, text="Logout", font=("times new roman", 15, "bold"), bg="yellow", cursor="hand2").place(x=1100, y=10, height=50, width=150)

        #------Clock----
        self.lbl_clock = Label(self.root, text="Welcome to Dashboard \t\t\t Date: DD-MM-YYYY \t\t\t Time: HH:MM:SS", font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

      #---------Product Frame--------------
        self.var_search=StringVar()

        Product_frame=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        Product_frame.place(x=0,y=110,width=350,height=530)

        P_title=Label(Product_frame,text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
        
        Product_frame2=Frame(Product_frame,bd=2,relief=RIDGE,bg="white")
        Product_frame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(Product_frame2,text="Search Product | By Name",font=("goudy old style",14,"bold"),bg="white",fg="green").place(x=2,y=8)
        lbl_name=Label(Product_frame2,text="Product Name",font=("goudy old style",12,"bold"),bg="white").place(x=5,y=45)
        txt_search=Entry(Product_frame2,textvariable=self.var_search,font=("goudy old style",12),bg="lightyellow").place(x=125,y=47,width=130,height=22)

        btn_search=Button(Product_frame2,command=self.search_data,text="Search",font=("goudy old style",13),bg="#2196f3",fg="white").place(x=260,y=45,width=80,height=25)
        btn_show_all=Button(Product_frame2,command=self.fetch_data,text="Show All",font=("goudy old style",13),bg="#083531",fg="white").place(x=260,y=10,width=80,height=25)
        
    #--------------------------------------Frame3---------------------------------------------------------------
 
        Product_frame3 = Frame(Product_frame, bd=2, relief=RIDGE)
        Product_frame3.place(x=2, y=140, width=350, height=385)

        scrolly = Scrollbar(Product_frame3, orient=VERTICAL,width=20)
        scrollx = Scrollbar(Product_frame3, orient=HORIZONTAL,width=20)

    # Create the Treeview widget
        self.Product_table = ttk.Treeview(Product_frame3,columns=("p_id", "name", "price", "qty","status"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    
    # Bind the on_treeview_click function to the Treeview click event
       # self.Product_table.bind("<ButtonRelease-1>", self.on_treeview_click)

    # Set up column headings
        self.Product_table.heading("p_id", text="P_id")
        self.Product_table.heading("name", text="Name")
        self.Product_table.heading("price", text="Price")
        self.Product_table.heading("qty", text="Quantity")
        self.Product_table.heading("status", text="Status")

    # Set up column widths
        self.Product_table.column("#0", width=0)  # Hide the first column
        self.Product_table.column("p_id", width=50)
        self.Product_table.column("name", width=100)
        self.Product_table.column("price", width=100)
        self.Product_table.column("qty", width=100)
        self.Product_table.column("status", width=100)
    

    # Attach scrollbars
        scrolly.config(command=self.Product_table.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.Product_table.xview)
        scrollx.pack(side=BOTTOM, fill=X)

    # Pack the Treeview widget
        self.Product_table.pack(fill=BOTH,expand=1)

    # Bind the on_treeview_click function to the Treeview click event
        self.Product_table.bind("<ButtonRelease-1>", self.on_treeview_click)

    #--------------------------------------------------------------------------------
        self.var_cname=StringVar()
        self.var_contact=StringVar()

        CustomerFrame=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        CustomerFrame.place(x=355,y=110,width=530,height=70)

        C_title=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgrey").pack(side=TOP,fill=X)

        lbl_name=Label(CustomerFrame,text="Name",font=("goudy old style",15),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("goudy old style",13),bg="lightyellow").place(x=65,y=35,width=180)
 
        lbl_contact=Label(CustomerFrame,text="Contact",font=("goudy old style",15),bg="white").place(x=280,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("goudy old style",13),bg="lightyellow").place(x=360,y=35,width=140)

        CustomerFrame2=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        CustomerFrame2.place(x=355,y=190,width=530,height=360)
        
        #--------------Calculator Frame----------------------------------
        self.var_cal_input=StringVar()

        Cal_Frame=Frame(CustomerFrame2,bd=9,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=268,height=340)

        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=5)
        
        btn7=Button(Cal_Frame,text=7,font=("arial",15,"bold"),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=0)
        btn8=Button(Cal_Frame,text=8,font=("arial",15,"bold"),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=1)
        btn9=Button(Cal_Frame,text=9,font=("arial",15,"bold"),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=("arial",15,"bold"),command=lambda:self.get_input('+'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=3)

        btn4=Button(Cal_Frame,text=4,font=("arial",15,"bold"),command=lambda:self.get_input(4),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=0)
        btn5=Button(Cal_Frame,text=5,font=("arial",15,"bold"),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=1)
        btn6=Button(Cal_Frame,text=6,font=("arial",15,"bold"),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=2)
        btn_subtract=Button(Cal_Frame,text='-',font=("arial",15,"bold"),command=lambda:self.get_input('-'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=3)

        btn1=Button(Cal_Frame,text=1,font=("arial",15,"bold"),command=lambda:self.get_input(1),bd=5,width=4,pady=15,cursor="hand2").grid(row=3,column=0)
        btn2=Button(Cal_Frame,text=2,font=("arial",15,"bold"),command=lambda:self.get_input(2),bd=5,width=4,pady=15,cursor="hand2").grid(row=3,column=1)
        btn3=Button(Cal_Frame,text=3,font=("arial",15,"bold"),command=lambda:self.get_input(3),bd=5,width=4,pady=15,cursor="hand2").grid(row=3,column=2)
        btn_Mul=Button(Cal_Frame,text='*',font=("arial",15,"bold"),command=lambda:self.get_input('*'),bd=5,width=4,pady=15,cursor="hand2").grid(row=3,column=3)

        btn0=Button(Cal_Frame,text=0,font=("arial",15,"bold"),command=lambda:self.get_input(0),bd=5,width=4,pady=10,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text='c',font=("arial",15,"bold"),command=self.clear_cal,bd=5,width=4,pady=10,cursor="hand2").grid(row=4,column=1)
        btn_equal=Button(Cal_Frame,text='=',font=("arial",15,"bold"),command=self.perform_cal,bd=5,width=4,pady=10,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=("arial",15,"bold"),command=lambda:self.get_input('/'),bd=5,width=4,pady=10,cursor="hand2").grid(row=4,column=3)

        Cart_Frame = Frame(CustomerFrame2, bd=2, relief=RIDGE)
        Cart_Frame.place(x=280, y=8, width=245, height=342)
        self.Cart_title=Label(Cart_Frame,text="Cart\tTotal Products: [0]",font=("goudy old style",13),bg="lightgrey")
        self.Cart_title.pack(side=TOP,fill=X)

        scrolly = Scrollbar(Cart_Frame, orient=VERTICAL,width=20)
        scrollx = Scrollbar(Cart_Frame, orient=HORIZONTAL,width=20)

    # Create the Treeview widget
        self.cart_table = ttk.Treeview(Cart_Frame,columns=("p_id", "name", "price", "qty"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    
    # Set up column headings
        self.cart_table.heading("p_id", text="P_id")
        self.cart_table.heading("name", text="Name")
        self.cart_table.heading("price", text="Price")
        self.cart_table.heading("qty", text="Qty")
        
    # Set up column widths
        self.cart_table.column("#0", width=0)  # Hide the first column
        self.cart_table.column("p_id", width=30)
        self.cart_table.column("name", width=120)
        self.cart_table.column("price", width=70)
        self.cart_table.column("qty", width=50)

    # Attach scrollbars
        scrolly.config(command=self.cart_table.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.cart_table.xview)
        scrollx.pack(side=BOTTOM, fill=X)

    # Pack the Treeview widget
        self.cart_table.pack(fill=BOTH,expand=1)

    # Binding cart Table
        self.cart_table.bind("<ButtonRelease-1>", self.on_treeview_click_cart)
    #---------Add Cart Widgets------------------------
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()

        Buttons_Frame=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        Buttons_Frame.place(x=355,y=550,width=530,height=110)

        lbl_p_name=Label(Buttons_Frame,text="Product Name",font=("goudy old style",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Buttons_Frame,textvariable=self.var_pname,font=("goudy old style",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(Buttons_Frame,text="Price Per Qty",font=("goudy old style",15),bg="white").place(x=210,y=5)
        txt_p_price=Entry(Buttons_Frame,textvariable=self.var_price,font=("goudy old style",15),bg="lightyellow",state='readonly').place(x=210,y=35,width=150,height=22)
        
        lbl_p_quantity=Label(Buttons_Frame,text="Quantity",font=("goudy old style",15),bg="white").place(x=370,y=5)
        txt_p_quantity=Entry(Buttons_Frame,textvariable=self.var_qty,font=("goudy old style",15),bg="lightyellow").place(x=370,y=35,width=150,height=22)

        self.lbl_inStock=Label(Buttons_Frame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_inStock.place(x=5,y=60)
    
        btn_clear_cart=Button(Buttons_Frame,command=self.clear_cart,text="Clear",font=("goudy font style",15,),bg="lightgrey",cursor="hand2").place(x=170,y=65,width=150,height=25)
        btn_add_cart=Button(Buttons_Frame,command=self.add_update_cart,text="Add | Update Cart",font=("goudy font style",15,),bg="orange",cursor="hand2").place(x=340,y=65,width=170,height=25)

#==================Billing Area=======================================================

        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billFrame.place(x=888,y=110,width=380,height=410)

        btn_save=Button(billFrame,command=self.save_bill,text="Save Bill",font=('goudy old style',13,'bold'),bg='#3f51b5',fg='white',cursor="hand2")
        btn_save.pack(side=BOTTOM,fill=X)

        B_title=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        
#==================================Billing Buttons==========================================

        buttonFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        buttonFrame.place(x=888,y=520,width=380,height=130)

        self.lbl_amount=Label(buttonFrame,text="Bill Amount\n[0]",font=('goudy old style',13,'bold'),bg='#3f51b5',fg='white')
        self.lbl_amount.place(x=5,y=5,width=120,height=55)
        
        self.lbl_discount=Label(buttonFrame,text="Discount\n[5%]",font=('goudy old style',13,'bold'),bg='#3f51b5',fg='white')
        self.lbl_discount.place(x=130,y=5,width=120,height=55)

        self.lbl_netpay=Label(buttonFrame,text="NetPay\n[0]",font=('goudy old style',13,'bold'),bg='#3f51b5',fg='white')
        self.lbl_netpay.place(x=255,y=5,width=120,height=55)

        btn_print=Button(buttonFrame,command=self.print_bill,text="Print",font=('goudy old style',13,'bold'),bg='#3f51b5',fg='white')
        btn_print.place(x=5,y=65,width=120,height=50)
        
        btn_clear_all=Button(buttonFrame,command=self.clear_all,text="Clear All",font=('goudy old style',13,'bold'),bg='#3f51b5',fg='white')
        btn_clear_all.place(x=130,y=65,width=120,height=50)

        btn_generate=Button(buttonFrame,command=self.generate_bill,text="Generate Bill",font=('goudy old style',13,'bold'),bg='#3f51b5',fg='white')
        btn_generate.place(x=255,y=65,width=120,height=50)

        self.fetch_data()
        self.update_date_time()
        
#---------------All Functions---------------------------------------------------------

    def get_input(self,num):
       xnum=self.var_cal_input.get()+str(num)
       self.var_cal_input.set(xnum)    

    def clear_cal(self):
       self.var_cal_input.set('')

    def perform_cal(self):
       result=self.var_cal_input.get()
       self.var_cal_input.set(eval(result))   

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
            cursor.execute("SELECT p_id, name, price, quantity, status FROM product WHERE status = 'active'")
            products = cursor.fetchall()

            # Clear the existing data in the Treeview
            self.Product_table.delete(*self.Product_table.get_children())

            # Insert the fetched data into the Treeview
            for product in products:
                self.Product_table.insert("", END, values=product)

            # Commit the transaction and close the cursor and connection
            connection.commit()
            cursor.close()
            connection.close()

        except Exception as e:
            # Show error message if there's an exception
            messagebox.showerror("Error", f"Error occurred: {str(e)}")
    
    def search_data(self):
     # Get the search query from the user
     search_query = self.var_search.get()

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
             query = "SELECT * FROM product WHERE name LIKE %s"
             cursor.execute(query, ('%' + search_query + '%',))
             rows = cursor.fetchall()

            # Check if the row is found
             if rows:
                # Clear existing data in the Treeview
                for item in self.Product_table.get_children():
                    self.Product_table.delete(item)
                
                # Insert the fetched row(s) into the Treeview
                for row in rows:
                # Extracting specific columns from the row
                 p_id = row[0]  # Assuming p_id is the first column
                 name = row[3]  # Assuming name is the second column
                 price = row[4]  # Assuming price is the third column
                 quantity = row[5]  # Assuming quantity is the fourth column
                 status = row[6]  # Assuming status is the fifth column

                 # Inserting extracted values into the Product_table
                 self.Product_table.insert(parent="", index="end", values=(p_id, name, price, quantity, status))

             else:
                messagebox.showinfo("Information", "No matching record found.")

              # Commit changes and close cursor
                connection.commit()
                cursor.close()

     except Exception as e:
         messagebox.showerror("Error", f"Error occurred while searching data: {str(e)}")

    def on_treeview_click(self, event):
       f=self.Product_table.focus()
       content=(self.Product_table.item(f))
       row=content['values']

       self.var_pid.set(row[0])
       self.var_pname.set(row[1])
       self.var_price.set(row[2])
       self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
       self.var_qty.set('1')
       self.var_stock.set(row[3])

    def add_update_cart(self):
       if self.var_pid.get()=='':
          messagebox.showerror('Error','Please Select Product From the List',parent=self.root)
       elif self.var_qty.get()=='' : 
         messagebox.showerror('Error','Quantity is Required',parent=self.root)
       elif int(self.var_qty.get())>int(self.var_stock.get()) : 
         messagebox.showerror('Error','Invalid Quantity',parent=self.root)
       else:
         #price_cal=int(self.var_qty.get())*float(self.var_price.get())
         #price_cal=float(price_cal)
         price_cal=self.var_price.get()
         cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
         
         #================Update Cart====================================================
         present='no'
         index_=0
         for row in self.cart_list:
            if self.var_pid.get()==row[0]:
               present='yes'
               break
            index_+=1
         if present=='yes':
            op=messagebox.askyesno('Confirm','Product already present\n Do You Want to Update| Remove from the Cart',parent=self.root)
            if op==True:
               if self.var_qty.get()=="0":
                  self.cart_list.pop(index_)
               else:
                  #self.cart_list[index_][2]=price_cal
                  self.cart_list[index_][3]=self.var_qty.get()
                   
         else:
            self.cart_list.append(cart_data)
        
         self.show_cart()
         self.bill_updates()

    def show_cart(self):
        try:
          self.cart_table.delete(*self.cart_table.get_children())
          for row in self.cart_list:
             self.cart_table.insert('',END,values=row)
        except Exception as ex:
           messagebox.showerror('Error',f'Error due to : {str(ex)}',parent=self.root)
    
    def bill_updates(self):
       self. bill_amnt=0
       self.net_pay=0
       self.discount=0     

       for row in self.cart_list:
          self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))

          self.discount=(self.bill_amnt*5)/100
          self.net_pay=(self.bill_amnt)-(self.discount)
          
       self.lbl_amount.config(text=f"Bill Amount\n[{str(self.bill_amnt)}]")  
       self.lbl_netpay.config(text=f"Net Pay\n[{str(self.net_pay)}]")     
       self.Cart_title.config(text=f"Cart\tTotal Products: [{str(len(self.cart_list))}]")

    def on_treeview_click_cart(self, event):
       f=self.cart_table.focus()
       content=(self.cart_table.item(f))
       row=content['values']

       self.var_pid.set(row[0])
       self.var_pname.set(row[1])
       self.var_price.set(row[2])
       self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
       self.var_qty.set(row[3])
       self.var_stock.set(row[4])
    
    def generate_bill(self):
       if self.var_cname.get()=='' or self.var_contact.get()=='':
          messagebox.showerror('Error',"Customer Details are Required",parent=self.root)
       elif len(self.cart_list)==0:
         messagebox.showerror('Error',"Please Add Product To the Cart",parent=self.root)
       else:
          #====Bill Top========
          self.bill_top()
          #====Bill Mid========
          self.bill_mid()
          #====Bill Bottom=====
          self.bill_bottom()

          self.chk_print=1
    
    def save_bill(self):
         
        try:
           # Save the bill to a text file
          self.save_customer_data()
          with open(f'bill/{str(self.invoice)}.txt', 'w') as fp:
            fp.write(self.txt_bill_area.get('1.0', END))
        
         # Show a message box indicating that the bill has been generated
          messagebox.showinfo('Saved', 'Bill has been generated')
         
         

         # Update product quantities in the database
          connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="company"
         )
          cursor = connection.cursor()

          for item in self.cart_list:
            product_id = item[0]
            sale_quantity = int(item[3])  # Assuming sale quantity is stored at index 3

            cursor.execute("SELECT quantity FROM product WHERE p_id = %s", (product_id,))
            current_quantity = cursor.fetchone()[0]

            cursor.execute("SELECT status FROM product WHERE p_id = %s", (product_id,))
            status = cursor.fetchone()[0]

            print("Current Quantity:", current_quantity)  # Debugging
            updated_quantity = current_quantity - sale_quantity
            print("Updated Quantity:", updated_quantity)  # Debugging

            cursor.execute("UPDATE product SET quantity = %s WHERE p_id = %s", (updated_quantity, product_id))
            print("Quantity updated for Product ID:", product_id)  # Debugging

            if updated_quantity==0:
               cursor.execute("UPDATE product SET status = 'Inactive' WHERE p_id = %s", (product_id,))

            connection.commit()
            print("Transaction committed successfully")  # Debugging
            

            cursor.close()
            connection.close()

             # Clear all data in the GUI
            self.clear_all()
            self.fetch_data()
            
        except Exception as e:
         messagebox.showerror('Error', f'Error occurred: {str(e)}')

    def bill_top(self):
       self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
       bill_top_temp=f'''
\t\tXYZ-Inventory

  Phone No. 9876543210 , Delhi-125001
{str("="*44)}
Customer Name: {self.var_cname.get()}
Ph no.: {self.var_contact.get()}
Bill No. {str(self.invoice)}\t\t\t Date: {str(time.strftime("%d/%m/%Y"))}
{str("="*44)}
 Product Name\t\t\tQTY\tPrice
{str("="*44)}
'''
       self.txt_bill_area.delete('1.0',END)
       self.txt_bill_area.insert('1.0',bill_top_temp)    

    def bill_bottom(self):
       bill_bottom_temp=f'''
{str("="*44)}
Bill Amount\t\t\t\tRs.{self.bill_amnt}
Discount\t\t\t\tRs.{self.discount}
Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*44)}\n
'''
       self.txt_bill_area.insert(END,bill_bottom_temp)

    def bill_mid(self):


         for row in self.cart_list:
          name=row[1]
          qty=row[3]
          price=float(row[2])*int(row[3])
          price=str(price)
          self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+qty+"\tRs."+price)

    def save_customer_data(self):       
        try:
            connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="company")

            cursor = connection.cursor()

            # Retrieve data from Tkinter variables
            name = self.var_cname.get()
            contact = self.var_contact.get()
            
            # Execute SQL INSERT query
            query = "INSERT INTO customers (name,contact) VALUES (%s, %s)"
            values = (name, contact)
            cursor.execute(query, values)

            # Commit the transaction
            connection.commit()

        except Exception as e:
        # Show error message if there's an exception
            messagebox.showerror("Error", f"Error occurred: {str(e)}")
        
    def clear_cart(self):
       self.var_pid.set('')
       self.var_pname.set('')
       self.var_price.set('')
       self.lbl_inStock.config(text=f"In Stock")
       self.var_qty.set('')
       self.var_stock.set('')
    
    def clear_all(self):
       del self.cart_list[:]
       self.var_cname.set('')
       self.var_contact.set('')
       self.clear_cart()
       self.txt_bill_area.delete('1.0',END)
       self.Cart_title.config(text=f"Cart\tTotal Products: [0]")
       for item in self.cart_table.get_children():
        self.cart_table.delete(item)

    def update_date_time(self):
      current_time = time.strftime("%I:%M:%S")
      current_date = time.strftime("%d-%m-%Y")
      self.lbl_clock.config(text=f"Welcome to Dashboard \t\t\t Date: {current_date} \t\t\t Time:{current_time}")

      self.lbl_clock.after(200, self.update_date_time)   

    def print_bill(self):
       if self.chk_print==1:
          messagebox.showinfo('Print',"Please wait while Printing",parent=self.root)
          new_file=tempfile.mktemp('.txt')
          open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
          os.startfile(new_file,'print')
       else:
          messagebox.showerror('Print',"Please generate bill to print the receipt",parent=self.root)    
          
          


if __name__=="__main__":   
 root = Tk()
 obj = Billing(root)
 root.mainloop()