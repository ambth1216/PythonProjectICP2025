from tkinter import *


# def update_display():
#     root.update_idletasks()
#     rootWidth = root.winfo_width()
#     rootHeight = root.winfo_height()

def on_resize(event):
    # update_display()
    root.update_idletasks()
    rootWidth = root.winfo_width()
    rootHeight = root.winfo_height()
    print(rootWidth)
    print(rootHeight)

root = Tk()

root.title('Dashborad')
root.geometry('500x500+50+50')

root.update_idletasks()
rootWidth = root.winfo_width()
rootHeight = root.winfo_height()


top_frame = Frame(root, bg='#3266a8')
top_frame.place(x=0, y=0, width=rootWidth, height=30)

label = Label(top_frame, text='Hello', font=('Arial', 20, 'bold'), bg='#3266a8', fg='White')
label.place(x=0, y=0)

logout_button = Button(top_frame, text='Logout', font=('Arial', 10, 'bold'), bg='#3266a8', fg='white')
logout_button.place(x=rootWidth-100, y=0)

root.bind('<Configure>', on_resize)

root.mainloop()