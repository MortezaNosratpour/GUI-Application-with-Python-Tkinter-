import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import font as tkfont
from tkinter import messagebox

# from PIL import Image, ImageTk
import csv
import os
import time
from TkinterDnD2 import DND_FILES, TkinterDnD


class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.root = TkinterDnD.Tk()
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

        pages = [WelcomePage, FileNewPage, FileNewProject, FileOpenPage, ProcessPage, ViewThemePage]
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
        #clear all values and get back to welcome page
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
        # path of txt file of project
        self.file_path = None
        #protocols and parameters that user had selected during creating the projects
        self.protocol = ""
        self.selected_parameters = []
        # buttons
        self.browse_button = None
        self.cancel_button = None

        #drag and drop area
        self.listb = None
        self.box_scrollbar = None

        #list of csv files
        self.files_list = []




        label = tk.Label(self, text="Drag and drop files : ", font=controller.titlefont)
        label.pack()

        # a button for getting back to welcome page
        self.cancel_button = Button(self, text="Back", command=self.cancel_button)
        self.cancel_button.pack(side='bottom')
        # a button for getting to process page
        self.browse_button = Button(self, text="Next", command=lambda: self.controller.up_frame("ProcessPage"))
        self.browse_button.pack(side='bottom')


        #run drag and drop and get csv files
        self.import_csv_files()

    #a function for importing the txt file of project including the protocol and parameters of the project
    def import_project(self):
        #clear all elements in listbox
        self.listb.delete("0", "end")
        self.files_list.clear()

        #import the .txt file of the project
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        self.file_path = tk.filedialog.askopenfilename(
            title='Import the project',
            filetypes=filetypes)

        #initiate the protocol and parameters variable by values in txt file of project
        if self.file_path != None:
            with open(self.file_path) as f:
                contents = f.readlines()

            self.protocol = contents[0]
            self.selected_parameters = contents[1:]

            print(self.protocol, self.selected_parameters)

            button_style = ButtonStyle()



    #getting the paths of the csv files and printing them in drag and drop listbox
    def drop_inside_listbox(self, event):
        print(event.data[1:-1])
        if event.data[1:-1].endswith(".csv"):
            self.listb.insert("end", event.data)
            self.files_list.append(event.data[1:-1])

        else:
            tk.messagebox.showwarning(title="Warning!", message="Wrong file! \nPlease select files with .csv suffix.")
            return



    #create a listbox for draging and droping the files in it (it also has scrollbar)
    def import_csv_files(self):
        self.listb = tk.Listbox(self, background="#ffe0d6", width=60, height=15)
        self.box_scrollbar = tk.Scrollbar(self, orient='vertical')
        self.listb.config(yscrollcommand=self.box_scrollbar.set, selectmode='extended')
        self.box_scrollbar.config(command=self.listb.yview)
        self.box_scrollbar.pack(side='right', fill='y')
        self.listb.pack(side='right', fill='y')
        self.listb.drop_target_register(DND_FILES)
        self.listb.dnd_bind("<<Drop>>", self.drop_inside_listbox)



    def cancel_button(self):
        #make the list of files path empty
        self.files_list.clear()
        #get back to welcome page
        self.controller.up_frame("WelcomePage")



class ProcessPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id
        #progress bar
        self.pb = None

        process_font = tkfont.Font(family='Verdana', size=9, weight="bold", slant='roman')

        label1 = tk.Label(self, text = "Current project: ", font=controller.titlefont)
        label1.pack(side ='top')

        # label2 = tk.Label(self, text= app.listing["FileOpenPage"].file_path[:-15], font=process_font)
        # label2.pack(side='top')

        # label3 = tk.Label(self, text= app.listing["Imported files: "].file_path[:-15], font=controller.titlefont)
        # label3.pack(side='top')

        # for i in range(len(app.listing["FileOpenPage"].files_list)):
        #     label4 = tk.Label(self, text= app.listing["FileOpenPage"].files_list[i], font=process_font)
        #     label4.pack(side='top')



        bs = ButtonStyle()
        #start button
        new_button = Button(self,style='TButton', text = "Start", command=self.progress_start)
        new_button.pack(side='bottom')

        #stop button
        new_button = Button(self, style='TButton', text="Stop", command=self.stop)
        new_button.pack(side='bottom')

        self.pb = ttk.Progressbar(self, orient='horizontal', mode='determinate', cursor='spider', length=280)
        self.pb.pack(side='right')

        # label
        global value_label
        value_label = ttk.Label(self, text=self.update_progress_label())
        value_label.pack(side='right')

    def update_progress_label(self):
        return f"Current Progress: {self.pb['value']}%"


    def progress_start(self):
        number_of_files = len(app.listing["FileOpenPage"].files_list)
        step = 100/number_of_files
        for file_path in app.listing["FileOpenPage"].files_list:
            #get data from each csv file
            #TODO
            if self.pb['value'] < 100:
                self.pb['value'] += step
                self.update()
                value_label['text'] = self.update_progress_label()
            else:
                messagebox.showinfo(message='The progress completed!')


    def stop(self):
        self.pb.stop()
        value_label['text'] = self.update_progress_label()






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