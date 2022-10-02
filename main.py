from tkinter import *
from datetime import date,timedelta
from PIL import Image, ImageTk
from functools import partial
import mysql.connector
con=mysql.connector.connect(host="localhost",user=" ",passwd=" ",database="LibraryManagement")
c=con.cursor()

def empdisplayBooks():
    display2_obj = Toplevel(obj)
    display2_obj.title("List of Books")
    Label(display2_obj, text="List of Books in Library", bg="dark blue", fg="white", width=50, height="2",font=("Calibri", 13)).grid(row=0, columnspan=5)
    c.execute("select * from Books")
    pos_val = 2
    Label(display2_obj, text="Book ID", font=("Calibri", 12, "bold")).grid(row=pos_val, column=0, columnspan=1)
    Label(display2_obj, text="Book Name", font=("Calibri", 12, "bold")).grid(row=pos_val, column=1, columnspan=1)
    Label(display2_obj, text="Author", font=("Calibri", 12, "bold")).grid(row=pos_val, column=2, columnspan=1)
    Label(display2_obj, text="Total", font=("Calibri", 12, "bold")).grid(row=pos_val, column=3, columnspan=1)
    Label(display2_obj, text="Available", font=("Calibri", 12, "bold")).grid(row=pos_val, column=4, columnspan=1)
    for b_id, b_nm, b_au, b_qt, b_qt_r in c:
        pos_val = pos_val + 1
        Label(display2_obj, text=b_id).grid(row=pos_val, column=0, columnspan=1)
        Label(display2_obj, text=b_nm).grid(row=pos_val, column=1, columnspan=1)
        Label(display2_obj, text=b_au).grid(row=pos_val, column=2, columnspan=1)
        Label(display2_obj, text=b_qt).grid(row=pos_val, column=3, columnspan=1)
        Label(display2_obj, text=b_qt_r).grid(row=pos_val, column=4, columnspan=1)

def displayBooks():
    display_obj = Toplevel(obj)
    display_obj.title("List of Books")
    Label(display_obj, text="List of Books in Library", bg="dark blue", fg="white", width=50, height="2",font=("Calibri", 13)).grid(row=0, columnspan=3)
    c.execute("select * from Books")
    pos_val = 2
    Label(display_obj, text="Book ID", font=("Calibri", 12, "bold")).grid(row=pos_val, column=0, columnspan=1)
    Label(display_obj, text="Book Name", font=("Calibri", 12, "bold")).grid(row=pos_val, column=1, columnspan=1)
    Label(display_obj, text="Author", font=("Calibri", 12, "bold")).grid(row=pos_val, column=2, columnspan=1)
    for b_id, b_nm, b_au, b_qt, b_qt_r in c:
        pos_val = pos_val + 1
        if b_qt_r=="0":
            Label(display_obj, text=b_id,fg='red').grid(row=pos_val, column=0, columnspan=1)
            Label(display_obj, text=b_nm,fg='red').grid(row=pos_val, column=1, columnspan=1)
            Label(display_obj, text=b_au,fg='red').grid(row=pos_val, column=2, columnspan=1)
        else:
            Label(display_obj, text=b_id).grid(row=pos_val, column=0, columnspan=1)
            Label(display_obj, text=b_nm).grid(row=pos_val, column=1, columnspan=1)
            Label(display_obj, text=b_au).grid(row=pos_val, column=2, columnspan=1)

    Label(display_obj, text="Red color text represents the book is not available for issue",fg='red').grid(row=(pos_val+1), columnspan=3)

def emplendBook():
    Label(empBook_obj, text=" ", fg="green", font=("calibri", 11)).grid(row=10, columnspan=8)
    lend_book_info=empl_book.get()
    lroll_info=emplroll.get()
    quer1='select * from Books'
    c.execute(quer1)
    count=0
    book_flag=-1
    for b_id,b_nm,b_au,b_qt,b_qt_r in c:
        if(lend_book_info==b_id):
            count=1
            if(int(b_qt_r)>0):
                book_flag=int(b_qt_r)-1
    if(count==1):
        roll_flag=0
        c.execute('select * from rentbook')
        return_day=""
        for b_id, rol_no,iss_day,ret_day in c:
            if rol_no == lroll_info and b_id==lend_book_info:
                roll_flag=1
                return_day=ret_day
        if roll_flag==1:
            msg="Book is already issued! Return until "+str(return_day)
            Label(empBook_obj, text=msg, fg="green", font=("calibri", 11)).grid(row=10, columnspan=8)
            # messagebox.showinfo("Message", "Book is already issued to you")
        else:
            if book_flag!=-1:
                issue_today = date.today()
                ret_day = date.today() + timedelta(days=15)
                c.execute("insert into rentbook(Book_ID,Roll_No,Issue_day,Last_day) values(%s,%s,%s,%s)", (lend_book_info, lroll_info,issue_today,ret_day))
                con.commit()
                c.execute('update Books set Qty_rem=%s where Book_ID=%s',(str(book_flag),lend_book_info))
                con.commit()
                msg2="Book is issued to you! Return it until "+str(ret_day)
                Label(empBook_obj, text=msg2, fg="green", font=("calibri",11)).grid(row=10, columnspan=8)
            else:
                Label(empBook_obj, text="Sorry! The book is not available for issue", fg="green", font=("calibri", 11)).grid(row=10,columnspan=8)
                # messagebox.showinfo("Message", "Sorry! All the books are issued to someone")
    else:
        Label(empBook_obj, text="You entered wrong Book ID", fg="green", font=("calibri", 11)).grid(row=10, columnspan=8)
        # messagebox.showinfo("Message", "You entered wrong Book ID")
    empl_book_entry.delete(0, END)
    emplroll_entry.delete(0, END)
    # lend_obj.after(15000, lend_obj.destroy)

def empreturnBook():
    Label(empBook_obj, text=" ", fg="green", font=("calibri", 11)).grid(row=10, columnspan=8)
    return_book_info = empl_book.get()
    rroll_info = emplroll.get()
    c.execute("select * from rentbook")
    count=0
    fine=0
    for x,y,a,b in c:
        if(x==return_book_info and y==rroll_info):
            count=1
            ret_date = date.today()
            if ret_date>b:
                fine=((ret_date-b).days)*5
    if(count==1):
        c.execute("delete from rentbook where Book_ID=%s and Roll_No=%s", (return_book_info, rroll_info,))
        con.commit()
        c.execute("select * from student where stu_roll=%s",(rroll_info,))
        for p,q,r,s in c:
            fine=str(fine+int(s))
        c.execute("update student set fine=%s where stu_roll=%s",(fine,rroll_info))
        c.execute('select * from Books where Book_ID=%s',(return_book_info,))
        book_flag=0
        for p,q,r,s,t in c:
            book_flag=int(t)+1
        c.execute('update Books set Qty_rem=%s where Book_ID=%s', (str(book_flag), return_book_info))
        con.commit()
        Label(empBook_obj, text="The Book is returned", fg="green", font=("calibri",11)).grid(row=10, columnspan=8)
    else:
        Label(empBook_obj, text="The Book is not issued to you", fg="green", font=("calibri", 11)).grid(row=10, columnspan=8)
    empl_book_entry.delete(0, END)
    emplroll_entry.delete(0, END)
    # return_obj.after(15000, return_obj.destroy)

def emplendreturnBook():
    global empBook_obj
    empBook_obj = Toplevel(obj)
    empBook_obj.title("Lend/Return a Book")
    Label(empBook_obj, text="Enter the following details", bg="dark blue",fg="white", width=50, height="2", font=("Calibri", 13)).grid(row=0,columnspan=8)
    global empl_book
    global emplroll
    global empl_book_entry
    global emplroll_entry
    empl_book=StringVar()
    emplroll=StringVar()
    Label(empBook_obj, text="").grid(row=1, columnspan=8)
    Label(empBook_obj, text="Book's ID").grid(row=2,columnspan=8)
    empl_book_entry=Entry(empBook_obj, textvariable=empl_book)
    empl_book_entry.grid(row=3,columnspan=8)
    Label(empBook_obj, text="").grid(row=4, columnspan=8)
    Label(empBook_obj, text="Your Roll No.").grid(row=5, columnspan=8)
    emplroll_entry=Entry(empBook_obj, textvariable=emplroll)
    emplroll_entry.grid(row=6, columnspan=8)
    Label(empBook_obj, text="").grid(row=7, columnspan=8)
    Label(empBook_obj, text="").grid(row=8,column=0, columnspan=3)
    Button(empBook_obj, text="Issue", width=8, height=1, bg="dark blue",fg="white",  command=emplendBook).grid(row=8,column=3, columnspan=1)
    Button(empBook_obj, text="Return", width=8, height=1, bg="dark blue", fg="white", command=empreturnBook).grid(row=8, column=4, columnspan=1)
    Label(empBook_obj, text="").grid(row=8, column=5, columnspan=3)
    Label(empBook_obj, text="").grid(row=9, columnspan=8)

def addBook2():
    Label(add_obj, text=" ", fg="green", font=("calibri", 11)).grid(row=13, columnspan=4)
    # add_book_id_info = add_book_id.get()
    add_book_name_info = add_book_name.get()
    add_author_info = add_author.get()
    add_book_qty_info = add_book_qty.get()
    c.execute("select * from Books")
    count=0
    book_qty=""
    book_rem=""
    books_count=1
    max=0
    book_id=""
    for b_id,b_nm,b_au,b_qty,b_rem in c:
        if (add_book_name_info==b_nm and add_author_info==b_au):
            count=1
            book_qty=str(int(b_qty)+add_book_qty_info)
            book_rem=str(int(b_rem)+add_book_qty_info)
            book_id=b_id

        # books_count=books_count+1
        if int(b_id)>max:
            books_count=int(b_id)+1
            max=int(b_id)

    if count==1:
        c.execute("update Books set Qty=%s,Qty_rem=%s where Book_ID=%s",(book_qty,book_rem,book_id))
        con.commit()
        Label(add_obj, text="The Quantity of books is updated", fg="green", font=("calibri", 11)).grid(row=13, columnspan=4)
    else:
        if books_count<=9:
            book_id_up="000"+str(books_count)
        elif books_count>=10 and books_count<=99:
            book_id_up="00"+str(books_count)
        elif books_count>=100 and books_count<=999:
            book_id_up="0"+str(books_count)
        elif books_count>999:
            book_id_up=str(books_count)
        c.execute("insert into Books values(%s,%s,%s,%s,%s)", (book_id_up,add_book_name_info,add_author_info,add_book_qty_info,add_book_qty_info))
        con.commit()
        Label(add_obj, text="The Book is added", fg="green", font=("calibri",11)).grid(row=13, columnspan=4)
    # add_book_id_entry.delete(0, END)
    add_book_name_entry.delete(0, END)
    add_author_entry.delete(0, END)
    add_book_qty_entry.delete(0, END)
    # add_obj.after(15000, add_obj.destroy)

def addBook():
    global add_obj
    add_obj = Toplevel(obj)
    add_obj.title("Add a Book")
    Label(add_obj, text="Enter the following details", bg="dark blue",fg="white", width=50, height="2", font=("Calibri", 13)).grid(row=0,columnspan=4)
    global add_book_name
    global add_book_name_entry
    global add_author
    global add_author_entry
    global add_book_qty
    global add_book_qty_entry
    add_book_name= StringVar()
    add_author = StringVar()
    add_book_qty = IntVar()
    Label(add_obj, text="").grid(row=1, columnspan=4)
    Label(add_obj, text="Book's Name").grid(row=2, columnspan=4)
    add_book_name_entry = Entry(add_obj, textvariable=add_book_name)
    add_book_name_entry.grid(row=3, columnspan=4)
    Label(add_obj, text="").grid(row=4, columnspan=4)
    Label(add_obj, text="Author's Name").grid(row=5, columnspan=4)
    add_author_entry = Entry(add_obj, textvariable=add_author)
    add_author_entry.grid(row=6, columnspan=4)
    Label(add_obj, text="").grid(row=7, columnspan=4)
    Label(add_obj, text="Quantity of Book").grid(row=8, columnspan=4)
    add_book_qty_entry = Entry(add_obj, textvariable=add_book_qty)
    add_book_qty_entry.grid(row=9, columnspan=4)
    Label(add_obj, text="").grid(row=10, columnspan=4)
    Button(add_obj, text="Add a Book", width=15, height=1, bg="dark blue",fg="white",  command=addBook2).grid(row=11, columnspan=4)
    Label(add_obj, text="").grid(row=12, columnspan=4)

def deleteBook2():
    Label(delete_obj, text=" ", fg="green", font=("calibri", 11)).grid(row=10, columnspan=4)
    delete_book_id_info=delete_book_id.get()
    delete_book_qty_info = delete_book_qty.get()
    c.execute('select * from Books')
    count=0
    book_qty=""
    book_rem=""
    book_id=""
    for b_id,b_nm,b_au,b_qt,b_rem in c:
        if delete_book_id_info==b_id:
            count=1
            book_qty=b_qt
            book_rem=b_rem
            book_id=b_id
    if count==1:
        if delete_book_qty_info>int(book_qty):
            Label(delete_obj, text="These many books are not available in Library", fg="green", font=("calibri", 11)).grid(row=10,columnspan=4)
        elif delete_book_qty_info==int(book_qty):
            if delete_book_qty_info==int(book_rem):
                c.execute("delete from Books where Book_ID=(%s)", (delete_book_id_info,))
                con.commit()
                Label(delete_obj, text="The Book is no more in the library", fg="green", font=("calibri", 11)).grid(row=10,columnspan=4)
            elif delete_book_qty_info>int(book_rem):
                Label(delete_obj, text="Few Books are still issued", fg="green", font=("calibri", 11)).grid(row=10, columnspan=4)
        elif delete_book_qty_info<int(book_qty):
            if delete_book_qty_info<=int(book_rem):
                up_qty=str(int(book_qty)-delete_book_qty_info)
                up_qty_rem=str(int(book_rem)-delete_book_qty_info)
                c.execute("update Books set Qty=%s, Qty_rem=%s where Book_ID=%s", (up_qty,up_qty_rem,book_id))
                con.commit()
                Label(delete_obj, text="The quantity of book is reduced", fg="green", font=("calibri", 11)).grid(row=10, columnspan=4)
            elif delete_book_qty_info>int(book_rem):
                Label(delete_obj, text="Few Books are still issued", fg="green", font=("calibri", 11)).grid(row=10, columnspan=4)
    else:
        Label(delete_obj, text="You entered wrong Book ID", fg="green", font=("calibri", 11)).grid(row=10, columnspan=4)
    delete_book_id_entry.delete(0, END)
    delete_book_qty_entry.delete(0, END)
    # delete_obj.after(15000, delete_obj.destroy)

def deleteBook():
    global delete_obj
    delete_obj= Toplevel(obj)
    delete_obj.title("Delete the Books")
    Label(delete_obj, text="Enter the following details", bg="dark blue",fg="white", width=50, height="2", font=("Calibri", 13)).grid(row=0,columnspan=4)
    global delete_book_id
    global delete_book_id_entry
    global delete_book_qty
    global delete_book_qty_entry
    delete_book_id = StringVar()
    delete_book_qty = IntVar()
    Label(delete_obj, text="").grid(row=1, columnspan=4)
    Label(delete_obj, text="Book's ID").grid(row=2,columnspan=4)
    delete_book_id_entry = Entry(delete_obj, textvariable=delete_book_id)
    delete_book_id_entry.grid(row=3,columnspan=4)
    Label(delete_obj, text="").grid(row=4, columnspan=4)
    Label(delete_obj, text="Quantity of Book").grid(row=5, columnspan=4)
    delete_book_qty_entry = Entry(delete_obj, textvariable=delete_book_qty)
    delete_book_qty_entry.grid(row=6, columnspan=4)
    Label(delete_obj, text="").grid(row=7, columnspan=4)
    Button(delete_obj, text="Delete the books", width=15, height=1, bg="dark blue",fg="white",  command=deleteBook2).grid(row=8, columnspan=4)
    Label(delete_obj, text="").grid(row=9, columnspan=4)

def finepaid2():
    Label(fine_obj, text=" ", fg="green", font=("calibri", 11)).grid(row=12, columnspan=4)
    stu_roll_info=stu_roll.get()
    fine_amt_info = fine_amt.get()
    c.execute('select * from student')
    count=0
    fine_left=""
    for sid,snm,spswd,sfine in c:
        if stu_roll_info==sid:
            count=1
            fine_left=str(int(sfine)-fine_amt_info)
    if count==1:
        c.execute('update student set fine=%s where stu_roll=%s',(fine_left,stu_roll_info))
        con.commit()
        msg="Fine amount left is Rs."+fine_left
        Label(fine_obj, text=msg, fg="green", font=("calibri", 11)).grid(row=12,columnspan=4)
    else:
        Label(fine_obj, text="Entered wrong student roll no.", fg="green", font=("calibri", 11)).grid(row=12, columnspan=4)
    stu_roll_entry.delete(0, END)
    fine_amt_entry.delete(0, END)
    # delete_obj.after(15000, delete_obj.destroy)

def displayfine():
    Label(fine_obj,text=" ",fg="green", font=("calibri", 11)).grid(row=12, columnspan=4)
    stu_roll_info=stu_roll.get()
    c.execute('select * from student')
    dispfine=""
    name=""
    count=0
    for sid,snm,sp,sfine in c:
        if sid==stu_roll_info:
            count=1
            dispfine=sfine
            name=snm
    if count==1:
        msg="The fine for "+name+" is Rs. "+dispfine
        Label(fine_obj, text=msg,fg='green').grid(row=12, columnspan=4)
    else:
        Label(fine_obj, text="Entered wrong student roll no.", fg='green').grid(row=12, columnspan=4)

def finepaid():
    global fine_obj
    fine_obj = Toplevel(obj)
    fine_obj.title("Fine Payment")
    Label(fine_obj, text="Enter the following details", bg="dark blue", fg="white", width=50, height="2",font=("Calibri", 13)).grid(row=0, columnspan=4)
    global stu_roll
    global stu_roll_entry
    global fine_amt
    global fine_amt_entry
    stu_roll = StringVar()
    fine_amt = IntVar()
    Label(fine_obj, text="").grid(row=1, columnspan=4)
    Label(fine_obj, text="Student's Roll No.").grid(row=2, columnspan=4)
    stu_roll_entry = Entry(fine_obj, textvariable=stu_roll)
    stu_roll_entry.grid(row=3, columnspan=4)
    Label(fine_obj, text="").grid(row=4, columnspan=4)
    Button(fine_obj, text="Search", width=15, height=1, bg="dark blue", fg="white", command=displayfine).grid(row=5,columnspan=4)
    Label(fine_obj, text="").grid(row=6, columnspan=4)
    Label(fine_obj, text="Amount Received").grid(row=7, columnspan=4)
    fine_amt_entry = Entry(fine_obj, textvariable=fine_amt)
    fine_amt_entry.grid(row=8, columnspan=4)
    Label(fine_obj, text="").grid(row=9, columnspan=4)
    Button(fine_obj, text="Update", width=15, height=1, bg="dark blue", fg="white",command=finepaid2).grid(row=10, columnspan=4)
    Label(fine_obj, text="").grid(row=11, columnspan=4)

def empportal():
    eportal_obj = Toplevel(obj)
    eportal_obj.title("Employee Dashboard")
    render = ImageTk.PhotoImage(Image.open("book.jpg"))
    img = Label(eportal_obj,image=render)
    img.image = render
    img.place(x=0, y=0)
    Label(eportal_obj, text="Employee Dashboard", bg="dark blue", fg="white", width=50, height="2", font=("Calibri", 13)).pack()
    Button(eportal_obj,text="Display all Books", bg="light blue", fg="blue", height="2", width="20", command=empdisplayBooks).pack(pady=10)
    Button(eportal_obj,text="Lend/Return a Book", bg="light blue", fg="blue", height="2", width="20", command=emplendreturnBook).pack(pady=10)
    Button(eportal_obj,text="Fine Payment", bg="light blue", fg="blue", height="2", width="20", command=finepaid).pack(pady=10)
    Button(eportal_obj, text="Add a Book", bg="light blue", fg="blue", height="2", width="20", command=addBook).pack(pady=10)
    Button(eportal_obj, text="Delete a Book", bg="light blue", fg="blue", height="2", width="20",command=deleteBook).pack(pady=10)

def empregister2():
    Label(emp_obj2, text=" ",fg="green", font=("calibri", 11)).grid(row=10, columnspan=8)
    employ_id_info = employ_id.get()
    employ_pswd_info = employ_pswd.get()
    employ_nm_info=employ_nm.get()
    c.execute("select * from employee")
    count = 0
    for eid, enm, eps in c:
        if (eid == employ_id_info):
            count = 1
    if count == 1:
        Label(emp_obj2, text="Already Registerd", fg="green", font=("calibri", 11)).grid(row=13, columnspan=8)
    else:
        c.execute("insert into employee values(%s,%s,%s)",(employ_id_info,employ_nm_info,employ_pswd_info))
        con.commit()
        emp_obj2.after(1, emp_obj2.destroy)
        empportal()
    employ_id_entry.delete(0, END)
    employ_pswd_entry.delete(0, END)
    employ_nm_entry.delete(0, END)

def empregister():
    emp_obj.after(1, emp_obj.destroy)
    global emp_obj2
    emp_obj2 = Toplevel(obj)
    emp_obj2.title("Employee Registration")
    Label(emp_obj2, text="Employee Registration", bg="dark blue", fg="white", width=50, height="2", font=("Calibri", 13)).grid(row=0, columnspan=8)
    global employ_id
    global employ_pswd
    global employ_nm
    global employ_id_entry
    global employ_pswd_entry
    global employ_nm_entry
    employ_id = StringVar()
    employ_pswd = StringVar()
    employ_nm = StringVar()
    Label(emp_obj2, text="").grid(row=1, columnspan=8)
    Label(emp_obj2, text="Employee ID").grid(row=2, columnspan=8)
    employ_id_entry = Entry(emp_obj2, textvariable=employ_id)
    employ_id_entry.grid(row=3, columnspan=8)
    Label(emp_obj2, text="").grid(row=4, columnspan=8)
    Label(emp_obj2, text="Name").grid(row=5, columnspan=8)
    employ_nm_entry = Entry(emp_obj2, textvariable=employ_nm)
    employ_nm_entry.grid(row=6, columnspan=8)
    Label(emp_obj2, text="").grid(row=7, columnspan=8)
    Label(emp_obj2, text="Password").grid(row=8, columnspan=8)
    employ_pswd_entry = Entry(emp_obj2, textvariable=employ_pswd,show="*")
    employ_pswd_entry.grid(row=9, columnspan=8)
    Label(emp_obj2, text="").grid(row=10, columnspan=8)
    Button(emp_obj2, text="Register", width=8, height=1, bg="dark blue", fg="white", command=empregister2).grid(row=11,columnspan=8)
    Label(emp_obj2, text="").grid(row=12, columnspan=8)

def emplogin():
    Label(emp_obj, text=" ", fg="green", font=("calibri", 11)).grid(row=10, columnspan=8)
    eid_info=e_id.get()
    epswd_info=e_pswd.get()
    c.execute("select * from employee")
    count=0
    for eid,enm,eps in c:
        if(eid==eid_info and eps==epswd_info):
            count=1
    if count==1:
        emp_obj.after(1, emp_obj.destroy)
        empportal()
    else:
        Label(emp_obj,text="Wrong ID or Password",fg="green", font=("calibri", 11)).grid(row=10, columnspan=8)
    e_id_entry.delete(0, END)
    e_pswd_entry.delete(0, END)

def employee():
    global emp_obj
    emp_obj = Toplevel(obj)
    emp_obj.title("Employee Login")
    Label(emp_obj, text="Employee Login", bg="dark blue", fg="white", width=50, height="2",font=("Calibri", 13)).grid(row=0, columnspan=8)
    global e_id
    global e_pswd
    global e_id_entry
    global e_pswd_entry
    e_id = StringVar()
    e_pswd = StringVar()
    Label(emp_obj, text="").grid(row=1, columnspan=8)
    Label(emp_obj, text="Employee ID").grid(row=2, columnspan=8)
    e_id_entry = Entry(emp_obj, textvariable=e_id)
    e_id_entry.grid(row=3, columnspan=8)
    Label(emp_obj, text="").grid(row=4, columnspan=8)
    Label(emp_obj, text="Password").grid(row=5, columnspan=8)
    e_pswd_entry = Entry(emp_obj, textvariable=e_pswd,show="*")
    e_pswd_entry.grid(row=6, columnspan=8)
    Label(emp_obj, text="").grid(row=7, columnspan=8)
    Label(emp_obj, text="").grid(row=8,column=0, columnspan=3)
    Button(emp_obj, text="Login", width=8, height=1, bg="dark blue", fg="white",command=emplogin).grid(row=8,column=3,columnspan=1)
    Button(emp_obj, text="Register", width=8, height=1, bg="dark blue", fg="white", command=empregister).grid(row=8,column=4,columnspan=1)
    Label(emp_obj, text="").grid(row=8, column=5, columnspan=3)
    Label(emp_obj, text="").grid(row=9, columnspan=8)

def stulendBook(lroll_info):
    Label(stuBook_obj, text=" ", fg="green", font=("calibri", 11)).grid(row=7, columnspan=8)
    lend_book_info=stubookid.get()
    quer1='select * from Books'
    c.execute(quer1)
    count=0
    book_flag=-1
    for b_id,b_nm,b_au,b_qt,b_qt_r in c:
        if(lend_book_info==b_id):
            count=1
            if(int(b_qt_r)>0):
                book_flag=int(b_qt_r)-1
    if(count==1):
        roll_flag=0
        c.execute('select * from rentbook')
        return_day=""
        for b_id, rol_no,iss_day,ret_day in c:
            if rol_no == lroll_info and b_id==lend_book_info:
                roll_flag=1
                return_day=ret_day
        if roll_flag==1:
            msg="Book is already issued! Return until "+str(return_day)
            Label(stuBook_obj, text=msg, fg="green", font=("calibri", 11)).grid(row=7, columnspan=8)
            # messagebox.showinfo("Message", "Book is already issued to you")
        else:
            if book_flag!=-1:
                issue_today = date.today()
                ret_day = date.today() + timedelta(days=15)
                c.execute("insert into rentbook(Book_ID,Roll_No,Issue_day,Last_day) values(%s,%s,%s,%s)", (lend_book_info, lroll_info,issue_today,ret_day))
                con.commit()
                c.execute('update Books set Qty_rem=%s where Book_ID=%s',(str(book_flag),lend_book_info))
                con.commit()
                msg2="Book is issued to you! Return it until "+str(ret_day)
                Label(stuBook_obj, text=msg2, fg="green", font=("calibri",11)).grid(row=7, columnspan=8)
            else:
                Label(stuBook_obj, text="Sorry! The book is not available for issue", fg="green", font=("calibri", 11)).grid(row=7,columnspan=8)
                # messagebox.showinfo("Message", "Sorry! All the books are issued to someone")
    else:
        Label(stuBook_obj, text="You entered wrong Book ID", fg="green", font=("calibri", 11)).grid(row=7, columnspan=8)
        # messagebox.showinfo("Message", "You entered wrong Book ID")
    stubookid_entry.delete(0, END)
    # lend_obj.after(15000, lend_obj.destroy)

def stureturnBook(rroll_info):
    Label(stuBook_obj, text=" ", fg="green", font=("calibri", 11)).grid(row=7, columnspan=8)
    return_book_info = stubookid.get()
    c.execute("select * from rentbook")
    count=0
    fine=0
    for x,y,a,b in c:
        if(x==return_book_info and y==rroll_info):
            count=1
            ret_date = date.today()
            if ret_date>b:
                fine=((ret_date-b).days)*5
    if(count==1):
        c.execute("delete from rentbook where Book_ID=%s and Roll_No=%s", (return_book_info, rroll_info,))
        con.commit()
        c.execute("select * from student where stu_roll=%s",(rroll_info,))
        for p,q,r,s in c:
            fine=str(fine+int(s))
        c.execute("update student set fine=%s where stu_roll=%s",(fine,rroll_info))
        c.execute('select * from Books where Book_ID=%s',(return_book_info,))
        book_flag=0
        for p,q,r,s,t in c:
            book_flag=int(t)+1
        c.execute('update Books set Qty_rem=%s where Book_ID=%s', (str(book_flag), return_book_info))
        con.commit()
        Label(stuBook_obj, text="The Book is returned", fg="green", font=("calibri",11)).grid(row=7, columnspan=8)
    else:
        Label(stuBook_obj, text="The Book is not issued to you", fg="green", font=("calibri", 11)).grid(row=7, columnspan=8)
    stubookid_entry.delete(0, END)
    # return_obj.after(15000, return_obj.destroy)

def stulendreturnBook(student_id):
    global stuBook_obj
    stuBook_obj = Toplevel(obj)
    stuBook_obj.title("Lend/Return a Book")
    Label(stuBook_obj, text="Lend/Return a Book", bg="dark blue",fg="white", width=50, height="2", font=("Calibri", 13)).grid(row=0,columnspan=8)
    global stubookid
    global stubookid_entry
    stubookid=StringVar()
    Label(stuBook_obj, text="").grid(row=1, columnspan=8)
    Label(stuBook_obj, text="Book's ID").grid(row=2,columnspan=8)
    stubookid_entry=Entry(stuBook_obj, textvariable=stubookid)
    stubookid_entry.grid(row=3,columnspan=8)
    Label(stuBook_obj, text="").grid(row=4, columnspan=8)
    Label(stuBook_obj, text="").grid(row=5,column=0, columnspan=3)
    Button(stuBook_obj, text="Issue", width=8, height=1, bg="dark blue",fg="white",  command=partial(stulendBook,student_id)).grid(row=5,column=3, columnspan=1)
    Button(stuBook_obj, text="Return", width=8, height=1, bg="dark blue", fg="white", command=partial(stureturnBook,student_id)).grid(row=5, column=4, columnspan=1)
    Label(stuBook_obj, text="").grid(row=5, column=5, columnspan=3)
    Label(stuBook_obj, text="").grid(row=6, columnspan=8)

def issueBooks(st_id_info):
    issue_obj = Toplevel(obj)
    issue_obj.title("Student Dashboard")
    Label(issue_obj, text="Issued Books", bg="dark blue", fg="white", width=50, height="2",font=("Calibri", 13)).grid(row=0, columnspan=5)
    c.execute("select * from rentbook")
    lst=[]
    lst2=[]
    lst3=[]
    for bid,sid,iday,rday in c:
        if(sid==st_id_info):
            lst.append(bid)
            lst2.append(iday)
            lst3.append(rday)
    pos_val = 1
    Label(issue_obj, text="Book ID", font=("Calibri", 12, "bold")).grid(row=pos_val, column=0, columnspan=1)
    Label(issue_obj, text="Book Name", font=("Calibri", 12, "bold")).grid(row=pos_val, column=1, columnspan=1)
    Label(issue_obj, text="Author", font=("Calibri", 12, "bold")).grid(row=pos_val, column=2, columnspan=1)
    Label(issue_obj, text="Issue Day", font=("Calibri", 12, "bold")).grid(row=pos_val, column=3,columnspan=1)
    Label(issue_obj, text="Return Day", font=("Calibri", 12, "bold")).grid(row=pos_val, column=4, columnspan=1)
    c.execute("select * from books")
    for book_id,bnm,aut,qty,qtyr in c:
        for x,y in enumerate(lst):
            if(y==book_id):
                pos_val = pos_val + 1
                Label(issue_obj, text=book_id).grid(row=pos_val, column=0, columnspan=1)
                Label(issue_obj, text=bnm).grid(row=pos_val, column=1, columnspan=1)
                Label(issue_obj, text=aut).grid(row=pos_val, column=2, columnspan=1)
                Label(issue_obj, text=lst2[x]).grid(row=pos_val, column=3, columnspan=1)
                Label(issue_obj, text=lst3[x]).grid(row=pos_val, column=4, columnspan=1)
    c.execute('select * from student')
    for stu_id,stnm,stps,stfine in c:
        if stu_id==st_id_info:
            var1="Your total fine is Rs."+stfine
            Label(issue_obj, text=var1,fg="red").grid(row=(pos_val+1),columnspan=5)

def stuportal(student_id):
    sportal_obj = Toplevel(obj)
    sportal_obj.title("Student Dashboard")
    render = ImageTk.PhotoImage(Image.open("book.jpg"))
    img = Label(sportal_obj,image=render)
    img.image = render
    img.place(x=0, y=0)
    Label(sportal_obj, text="Student Dashboard", bg="dark blue", fg="white", width=50, height="2", font=("Calibri", 13)).pack()
    Button(sportal_obj,text="Display all Books", bg="light blue", fg="blue", height="3", width="18", command=displayBooks).pack(pady=23)
    Button(sportal_obj,text="Lend/Return a Book", bg="light blue", fg="blue", height="3", width="18", command=partial(stulendreturnBook,student_id)).pack(pady=23)
    Button(sportal_obj,text="Issued Books", bg="light blue", fg="blue", height="3", width="18", command=partial(issueBooks,student_id)).pack(pady=23)

def sturegister2():
    Label(stu_obj2, text=" ",fg="green", font=("calibri", 11)).grid(row=10, columnspan=8)
    st_id_info = st_id.get()
    st_pswd_info = st_pswd.get()
    st_nm_info=st_nm.get()
    st_fine="0"
    c.execute("select * from student")
    count = 0
    for sid, snm, sps, sfine in c:
        if (sid == st_id_info):
            count = 1
    if count == 1:
        Label(stu_obj2, text="Already Registerd", fg="green", font=("calibri", 11)).grid(row=13, columnspan=8)
    else:
        c.execute("insert into student values(%s,%s,%s,%s)",(st_id_info,st_nm_info,st_pswd_info,st_fine))
        con.commit()
        stu_obj2.after(1, stu_obj2.destroy)
        stuportal(st_id_info)
    st_id_entry.delete(0, END)
    st_pswd_entry.delete(0, END)
    st_nm_entry.delete(0, END)

def sturegister():
    stu_obj.after(1, stu_obj.destroy)
    global stu_obj2
    stu_obj2 = Toplevel(obj)
    stu_obj2.title("Student Registration")
    Label(stu_obj2, text="Student Registration", bg="dark blue", fg="white", width=50, height="2",font=("Calibri", 13)).grid(row=0, columnspan=8)
    global st_id
    global st_pswd
    global st_nm
    global st_id_entry
    global st_pswd_entry
    global st_nm_entry
    st_id = StringVar()
    st_pswd = StringVar()
    st_nm = StringVar()
    Label(stu_obj2, text="").grid(row=1, columnspan=8)
    Label(stu_obj2, text="Roll No.").grid(row=2, columnspan=8)
    st_id_entry = Entry(stu_obj2, textvariable=st_id)
    st_id_entry.grid(row=3, columnspan=8)
    Label(stu_obj2, text="").grid(row=4, columnspan=8)
    Label(stu_obj2, text="Name").grid(row=5, columnspan=8)
    st_nm_entry = Entry(stu_obj2, textvariable=st_nm)
    st_nm_entry.grid(row=6, columnspan=8)
    Label(stu_obj2, text="").grid(row=7, columnspan=8)
    Label(stu_obj2, text="Password").grid(row=8, columnspan=8)
    st_pswd_entry = Entry(stu_obj2, textvariable=st_pswd, show="*")
    st_pswd_entry.grid(row=9, columnspan=8)
    Label(stu_obj2, text="").grid(row=10, columnspan=8)
    Button(stu_obj2, text="Register", width=8, height=1, bg="dark blue", fg="white", command=sturegister2).grid(row=11,columnspan=8)
    Label(stu_obj2, text="").grid(row=12, columnspan=8)

def stulogin():
    Label(stu_obj, text=" ", fg="green", font=("calibri", 11)).grid(row=10, columnspan=8)
    stu_id_info=stuid.get()
    stu_pswd_info=stu_pswd.get()
    c.execute("select * from student")
    count=0
    for stu_id,stu_nm,stu_ps,stu_fine in c:
        if(stu_id==stu_id_info and stu_ps==stu_pswd_info):
            count=1
    if count==1:
        stu_obj.after(1, stu_obj.destroy)
        stuportal(stu_id_info)
    else:
        Label(stu_obj,text="Wrong ID or Password",fg="green", font=("calibri", 11)).grid(row=10, columnspan=8)
    stu_id_entry.delete(0, END)
    stu_pswd_entry.delete(0, END)

def student():
    global stu_obj
    stu_obj = Toplevel(obj)
    stu_obj.title("Student Login")
    Label(stu_obj, text="Student Login", bg="dark blue", fg="white", width=50, height="2",font=("Calibri", 13)).grid(row=0, columnspan=8)
    global stuid
    global stu_pswd
    global stu_id_entry
    global stu_pswd_entry
    stuid = StringVar()
    stu_pswd = StringVar()
    Label(stu_obj, text="").grid(row=1, columnspan=8)
    Label(stu_obj, text="Student Roll No.").grid(row=2, columnspan=8)
    stu_id_entry = Entry(stu_obj, textvariable=stuid)
    stu_id_entry.grid(row=3, columnspan=8)
    Label(stu_obj, text="").grid(row=4, columnspan=8)
    Label(stu_obj, text="Password").grid(row=5, columnspan=8)
    stu_pswd_entry = Entry(stu_obj, textvariable=stu_pswd,show="*")
    stu_pswd_entry.grid(row=6, columnspan=8)
    Label(stu_obj, text="").grid(row=7, columnspan=8)
    Label(stu_obj, text="").grid(row=8,column=0, columnspan=3)
    Button(stu_obj, text="Login", width=8, height=1, bg="dark blue", fg="white",command=stulogin).grid(row=8,column=3,columnspan=1)
    Button(stu_obj, text="Register", width=8, height=1, bg="dark blue", fg="white", command=sturegister).grid(row=8,column=4,columnspan=1)
    Label(stu_obj, text="").grid(row=8, column=5, columnspan=3)
    Label(stu_obj, text="").grid(row=9, columnspan=8)

def main_screen():
    global obj
    obj=Tk()
    obj.title("Welcome to Library")
    render = ImageTk.PhotoImage(Image.open("book.jpg"))
    img = Label(image=render)
    img.image = render
    img.place(x=0,y=0)
    Label(text="Select Your Choice", bg="dark blue",fg="white", width=50, height="2", font=("Calibri", 13)).pack()
    Button(text="Display Books", bg="light blue",fg="blue", height="3", width="18", command=displayBooks).pack(pady=23)
    Button(text="Employee", bg="light blue",fg="blue", height="3", width="18", command=employee).pack(pady=23)
    Button(text="Student", bg="light blue",fg="blue", height="3", width="18", command=student).pack(pady=23)
    obj.mainloop()

main_screen()
