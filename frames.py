import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import font as tkfont
from tkinter import messagebox
from PIL import Image, ImageTk
import csv
import os
import datetime



class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.root = tk.Tk()
        self.root.title('IPCO')
        # setting the icon
        self.root.iconbitmap('icon.ico')
        # set minimum window size value
        self.root.minsize(900, 600)

        # set maximum window size value
        self.root.maxsize(1100, 1000)

        # setting the logo
        # logo = Image.open("Ipco-Logo.jpg")
        # logo = ImageTk.PhotoImage(logo)
        # logo_label = tk.Label(image=logo)
        # logo_label.image = logo
        # logo_label.grid(column=0, row=1)

        self.titlefont = tkfont.Font(family='Verdana', size=12, weight="bold", slant='roman')

        container = tk.Frame()
        container.grid(column=0, row=0, sticky = 'nesw', padx = 200, pady = 150)
        self.id = tk.StringVar()
        self.id.set("Mr Smith")

        self.listing = {}

        pages = [WelcomePage, FileNewPage, FileNewProject, FileOpenPage, ViewThemePage]
        for p in pages:
            page_name = p.__name__
            frame = p(parent=container, controller=self)
            frame.grid(column=0, row=0, sticky = 'nesw',  padx = 200, pady = 150)
            self.listing[page_name] = frame


        self.up_frame('WelcomePage')
        # setting the menubar
        self.menu = self.menubar()


    def menubar(self):
        # creating a menubar
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # creating the File menu
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label='New', command=lambda : self.up_frame("FileNewPage"))
        # up_frame("FileNewProject"))
        file_menu.add_command(label='Open', command=lambda : self.open_project())
        file_menu.add_command(label='Save As', command=self.root.destroy)
        file_menu.add_command(label='Save', command=self.root.destroy)
        file_menu.add_command(label='Exit', command=self.root.destroy)
        menu.add_cascade(label="File", menu=file_menu, underline=0)

        # creating the View menu
        view_menu = tk.Menu(menu, tearoff=False)
        view_menu.add_command(label='Theme', command=lambda : self.up_frame("ViewThemePage"))
        menu.add_cascade(label="View", menu=view_menu, underline=0)

        # creating the Help menu
        help_menu = tk.Menu(menu, tearoff=False)
        help_menu.add_command(label='Help', command=self.root.destroy)
        menu.add_cascade(label="Help", menu=help_menu, underline=0)


    def open_project(self):
        self.listing["FileOpenPage"].import_project()
        self.up_frame("FileOpenPage")

    def up_frame(self, page_name):
        page = self.listing[page_name]
        page.tkraise()


class ButtonStyle:
    def __init__(self):
        style = Style()

        # Will add style to every available button
        # even though we are not passing style
        # to every button widget.
        style.configure('TButton', font=('calibri', 12, 'bold'), borderwidth='4')

        # Changes will be reflected
        # by the movement of mouse.
        style.map('TButton', foreground=[('active', '!disabled', 'green')], background=[('active', 'black')])



class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id


        label = tk.Label(self, text = """IPCO \n\n ***Welcome***\n""", font=controller.titlefont)
        label.pack()

        bs = ButtonStyle()
        # New Button
        new_button = Button(self, style='TButton', text = "New Project", command=lambda : app.up_frame("FileNewPage"))
        new_button.pack(pady=10)

        #Open Button
        new_button = Button(self,style='TButton', text = "Open Project", command=lambda : app.open_project())
        new_button.pack()





class FileNewPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        self.file_directory = ""
        self.project_name = ""

        name_label = tk.Label(self, text="Project Name  :   ", font=controller.titlefont)
        name_label.pack(side='top')

        # TextBox Creation
        self.inputtxt = tk.Text(self, height=1, width=20)
        self.inputtxt.pack(side='top')


        newline = tk.Label(self, text="\n\n", font=controller.titlefont)
        newline.pack(side='right')

        #Getting the directory where the project will be saved
        dir_font = tkfont.Font(family='Verdana', size=8, slant='roman')
        label = tk.Label(self, text="Project directory  :   ", font=controller.titlefont)
        label.pack(side='left')


        browse_button = Button(self, text="Browse", command=self.browse_directory)
        browse_button.pack(side='left', pady=100, padx=10)


        cancel_button = Button(self, text="Back", command=self.cancel_project)
        cancel_button.pack(side='bottom')

        ok_button = Button(self, text="Next", command=self.create_project)
        ok_button.pack(side='bottom')



    def browse_directory(self):
        self.file_directory = filedialog.askdirectory()





    def create_project(self):
        # Getting the name for project
        self.project_name = self.inputtxt.get(1.0, 'end-1c')

        if (self.project_name == None or self.project_name == "" ) and self.file_directory == "":
            tk.messagebox.showwarning(title="Warning!", message="Project name and Project directory are not selected!")
            return

        elif (self.project_name == None or self.project_name == "" ):
            tk.messagebox.showwarning(title="Warning!", message="Project name and is not selected!")
            return

        elif (self.file_directory == ""):
            tk.messagebox.showwarning(title="Warning!", message="Project directory is not selected!")
            return

        elif (self.project_name != None or self.project_name != "" ) and self.file_directory != "":
            # creat project folder


            self.file_directory = os.path.join(self.file_directory, self.project_name)
            os.mkdir(self.file_directory)
            tk.messagebox.showinfo(title=None, message="File \"" + self.project_name + "\" was created successfully at \"" + str(self.file_directory) + "\"!")
            app.up_frame("FileNewProject")


    def cancel_project(self):
        self.file_directory= ""
        self.project_name = ""
        self.controller.up_frame("WelcomePage")




class FileNewProject(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id
        #dropdown menu
        self.protocol_option = None
        #listbox containing parameters corresponding to each protocol
        self.parameter_listbox = None
        #selected protocol
        self.protocol = None
        self.selected_parameters = []
        #dictionary containing list of parameter for each protocol
        self.protocol_parameters = {}
        self.parameters_list = None
        #scorllbar for listbox
        self.box_scrollbar = None


        global options
        options = ["None", "protocol 1", "protocol 2", "protocol 3"]
        self.protocol_parameters[options[1]] = ["parameter1_1", "parameter1_2", "parameter1_3", "parameter1_4",
                                                "parameter1_5"]
        self.protocol_parameters[options[2]] = ["parameter2_1", "parameter2_2", "parameter2_3", "parameter2_4",
                                                "parameter2_5", "parameter2_6", "parameter2_7", "parameter2_8"]
        self.protocol_parameters[options[3]] = ["parameter3_1", "parameter3_2", "parameter3_3", "parameter3_4",
                                                "parameter3_5", "parameter3_6", "parameter3_7", "parameter3_8",
                                                "parameter3_9", "parameter3_10", "parameter3_11", "parameter3_12", "parameter3_13", "parameter3_14",
                                                "parameter3_15", "parameter3_16", "parameter3_17", "parameter3_18",
                                                "parameter3_19", "parameter3_20"]


        label = tk.Label(self, text="Protocol  : \n", font=controller.titlefont)
        label.pack()

        # Create Dropdown menu
        self.create_dropmenu()

        label = tk.Label(self, text="Parameters  : \n", font=controller.titlefont)
        label.pack(pady=15)

        # Create Listbox of related parameters
        self.create_listbox()


        button_style = ButtonStyle()
        cancel_button = Button(self, text="Back", command=self.cancel_file)
        cancel_button.pack(side='bottom')

        ok_button = Button(self, text="Create", command= self.create_file)
        ok_button.pack(side='bottom', pady=15)

    def create_dropmenu(self):
        # Dropdown menu options

        # datatype of menu text
        self.clicked = tk.StringVar()

        # initial menu text
        self.clicked.set("None")

        # Create Dropdown menu
        self.protocol_option = OptionMenu(self, self.clicked, *options, command=self.config_listbox)
        self.protocol_option.pack()


    def create_listbox(self):
        font = tkfont.Font(family='Verdana', size=9, slant='roman')
        self.parameter_listbox = tk.Listbox(self, width=40, height=15, font=font)
        self.box_scrollbar = tk.Scrollbar(self, orient='vertical')



    def config_listbox(self, event):
        self.protocol = self.clicked.get()
        print(self.protocol)

        self.parameters_list = self.wanted_parameters()

        self.parameter_listbox.delete(0, 'end')
        for p in self.parameters_list:
            self.parameter_listbox.insert(len(self.parameters_list)-1, p)

        self.parameter_listbox.config(yscrollcommand=self.box_scrollbar.set, selectmode='extended')
        self.box_scrollbar.config(command=self.parameter_listbox.yview)
        self.box_scrollbar.pack(side='right', fill='y')
        self.parameter_listbox.pack(side='left')


    def wanted_parameters(self):

        if self.protocol == "protocol 1":
            return self.protocol_parameters["protocol 1"]

        elif self.protocol == "protocol 2":
            return self.protocol_parameters["protocol 2"]

        elif self.protocol == "protocol 3":
            return self.protocol_parameters["protocol 3"]

        else:
            pass


    def create_file(self):
        selected_index = self.parameter_listbox.curselection()
        self.selected_parameters.clear()
        if(len(selected_index) != 0) :
            for i in selected_index:
                self.selected_parameters.append(self.protocol_parameters[self.protocol][i])
            print("selected parameters : " + str(self.selected_parameters))

            file_directory = app.listing["FileNewPage"].file_directory
            file_name = 'parameters.csv'
            file_name2 = 'Config_data.txt'

            path1 = os.path.join(file_directory, file_name2)
            path2 = os.path.join(file_directory, file_name)

            with open(path1, 'w') as file:
                file.write(self.protocol)
                file.write('\n')
                file.write('\n'.join(self.selected_parameters))

            with open(path2, 'w') as file:
                file.write('\n'.join(self.selected_parameters))

            tk.messagebox.showinfo(title=None, message="File \"" + file_name + "\" was created successfully at \"" + str(file_directory) +"\"!")
            app.up_frame("FileOpenPage")
            return
        else:
            tk.messagebox.showwarning(title="Warning!", message="You have not selected parameters.")
            return


    def cancel_file(self):
        self.parameter_listbox.delete(0, 'end')
        self.clicked.set("None")
        self.controller.up_frame("WelcomePage")





class FileOpenPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id
        self.file_path = None
        self.protocol = ""
        self.selected_parameters = []
        self.browse_button = None
        self.cancel_button = None

        label = tk.Label(self, text="Import Files : ", font=controller.titlefont)
        label.pack()


    def import_project(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        self.file_path = tk.filedialog.askopenfilename(
            title='Import the project',
            filetypes=filetypes)

        if self.file_path != None:
            with open(self.file_path) as f:
                contents = f.readlines()

            self.protocol = contents[0]
            self.selected_parameters = contents[1:]

            print(self.protocol, self.selected_parameters)

            button_style = ButtonStyle()
            if self.browse_button != None:
                self.browse_button.pack_forget()
                self.cancel_button.pack_forget()

            self.browse_button = Button(self, text="Import", command=lambda: self.controller.up_frame("WelcomePage"))
            self.browse_button.pack(side='left')

            self.cancel_button = Button(self, text="Back", command=lambda: self.controller.up_frame("WelcomePage"))
            self.cancel_button.pack(side='right')


class ViewThemePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        label = tk.Label(self, text = "Themes : ", font=controller.titlefont)
        label.pack(side ='top')

        bs = ButtonStyle()
        new_button = Button(self,style='TButton', text = "Select", command=lambda:controller.up_frame("ViewThemePage"))
        new_button.pack(side='right')


if __name__ == "__main__" :
        global app
        app = MainFrame()
        app.root.mainloop()