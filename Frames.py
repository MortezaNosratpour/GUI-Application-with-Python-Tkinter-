import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import font as tkfont
from tkinter import messagebox
# from PIL import Image, ImageTk
import os
import math
from TkinterDnD2 import DND_FILES, TkinterDnD
import pandas as pd
import time

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

        global listing
        listing = {}

        pages = [WelcomePage, FileNewPage, FileNewProject, FileOpenPage, ProcessPage, ViewThemePage]
        for p in pages:
            page_name = p.__name__
            frame = p(parent=container, controller=self)
            frame.grid(column=0, row=0, sticky = 'nesw',  padx = 200, pady = 150)
            listing[page_name] = frame


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
        listing["FileOpenPage"].import_project()
        self.up_frame("FileOpenPage")

    def up_frame(self, page_name):
        page = listing[page_name]
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
        options = ["None", "CAN", "protocol 2", "protocol 3"]
        self.protocol_parameters[options[1]] = ["EGR position sensor voltage", "Intake manifold absolute pressure sensor voltage",
                                                "Accelerator pedal position 1 voltage", "Accelerator pedal position 1 voltage",
                                                "Throttle position 1 voltage", "Throttle position 2 voltage", "Fuel tank vacuum sensor voltage",
                                                "Booster pressure sensor voltage", "Oil level sensor voltage", "Battery voltage",
                                                "Upstream oxygen sensor voltage", "Downstream oxygen sensor voltage", "Coolant temperature sensor voltage",
                                                "Intake air temperature sensor voltage", "Air conditioner evaporator temperature", "Turbo charge intake aur temperature sensor voltage",
                                                "Electrical load", "Switch", "5v reference voltage1 (Byte1)", "Fuel level", "Atmospheric pressure", "Intake manifold absolute pressure",
                                                "EGR valve position", "Throttle position", "Tank vacuum", "Accelerator pedal position", "Boost pressure", "GPF inlet pressure",
                                                "Coolant temperature", "Intake air temperature", "Air conditioner evapurator temperature", "Boost intake air temperature", "Cruise switch status",
                                                "Total knock retreat angle of each cylinder (There are 4 cylinders)", "Intake VVT actual opening", "Exhaust VVT actual openning", "Speed",
                                                "Engine speed", "Short-term fuel correction factor", "Fuel correction zone", "Long-term fuel correction factor", "Fuel injection pulse width",
                                                "Target air-fuel ratio", "Fuel control status", "PWM fan control duty ratio"]

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
        self.parameter_listbox = tk.Listbox(self, background="#ffe0d6", width=60, height=15, font=font, highlightcolor="green",
                                                selectbackground="green", cursor='plus', activestyle='dotbox', relief='groove')
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

        if self.protocol == "CAN":
            return self.protocol_parameters["CAN"]

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

            file_directory = listing["FileNewPage"].file_directory
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

        # right click menu
        self.right_click_menu = None




        label = tk.Label(self, text="Drag and drop files : ", font=controller.titlefont)
        label.pack()
        L = Label(self, text="Press right-click inside the listbox to delete selected files")
        L.pack()


        # a button for getting back to welcome page
        self.cancel_button = Button(self, text="Back", command=self.cancel_button)
        self.cancel_button.pack(side='bottom')
        # a button for getting to process page
        self.browse_button = Button(self, text="Next", command=self.go_to_progress_page)
        self.browse_button.pack(side='bottom')


        #run drag and drop and get csv files
        self.import_csv_files()
        self.listb.bind("<Button-3>", self.do_popup)

        # right click menu
        self.right_click_menu = tk.Menu(self, tearoff=0)
        self.right_click_menu.add_command(label="Delete selected files", command=self.delete_selected_files)


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
        self.listb = tk.Listbox(self, background="#ffe0d6", width=60, height=15, selectmode='extended')
        self.box_scrollbar = tk.Scrollbar(self, orient='vertical')
        self.listb.config(yscrollcommand=self.box_scrollbar.set, selectmode='extended')
        self.box_scrollbar.config(command=self.listb.yview)
        self.box_scrollbar.pack(side='right', fill='y')
        self.listb.pack(side='right', fill='y')
        self.listb.drop_target_register(DND_FILES)
        self.listb.dnd_bind("<<Drop>>", self.drop_inside_listbox)



    def cancel_button(self):
        #empty the listbox
        self.listb.delete(0, 'end')
        #make the list of files path empty
        self.files_list.clear()
        #get back to welcome page
        self.controller.up_frame("WelcomePage")


    def delete_selected_files(self):
        selected_index = self.listb.curselection()
        print(selected_index)
        for idx in selected_index:
            self.files_list.pop(idx)
            self.listb.delete(idx)
        for i in self.files_list:
            print(i)


    def do_popup(self, event):
        try:
            self.right_click_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.right_click_menu.grab_release()


    def go_to_progress_page(self):
        if len(self.files_list)==0:
            messagebox.showwarning(title="Warning!", message="You have not select any file.")
            return
        else:
            self.controller.up_frame("ProcessPage")





class ProcessPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        #progress bar
        self.pb = None

        #the dictionary will be used to collect datas for each parameter ; keys : parameters, values = lists of datas
        self.data = {}
        # process_font = tkfont.Font(family='Verdana', size=9, weight="bold", slant='roman')

        #the time when Start button is pushed
        self.start_time = 0

        #boolean for stoping when Stop button is pushed
        self.break_progress = False


        label1 = tk.Label(self, text="Processing...", font=self.controller.titlefont)
        label1.pack(side="top", pady=20)

        self.pb = ttk.Progressbar(self, orient='horizontal', mode='determinate', cursor='spider', length=280)
        self.pb.pack()

        # label
        global value_label, time_label
        value_label = ttk.Label(self, text=self.update_progress_label())
        value_label.pack()


        time_label = ttk.Label(self, text=self.update_time_label())
        time_label.pack()


        bs = ButtonStyle()
        #stop button
        self.stop_button = Button(self, style='TButton', text="Stop", command=self.stop)
        self.stop_button.pack(side='bottom')

        #start button
        start_button = Button(self, style='TButton', text = "Start", command=self.progress_start)
        start_button.pack(side='bottom')



    def update_time_label(self):
        return f"Speneded time : {(time.time() - self.start_time)} seconds"

    def update_progress_label(self):
        return f"Current Progress: {self.pb['value']}%"


    def progress_start(self):
        self.break_progress=False
        self.stop_button.config(text="Stop", command=self.stop)
        self.stop_button.pack(side='bottom')

        self.start_time = time.time()

        self.error7F_data=[]
        #TODO DEFINE AN ARRAY OF DICTIONORIES EACH FOR EVERY FILES
        data = {}

        number_of_files = len(listing["FileOpenPage"].files_list)
        step = math.ceil(100/number_of_files)
        for file_path in listing["FileOpenPage"].files_list:

            #get data from each csv file
            #TODO CHECK THE PARAMETERS IN DATA CONFIG.TXT WITH PARAMETERS IN DATA LOGGER.CSV
            print(file_path)

            df = pd.read_csv(file_path, header=None)
            step/=len(df.index)


            for indx in range(len(df.index)):
                if not self.break_progress:
                    if df.iloc[indx][3] == "7F" or df.iloc[indx][3] == "7f":
                        self.error7F_data.append(df.iloc[indx])
                        continue

                    else:
                        message_length = df.iloc[indx][2]
                        # TODO THERE IS SOME ROWS IN DATASET THAT THE LENGTH OF RESPOSE IS NOT EQUAL TO WHAT AHS BEEN DECLARED FOR EXAMPLE : ROW : 10000 ALSO

                        if message_length > 7:
                            #TODO WRITE THIS CASES IN OTHER FILE
                            continue

                        response_length = message_length - 3
                        parameter_code = str(df.iloc[indx][4]) + str(df.iloc[indx][5])
                        response = ""
                        for i in range(response_length):
                            response += str(df.iloc[indx][i + 6])

                        print(indx, response)

                        if data.get(parameter_code) == None:
                            data[parameter_code] = []
                            data[parameter_code].append((df.iloc[indx][0], response))
                        else:
                            data[parameter_code].append((df.iloc[indx][0], response))

                    if self.pb['value'] < 100:
                        self.pb['value'] += step
                        self.update()
                        value_label['text'] = self.update_progress_label()
                        time_label['text'] = self.update_time_label()
                else:
                    self.pb['value']=0
                    value_label['text'] = "Current Progress: 0%"
                    value_label['text'] = self.update_progress_label()
                    break

            value_label['text'] = "Current Progress: 100%"

            # messagebox.showinfo(message='The progress completed!')


    def back_to_open_page(self):
        self.controller.up_frame("FileOpenPage")

    def stop(self):
        self.break_progress=True
        self.pb.stop()
        value_label['text'] = self.update_progress_label()
        self.start_time=0
        self.stop_button.config(text="Back", command=self.back_to_open_page)
        self.stop_button.pack(side='bottom')







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

