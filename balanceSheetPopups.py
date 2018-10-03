#Developer: Tyler Smith
#Date:      11.06.16
#Purpose:   This is the popup that is activated
#           when the user adds an asset or liability
#           to their balance sheet. 

from tkinter import *       # Import tkinter library

class assetPopup(Tk):
  def __init__(self):       # Constructor of the class that gets ran when called
    Tk.__init__(self)
    
    # Big space on screen   
    Label(self, text = "", font = ("Helvetica", "12")).grid(row = 0, columnspan = 2)
    
    # Title of popup
    Label(self, text = "            Asset Information             ", font = ("Helvetica", "16")).grid(row = 1, columnspan = 2)

    # Big space on screen   
    Label(self, text = "", font = ("Helvetica", "14")).grid(row = 2, columnspan = 2)

    # Asset Name label
    Label(self, text = "Asset Name", font = ("Helvetica", "14")).grid(row = 3, column = 0)
    self.txtAssetName = Entry(self, width = 20) # Asset Name entry
    self.txtAssetName.grid(row = 3, column = 1) #
    
    # Big space on screen
    Label(self, text = "", font = ("Helvetica", "14")).grid(row = 4, columnspan = 2)
    
    #Continue Button
    self.btnContinue = Button(self, text = 'Continue', font = ("Helvetica", "14"))
    self.btnContinue.grid(row = 5, column = 1)
    self.btnContinue["command"] = self.Continue
    self.assetName = ''

    Label(self, text = "", font = ("Helvetica", "10")).grid(row = 6, columnspan = 2)  

  def Continue(self):
    self.assetName = self.txtAssetName.get()

  def getAssetName(self):  
    return self.assetName[:18]   # Limit the user to only a certain amount of characters

class liabilityPopup(Tk):
  def __init__(self):       # Constructor of the class that gets ran when
    Tk.__init__(self)
    
    # Big space on screen   
    Label(self, text = "", font = ("Helvetica", "12")).grid(row = 0, columnspan = 2)
    
    # Title of popup
    Label(self, text = "            Liability Information             ", font = ("Helvetica", "16")).grid(row = 1, columnspan = 2)

    # Big space on screen   
    Label(self, text = "", font = ("Helvetica", "14")).grid(row = 2, columnspan = 2)

    # Expense Name label
    Label(self, text = "Liability Name", font = ("Helvetica", "14")).grid(row = 3, column = 0)
    self.txtLiabilityName = Entry(self, width = 20) # Expense Name entry
    self.txtLiabilityName.grid(row = 3, column = 1) #
    
    # Big space on screen
    Label(self, text = "", font = ("Helvetica", "14")).grid(row = 4, columnspan = 2)
    
    #Continue Button
    self.btnContinue = Button(self, text = 'Continue', font = ("Helvetica", "14"))
    self.btnContinue.grid(row = 5, column = 1)
    self.btnContinue["command"] = self.Continue
    self.liabilityName = ''

    Label(self, text = "", font = ("Helvetica", "10")).grid(row = 6, columnspan = 2)  

  def Continue(self):
    self.liabilityName = self.txtLiabilityName.get()

  def getLiabilityName(self):  
    return self.liabilityName[:18]  # Limit the user to only a certain amount of characters
    

