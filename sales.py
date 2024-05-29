from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import os

class sales:
     
     def __init__(self, root):
        self.root = root
        self.root.geometry("1100x550+150+50")
        self.root.title("Sales")
        self.root.config(bg="white")
        self.root.focus_force()
        
        self.bill_list=[]
        self.var_invoice=StringVar()

        title_lbl = Label(self.root, text="View Bill Reports", font=("Times New Roman", 20), background="#009688")
        title_lbl.place(x=50,y=20,width=1000)

        invoice_lbl=Label(self.root,text="Invoice No.",font=("Times New Roman", 15)).place(x=50,y=90)

        invoice_entry=Entry(self.root,textvariable=self.var_invoice,font=("Times New Roman", 15),bg="lightyellow")
        invoice_entry.place(x=170,y=90)
        
        search_btn=Button(self.root,command=self.search,text="Search",font=("Times New Roman", 15),bg="#78281F", fg="white")
        search_btn.place(x=400,y=90,width=100,height=30)

        clear_btn=Button(self.root,command=self.clear,text="Clear",font=("Times New Roman", 15),bg="#78281F", fg="white")
        clear_btn.place(x=520,y=90,width=100,height=30)

        sales_frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_frame.place(x=50,y=140,height=330,width=200)

        scrolly=Scrollbar(sales_frame,orient=VERTICAL)
        self.Sales_List=Listbox(sales_frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)

        bill_frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_frame.place(x=280,y=140,height=330,width=380)

        title_lbl = Label(bill_frame, text="Customer Bill Area", font=("Times New Roman", 20), background="orange")
        title_lbl.pack(side=TOP,fill=X)

        scrolly2=Scrollbar(bill_frame,orient=VERTICAL)
        self.bill_area=Listbox(bill_frame,bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)
        self.Sales_List.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        
        
     
     def show(self):
        del self.bill_list[:]
        self.Sales_List.delete(0,END)
        for i in os.listdir('bill'):
            if i.split('.')[-1]=='txt':
                self.Sales_List.insert(END,i) 
                self.bill_list.append(i.split('.')[1])    
       
     def get_data(self, ev):
         row = self.Sales_List.curselection()
         if row:
          file_name = self.Sales_List.get(row[0])
         print("File name:", file_name)
         self.bill_area.delete('0', END)
         file_path = f'bill/{file_name}'
         print("File path:", file_path)  # Debugging statement
         try:
            with open(file_path, 'r') as fp:
                for line in fp:
                    print("Line:", line)  # Debugging statement
                    self.bill_area.insert(END, line)
         except FileNotFoundError:
            messagebox.showerror("Error", "File not found!")
     
     def search(self):
        if self.var_invoice.get() == "":
         messagebox.showerror("Error", "Invoice No. should be required", parent=self.root)
        else:
         if self.var_invoice.get() in self.bill_list:
            file_name = self.var_invoice.get() + ".txt"  # Assuming your file names are the invoice numbers with '.txt' extension
            file_path = os.path.join("bill", file_name)
            try:
                with open(file_path, 'r') as fp:
                    self.bill_area.delete(0, END)  # Clear the bill_area Listbox
                    for line in fp:
                        self.bill_area.insert(END, line.strip())  # Insert each line from the file into the Listbox
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found!")
         else:
            messagebox.showerror("Error", f"Invoice No. {self.var_invoice.get()} not found", parent=self.root)

     def clear(self):
         self.bill_area.delete('1.0',END)    

if __name__ == "__main__":
    root = Tk()
    obj = sales(root)
    root.mainloop()
