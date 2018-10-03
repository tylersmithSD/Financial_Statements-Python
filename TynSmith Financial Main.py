#Developer: Tyler Smith
#Date:      11.06.16
#Purpose:   This is the main program where the
#           user types in their company name and
#           fiscal year to be used with financial
#           information. The three documents used are
#           great for finding out a companies health.
#           This information could be used by investors,
#           stakeholders or managers to determine the health
#           of a company based on the industry the company is in.

from tkinter import *         # Import tkinter library 

from incomeStatementApplication   import *  # Import GUI for Income Statement

from balanceSheetApplication      import *  # Import GUI for Balance Sheet

from cashFlowStatementApplication import *  # Import GUI from Cash Flow Statement

class mainApp(Tk):        
  def __init__(self):   # Constructor for GUI class
    Tk.__init__(self)   # 
    self.addTitle()     #
    self.addUserInfo()  #
    self.addButtons()   #
    

  # Put title on GUI
  def addTitle(self):
    Label(self, text = "     Financial Statement Options    ", font =
          ("Helvetica", "16", "bold italic")).grid(columnspan = 2, row = 0)
    Label(self, text = "------------------------------------------", font =
          ("Helvetica", "16")).grid(columnspan = 2, row = 1)

  def addUserInfo(self):
    Label(self, text = "Company Name:", font =
          ("Helvetica", "12")).grid(column = 0, row = 2)
    self.compName = Entry(self)
    self.compName.grid(column = 1, row = 2)
    
    Label(self, text = "Fiscal Year:", font =
          ("Helvetica", "12")).grid(column = 0, row = 3)
    self.fiscYear = Entry(self)
    self.fiscYear.grid(column = 1, row = 3)
    
    Label(self, text = "------------------------------------------", font =
          ("Helvetica", "16")).grid(columnspan = 2, row = 4)  

  # Put buttons on GUI
  def addButtons(self):
    self.btn = Button(self, text = 'Income Statement', font =
                      ("Helvetica", "14"))
    self.btn.grid(row = 5, columnspan = 2)                      
    self.btn["command"] = self.incomeTrigger

    Label(self, text = "", font =                                 
         ("Helvetica", "16")).grid(columnspan = 2)   # Big Space between each button 

    self.btn = Button(self, text = 'Balance Sheet', font = ("Helvetica", "14"))
    self.btn.grid(row = 7, columnspan = 2)
    self.btn["command"] = self.balanceTrigger    

    Label(self, text = "", font =                                
          ("Helvetica", "16", "bold italic")).grid(columnspan = 2)  # Big Space between each button 

    self.btn = Button(self, text = 'Cash Flow Statement', font =("Helvetica", "14"))                       
    self.btn.grid(row = 9, columnspan = 2)
    self.btn["command"] = self.cashTrigger

    Label(self, text = "", font =
          ("Helvetica", "16", "bold italic")).grid(columnspan = 2)  # Big space after last button

  def incomeTrigger(self):                        # When income button is clicked, income application
    self.incomeApplicationRun  = incomeStatementApp(self.compName.get(), self.fiscYear.get())
    self.incomeApplicationRun.mainloop()
    
  def balanceTrigger(self):                       # When balance button is clicked, balance application
    balanceApplicationRun = balanceSheetApp(self.compName.get(), self.fiscYear.get()) # will be ran and GUI will be displayed
    balanceApplicationRun.mainloop()

  def cashTrigger(self):                          # When cash button is clicked, cash application
    cashApplicationRun = cashFlowApp(self.compName.get(), self.fiscYear.get()) # will be ran and GUI will be displayed
    cashApplicationRun.mainloop()
    
   
def main():
  mainGui = mainApp()                  # Instantiate myGUI object to begin building GUI  
  mainGui.mainloop()

#Run main function
if(__name__ == "__main__"):
  main() 

