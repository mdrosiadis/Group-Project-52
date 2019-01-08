# pylint: disable = W0614
import tkinter as tk
import os
from tkinter.filedialog import *

from tkinter import colorchooser, simpledialog, messagebox

from tkinter import *



class Notepod:
#Κύρια κλάση του προγράμματος

    #κατασκευαστής κλάσης(constructor)
    def __init__(self):
        #Δημιουργία παραθύρου
        self.root = tk.Tk()

        self.mainframe = tk.Frame(self.root, width = 500)
        #self.tagFrame = tk.Frame(self.root, width = 100, background = 'yellow')
        self.tagFrame = ButtonListFrame(self.root)

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
        filemenu.add_command(label="Exit", command= self.exit)

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
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        

        
        self.tagFrame.pack(side = RIGHT, fill = BOTH)
        self.mainframe.pack(side = LEFT, fill = BOTH, expand = 1)

        # Tagging 

        self.tags = []
        
        self.newFile()

        #Έναρξη βρόγχου παραθύρου
        self.root.mainloop()


    def rightClickMenu(self, event):
       
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
    
    def addTag(self, name = None):
        
        #if nothin is selected, just do nothing
        if SEL_FIRST == SEL_LAST:return
        if name is not None:
            tag = self.createTag(name,"","","") # we will get other data later
        else:
            tag = TagCreator(self.root).tag
            tag = self.createTag(tag.tagname, tag.auth, tag.text, tag.color)

        # add the tag
        if tag is None:
            return # dialog canceled
        self.textArea.tag_add(tag.tagname, SEL_FIRST, SEL_LAST)
        self.textArea.tag_configure(tag.tagname,  background = tag.color)
      
        self.textArea.tag_bind(tag.tagname, "<Enter>", tag.showinfo)
        self.textArea.tag_bind(tag.tagname, "<Leave>", tag.hideinfo)      
        
        # increment the tag naming counter
        self.tagid += 1


    def openFile(self):
        if self.onFileClose() == False : return
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

                t = self.createTag(tagdata[0], tagdata[1], tagdata[2], tagdata[3])
                pairs = tagdata[4:]
                for i in range(len(pairs))[::2]:
                    self.textArea.tag_add(t.tagname, pairs[i], pairs[i+1])
                    self.textArea.tag_configure(t.tagname,  background = t.color)
                

                    self.textArea.tag_bind(t.tagname, "<Enter>", t.showinfo)
                    self.textArea.tag_bind(t.tagname, "<Leave>", t.hideinfo)


            self.root.title("{} - Notepod".format(self.currentfile))
            
                

        except:
            messagebox.showerror('Notepod', "Error opening file : {}".format(self.currentfile))
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
                        limits = self.textArea.tag_ranges(currentTag.tagname)
                        #if len(limits) != 2 : continue
                        # TAGINFO FORMAT ---> #tagname~tagauthor~tagtext~tagcolor~tagstart1~tagend1~tagstart2~tagend2# etc
                        f.write('#{}~{}~{}~{}'.format(currentTag.tagname, currentTag.auth, currentTag.text, currentTag.color))
                        for i in limits:
                            f.write('~{}'.format(str(i)))
                        f.write('#\n')
                    f.write("#TAGINFOEND#\n")
                f.write(self.textArea.get("1.0", END))
                self.textArea.edit_modified(False)
                f.close()
            except:
                messagebox.showerror('Notepod', 'Error saving {}'.format(self.currentfile))
        else :
            self.saveFileAs()
    
    def saveFileAs(self):

        f = asksaveasfile(mode = "w", filetypes = (('All Files', ''), ('Text Files', '.txt')), defaultextension = '.txt', initialfile = 'Document.txt')
        if f:
            self.currentfile = f.name
            self.saveFile()
    
    def newFile(self):
        
        self.onFileClose()
        
        self.currentfile = None
        self.root.title('Untitled - Notepod')
        self.textArea.tag_delete([t.tagname for t in self.tags])
        self.textArea.delete('1.0', END)
        self.textArea.edit_modified(False)
    
    def createTag(self, title, auth, text, color):
        
        tmp = [i.tagname for i in self.tags]
        # if there is not a tag name as this one, append this tag in the list and create a new button
        # Otherwise just return the tag
        if title in tmp:
            t = self.tags[tmp.index(title)]
        else:
            t = Tag(title, auth, text, color)
            t.root = self.root
            self.tags.append(t)
            self.tagFrame.addButton(t, self.addTag)

        return t

    def onFileClose(self):
        # Returns True if we can exit / open new file, False otherwise
        if self.textArea.edit_modified():
            ans = messagebox.askyesnocancel('Notepod', 'Unsaved Changes. Save?')
            
            if ans == True:
                self.saveFile()
                toReturn = True
            if ans == False: toReturn = True
            if ans is None: toReturn = False
        else:
            toReturn =  True

        if toReturn:
            self.tagFrame.clearButtons()
        
        return toReturn
            
    def exit(self):
        if self.onFileClose(): self.root.destroy()

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

        self.color = '#ffff00'

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

    def __eq__(self, other):
        return self.tagname == other.tagname
    
    def __str__(self):
        return "Name: {}\nAuthor: {}\nText: {}\nColor: {}".format(self.tagname, self.auth, self.text, self.color)
        
class ButtonListFrame(tk.Frame):

    def __init__(self, master):
        self.master = master
        super().__init__(self.master, width =100, bg = 'skyblue')
        tk.Label(self, text = 'Labels', bg = 'skyblue', font = 'Arial 24').pack(side = TOP, fill = X)
        self.buttons = []
        
        
    
    def addButton(self, tag, func):
        b = tk.Button(self, text = tag.tagname, bg = tag.color, wraplength = 100, command = lambda : func(name = tag.tagname))
        b.pack(side = TOP, fill = X)
        self.buttons.append(b)

    def clearButtons(self):
        for button in self.buttons:
            button.destroy()

   
        
    


app = Notepod()


    
