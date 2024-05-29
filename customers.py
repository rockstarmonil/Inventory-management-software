from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector


class Customers:
        
    def __init__(self, root):
        self.root = root
        self.root.geometry("450x400+150+50")
        self.root.title("Customer Details")
        self.root.config(bg="grey")
        self.root.focus_force()
    
        
if __name__=="__main__":   
 root = Tk()
 obj = Customers(root)
 root.mainloop()
