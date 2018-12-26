# pylint: disable = W0614
import tkinter as tk
import os
from tkinter.filedialog import *

from tkinter import colorchooser, simpledialog

from tkinter import *



class Notepod:
#Κύρια κλάση του προγράμματος

    #κατασκευαστής κλάσης(constructor)
    def __init__(self):
        #Δημιουργία παραθύρου
        self.root = tk.Tk()

        self.mainframe = tk.Frame(self.root)
        
        #Αλλαγή Τίτλου Παραθύρου
        self.root.title('Notepod')

        #Αλλαγή Μεγέθους Παραθύρου
        self.root.geometry('600x600')

        self.mainframe.grid_rowconfigure(0, weight = 1)
        self.mainframe.grid_columnconfigure(0, weight = 1)

        self.tagid = 0

        # Τρεχον Αρχειο
        self.currentfile = None 
       

        #TextArea

        self.textArea = tk.Text(self.mainframe, font = 'Times')
        self.textArea.grid(row = 0, column = 0, sticky = NSEW, padx = 2, pady = 2)
        
        #Scrollbar
        self.scrollbar = Scrollbar(self.mainframe, command = self.textArea.yview)
        self.scrollbar.grid(row = 0, column = 1, sticky = NSEW)

        self.textArea.config(yscrollcommand = self.scrollbar.set)
        

        #Μενου Εφαρμογης
        self.appMenu = tk.Menu(self.root)

        filemenu = Menu(self.appMenu, tearoff=0)
        filemenu.add_command(label="Open", command = self.openFile)
        filemenu.add_command(label="Save", command = self.saveFile)
        filemenu.add_command(label="Save As", command = self.saveFileAs)
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
        self.appMenu.add_cascade(label="Edit", menu= editMenu)
        self.appMenu.add_cascade(label="View", menu= viewMenu)
        self.root.config(menu = self.appMenu)

        self.textArea.bind('<Button-3>', self.rightClickMenu)

        self.mainframe.pack(fill = BOTH, expand = 1)


        # Tagging 

        self.tags = {}


        self.taginfo = None
        

        #Έναρξη βρόγχου παραθύρου
        self.root.mainloop()


    def rightClickMenu(self, event):
        print(self.textArea.tag_names())
        # display the popup menu
        editMenu = Menu(self.textArea, tearoff = 0)
        editMenu.add_command(label = 'Undo')
        editMenu.add_separator()
        editMenu.add_command(label = 'Copy' , command = lambda: self.textArea.event_generate("<<Copy>>" ))
        editMenu.add_command(label = 'Cut'  , command = lambda: self.textArea.event_generate("<<Cut>>"  ))
        editMenu.add_command(label = 'Paste', command = lambda: self.textArea.event_generate("<<Paste>>"))
        editMenu.add_command(label = 'Add Tag', command = self.addTag)
        try:
            editMenu.tk_popup(event.x_root, event.y_root, 0)
        finally:
        
            editMenu.grab_release()
    
    def addTag(self):
        
        #if nothin is selected, just do nothing
        if SEL_FIRST == SEL_LAST:return
        
        tag = TagCreator(self.root).tag
        # add the tag
        if tag is None:
            print("Dialog Canceled")
            return # dialog canceled
        self.textArea.tag_add(tag.tagname, SEL_FIRST, SEL_LAST)
        self.textArea.tag_configure(tag.tagname,  background = tag.color, foreground = 'red')
        self.textArea.tag_bind(tag.tagname, "<Enter>", lambda event: self.showTagInfo(event, tag.tagname))
        self.textArea.tag_bind(tag.tagname, "<Leave>", lambda event: self.hideTagInfo())

        self.tags[tag.tagname] = tag
        # increment the tag naming counter
        self.tagid += 1
    
    
    def showTagInfo(self, event, tag):
        
        if self.taginfo is not None : return
        tag = self.tags[tag]
       
        
        self.taginfo = tk.Frame(self.root, height = 100, width = 100, bg = tag.color)
        Label(self.taginfo, bg = tag.color, text = "Tag Name: {}".format(tag.tagname)).pack()
        Label(self.taginfo, bg = tag.color, text = "Tag Author: {}".format(tag.auth)).pack()
        Label(self.taginfo, bg = tag.color, text = "Tag Text: {}".format(tag.text)).pack()

        self.taginfo.place(x = event.x, y = event.y + 10)
        self.taginfo.tkraise() 

    def hideTagInfo(self):
        if self.taginfo:
            self.mainframe.tkraise()
            self.taginfo.destroy()
            self.taginfo = None


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
        
       

    def saveFile(self):
        # if we currently have opened a file, we just save. 
        # Otherwise, we have to save the file as
        if self.currentfile:
            try:
                f = open(self.currentfile, "w")
                f.write(self.textArea.get("1.0", END))
                f.close()
            except Exception as e:
                print(e)
        else :
            self.saveFileAs()
    
    def saveFileAs(self):

        f = asksaveasfile(mode = "w", filetypes = (('All Files', ''), ('Text Files', '.txt')), defaultextension = '.txt', initialfile = 'Document.txt')
        if f:
            f.write(self.textArea.get('1.0', END))

            self.currentfile = f.name
            f.close()
        


class TagCreator(simpledialog.Dialog):

    def body(self, master):
        self.tag = None

        Label(master, text = 'Tag Title:').grid(row = 0, column = 0)
        Label(master, text = 'Tag Author:').grid(row = 1, column = 0)
        Label(master, text = 'Tag Text:').grid(row = 2, column = 0)
        Label(master, text = 'Tag Color:').grid(row = 3, column = 0)

        self.titleEntry = Entry(master)
        self.authorEntry = Entry(master)
        self.textEntry = Entry(master)

        self.titleEntry.grid(row = 0, column = 1)
        self.authorEntry.grid(row = 1, column = 1)
        self.textEntry.grid(row = 2, column = 1)

        self.color = None

        self.pickColorButton = Button(master, text = 'Pick Color', command = self.pickColor)
        self.pickColorButton.grid(row = 3, column = 1)

    def pickColor(self):

        self.color = colorchooser.askcolor('yellow')[1]

    def apply(self):
        self.tag = Tag(self.titleEntry.get(), self.authorEntry.get(), self.textEntry.get(), self.color)
        return 
        










class Tag:

    def __init__(self, title, auth, text, color):
        self.tagname = title
        self.auth = auth
        self.color = color
        self.text = text
        

    


app = Notepod()


    
