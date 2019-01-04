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
        self.textArea.config(undo = True)

        #Μενου Εφαρμογης
        self.appMenu = tk.Menu(self.root)

        filemenu = Menu(self.appMenu, tearoff=0)
        filemenu.add_command(label="New", command = self.newFile)
        filemenu.add_command(label="Open", command = self.openFile)
        filemenu.add_command(label="Save", command = self.saveFile)
        filemenu.add_command(label="Save As", command = self.saveFileAs)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command= self.root.quit)

        editMenu = Menu(self.appMenu, tearoff = 0)
        editMenu.add_command(label = 'Undo', command = self.textArea.edit_undo)
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

        self.tags = []
        
        self.newFile()
        
        #Έναρξη βρόγχου παραθύρου
        self.root.mainloop()


    def rightClickMenu(self, event):
        print(self.textArea.tag_names())
       
        # display the popup menu
        editMenu = Menu(self.textArea, tearoff = 0)
        editMenu.add_command(label = 'Undo', command = self.textArea.edit_undo)
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
        self.textArea.tag_configure(tag.tagname,  background = tag.color)
        #self.textArea.tag_bind(tag.tagname, "<Enter>", lambda event: self.showTagInfo(event, tag.tagname))
        #self.textArea.tag_bind(tag.tagname, "<Leave>", lambda event: self.hideTagInfo())

        self.textArea.tag_bind(tag.tagname, "<Enter>", tag.showinfo)
        self.textArea.tag_bind(tag.tagname, "<Leave>", tag.hideinfo)
        
        self.tags.append(tag)       
        
        # increment the tag naming counter
        self.tagid += 1


    def openFile(self):
        self.currentfile = askopenfilename(defaultextension=".txt", 
                                      filetypes=[("All Files","*.*"), 
                                        ("Text Documents","*.txt")]) 
        self.textArea.tag_delete(self.textArea.tag_names())
        self.tags = []
        try :
            file = open(self.currentfile, 'r')
            self.textArea.tag_delete([t.tagname for t in self.tags])
            self.textArea.delete(1.0, END)
            pendingTags = [] 
            if file.readline().strip() == "#TAGINFOSTART#":
                while True:
                    line = file.readline().strip()

                    if line == '': 
                        file.seek(0)
                        break
                    
                    if line[0] != '#' or line[-1] != '#':
                        #raise Exception() # corrupted data
                        file.seek(0)
                        break
                    else :
                        line = line[1:-1] # removing '#'
                    
                    if line == 'TAGINFOEND' : break # all tag data were collected
                    
                    pendingTags.append(line.split('~'))
                    
            else:
                file.seek(0)
            self.textArea.delete('1.0', END)
            self.textArea.insert('1.0' , file.read())

            for tagdata in pendingTags:
                
                print(tagdata)
                t = self.createTag(tagdata[0], tagdata[1], tagdata[2], tagdata[3])
                self.tags.append(t)
                self.textArea.tag_add(t.tagname, tagdata[4], tagdata[5])
                self.textArea.tag_configure(t.tagname,  background = t.color)
                

                self.textArea.tag_bind(t.tagname, "<Enter>", t.showinfo)
                self.textArea.tag_bind(t.tagname, "<Leave>", t.hideinfo)

                self.textArea.tag_raise(t.tagname)

            self.root.title("{} - Notepod".format(self.currentfile))
            
                

        except Exception as e:
            print("Error opening file :", self.currentfile)
            print(e)
        finally:
            file.close()
        
       
       

    def saveFile(self):
        # if we currently have opened a file, we just save. 
        # Otherwise, we have to save the file as
        if self.currentfile:
            try:
                f = open(self.currentfile, "w")
                # Save Tags
                
                if len(self.tags) > 0:
                    f.write("#TAGINFOSTART#\n")
                    for currentTag in self.tags:
                        if currentTag == 'sel': continue
                        
                        limits = self.textArea.tag_ranges(currentTag.tagname)
                        if len(limits) != 2 : continue
                        # TAGINFO FORMAT ---> #tagname~tagauthor~tagtext~tagcolor~tagstart~tagend#
                        f.write('#{}~{}~{}~{}~{}~{}#\n'.format(currentTag.tagname, currentTag.auth, currentTag.text, currentTag.color, str(limits[0]), str(limits[1])))
                f.write("#TAGINFOEND#\n")
                f.write(self.textArea.get("1.0", END))
                f.close()
            except Exception as e:
                print(e)
        else :
            self.saveFileAs()
    
    def saveFileAs(self):

        f = asksaveasfile(mode = "w", filetypes = (('All Files', ''), ('Text Files', '.txt')), defaultextension = '.txt', initialfile = 'Document.txt')
        if f:
            self.currentfile = f.name
            self.saveFile()
    
    def newFile(self):
        if self.currentfile is not None:
            print('Alert!')
        
        self.currentfile = None
        self.root.title('Untitled - Notepod')
        self.textArea.tag_delete([t.tagname for t in self.tags])
        self.textArea.delete('1.0', END)
    def createTag(self, title, auth, text, color):
        t = Tag(title, auth, text, color)
        t.root = self.root
        self.tags.append(t)
        return t


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
        self.tag.root = self._root()
        return 
        


class Tag:

    def __init__(self, title, auth, text, color):
        self.tagname = title
        self.auth = auth
        self.color = color
        self.text = text
    
    def showinfo(self, event):
        self.taginfo = tk.Frame(self.root, height = 100, width = 100, bg = self.color)
        Label(self.taginfo, bg = self.color, text = "Tag Name: {}".format(self.tagname)).pack()
        Label(self.taginfo, bg = self.color, text = "Tag Author: {}".format(self.auth)).pack()
        Label(self.taginfo, bg = self.color, text = "Tag Text: {}".format(self.text)).pack()

        self.taginfo.place(x = event.x, y = event.y + 10)
        self.taginfo.tkraise() 

    def hideinfo(self, event):
        self.taginfo.destroy()
    
    def __str__(self):
        return "Name: {}\nAuthor: {}\nText: {}\nColor: {}".format(self.tagname, self.auth, self.text, self.color)
        

    


app = Notepod()


    
