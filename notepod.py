import tkinter as tk
import os
from tkinter.filedialog import *

from tkinter import *



class Notepod:
#Κύρια κλάση του προγράμματος

    #κατασκευαστής κλάσης(constructor)
    def __init__(self):
        #Δημιουργία παραθύρου
        self.root = tk.Tk()
        #Αλλαγή Τίτλου Παραθύρου
        self.root.title('Notepod')

        #Αλλαγή Μεγέθους Παραθύρου
        self.root.geometry('600x600')


        # Τρεχον Αρχειο
        self.currentfile = None 
       

        #TextArea

        self.textArea = tk.Text(self.root, font = 'Arial')
        self.textArea.pack(fill = BOTH, expand = 1)
        

        #Μενου Εφαρμογης
        self.appMenu = tk.Menu(self.root)

        filemenu = Menu(self.appMenu, tearoff=0)
        filemenu.add_command(label="Open", command = self.openFile)
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Save As")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command= self.root.quit)

        editMenu = Menu(self.appMenu, tearoff = 0)
        editMenu.add_command(label = 'Undo')
        editMenu.add_separator()
        editMenu.add_command(label = 'Copy' , command = lambda: self.textArea.event_generate("<<Copy>>" ))
        editMenu.add_command(label = 'Cut'  , command = lambda: self.textArea.event_generate("<<Cut>>"  ))
        editMenu.add_command(label = 'Paste', command = lambda: self.textArea.event_generate("<<Paste>>"))

        viewMenu = Menu(self.appMenu, tearoff = 0)
        viewMenu.add_command(label = 'Font', command = lambda : self.textArea.config(font = 'Arial 40'))



        self.appMenu.add_cascade(label="File", menu= filemenu)
        self.appMenu.add_cascade(label="File", menu= editMenu)
        self.appMenu.add_cascade(label="View", menu= viewMenu)
        self.root.config(menu = self.appMenu)

        self.textArea.bind('<Button-3>', self.rightClickMenu)

        

        #Έναρξη βρόγχου παραθύρου
        self.root.mainloop()


    def rightClickMenu(self, event):
        # display the popup menu
        editMenu = Menu(self.textArea, tearoff = 0)
        editMenu.add_command(label = 'Undo')
        editMenu.add_separator()
        editMenu.add_command(label = 'Copy' , command = lambda: self.textArea.event_generate("<<Copy>>" ))
        editMenu.add_command(label = 'Cut'  , command = lambda: self.textArea.event_generate("<<Cut>>"  ))
        editMenu.add_command(label = 'Paste', command = lambda: self.textArea.event_generate("<<Paste>>"))
        try:
            editMenu.tk_popup(event.x_root, event.y_root, 0)
        finally:
        
            editMenu.grab_release()
    
    def openFile(self):
        self.currentfile = askopenfilename(defaultextension=".txt", 
                                      filetypes=[("All Files","*.*"), 
                                        ("Text Documents","*.txt")]) 
        try :
            file = open(self.currentfile, 'r')
            self.textArea.delete(1.0, END)
            self.textArea.insert(1.0 , file.read())
        except:
            print("Error opening file :", self.currentfile)
        finally:
            file.close()
        '''
        self.textArea.tag_add("tag1", '1.0', '1.5')
        self.textArea.tag_config("tag1", background="yellow", foreground="red")
        '''
        
    def saveFile(self):
        pass


app = Notepod()


    

