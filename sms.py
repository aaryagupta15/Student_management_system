from tkinter import *
import time
import pymysql
from tkinter import messagebox, ttk, filedialog
import ttkthemes
import pandas

#######################################################################################################################

# Phone Number limit function
def limit_length(event):
    current_text = phoneEntry.get()
    if len(current_text) > 10:
        phoneEntry.delete(10, END)

# Repeated Window Code:
def window_data(title,button_text,command):
    global idEntry, nameEntry, phoneEntry,emailEntry,addressEntry,genderEntry,dobEntry,screen
    screen = Toplevel()
    screen.grab_set()
    screen.title(title)
    screen.resizable(False,False)

    idLabel = Label(screen, text='Id', font = ('times new roman', 20, 'bold'))
    idLabel.grid(row=0,column = 0, padx=30, pady=15, sticky = W)
    idEntry = Entry(screen, font = ('times new roman', 15, 'bold'), bd = 2, width=24)
    idEntry.grid(row=0, column = 1, padx=10,pady=15)

    nameLabel = Label(screen, text='Name', font = ('times new roman', 20, 'bold'))
    nameLabel.grid(row=1,column = 0, padx=30, pady=15, sticky = W)
    nameEntry = Entry(screen, font = ('times new roman', 15, 'bold'), bd = 2, width=24)
    nameEntry.grid(row=1, column = 1, padx=10,pady=15)

    phoneLabel = Label(screen, text='Phone', font = ('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2,column = 0, padx=30, pady=15, sticky = W)
    phoneEntry = Entry(screen, font = ('times new roman', 15, 'bold'), bd = 2, width=24)
    phoneEntry.grid(row=2, column = 1, padx=10,pady=15)

    if title=='Add Student' or 'Update Student' or 'Search Student':
        phoneEntry.bind("<KeyRelease>",limit_length)

    emailLabel = Label(screen, text='Email', font = ('times new roman', 20, 'bold'))
    emailLabel.grid(row=3,column = 0, padx=30, pady=15, sticky = W)
    emailEntry = Entry(screen, font = ('times new roman', 15, 'bold'), bd = 2, width=24)
    emailEntry.grid(row=3, column = 1, padx=10,pady=15)

    addressLabel = Label(screen, text='Address', font = ('times new roman', 20, 'bold'))
    addressLabel.grid(row=4,column = 0, padx=30, pady=15, sticky = W)
    addressEntry = Entry(screen, font = ('times new roman', 15, 'bold'), bd = 2, width=24)
    addressEntry.grid(row=4, column = 1, padx=10,pady=15)

    genderLabel = Label(screen, text='Gender', font = ('times new roman', 20, 'bold'))
    genderLabel.grid(row=5,column = 0, padx=30, pady=15, sticky = W)
    genderEntry = Entry(screen, font = ('times new roman', 15, 'bold'), bd = 2, width=24)
    genderEntry.grid(row=5, column = 1, padx=10,pady=15)

    dobLabel = Label(screen, text='D.O.B', font = ('times new roman', 20, 'bold'))
    dobLabel.grid(row=6,column = 0, padx=30, pady=15, sticky = W)
    dobEntry = Entry(screen, font = ('times new roman', 15, 'bold'), bd = 2, width=24)
    dobEntry.grid(row=6, column = 1, padx=10,pady=15)

    studentButton = ttk.Button(screen, text=button_text, command=command)
    studentButton.grid(row=7, columnspan=2)

    if title=='Update Student':
        indexing=studentTable.focus()
        content=studentTable.item(indexing)
        list_data = content['values']
        idEntry.insert(0,list_data[0])
        nameEntry.insert(0,list_data[1])
        phoneEntry.insert(0,list_data[2])
        emailEntry.insert(0,list_data[3])
        addressEntry.insert(0,list_data[4])
        genderEntry.insert(0,list_data[5])
        dobEntry.insert(0,list_data[6])

# Exit Function:
def exit_window():
    ans = messagebox.askyesno('Confirm','Do you want to exit?')
    if ans:
        root.destroy()
    else:
        pass

# Export Function:
def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studentTable.get_children()
    new_list = []
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        new_list.append(datalist)
    table = pandas.DataFrame(new_list, columns=['Id','Name','Mobile','Email','Address','Gender','D.O.B','Added Date','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','The data is exported succesfully.')

# Clock Function
def clock():
    day = time.strftime('%d/%m/%Y')
    timing = time.strftime('%H:%M:%S')
    print(day,timing)
    datetimelabel.config(text = f'Date: {day} | Time: {timing}')
    datetimelabel.after(1000, clock)

# Update Function
def update_data():
    day = time.strftime('%d/%m/%Y')
    timing = time.strftime('%H:%M:%S')
    query = 'update student set name=%s,mobile=%s,mail=%s,address=%s,gender=%s,dob=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query,(nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get(),day,timing,idEntry.get()))
    con.commit()
    messagebox.showinfo('Success',f'The id {idEntry.get()} is successfully updated.', parent=screen)
    screen.destroy()
    show_data()

# Show Function
def show_data():
    query='select * from student'
    mycursor.execute(query)
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('',END,values=data)

# Delete Function
def delete_data():
    indexing=studentTable.focus()
    print(indexing)
    content=studentTable.item(indexing)
    content_id = content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Deleted',f'The id {content_id} is successfully deleted.')
    query='select * from student'
    mycursor.execute(query)
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('',END,values=data)

# Search Function
def search_data():
    query='select * from student where Id=%s or Name=%s or mobile=%s or mail=%s or Address=%s or Gender=%s or dob=%s'
    mycursor.execute(query,(idEntry.get(),nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('',END,values=data)


# Add Function
def add_data():
    if nameEntry.get()=='' or idEntry.get()=='' or emailEntry.get()=='' or addressEntry.get()=='' or phoneEntry.get()=='' or genderEntry.get()=='' or dobEntry.get()=='':
        messagebox.showerror('Error','All fields are required', parent=screen)
    else:
        day = time.strftime('%d/%m/%Y')
        timing = time.strftime('%H:%M:%S')
        try:
            query = 'INSERT into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(),nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get(),day,timing))
            con.commit()
            result = messagebox.askyesno('Confirm','Data added successfully. Do you want to clean the form?', parent=screen)
            if result:
                idEntry.delete(0,END)
                nameEntry.delete(0,END)
                phoneEntry.delete(0,END)
                emailEntry.delete(0,END)
                addressEntry.delete(0,END)
                genderEntry.delete(0,END)
                dobEntry.delete(0,END)
            else:
                pass
        except:
            messagebox.showerror('Error','ID already exists', parent=screen)
            return
        
    query = 'SELECT * FROM student'
    mycursor.execute(query)
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        datalist = list(data)
        studentTable.insert('', END,values=datalist)

# Database Connection
def connect_database():
        # Connect the database
        def connect():
            global mycursor
            global con
            try:
                con = pymysql.connect(host=hostEntry.get(), user=usernameEntry.get(),password=passwordEntry.get())
                mycursor = con.cursor()
            except:
                 messagebox.showerror('Error','Invalid Details' ,parent = connectwindow)
                 return
            try:
                query = 'create database studentmanagementsystem'
                mycursor.execute(query)
                query = 'use studentmanagementsystem'
                mycursor.execute(query)
                query = 'CREATE TABLE IF NOT EXISTS student(id INT NOT NULL PRIMARY KEY, name VARCHAR(30), mobile VARCHAR(10), mail VARCHAR(30), address VARCHAR(108), gender VARCHAR(20), dob VARCHAR(20), date VARCHAR(58), time VARCHAR(50))'
                mycursor.execute(query) 
            except:
                 query = 'use studentmanagementsystem'
                 mycursor.execute(query)

            messagebox.showinfo('Success', 'Connection is successfull',parent = connectwindow)
            connectwindow.destroy()
            addButton.config(state=NORMAL)
            searchbutton.config(state=NORMAL)
            deleteButton.config(state=NORMAL)
            updateButton.config(state=NORMAL)
            showButton.config(state=NORMAL)
            exportButton.config(state=NORMAL)
            exitButton.config(state=NORMAL)

        # Hostname, Username, Password            
        connectwindow = Toplevel()
        connectwindow.grab_set()
        connectwindow.geometry('550x250+0+0')
        connectwindow.title('Database connection')
        connectwindow.resizable(False,False)

        hostnameLabel = Label(connectwindow, text = 'Host Name', font = ('times new roman', 20, 'bold'), fg = 'brown')
        hostnameLabel.grid(row = 0, column = 0, padx = 20)
        hostEntry = Entry(connectwindow,font = ('times new roman', 15, 'bold'), bd = 2)
        hostEntry.grid(row = 0, column = 1, padx = 40, pady = 20)

        usernameLabel = Label(connectwindow, text = 'Username', font = ('times new roman', 20, 'bold'), fg = 'brown')
        usernameLabel.grid(row = 1, column = 0, padx = 20)
        usernameEntry = Entry(connectwindow,font = ('times new roman', 15, 'bold'), bd = 2)
        usernameEntry.grid(row = 1, column = 1, padx = 40, pady = 20)

        passwordLabel = Label(connectwindow, text = 'Password', font = ('times new roman', 20, 'bold'), fg = 'brown')
        passwordLabel.grid(row = 2, column = 0, padx = 20)
        passwordEntry = Entry(connectwindow,font = ('times new roman', 15, 'bold'), bd = 2)
        passwordEntry.grid(row = 2, column = 1, padx = 40, pady = 20)

        connectButton = ttk.Button(connectwindow, text = 'Connect the database', command=connect)
        connectButton.grid(row = 3, column = 1)

# Student Management System Slider
count = 0
text = ''
def slider():
    global text
    global count
    if count==len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderlabel.config(text = text)
    count = count + 1
    sliderlabel.after(300, slider)

#######################################################################################################################

root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1174x680+0+0')
root.title('Student Management System')

datetimelabel = Label(root, text='hello', font = ('times new roman' ,18, 'bold'), fg = 'brown')
datetimelabel.place(x=5,y=5)
clock()

s = 'Student Management System'
sliderlabel = Label(root,text = s ,font = ('times new roman', 20, 'bold'), fg = 'brown', width = 20)
sliderlabel.place(x=450, y=0) 
slider()

connectButton = ttk.Button(root, text = 'Connect Database', command = connect_database)
connectButton.place(x=1000, y=10)

# Left Frame
leftFrame = Frame(root)
leftFrame.place(x=50, y=50,width = 300, height = 600)

addButton = ttk.Button(leftFrame, text = 'Add Student' ,width = 25, state=DISABLED, command= lambda:window_data('Add Student','Add', add_data))
addButton.grid(row = 1, column = 0, pady = 20)
searchbutton = ttk.Button(leftFrame, text = 'Search Student',width = 25, state = DISABLED, command=lambda:window_data('Search Student','Search', search_data))
searchbutton.grid(row = 2, column = 0, pady = 20)
deleteButton = ttk.Button(leftFrame, text = 'Delete Student',width = 25, state = DISABLED, command=delete_data)
deleteButton.grid(row = 3, column = 0, pady = 20)
updateButton = ttk.Button(leftFrame, text = 'Update Student',width = 25, state = DISABLED,command=lambda:window_data('Update Student', 'Update',update_data))
updateButton.grid(row = 4, column = 0, pady = 20)
showButton = ttk.Button(leftFrame, text = 'Show Student',width = 25, state = DISABLED, command=show_data)
showButton.grid(row = 5, column = 0, pady = 20)
exportButton = ttk.Button(leftFrame, text = 'Export Data',width = 25, state = DISABLED, command=export_data)
exportButton.grid(row = 6, column = 0, pady = 20)
exitButton = ttk.Button(leftFrame, text = 'Exit',width = 25, command=exit_window)
exitButton.grid(row = 7, column = 0, pady = 20)

# Right Frame
rightFrame = Frame(root)
rightFrame.place(x=300, y=50,width = 950, height = 600)

scrollBarX=Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame,columns=('Id', 'Name', 'Mobile No', 'Email', 'Address', "Gender", 'D.O.B', 'Added Date', 'Added Time')
                                      ,xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command = studentTable.xview)
scrollBarY.config(command = studentTable.yview)
scrollBarX.pack(side=BOTTOM, fill = X)
scrollBarY.pack(side=RIGHT, fill = Y)
studentTable.pack(fill = BOTH, expand=1)

studentTable.column("#0", width=0, stretch=NO)

studentTable.heading('Id', text='Id')
studentTable.heading('Name', text='Name')
studentTable.heading('Mobile No', text='Mobile No')
studentTable.heading('Email', text='Email')
studentTable.heading('Address', text='Address')
studentTable.heading('Gender', text='Gender')
studentTable.heading('D.O.B', text='D.O.B')
studentTable.heading('Added Date', text='Added Date')
studentTable.heading('Added Time', text='Added Time')

# Customizing the Tree View or Student Table
studentTable.column('Id',width=100,anchor=CENTER)
studentTable.column('Name',width=300,anchor=CENTER)
studentTable.column('Mobile No',width=300,anchor=CENTER)
studentTable.column('Email',width=200,anchor=CENTER)
studentTable.column('Address',width=300,anchor=CENTER)
studentTable.column('Gender',width=100,anchor=CENTER)
studentTable.column('D.O.B',width=100,anchor=CENTER)
studentTable.column('Added Date',width=200,anchor=CENTER)
studentTable.column('Added Time',width=200,anchor=CENTER)

style = ttk.Style()
style.configure('Treeview',rowheight=22,font=('times new roman',12),foreground='black')
style.configure('Treeview.Heading',font=('times new roman',15,'bold'))

root.mainloop()
