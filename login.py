from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

def login():
    if usernameEntry.get()=='' or passwordEntry.get()=='':
        messagebox.showerror('Error','Fields cannot be empty')
    elif usernameEntry.get()=='XYZ' and passwordEntry.get()=='0000':
        messagebox.showinfo('Login Succesfully', 'Welcome to the dashboard')
        window.destroy()
        import sms
    else:
        messagebox.showerror('Error', 'Please enter correct credentials')

window = Tk()
window.geometry('1280x700+0+0') 
window.title('Login Page') 
window.resizable(False,False)

backgroundImage = ImageTk.PhotoImage(file = 'bg.jpg')
bg_label = Label(window, image= backgroundImage)
bg_label.place(x=0,y=0)

login_frame = Frame(window, bg = 'white')
login_frame.place(x=400, y=150)

logo_img = PhotoImage(file='logo.png')
logo_label = Label(login_frame,image = logo_img)
logo_label.grid(row=0,column=0, columnspan=2, pady = 10)

user_img = PhotoImage(file='user.png')
usernameLabel = Label(login_frame, image =user_img, text = 'Username',
                      compound = LEFT, font = ('times new roman',20,'bold'), bg = 'white')
usernameLabel.grid(row = 1, column = 0, pady = 10, padx = 20)
usernameEntry = Entry(login_frame, font = ('times new roman',20,'bold'), bd = 5, fg = 'blue')
usernameEntry.grid(row = 1, column = 1, pady = 10, padx = 20)

password_img = PhotoImage(file='password.png')
passwordLabel = Label(login_frame, image =password_img, text = 'Password',
                      compound = LEFT, font = ('times new roman',20,'bold'), bg = 'white')
passwordLabel.grid(row = 2, column = 0, pady = 10, padx = 20)
passwordEntry = Entry(login_frame, font = ('times new roman',20,'bold'), bd = 5, fg = 'blue')
passwordEntry.grid(row = 2, column = 1, pady = 10, padx = 20)


loginButton = Button(login_frame, text = 'Login', font = ('times new roman',15,'bold'), bd = 5, fg = 'white',
                      bg = 'cornflowerblue', width = 15, activebackground='cornflowerblue', activeforeground='white',
                      cursor = 'hand2', command = login)
loginButton.grid(row = 3, column = 1, pady = 10)


window.mainloop()
