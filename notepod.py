import tkinter as tk

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

        '''
        #Ένα Label
        self.myLabel = tk.Label(self.root, text = 'Hello World!', font = 'Arial', bg = 'white', fg = 'blue', anchor = CENTER)
        self.myLabel.pack(fill = BOTH, expand = 1)
        '''

        #TextArea

        self.textArea = tk.Text(self.root)
        self.textArea.pack(fill = BOTH, expand = 1)
        

        #Έναρξη βρόγχου παραθύρου
        self.root.mainloop()


app = Notepod()


    
