#Developer: Tyler Smith
#Date:      11.06.16
#Purpose:   This is the popup that is activated
#           when the user decides to add a new
#           activity to their cash flow statement.

from tkinter import *       # Import tkinter library

class finPopup(Tk):
  def __init__(self):       # Constructor of the class that gets ran when
    Tk.__init__(self)
    
    # Big space on screen   
    Label(self, text = "", font = ("Helvetica", "12")).grid(row = 0, columnspan = 2)
    
    # Title of popup
    Label(self, text = "            Cash Activity Information             ", font = ("Helvetica", "16")).grid(row = 1, columnspan = 2)

    # Big space on screen   
    Label(self, text = "", font = ("Helvetica", "14")).grid(row = 2, columnspan = 2)

    # Expense Name label
    Label(self, text = "Cash Activity Name", font = ("Helvetica", "14")).grid(row = 3, column = 0)
    self.txtCashActivity = Entry(self, width = 20) # Cash Activity Name entry
    self.txtCashActivity.grid(row = 3, column = 1) #
    
    # Big space on screen
    Label(self, text = "", font = ("Helvetica", "14")).grid(row = 4, columnspan = 2)
    
    #Continue Button
    self.btnContinue = Button(self, text = 'Continue', font = ("Helvetica", "14"))
    self.btnContinue.grid(row = 5, column = 1)
    self.btnContinue["command"] = self.Continue
    self.cashActivity = ''

    Label(self, text = "", font = ("Helvetica", "10")).grid(row = 6, columnspan = 2)  

  def Continue(self):
    self.cashActivity = self.txtCashActivity.get()

  def getExpenseName(self):  
    return self.cashActivity[:18]


    

