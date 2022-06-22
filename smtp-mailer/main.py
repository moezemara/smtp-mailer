from tkinter import *
from functools import partial
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox
from tkinter import filedialog as fd
import commands
import functions
from datetime import datetime
import users
import sys, os

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("SMTP Mailer")
        self.minsize(800, 600)
        self.configure(background="gray")
    
        tabControl = ttk.Notebook(self)

        user = users.verify(users.loadsession())

        if user == 0:
            self.signin_tab = ttk.Frame(tabControl)
            tabControl.add(self.signin_tab, text="signin")
            self.add_signin_tab()
        else:
            username = user['username']

            self.loadlist_tab = ttk.Frame(tabControl)
            tabControl.add(self.loadlist_tab, text="Loadlist")
            self.add_loadlist_tab()

            self.message_tab = ttk.Frame(tabControl)
            tabControl.add(self.message_tab, text="Message")
            self.add_message_tab()

            self.html_message_tab = ttk.Frame(tabControl)
            tabControl.add(self.html_message_tab, text="Html Message")
            self.add_html_message_tab()
    
            self.settings_tab = ttk.Frame(tabControl)
            tabControl.add(self.settings_tab, text="Settings")
            self.add_settings_tab()

            self.start_tab = ttk.Frame(tabControl)
            tabControl.add(self.start_tab, text=f"Start as {username}")
            self.add_start_tab()
            self.start_label = Label(self.start_tab, textvariable = '')
            if user['perm'] == 'admin':
                self.admin_tab = ttk.Frame(tabControl)
                tabControl.add(self.admin_tab, text="Admin panel")
                self.add_admin_tab()

        
        tabControl.pack(expand=1, fill="both")
         
        self.tab_control = tabControl
        self.cart_counter = 0
        style = ttk.Style()
        style.theme_use("default")
        style.map("Treeview")


    def add_admin_tab(self):
        self.tv_admin = ttk.Treeview(self.admin_tab, columns=(1,2), show='headings', height=8)
        self.tv_admin.place(x=20,y=10)

        self.tv_admin.heading(1, text="id")
        self.tv_admin.column(1, width=70, anchor='w')
        self.tv_admin.heading(2, text="username")
        self.tv_admin.column(2, width=500)        


        Label(self.admin_tab, text='username').place(x=450, y=300)
        self.admin_tab_usernamevariable= StringVar()
        Entry(self.admin_tab, textvariable=self.admin_tab_usernamevariable).place(x=550, y=300)

        Label(self.admin_tab, text='password').place(x=450, y=330)
        self.admin_tab_passwordvariable = StringVar()
        Entry(self.admin_tab, textvariable=self.admin_tab_passwordvariable).place(x=550, y=330)

        self.adminstatusvariable = StringVar()
        Label(self.admin_tab, textvariable=self.adminstatusvariable).place(x=450, y=360)
        
        self.admin_tab_loadlist()
        Button(self.admin_tab, text='Register user', command=self.admin_tab_loadlist_add_user).place(x=680, y=300)
        
        Button(self.admin_tab, command=self.admin_tab_loadlist_delete_user, text='Delete selected username').place(x=50,y=300)


    def user_logout(self):
        users.logout()
        self.restart()

    def admin_tab_loadlist(self):
        counter = 0
        results = users.listusers()
        if results['success'] == 0:
            self.tv_admin.insert(parent='', index=counter, iid=counter, values=[counter+1,results['message']])
        elif results['success'] == 1:
            for user in results['message']:
                self.tv_admin.insert(parent='', index=counter, iid=counter, values=[counter+1,user['username']])
                counter+=1

    def admin_tab_loadlist_delete_user(self):
        selected = self.tv_admin.focus()
        selected = self.tv_admin.item(selected, 'values')
        if len(selected) != 0:
            self.adminstatusvariable.set(users.deleteuser(selected[1]))
            self.admin_tab_clear_loadlist()
            self.admin_tab_loadlist()

    def admin_tab_loadlist_add_user(self):
        results = users.register(self.admin_tab_usernamevariable.get(), self.admin_tab_passwordvariable.get())
        self.adminstatusvariable.set(results)
        self.admin_tab_clear_loadlist()
        self.admin_tab_loadlist()
    
    def admin_tab_clear_loadlist(self):
        self.tv_admin.delete(*self.tv_admin.get_children())
    
    def add_signin_tab(self):
        Label(self.signin_tab, text='Username').place(x=450, y=200)
        Label(self.signin_tab, text='Password').place(x=450, y=250)

        self.signinstatus = StringVar()
        Label(self.signin_tab, textvariable=self.signinstatus).place(x=450, y=450)

        self.usernamevariable_signin = StringVar()
        self.passwordvariable_signin = StringVar()

        Entry(self.signin_tab, textvariable=self.usernamevariable_signin).place(x=550, y=200)
        Entry(self.signin_tab, textvariable=self.passwordvariable_signin, show='*').place(x=550, y=250)

        Button(self.signin_tab, text='Login', command=self.signin_tab_checklog).place(x=450, y=350)

    def signin_tab_checklog(self):
        result = users.login(self.usernamevariable_signin.get(), self.passwordvariable_signin.get())
        if result == 1:
            self.restart()
        else:
            self.signinstatus.set(result)

    def restart(self):
        root.destroy()
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def add_start_tab(self):
        Button(self.start_tab, text='Start', command=self.startlib).place(x=300, y=300)
        self.progressvariable = StringVar()
        self.progressvariable.set('Idle')
        start_label = Label(self.start_tab, textvariable = self.progressvariable).place(x=300, y=340)

    def startlib(self):
        message = functions.loadmessage()
        htmlmessage = functions.loadhtmlmessage()
        emails = functions.loadlist()
        
        logs = open('./logs/logs.txt','a')

        num_emails = len(emails)
        progress = fail = success = 0

        for email in emails:
            result = functions.translate(email, message, htmlmessage)
            dateTimeObj = datetime.now()
            progress+=1
            if result == 'success':
                success+=1
            else:
                fail+=1
            echo = f'{dateTimeObj} => {email} --- Progress:{progress}/{num_emails} --- success:{success} --- fail:{fail} --- Result:{result}'
            print(echo)
            logs.write(echo+'\n')
            self.progressvariable.set(f'Finished:{progress}/{num_emails} --- success:{success} --- fail:{fail}')

    def add_loadlist_tab(self):
        self.tv = ttk.Treeview(self.loadlist_tab, columns=(1,2), show='headings', height=8)
        self.tv.place(x=20,y=10)

        self.tv.heading(1, text="id")
        self.tv.column(1, width=70, anchor='w')
        self.tv.heading(2, text="Email")
        self.tv.column(2, width=500)

        Label(self.loadlist_tab, text='Enter email to add').place(x=450, y=300)
        self.submission_variable = StringVar()
        Entry(self.loadlist_tab, textvariable=self.submission_variable).place(x=550, y=300)

        Button(self.loadlist_tab, text='Add Email', command=self.appenedemail).place(x=680, y=300)

        self.loadlist_counter = 0
        for email in functions.loadlist():
            self.tv.insert(parent='', index=self.loadlist_counter, iid=self.loadlist_counter, values=[self.loadlist_counter+1,email])
            self.loadlist_counter+=1
        
        Button(self.loadlist_tab, command=self.delete_loadlist, text='Delete selected email').place(x=50,y=300)
        Button(self.loadlist_tab, command=self.clear_loadlist, text='Clear list').place(x=200,y=300)
        Button(self.loadlist_tab, command=self.loadfile_loadlist, text='Select file to load').place(x=300,y=300)

    def add_message_tab(self):
        width = 400
        height = 370
        self.inputtxt_message_tab = Text(self.message_tab, height = 20, width = 98,bg = "light yellow")
        self.inputtxt_message_tab.place(x=0, y=0)
        self.load_default_message_tab()
        Button(self.message_tab, command=self.load_selected_message_tab, text='Load message').place(x=100,y=400)
        Button(self.message_tab, command=self.save_message_tab, text='Save message').place(x=200,y=400)

        Button(self.message_tab, command=partial(self.applycommand_message_tab, 'encrypt'), text='encrypt').place(x=width,y=height-30)
        Button(self.message_tab, command=partial(self.applycommand_message_tab, 'emailname'), text='emailname').place(x=width,y=height)
        Button(self.message_tab, command=partial(self.applycommand_message_tab, 'domain'), text='domain').place(x=width,y=height+30)
        Button(self.message_tab, command=partial(self.applycommand_message_tab, 'date'), text='date').place(x=width,y=height+60)
        self.datevariable_message_tab = StringVar()
        Entry(self.message_tab, textvariable=self.datevariable_message_tab).place(x=width+110, y=height+60)
        Button(self.message_tab, command=partial(self.applycommand_message_tab, 'random-string'), text='random-string').place(x=width,y=height+90)
        self.randomstringvariable_message_tab = StringVar()
        Entry(self.message_tab, textvariable=self.randomstringvariable_message_tab).place(x=width+110, y=height+90)
        Button(self.message_tab, command=partial(self.applycommand_message_tab, 'randomnumber'), text='random-number').place(x=width,y=height+120)
        self.randomnumbervariable_message_tab = StringVar()
        Entry(self.message_tab, textvariable=self.randomnumbervariable_message_tab).place(x=width+110, y=height+120)
        Button(self.message_tab, command=partial(self.applycommand_message_tab, 'attachment'), text='attachment').place(x=width,y=height+150)
        self.attachmentvariable_message_tab = StringVar()
        Entry(self.message_tab, textvariable=self.attachmentvariable_message_tab).place(x=width+110, y=height+150)

    def add_html_message_tab(self):
        width = 400
        height = 370
        self.inputtxt_html_message_tab = Text(self.html_message_tab, height = 20, width = 98,bg = "light yellow")
        self.inputtxt_html_message_tab.place(x=0, y=0)
        self.load_default_html_message_tab()
        Button(self.html_message_tab, command=self.load_selected_html_message_tab, text='Load message').place(x=100,y=400)
        Button(self.html_message_tab, command=self.save_html_message_tab, text='Save message').place(x=200,y=400)

        Button(self.html_message_tab, command=partial(self.applycommand_html_message_tab, 'encrypt'), text='encrypt').place(x=width,y=height-30)
        Button(self.html_message_tab, command=partial(self.applycommand_html_message_tab, 'emailname'), text='emailname').place(x=width,y=height)
        Button(self.html_message_tab, command=partial(self.applycommand_html_message_tab, 'domain'), text='domain').place(x=width,y=height+30)
        Button(self.html_message_tab, command=partial(self.applycommand_html_message_tab, 'date'), text='date').place(x=width,y=height+60)
        self.datevariable_html_message_tab = StringVar()
        Entry(self.html_message_tab, textvariable=self.datevariable_html_message_tab).place(x=width+110, y=height+60)
        Button(self.html_message_tab, command=partial(self.applycommand_html_message_tab, 'random-string'), text='random-string').place(x=width,y=height+90)
        self.randomstringvariable_html_message_tab = StringVar()
        Entry(self.html_message_tab, textvariable=self.randomstringvariable_html_message_tab).place(x=width+110, y=height+90)
        Button(self.html_message_tab, command=partial(self.applycommand_html_message_tab, 'randomnumber'), text='random-number').place(x=width,y=height+120)
        self.randomnumbervariable_html_message_tab = StringVar()
        Entry(self.html_message_tab, textvariable=self.randomnumbervariable_html_message_tab).place(x=width+110, y=height+120)
        Button(self.html_message_tab, command=partial(self.applycommand_html_message_tab, 'attachment'), text='attachment').place(x=width,y=height+150)
        self.attachmentvariable_html_message_tab = StringVar()
        Entry(self.html_message_tab, textvariable=self.attachmentvariable_html_message_tab).place(x=width+110, y=height+150)
        
    def add_settings_tab(self):
        width = 100
        height = 100

        Label(self.settings_tab, text='SMTP settings').place(x=width,y=height)

        Label(self.settings_tab, text='Username').place(x=width,y=height+30)
        Label(self.settings_tab, text='Password').place(x=width,y=height+60)
        Label(self.settings_tab, text='SMTP Host').place(x=width,y=height+90)
        Label(self.settings_tab, text='SMTP Port').place(x=width,y=height+120)
        Label(self.settings_tab, text='Secure').place(x=width,y=height+150)

        Label(self.settings_tab, text='Email Settings').place(x=width,y=height+180)

        Label(self.settings_tab, text='From').place(x=width,y=height+210)
        Label(self.settings_tab, text='Subject').place(x=width,y=height+240)
        Label(self.settings_tab, text='Text').place(x=width,y=height+270)
        Label(self.settings_tab, text='Html').place(x=width,y=height+300)

        self.smtpusernamevariable = StringVar()
        Entry(self.settings_tab, textvariable=self.smtpusernamevariable).place(x=width+150, y=height+30)
        self.smtppasswordvariable = StringVar()
        Entry(self.settings_tab, textvariable=self.smtppasswordvariable).place(x=width+150, y=height+60)
        self.smtphostvariable = StringVar()
        Entry(self.settings_tab, textvariable=self.smtphostvariable).place(x=width+150, y=height+90)
        self.smtpportvariable = StringVar()
        Entry(self.settings_tab, textvariable=self.smtpportvariable).place(x=width+150, y=height+120)
        self.smtpsecurevariable = IntVar()
        Checkbutton(self.settings_tab, variable=self.smtpsecurevariable).place(x=width+150, y=height+150)


        self.emailfromvariable = StringVar()
        Entry(self.settings_tab, textvariable=self.emailfromvariable).place(x=width+150, y=height+210)
        self.emailsubjectvariable = StringVar()
        Entry(self.settings_tab, textvariable=self.emailsubjectvariable).place(x=width+150, y=height+240)
        self.emailtextvariable = IntVar()
        Checkbutton(self.settings_tab, variable=self.emailtextvariable).place(x=width+150, y=height+270)
        self.emailhtmlvariable = IntVar()
        Checkbutton(self.settings_tab, variable=self.emailhtmlvariable).place(x=width+150, y=height+300)

        Button(self.settings_tab, command=self.saveconfig, text='Save').place(x=width,y=height+340)
        Button(self.settings_tab, text='Logout', command=self.user_logout).place(x=width+40, y=width+340)
        self.list_settings_tab()

    def saveconfig(self):
        settings = {'username':self.smtpusernamevariable.get(),'password':self.smtppasswordvariable.get(),'smtp':self.smtphostvariable.get(),'port':self.smtpportvariable.get(),'secure':self.smtpsecurevariable.get(),'from':self.emailfromvariable.get(),'subject':self.emailsubjectvariable.get(),'text':self.emailtextvariable.get(),'html':self.emailhtmlvariable.get()}
        functions.saveconfig(str(settings))

    def list_settings_tab(self):
        settings = functions.loadconfig()
        self.smtpusernamevariable.set(settings['username'])
        self.smtppasswordvariable.set(settings['password'])
        self.smtphostvariable.set(settings['smtp'])
        self.smtpportvariable.set(settings['port'])
        self.smtpsecurevariable.set(settings['secure'])
        self.emailfromvariable.set(settings['from'])
        self.emailsubjectvariable.set(settings['subject'])
        self.emailtextvariable.set(settings['text'])
        self.emailhtmlvariable.set(settings['html'])

    def applycommand_html_message_tab(self, action):
        if action == 'date':
            action = 'date-'+self.datevariable_html_message_tab.get()
        elif action == 'random-string':
            action = 'random-s-'+self.randomstringvariable_html_message_tab.get()
        elif action == 'random-number':
            action = 'random-n-'+self.randomnumbervariable_html_message_tab.get()
        elif action == 'attachment':
            action = 'attachment['+self.attachmentvariable_html_message_tab.get()+']'

        command=f'{{{{{action}}}}}'
        self.inputtxt_html_message_tab.insert('end-1c', command)

    def load_default_html_message_tab(self):
        self.inputtxt_html_message_tab.insert(1.0, functions.load_deafult_html_message())

    def load_selected_html_message_tab(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        self.inputtxt_html_message_tab.insert("end-1c",functions.load_html_message(filename))
    
    def save_html_message_tab(self):
        functions.save_html_message(self.inputtxt_html_message_tab.get(1.0,'end-1c'))

    def applycommand_message_tab(self, action):
        if action == 'date':
            action = 'date-'+self.datevariable_message_tab.get()
        elif action == 'random-string':
            action = 'random-s-'+self.randomstringvariable_message_tab.get()
        elif action == 'random-number':
            action = 'random-n-'+self.randomnumbervariable_message_tab.get()
        elif action == 'attachment':
            action = 'attachment['+self.attachmentvariable_message_tab.get()+']'

        command=f'{{{{{action}}}}}'
        self.inputtxt_message_tab.insert('end-1c', command)



    def load_default_message_tab(self):
        self.inputtxt_message_tab.insert(1.0, functions.load_deafult_message())

    def load_selected_message_tab(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        self.inputtxt_message_tab.insert("end-1c",functions.load_message(filename))
    
    def save_message_tab(self):
        functions.save_message(self.inputtxt_message_tab.get(1.0,'end-1c'))

    def list_loadlist(self):
        loadlist = functions.loadlist()
        self.loadlist_counter = 0
        for email in loadlist:
            self.tv.insert(parent='', index=self.loadlist_counter, iid=self.loadlist_counter, values=[self.loadlist_counter+1,email])
            self.loadlist_counter+=1

    def delete_loadlist(self):
        selected = self.tv.focus()
        selected = self.tv.item(selected, 'values') 
        if len(selected) != 0:
            functions.delete_loadlist(selected[1])
            self.tv.delete(*self.tv.get_children())
            self.list_loadlist()

    def appenedemail(self):
        functions.appenedemail(self.submission_variable.get())
        self.tv.delete(*self.tv.get_children())
        self.list_loadlist()
    
    def clear_loadlist(self):
        functions.clear()
        self.tv.delete(*self.tv.get_children())
        self.list_loadlist()
    
    def loadfile_loadlist(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        functions.loadfiletoloadlist(filename)
        self.tv.delete(*self.tv.get_children())
        self.list_loadlist()


root = Root()
root.mainloop()