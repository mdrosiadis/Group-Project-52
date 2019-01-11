# pylint: disable = W0614
import tkinter as tk
from tkinter.filedialog import *
from tkinter import colorchooser, simpledialog, messagebox

# Importing Wildcard to ease usage of Tcl/Tk constants/variables
from tkinter import *



class Notepod:
# Main Program Class

    # Class Constructor
    def __init__(self):
        # Window Creation ----------------------------------------------------------------------------------------
        self.root = tk.Tk()
        
        # Window Title
        self.root.title('Notepod')

        # Default Window size
        self.root.geometry('600x600')

        # App Variables ------------------------------------------------------------------------------------------

        self.bigfontOn = False
        
        # Tagging 

        self.tags = []

        self.currentUser = 'Default User'
        self.statusBarString = tk.StringVar()
        self.statusBarString.set('Editing as Default User')

        # Current Opened File
        self.currentfile = None 

        # GUI Creattion ------------------------------------------------------------------------------------------

        # Creating the 3 main Frames of the app
        self.mainframe = tk.Frame(self.root, width = 500)
        self.tagFrame = ButtonListFrame(self.root)
        self.statusBar = tk.Label(self.root, textvariable = self.statusBarString, relief = SUNKEN, anchor = W)
        
        # Configuring Text - Scrollbar Geometry
        self.mainframe.grid_rowconfigure(0, weight = 1)
        self.mainframe.grid_columnconfigure(0, weight = 1)

        # Main Text Area
        self.textArea = tk.Text(self.mainframe, font = 'Arial 20')
        self.textArea.grid(row = 0, column = 0, sticky = NSEW, padx = 2, pady = 2)
        
        # Text Area Scrollbar
        self.scrollbar = tk.Scrollbar(self.mainframe, command = self.textArea.yview)
        self.scrollbar.grid(row = 0, column = 1, sticky = NSEW)

        self.textArea.config(yscrollcommand = self.scrollbar.set)
        self.textArea.config(undo = True)

        # App Menu ----------------------------------------------------------------------------------------------
        self.appMenu = tk.Menu(self.root)

        filemenu = tk.Menu(self.appMenu, tearoff=0)
        filemenu.add_command(label="New", command = self.newFile)
        filemenu.add_command(label="Open", command = self.openFile)
        filemenu.add_command(label="Save", command = self.saveFile)
        filemenu.add_command(label="Save As", command = self.saveFileAs)
        filemenu.add_separator()
        filemenu.add_command(label = 'Change User', command = self.setUser)
        filemenu.add_command(label="Exit", command= self.exit)

        editMenu = tk.Menu(self.appMenu, tearoff = 0)
        editMenu.add_command(label = 'Undo', command = self.textArea.edit_undo)
        editMenu.add_separator()
        editMenu.add_command(label = 'Copy' , command = lambda: self.textArea.event_generate("<<Copy>>" ))
        editMenu.add_command(label = 'Cut'  , command = lambda: self.textArea.event_generate("<<Cut>>"  ))
        editMenu.add_command(label = 'Paste', command = lambda: self.textArea.event_generate("<<Paste>>"))

        viewMenu = tk.Menu(self.appMenu, tearoff = 0)
        viewMenu.add_checkbutton(label = 'Big Font', command = self.toggleFont)

        aboutMenu = tk.Menu(self.appMenu, tearoff = 0)
        aboutMenu.add_command(label = 'About Notepod', command = self.aboutInfo)



        self.appMenu.add_cascade(label = "File" , menu = filemenu )
        self.appMenu.add_cascade(label = "Edit" , menu = editMenu )
        self.appMenu.add_cascade(label = "View" , menu = viewMenu )
        self.appMenu.add_cascade(label = "About", menu = aboutMenu)
        self.root.config(menu = self.appMenu)

        # Handle Right Clicks
        self.textArea.bind('<Button-3>', self.rightClickMenu)

        # Make sure to check for unsaved changes if the window is forced to close
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        
       
        Tag.setFunc(self.addTag)
        
        # Packing onto main Window
        
        self.statusBar.pack(fill = X, side = BOTTOM, anchor = W)
        self.tagFrame.pack(side = RIGHT, fill = BOTH)
        self.mainframe.pack(side = LEFT, fill = BOTH, expand = 1)
        
        self.newFile()

        # Start the event handling loop
        self.root.mainloop()

    def toggleFont(self):

        if self.bigfontOn:
            self.textArea.config(font = 'Arial 20')
        else:
            self.textArea.config(font = 'Arial 40')
        
        self.bigfontOn = not self.bigfontOn

    def existingTagsMenu(self, parent):
        
        tagMenu = tk.Menu(parent, tearoff = 0)

        for tag in self.tags:
            tagMenu.add_command(label = tag.tagname, background = tag.color, command = tag.newTag)
        return tagMenu

    def rightClickMenu(self, event):
        
        # Create the tag specific menu 
        editMenu = Menu(self.textArea, tearoff = 0)
        helperMenu = tk.Menu(editMenu, tearoff = 0)

        helperMenu.add_cascade(label = 'Existing Tag', state = (DISABLED if len(self.tags) == 0 else NORMAL), menu = self.existingTagsMenu(helperMenu))
        helperMenu.add_separator()
        helperMenu.add_command(label = 'New Tag', command = self.addTag)

        # Create the popup menu
        
        editMenu.add_command(label = 'Undo', command = self.textArea.edit_undo)
        editMenu.add_separator()
        editMenu.add_command(label = 'Copy' , command = lambda: self.textArea.event_generate("<<Copy>>" ))
        editMenu.add_command(label = 'Cut'  , command = lambda: self.textArea.event_generate("<<Cut>>"  ))
        editMenu.add_command(label = 'Paste', command = lambda: self.textArea.event_generate("<<Paste>>"))
        editMenu.add_separator()
        editMenu.add_cascade(label = 'Add Tag', menu = helperMenu)

        # Display the Menu
        try:
            editMenu.tk_popup(event.x_root, event.y_root, 0)
        finally:
        
            editMenu.grab_release()
    
    def addTag(self, name = None):
        
        #if nothin is selected, just do nothing
        if SEL_FIRST == SEL_LAST: return
        if name is not None:
            tag = self.createTag(name,"","","") # we will get other data later
        else:
            tag = TagCreator(self.root, self.currentUser).tag
            if tag is None: return # not data returned
            tag = self.createTag(tag.tagname, tag.auth, tag.text, tag.color)

        # add the tag
        if tag is None:
            return # dialog canceled
        self.textArea.tag_add(tag.tagname, SEL_FIRST, SEL_LAST)
        self.textArea.tag_configure(tag.tagname,  background = tag.color)
      
        self.textArea.tag_bind(tag.tagname, "<Enter>", tag.showinfo)
        self.textArea.tag_bind(tag.tagname, "<Leave>", tag.hideinfo)      
        


    def openFile(self):
        if self.onFileClose() == False : return
        self.currentfile = askopenfilename(defaultextension=".txt", 
                                      filetypes=[("All Files","*.*"), 
                                        ("Text Documents","*.txt")]) 
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
                        # Corrupted  tag data
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

            # Adding Tags Gathered

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
                        if len(limits) == 0 : continue # all tags of that kind were desroyed
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
        self.root.title('Untitled - Notepod')
        
    
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
            self.tagFrame.addButton(t, self.toggleTag)

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
            self.textArea.tag_delete(self.textArea.tag_names())
            self.textArea.delete('1.0', END)
            self.textArea.edit_modified(False)
            self.tags = []
            self.currentfile = None
        
        return toReturn
            
    def exit(self):
        if self.onFileClose(): self.root.destroy()

    def setUser(self):
        t = simpledialog.askstring('Notepod', 'Current user: ')
        if t is not None:
            self.currentUser = t
        else:
            self.currentUser = 'Default User'
        self.statusBarString.set('Editing as {}'.format(self.currentUser))

    def aboutInfo(self):
        # Display app info
        
        win = tk.Toplevel(self.root)
        win.title('About Notepod')
        win.resizable(0,0)
        f = tk.Frame(win, width = 200, height = 300)
        txt = tk.Text(f, font = 'Arial 14', background = 'white', width = 30, height = 15)
        txt.tag_config('allign', justify = CENTER)
        txt.insert('1.0', 'Notepod v1.0\n\nCreated on Python 3 and tkinter\nProject of Group 52\nClass: ECE_Y106, University of Patras\n' + 
                        '\nGroup Members\n-----------\nΜιχάλης Δροσιάδης\nΜιχάλης Ταλιαντζής\nΓιάννης Ηλιόπουλος\nΣωτήρης Βόκολος\nΤζωρτζίνα Μέρκου\nΓιώργος Ρίπης\n\n', 'allign')
        txt.config(state = DISABLED)
        txt.pack(expand = 0)
        f.pack()
        win.mainloop()

    def toggleTag(self, tag):
        
        if tag.active: 
            self.textArea.tag_config(tag.tagname, background = '#ffffff')
        else:
            self.textArea.tag_config(tag.tagname, background = tag.color)

        tag.active = not tag.active

# Class responsible to create the New Tag Dialog ------------------------------------------------------------------
class TagCreator(simpledialog.Dialog):
    
    def __init__(self, master, user):
        self.user = user
        super().__init__(master)
        
    def body(self, master):
        self.tag = None
        self.resizable(0,0)
        self.title('Add Tag - Notepod')

        Label(master, text = 'Tag Title:').grid(row = 0, column = 0)
        Label(master, text = 'Tag Author:').grid(row = 1, column = 0)
        Label(master, text = 'Tag Text:').grid(row = 2, column = 0)
        Label(master, text = 'Tag Color:').grid(row = 3, column = 0)

        self.titleEntry = Entry(master)
        self.authorEntry = Entry(master)
        self.authorEntry.insert(0, self.user)
        self.textEntry = Entry(master)

        self.titleEntry.grid(row = 0, column = 1, columnspan = 2)
        self.authorEntry.grid(row = 1, column = 1, columnspan = 2)
        self.textEntry.grid(row = 2, column = 1, columnspan = 2)

        self.color = '#ffff00'

        self.pickColorButton = Button(master, text = 'Pick Color', command = self.pickColor)
        self.colorPreview = tk.Canvas(master, width = 20, height = 20, background = self.color)
        self.colorPreview.grid(row = 3, column = 1)
        self.pickColorButton.grid(row = 3, column = 2)

    def pickColor(self):

        self.color = colorchooser.askcolor('yellow')[1]
        self.colorPreview.config(background = self.color)

    def apply(self):
        self.tag = Tag(self.titleEntry.get(), self.authorEntry.get(), self.textEntry.get(), self.color)
        self.tag.root = self._root()
        return 
        

# Class responsible to create objects to store the tag specific data and display the info popups ---------------------
class Tag:

    func = lambda name : None
    @classmethod
    def setFunc(cls, f):
        cls.func = f


    def __init__(self, title, auth, text, color):
        self.tagname = title
        self.auth = auth
        self.color = color
        self.text = text
        self.active = True
    
    def showinfo(self, event):
        if not self.active:
            self.taginfo = None
            return
        self.taginfo = tk.Frame(self.root, height = 100, width = 100, bg = self.color)
        Label(self.taginfo, bg = self.color, text = "Tag Name: {}".format(self.tagname)).pack()
        Label(self.taginfo, bg = self.color, text = "Tag Author: {}".format(self.auth)).pack()
        Label(self.taginfo, bg = self.color, text = "Tag Text: {}".format(self.text)).pack()

        self.taginfo.place(x = event.x, y = event.y + 10)
        self.taginfo.tkraise() 

    def hideinfo(self, event):
        if self.taginfo is None: return
        self.taginfo.destroy()

    def newTag(self):
        Tag.func(name = self.tagname)
    # Python Calls - Created for debuging
    def __eq__(self, other):
        return self.tagname == other.tagname
    
    def __str__(self):
        return "Name: {}\nAuthor: {}\nText: {}\nColor: {}".format(self.tagname, self.auth, self.text, self.color)

# Class to handle the right side 'Tag Toggling' Box --------------------------------------------------------------------   
class ButtonListFrame(tk.Frame):

    def __init__(self, master):
        self.master = master
        super().__init__(self.master, width =100, bg = 'skyblue')
        tk.Label(self, text = 'Toggle Tags', bg = 'skyblue', font = 'Arial 24').pack(side = TOP, fill = X)
        self.buttons = []
        
    def addButton(self, tag, func):
        b = tk.Button(self, text = tag.tagname + ' by ' + tag.auth, bg = tag.color, wraplength = 100, command = lambda : func(tag))
        b.pack(side = TOP, fill = X, pady = 10)
        self.buttons.append(b)

    def clearButtons(self):
        for button in self.buttons:
            button.destroy()

   
# Run Application
app = Notepod()


    
