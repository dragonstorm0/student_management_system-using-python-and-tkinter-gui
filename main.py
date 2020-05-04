from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from dbinfo import *
from datetime import datetime
import re
create_table()
create_table_2()

win=Tk()
win.state('zoomed')
win.configure(bg='powder blue')
win.title('Ducat')
win.iconbitmap('favicon.ico')
win.resizable(width=False,height=False)
txtFrame=StringVar()   #declaring global variable txtFrame
txtFrame1=StringVar() #declaring global variable txtFrame1
txtFrame2=StringVar()   #declaring global variable txtFrame2
txtFrame3=StringVar() #declaring global variable txtFrame3


lbl_title=Label(win,text='Ducat Student Management System',font=('',40,'bold'),bg='powder blue',fg='red')
lbl_title.pack()

photo=PhotoImage(file="image.png")
label= Label(win, image=photo)
label.pack()

def due_amt_db(frm,e):
    sid=int(e.get())
    con=getcon()
    cur=con.cursor()
    cur.execute("select course_fee,stu_amt from students where stu_id=?",(sid,))
    row=cur.fetchone()
    if(row==None):
        messagebox.showwarning("balance","Student does not exist on this id")
    else:   
        messagebox.showinfo("Balance",f"Due Amount : {row[0]-row[1]}")
        MsgBox =messagebox.askyesno("deposit fee","click here to deposit your fees.")
        if(MsgBox==True):
            depositscreen(frm)
    con.close()

def add_course_db(e1,e2):
    c_name=e1.get()
    if not re.match("^[A-Za-z +]+$",c_name):
        #here the name is cheaked for only charcters that is A-Z and a-z.
        #if any value other tha these are present error window will respond.
        messagebox.showwarning('ADD COURSE','coursee Name must contain only charcters and "+".')
        return
    try:
        c_fees=int(e2.get())
    except ValueError:
        messagebox.showwarning('ADD COURSE','fees must be a numeric value.')
    con=getcon()
    cur=con.cursor()
    cur.execute("insert into courses values(?,?)",(c_name,c_fees))
    con.commit()
    messagebox.showinfo('ADD COURSE',f'Course added Successfully With name : {c_name} ')
    e1.delete(0,END)
    e2.delete(0,END)

def deposit_fee_db(e1,e2):
    sid=int(e1.get())
    amt=int(e2.get())
    con=getcon()
    cur=con.cursor()
    cur.execute("select course_fee,stu_amt from students where stu_id=?",(sid,))
    row=cur.fetchone()
    if(row==None):
        messagebox.showwarning("Fee Deposit",'Student does not exist on this id')
    else:
        if(row[1]<row[0]):
            if(row[0]>=(amt+row[1])):
                cur.execute("update students set stu_amt=stu_amt+? where stu_id=?",(amt,sid))
                messagebox.showinfo("Fee Deposit",'Fee Deposited')
                con.commit()
            else:
                messagebox.showinfo("Fee Deposit",'Deposited amount is not valid')
        else:
            messagebox.showwarning("Fee Deposit",'Already fullpaid')
    con.close()
def update_stu_db(e1,e2,e3,e4,e5,e6):
    sid=e1.get()
    name=e2.get()
    mob=e3.get()
    email=e4.get()
    course=e5.get()
    fee=e6.get()
    con=getcon()
    cur=con.cursor()
    cur.execute("""update students set stu_name=?, stu_mob=?, stu_email=?, stu_course=?,course_fee=? where stu_id=?""",(name,mob,email,course,fee,sid))
    con.commit()
    con.close()
    messagebox.showinfo("Update Student","Student Record Updated...")
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    e4.delete(0,END)
    txtFrame2.set('')
    txtFrame3.set('')
    e1.focus()

def search_stu_db(frm,e):
    sid=int(e.get())
    con=getcon()
    cur=con.cursor()
    cur.execute("select stu_id,stu_name,stu_mob,stu_course,course_fee from students where stu_id=?",(sid,))
    row=cur.fetchone()
    if(row==None):
        messagebox.showwarning("Student Search","Student Id does not exit")
    else:
        details=f"Id : {str(row[0])}\n\nName : {row[1]}\n\nMobile : {row[2]}\n\nCourse : {row[3]}\n\nCourse fee : {row[4]}"
        messagebox.showinfo("Student Search",details)
        option=messagebox.askyesno("Update Student", message="Do you want to update student?")
        if(option==True):
            updatescreen(frm,sid)
            
def reg_db(e1,e2,e3,e4,e5,e6):
    name=e1.get()
    if not re.match("^[A-Za-z ]+$",name):
        #here the name is cheaked for only charcters that is A-Z and a-z.
        #if any value other tha these are present error window will respond.
        messagebox.showwarning('Student Reg','Name must contain only charcters.')
        return
    mob=(e2.get())
    str_mob=str(mob)
    if not re.match("^[0-9]+$",mob):
        #cheaking the input for only numeric value.
        messagebox.showwarning('Student Reg','contact number must be numeric.')
        return
    if not re.match("^[6-9]",str_mob[0]):
        #cheaking that the start of number must be 6 or 7 or 8 or 9.
        messagebox.showwarning('Student Reg','invalid start for a mobile number.')
        return
    if(len(mob)!=10):
        #making sure that number is of ten digits.
        messagebox.showwarning('Student Reg','contact number must be of 10 charcter.')
        return
    email=e3.get()
    if not re.match("^\w+@\w+.\w+$",email):
        #here \w will cheak for any alphanumeric value then a @ sign then again any alphanumeric value then . and again any alphanumeric value.
        messagebox.showwarning('Student Reg','invalid email.')
        return
    course=str(e4.get())
    fee=int(e5.get())
    try:
        amt=int(e6.get())
    except ValueError:
        messagebox.showwarning('Student Reg','ammount must be a numeric value')
        
    if(amt>fee):
        messagebox.showwarning('Student Reg','amount must be equal or less than course fee')
        return
    dt=datetime.now().date()
    sid=getnextid()
    con=getcon()
    cur=con.cursor()
    cur.execute("insert into students values(?,?,?,?,?,?,?,?)",(sid,name,course,mob,email,dt,fee,amt))
    con.commit()
    messagebox.showinfo('Student Reg',f'Student Registered Successfully With Id:{sid} ')
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    e4.current(0)
    e6.delete(0,END)
    txtFrame.set('')
    e1.focus()
    
def reset_home_screen(e1,e2):
    e1.delete(0,END)
    e2.delete(0,END)
    e1.focus()

def reset_reg_screen(e1,e2,e3,e4,e5,e6):
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    e4.current(0)
    e6.delete(0,END)
    txtFrame.set('')
    e1.focus()

def logout(frm):
    frm.destroy()
    homescreen()

def login(frm,e1,e2):
    u=e1.get()
    p=e2.get()
    if(len(u)==0 or len(p)==0):
        messagebox.showwarning('Warning','Username or Password can not be empty ')
    else:
        if(u=='admin' and p=='admin'):
            messagebox.showinfo('Success','Welcome,Admin')
            frm.destroy()
            welcomescreen()
        else:
            messagebox.showerror('Error','Invalid Username or Password')



def back(frm):
    frm.destroy()
    welcomescreen()

def registerscreen(wfrm):
    wfrm.destroy()
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=170,relwidth=1,relheight=1)

    lbl_welcome=Label(frm,text='Welcome:Admin',font=('',20,'bold'),bg='pink')
    lbl_welcome.place(x=10,y=10)

    btn_logout=Button(frm,command=lambda:logout(frm),text='logout',font=('',15,'bold'),bd=5,width=8)
    btn_logout.place(relx=.9,y=10)

    btn_back=Button(frm,command=lambda:back(frm),text='back',font=('',15,'bold'),bd=5,width=8)
    btn_back.place(x=10,y=50)

    con=getcon()
    cur=con.cursor()
    cur.execute("select course_name,course_fees from courses") #invoking database for course name.
    row=cur.fetchall()
    con.close()

    lbl_name=Label(frm,text='Student Name:',font=('',20,'bold'),bg='pink')
    lbl_name.place(relx=.3,rely=.1)
    entry_name=Entry(frm,font=('',15,'bold'),bd=5)
    entry_name.place(relx=.47,rely=.1)
    entry_name.focus()

    lbl_mob=Label(frm,text='Student Mob:',font=('',20,'bold'),bg='pink')
    lbl_mob.place(relx=.3,rely=.2)
    entry_mob=Entry(frm,font=('',15,'bold'),bd=5)
    entry_mob.place(relx=.47,rely=.2)

    lbl_email=Label(frm,text='Student Email:',font=('',20,'bold'),bg='pink')
    lbl_email.place(relx=.3,rely=.3)
    entry_email=Entry(frm,font=('',15,'bold'),bd=5)
    entry_email.place(relx=.47,rely=.3)

    lbl_course=Label(frm,text='Course Name:',font=('',20,'bold'),bg='pink')
    lbl_course.place(relx=.3,rely=.4)
    entry_course=ttk.Combobox(frm, textvariable=txtFrame1,state="readonly",font=('',14,'bold'))
    entry_course['values']=(
                                    '',
                                    "Python", 
                                    "Python+Django",
                                    "Python+ML",
                                    "Python+ML+AI")
    entry_course.place(relx=.47,rely=.4)
    entry_course.current(0)
    entry_course.bind("<<ComboboxSelected>>", driver_combo)
    #using binding method to use autochange property on fee
    lenght=len(row)
    for count in range(lenght):
        entry_course['values']=entry_course['values']+(row[count][0],) #adding course names directly from database.

    lbl_fee=Label(frm,text='Course Fee:',font=('',20,'bold'),bg='pink')
    lbl_fee.place(relx=.3,rely=.5)
    entry_fee=Entry(frm, textvariable=txtFrame,state="readonly",font=('',15,'bold'),bd=5)
    entry_fee.place(relx=.47,rely=.5)
    


    lbl_amt=Label(frm,text='Amount:',font=('',20,'bold'),bg='pink')
    lbl_amt.place(relx=.3,rely=.6)
    entry_amt=Entry(frm,font=('',15,'bold'),bd=5)
    entry_amt.place(relx=.47,rely=.6)
    
    btn_reg=Button(frm,text='Register',command=lambda:reg_db(entry_name,entry_mob,entry_email,entry_course,entry_fee,entry_amt),font=('',15,'bold'),bd=5,width=8)
    btn_reg.place(relx=.4,rely=.7)

    btn_reset=Button(frm,text='reset',command=lambda:reset_reg_screen(entry_name,entry_mob,entry_email,entry_course,entry_fee,entry_amt),font=('',15,'bold'),bd=5,width=8)
    btn_reset.place(relx=.55,rely=.7)

    return entry_fee

def driver_combo(event):

    con=getcon()
    cur=con.cursor()
    cur.execute("select course_name,course_fees from courses")  #invoking database for fess related substances.
    row=cur.fetchall()
    con.close()
    lenght=len(row)
    #calling binding metood from reg_screen>entry_course combobox
    #print('new element selected')
    #print whenever a diffrent course is selected
    vmet=txtFrame1.get()
    #getting course details by using global string variable txtFrame1.
    if(vmet==''):
        txtFrame.set('')
    elif(vmet=="Python"):
        txtFrame.set('10000')            #setting course fee using global string variable txtFrame according to course Python.
    elif(vmet=="Python+Django"):
        txtFrame.set('15000')           #setting course fee using global string variable txtFrame according to course Python+Django.
    elif(vmet=="Python+ML"):
        txtFrame.set('18000')           #setting course fee using global string variable txtFrame according to course Python+ML.
    elif(vmet=="Python+ML+AI"):
        txtFrame.set('23000')           #setting course fee using global string variable txtFrame according to course Python+ML+AI.

    for count in range(lenght):
        if(vmet==row[count][0]):
            txtFrame.set(row[count][1])  #adding the fees collected from the database.

    

def updatescreen(wfrm,sid):
    wfrm.destroy()
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=170,relwidth=1,relheight=1)

    lbl_welcome=Label(frm,text='Welcome:Admin',font=('',20,'bold'),bg='pink')
    lbl_welcome.place(x=10,y=10)

    btn_logout=Button(frm,command=lambda:logout(frm),text='logout',font=('',15,'bold'),bd=5,width=8)
    btn_logout.place(relx=.9,y=10)

    btn_back=Button(frm,command=lambda:back(frm),text='back',font=('',15,'bold'),bd=5,width=8)
    btn_back.place(x=10,y=50)

    con2=getcon()
    cur2=con2.cursor()
    cur2.execute("select course_name,course_fees from courses") #invoking database for course name.
    row2=cur2.fetchall()
    con2.close()

    con=getcon()
    cur=con.cursor()
    cur.execute("select stu_id,stu_name,stu_course,stu_mob,stu_email,course_fee,stu_amt from students where stu_id=?",(sid,))
    row=cur.fetchone()
    con.close()

    lbl_name=Label(frm,text='Student Name:',font=('',20,'bold'),bg='pink')
    lbl_name.place(relx=.3,rely=.05)
    entry_name=Entry(frm,font=('',15,'bold'),bd=5)
    entry_name.place(relx=.47,rely=.05)
    entry_name.insert(0,row[1])
    entry_name.focus()

    lbl_mob=Label(frm,text='Student Mob:',font=('',20,'bold'),bg='pink')
    lbl_mob.place(relx=.3,rely=.15)
    entry_mob=Entry(frm,font=('',15,'bold'),bd=5)
    entry_mob.place(relx=.47,rely=.15)
    entry_mob.insert(0,row[3])

    lbl_email=Label(frm,text='Student Email:',font=('',20,'bold'),bg='pink')
    lbl_email.place(relx=.3,rely=.25)
    entry_email=Entry(frm,font=('',15,'bold'),bd=5)
    entry_email.place(relx=.47,rely=.25)
    entry_email.insert(0,row[4])
    
    lbl_course=Label(frm,text='Course Name:',font=('',20,'bold'),bg='pink')
    lbl_course.place(relx=.3,rely=.35)
    entry_course=ttk.Combobox(frm,textvariable=txtFrame3,state="readonly",font=('',14,'bold'))
    entry_course['values']=(
                                    f'{row[2]}',
                                    "Python", 
                                    "Python+Django",
                                    "Python+ML",
                                    "Python+ML+AI")
    entry_course.place(relx=.47,rely=.35)
    entry_course.current(0)
    entry_course.bind("<<ComboboxSelected>>", driver_combo2)
    #using binding method to use autochange property on fee
    lenght=len(row2)
    for count in range(lenght):
        entry_course['values']=entry_course['values']+(row2[count][0],) #adding course names directly from database.


    lbl_fee=Label(frm,text='Course Fee:',font=('',20,'bold'),bg='pink')
    lbl_fee.place(relx=.3,rely=.45)
    entry_fee=Entry(frm, textvariable=txtFrame2,state="readonly",font=('',15,'bold'),bd=5)
    entry_fee.place(relx=.47,rely=.45)
    entry_fee.insert(0,row[5])
    
    lbl_id=Label(frm,text='Student Id:',font=('',20,'bold'),bg='pink')
    lbl_id.place(relx=.3,rely=.55)
    entry_id=Entry(frm,font=('',15,'bold'),bd=5)
    entry_id.place(relx=.47,rely=.55)
    entry_id.insert(0,sid)
    entry_id.config(state='readonly')

    lbl_amt=Label(frm,text='Amount Deposited:',font=('',20,'bold'),bg='pink')
    lbl_amt.place(relx=.3,rely=.65)
    entry_amt=Entry(frm,font=('',15,'bold'),bd=5)
    entry_amt.place(relx=.47,rely=.65)
    entry_amt.insert(0,row[6])
    entry_amt.config(state='readonly')

    btn_update=Button(frm,text='Update',command=lambda:update_stu_db(entry_id,entry_name,entry_mob,entry_email,entry_course,entry_fee),font=('',15,'bold'),bd=5,width=8)
    btn_update.place(relx=.4,rely=.73)

    btn_reset=Button(frm,text='reset',command=lambda:reset_stu_change(entry_id,entry_name,entry_mob,entry_email,entry_course,entry_fee),font=('',15,'bold'),bd=5,width=8)
    btn_reset.place(relx=.55,rely=.73)

def reset_stu_change(e1,e2,e3,e4,e5,e6):
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    e4.delete(0,END)
    txtFrame2.set('')
    txtFrame3.set('')
    e1.focus()


def driver_combo2(event):
    con=getcon()
    cur=con.cursor()
    cur.execute("select course_name,course_fees from courses")  #invoking database for fess related substances.
    row=cur.fetchall()
    con.close()
    lenght=len(row)
    #calling binding metood from reg_screen>entry_course combobox
    #print('new element selected')
    #print whenever a diffrent course is selected
    vmet=txtFrame3.get()
    #getting course details by using global string variable txtFrame1.
    if(vmet==''):
        txtFrame2.set('')
    elif(vmet=="Python"):
        txtFrame2.set('10000')            #setting course fee using global string variable txtFrame according to course Python.
    elif(vmet=="Python+Django"):
        txtFrame2.set('15000')           #setting course fee using global string variable txtFrame according to course Python+Django.
    elif(vmet=="Python+ML"):
        txtFrame2.set('18000')           #setting course fee using global string variable txtFrame according to course Python+ML.
    elif(vmet=="Python+ML+AI"):
        txtFrame2.set('23000')           #setting course fee using global string variable txtFrame according to course Python+ML+AI.

    for count in range(lenght):
        if(vmet==row[count][0]):
            txtFrame2.set(row[count][1])  #adding the fees collected from the database.

def reset_search_stu(e1):
    e1.delete(0,END)
    
def searchscreen(wfrm):
    wfrm.destroy()
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=170,relwidth=1,relheight=1)

    lbl_welcome=Label(frm,text='Welcome:Admin',font=('',20,'bold'),bg='pink')
    lbl_welcome.place(x=10,y=10)

    btn_logout=Button(frm,command=lambda:logout(frm),text='logout',font=('',15,'bold'),bd=5,width=8)
    btn_logout.place(relx=.9,y=10)

    btn_back=Button(frm,command=lambda:back(frm),text='back',font=('',15,'bold'),bd=5,width=8)
    btn_back.place(x=10,y=50)

    lbl_name=Label(frm,text='Student Id:',font=('',20,'bold'),bg='pink')
    lbl_name.place(relx=.3,rely=.1)
    entry_name=Entry(frm,font=('',15,'bold'),bd=5)
    entry_name.place(relx=.47,rely=.1)
    entry_name.focus()

    
    btn_reg=Button(frm,text='Search',command=lambda:search_stu_db(frm,entry_name),font=('',15,'bold'),bd=5,width=8)
    btn_reg.place(relx=.4,rely=.2)

    btn_reset=Button(frm,text='reset',command=lambda:reset_search_stu(entry_name),font=('',15,'bold'),bd=5,width=8)
    btn_reset.place(relx=.55,rely=.2)

def reset_deposit_fee(e1,e2):
    e1.delete(0,END)
    e2.delete(0,END)

def depositscreen(wfrm):
    wfrm.destroy()
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=170,relwidth=1,relheight=1)

    lbl_welcome=Label(frm,text='Welcome:Admin',font=('',20,'bold'),bg='pink')
    lbl_welcome.place(x=10,y=10)

    btn_logout=Button(frm,command=lambda:logout(frm),text='logout',font=('',15,'bold'),bd=5,width=8)
    btn_logout.place(relx=.9,y=10)

    btn_back=Button(frm,command=lambda:back(frm),text='back',font=('',15,'bold'),bd=5,width=8)
    btn_back.place(x=10,y=50)

    lbl_name=Label(frm,text='Student Id:',font=('',20,'bold'),bg='pink')
    lbl_name.place(relx=.3,rely=.1)
    entry_sid=Entry(frm,font=('',15,'bold'),bd=5)
    entry_sid.place(relx=.47,rely=.1)
    entry_sid.focus()

    lbl_amt=Label(frm,text='Amount:',font=('',20,'bold'),bg='pink')
    lbl_amt.place(relx=.3,rely=.2)
    entry_amt=Entry(frm,font=('',15,'bold'),bd=5)
    entry_amt.place(relx=.47,rely=.2)
    entry_amt.focus()
    
    btn_reg=Button(frm,text='Deposit',command=lambda:deposit_fee_db(entry_sid,entry_amt),font=('',15,'bold'),bd=5,width=8)
    btn_reg.place(relx=.4,rely=.3)

    btn_reset=Button(frm,text='reset',command=lambda:reset_deposit_fee(entry_sid,entry_amt),font=('',15,'bold'),bd=5,width=8)
    btn_reset.place(relx=.55,rely=.3)


def reset_due_amt(e1):
    e1.delete(0,END)

def dueamountscreen(wfrm):
    wfrm.destroy()
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=170,relwidth=1,relheight=1)

    lbl_welcome=Label(frm,text='Welcome:Admin',font=('',20,'bold'),bg='pink')
    lbl_welcome.place(x=10,y=10)

    btn_logout=Button(frm,command=lambda:logout(frm),text='logout',font=('',15,'bold'),bd=5,width=8)
    btn_logout.place(relx=.9,y=10)

    btn_back=Button(frm,command=lambda:back(frm),text='back',font=('',15,'bold'),bd=5,width=8)
    btn_back.place(x=10,y=50)

    lbl_name=Label(frm,text='Student Id:',font=('',20,'bold'),bg='pink')
    lbl_name.place(relx=.3,rely=.1)
    entry_sid=Entry(frm,font=('',15,'bold'),bd=5)
    entry_sid.place(relx=.47,rely=.1)
    entry_sid.focus()
        
    btn_reg=Button(frm,text='Submit',command=lambda:due_amt_db(frm,entry_sid),font=('',15,'bold'),bd=5,width=8)
    btn_reg.place(relx=.4,rely=.2)

    btn_reset=Button(frm,text='reset',command=lambda:reset_due_amt(entry_sid),font=('',15,'bold'),bd=5,width=8)
    btn_reset.place(relx=.55,rely=.2)

def reset_course_db(e1,e2):
    e1.delete(0,END)
    e2.delete(0,END)
    
def addcourse(wfrm):
    wfrm.destroy()
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=170,relwidth=1,relheight=1)

    lbl_welcome=Label(frm,text='Welcome:Admin',font=('',20,'bold'),bg='pink')
    lbl_welcome.place(x=10,y=10)

    btn_logout=Button(frm,command=lambda:logout(frm),text='logout',font=('',15,'bold'),bd=5,width=8)
    btn_logout.place(relx=.9,y=10)

    btn_back=Button(frm,command=lambda:back(frm),text='back',font=('',15,'bold'),bd=5,width=8)
    btn_back.place(x=10,y=50)

    lbl_name=Label(frm,text='Course Name:',font=('',20,'bold'),bg='pink')
    lbl_name.place(relx=.3,rely=.1)
    entry_cname=Entry(frm,font=('',15,'bold'),bd=5)
    entry_cname.place(relx=.47,rely=.1)
    entry_cname.focus()

    lbl_amt=Label(frm,text='Course Fee:',font=('',20,'bold'),bg='pink')
    lbl_amt.place(relx=.3,rely=.2)
    entry_cfees=Entry(frm,font=('',15,'bold'),bd=5)
    entry_cfees.place(relx=.47,rely=.2)
    entry_cfees.focus()
    
    btn_reg=Button(frm,text='Add',command=lambda:add_course_db(entry_cname,entry_cfees),font=('',15,'bold'),bd=5,width=8)
    btn_reg.place(relx=.4,rely=.3)

    btn_reset=Button(frm,text='reset',command=lambda:reset_course_db(entry_cname,entry_cfees),font=('',15,'bold'),bd=5,width=8)
    btn_reset.place(relx=.55,rely=.3)




def welcomescreen():
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=170,relwidth=1,relheight=1)

    lbl_welcome=Label(frm,text='Welcome:Admin',font=('',20,'bold'),bg='pink')
    lbl_welcome.place(x=10,y=10)

    btn_logout=Button(frm,command=lambda:logout(frm),text='logout',font=('',15,'bold'),bd=5,width=8)
    btn_logout.place(relx=.9,y=10)

    btn_reg=Button(frm,text='Register New Student',command=lambda:registerscreen(frm),font=('',15,'bold'),bd=5,width=18)
    btn_reg.place(relx=.4,y=70)

    btn_search=Button(frm,text='Search Student',command=lambda:searchscreen(frm),font=('',15,'bold'),bd=5,width=18)
    btn_search.place(relx=.4,y=170)


    btn_bal=Button(frm,text='Due Amount',command=lambda:dueamountscreen(frm),font=('',15,'bold'),bd=5,width=18)
    btn_bal.place(relx=.4,y=270)

    btn_bal=Button(frm,text='Add course',command=lambda:addcourse(frm),font=('',15,'bold'),bd=5,width=18)
    btn_bal.place(relx=.4,y=370)

def homescreen():
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=170,relwidth=1,relheight=1)

    lbl_user=Label(frm,text='Username:',font=('',20,'bold'),bg='pink')
    lbl_user.place(x=500,y=100)

    lbl_pass=Label(frm,text='Password:',font=('',20,'bold'),bg='pink')
    lbl_pass.place(x=500,y=150)

    entry_user=Entry(frm,font=('',15,'bold'))
    entry_user.place(x=680,y=100)
    entry_user.focus()

    entry_pass=Entry(frm,font=('',15,'bold'),show='*')
    entry_pass.place(x=680,y=150)
    
    btn_login=Button(frm,command=lambda:login(frm,entry_user,entry_pass),text='login',font=('',15,'bold'),bd=5,width=8)
    btn_login.place(x=600,y=220)

    btn_reset=Button(frm,command=lambda:reset_home_screen(entry_user,entry_pass),text='reset',font=('',15,'bold'),bd=5,width=8)
    btn_reset.place(x=780,y=220)

    lbl_pass=Label(frm,text='Aayush kumar mishra',font=('',20,'bold'),bg='pink', fg='red')
    lbl_pass.place(x=1230,y=600)
homescreen()
win.mainloop() 
