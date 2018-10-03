#Developer: Tyler Smith
#Date:      11.06.16
#Purpose:   The cash flow statement application is the GUI 
#           and logic behind the popup that is displayed
#           when the user clicks the cash flow button 
#           on the main program.

from tkinter import *       # Import tkinter library 

from cashFlowSatementPopup import *     # Import cashFlowStatementPopup library

import sqlite3              # SQL Database

#This class is needed in order for the scrollbar to work. 
class AutoScrollbar(Scrollbar):
    # A scrollbar that hides itself if it's not needed.
    # Only works if you use the grid geometry manager!
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError("cannot use pack with this widget")
    def place(self, **kw):
        raise TclError("cannot use place with this widget")


#------------------------------------------------------------ Begin: Lists & Dictionaries
#--- Lists and dictionaries to hold objects and keep track of labels,
#--- entries and buttons. This allows us to change screen on the fly.
# Constant Lists and Dictionaries for things that aren't changing other than rows
constantNames = ["            Statement of Cash Flows            ", "(Values represented in $)",
                 "Space",                                             "Operating Cash Flow:",
                 "Space2",                                            "Investing Cash Flow:",
                 "Space3",                                            "Financing Cash Flow:",
                 "Space4",                                            "Net Increase in Cash:",
                 "Space5",                                            "Beginning Balance:",
                 "Ending Balance:",                                   "Space6",
                 "Space7"] 
constantEntries = {}
constantLabels  = {}
constantLblRows = {}
constantBtns = ["+ Add Operating Cash", "+ Add Investing Cash",
                "+ Add Financing Cash", "Update All Totals", "Save To Database"]
constantButtonObject = {}
constantBtnRows = [4, 7, 11, 18, 20]

# Operating Lists and Dictionaries (these dynamically change upon user actions)
operatingCash        = []
operatingLabels      = {}
operatingEntries     = {}
operatingCashRows = {}
operatingBtns        = {}
operatingEntryValues = {}

# Investing Lists and Dictionaries (these dynamically change upon user actions)
investingCash         = []
investingLabels       = {}
investingEntries      = {}
investingCashRows  = {}
investingBtns         = {}
investingEntryValues  = {}

# Financing Lists and Dictionaries (these dynamically change upon user actions)
financingCash        = []
financingLabels      = {}
financingEntries     = {}
financingCashRows = {}
financingBtns        = {}
financingEntryValues = {}
#-------------------------------------------------------------- End: Lists & Dictionaries

#-------------------------------------------------------------- Begin: Build up of rows for constant labels
# Build up the rows for the labels and entries on the screen
# when we initially load the program/screen
count = -1
for name in constantNames:
  count = (count + 1)
  if (count <= 3):
   constantLblRows[name] = count  
  elif (count > 3 and count < 6):
   constantLblRows[name] = (count + 1)
  elif (count > 5 and count < 7):
   constantLblRows[name] = (count + 2)
  elif (count > 6 and count < 8):
   constantLblRows[name] = (count + 3)
  elif (count > 7 and count < 14):
   constantLblRows[name] = (count + 4)
  elif (count > 13):
   constantLblRows[name] = (count + 5)
#-------------------------------------------------------------- End: Build up of rows for constant labels  

#-------------------------------------------------------------- Begin: Class of actual screen building
#                                                               and reacting to user activity
class cashFlowApp(Tk):        
  def __init__(self, companyName, fiscalYear):   # Constructor for GUI class
    Tk.__init__(self)
    self.companyName = companyName # Set variables for database use
    self.fiscalYear  = fiscalYear  # Set variables for database use

    #------------------------------------------- Begin: Frame building to get scrollbar in program
    vscrollbar = AutoScrollbar(self)
    vscrollbar.grid(row=0, column=3, sticky=N+S)

    canvas = Canvas(self, yscrollcommand=vscrollbar.set, width = 515, height = 600)
    canvas.grid(row=0, column = 1, sticky=N+S+E+W)

    vscrollbar.config(command=canvas.yview)

    # make the canvas expandable
    self.grid_rowconfigure(0, weight=3)
    self.grid_columnconfigure(0, weight=1)

    # create canvas contents
    self.frame = Frame(canvas, width = 200,height = 2000)
    self.frame.rowconfigure(1, weight=1)
    self.frame.columnconfigure(1, weight=1)

    canvas.create_window(0, 0, anchor=NW, window=self.frame)
    self.frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
 
    #---- Begin: Build labels and entries that the user can't change
    count = -1
    for name in constantNames:
     count = (count + 1)
     if (count == 0):                 # Title of popup
      lb = Label(self.frame, text = (constantNames[count]), font = ("Helvetica", "20"))           
      lb.grid(row = constantLblRows[name], columnspan = 3)
      constantLabels[name] = lb

     elif (count == 1):               # Subtitle under popup
      lb = Label(self.frame, text = (constantNames[count]), font = ("Helvetica", "12"))           
      lb.grid(row = constantLblRows[name], columnspan = 3)
      constantLabels[name] = lb
      
     else:
      if (name == 'Space' or name == 'Space2' or name == 'Space3'
          or name == 'Space4' or name == 'Space5'
          or name == 'Space6' or name == 'Space7'): # Big space in between everything else    
       lb = Label(self.frame, text = ' ', font = ("Helvetica", "14"))                     
       lb.grid(row = constantLblRows[name], columnspan = 2)
       constantLabels[name] = lb
       
      else:
       lb = Label(self.frame, text = (self.formatLabel(constantNames[count])), font = ("Helvetica", "16"))
       lb.grid(row = constantLblRows[name], column = 0)
       constantLabels[name] = lb
       
       #Some entry fields need to be non enterable with data
       if (name == 'Operating Cash Flow:' or name == 'Investing Cash Flow:' or 
           name == 'Financing Cash Flow:' or name == 'Net Increase in Cash:' or
           name == 'Ending Balance:'):
        e = Label(self.frame, bg = "#fff", anchor = "w", relief = "groove", width = 17)
        e.grid(row = constantLblRows[name], column = 1)
        constantEntries[name] = e
        
       #Other entry fields need to have enterable txt fields
       else:
        e = Entry(self.frame)
        e.grid(row = constantLblRows[name], column = 1)
        constantEntries[name] = e
    #---- End: Build labels and entries that the user can't change
        
    #---- Build buttons on screen that are always shown and can't change
    count = -1
    for name in constantBtns:
     count = (count + 1)
     btn = Button(self.frame, text = constantBtns[count], font = ("Helvetica", "8"))
     btn.grid(row = constantBtnRows[count], column = 1)
     
     # Different buttons require different commands
     if (name == "+ Add Operating Cash"):      
      btn["command"] = self.addOperatingCash
     elif (name == "+ Add Investing Cash"):
      btn["command"] = self.addInvestingCash
     elif (name == "+ Add Financing Cash"):
      btn["command"] = self.addFinancingCash
     elif (name == "Update All Totals"):
      btn.destroy()
      btn = Button(self.frame, text = constantBtns[count], font = ("Helvetica", "13")) 
      btn["command"] = self.updateAllTotals
      btn.grid(row = constantBtnRows[count], column = 1)
     elif (name == "Save To Database"):
      btn.destroy()
      btn = Button(self.frame, text = constantBtns[count], font = ("Helvetica", "13")) 
      btn["command"] = self.saveToDatabase
      btn.grid(row = constantBtnRows[count], column = 1) 
      
     constantButtonObject[name] = btn             # Save object in dictionary
    #---- End of building buttons on screen that are always shown and can't change

    # Update the totals of everything on the screen
    self.getDatabaseData()
    self.updateAllTotals()
  #----------------------------------------------- End: Intialization of class
     
  #----------------------------------------------- Begin: Methods that calculate all totals on our screen
  def getDatabaseData(self):
     # Build connection to database
     conn = sqlite3.connect("cashFlowDatabase.db")
     c = conn.cursor()

     #--------------------------------------------- Get header data from program
     #create a table
     c.execute("""CREATE TABLE IF NOT EXISTS cfht
                 (company       VARCHAR(20),
                  fiscal_year   VARCHAR(4),
                  beg_balance   VARCHAR(10),
                  PRIMARY KEY (company, fiscal_year))""")
     
     # Get everything from the header table
     existingData = c.execute("SELECT * FROM cfht where company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))
     count = 0
     for record in existingData:
      for field in record:
       count = count + 1
       # Prefill fields on selection screen
       if count == 3:
        e = constantEntries["Beginning Balance:"]             
        e.insert(END, field)

     #---------------------------------------------- Begin getting Item Data
     #create a table
     c.execute("""CREATE TABLE IF NOT EXISTS cfit
                 (company        VARCHAR(20),
                  fiscal_year    VARCHAR(4),
                  expenseName    VARCHAR(24),
                  valueOfExpense VARCHAR(10),
                  PRIMARY KEY (company, fiscal_year, expenseName))""")
     
     # Get everything from the item table
     nextValueFlagOper  = '' # Reference the values before if statements
     nextValueFlagInves = '' # Reference the values before if statements
     nextValueFlagFinan = '' # Reference the values before if statements
     
     #Insert default values for user to have as guide to each fin. statement
     defaultFound = ''
     defaultLoad = c.execute("SELECT * FROM cfit where company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))
     for record in defaultLoad:
      defaultFound = 'X'

     # Company hasn't ever before entered data, preload data for them 
     if defaultFound == '':
      # Purge pre-existing data
      c.execute("DELETE FROM cfit WHERE company = '' and fiscal_year = ''")
      # Insert data to be preloaded
      c.execute("INSERT INTO cfit VALUES (?, ?, ?, ?)",('', '', '> OC: Net Income', '23000'))
      c.execute("INSERT INTO cfit VALUES (?, ?, ?, ?)",('', '', '> OC: Account Rec.', '2000'))
      c.execute("INSERT INTO cfit VALUES (?, ?, ?, ?)",('', '', '> OC: Inventory Gain', '-3000'))

      c.execute("INSERT INTO cfit VALUES (?, ?, ?, ?)",('', '', '> IC: Capital Exp.', '25000'))
      c.execute("INSERT INTO cfit VALUES (?, ?, ?, ?)",('', '', '> IC: Property Sales', '6500'))

      c.execute("INSERT INTO cfit VALUES (?, ?, ?, ?)",('', '', '> FC: Long-term Debt', '5000'))
      c.execute("INSERT INTO cfit VALUES (?, ?, ?, ?)",('', '', '> FC: Cash Dividends', '2000'))

      result = c.execute("SELECT * FROM cfit where company = '' and fiscal_year = ''")
     else: 
      result = c.execute("SELECT * FROM cfit where company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))

     # Build screen
     for record in result:
      for field in record:
       #Operating cash If statements   
       if nextValueFlagOper == 'X':
        nextValueFlagOper = ''          #Reset for next field
        # Save new label and txt field from expense name
        operatingCash.append(expenseName)      #Add expense name to list
        operatingCashRows[expenseName] = constantBtnRows[0]  

        #----------------------------------------------------- Begin: destroying everything under
        #                                                      new expense to build screen back up
        self.destroyConstantNames(constantLblRows['Operating Cash Flow:'], 'Move Down')   # Destroy constant labels & entries
        self.destroyConstantButtons(constantLblRows['Operating Cash Flow:'], 'Move Down') # Destroy constant buttons

        self.destroyInvestingCash('Move Down')      # Destroy all things related to interest expenses
        self.destroyFinancingCash('Move Down')      # Destroy all things related to tax expenses
        
        #----------------------------------------------------- End: destroying everything under
        #                                                      new expense to build screen back up

        #----------------------------------------------------- Begin: Build new screen 
        # Build new label, entry & button on screen
        self.buildNewOperatingCash(expenseName, field)

        #-------------------- Pre-existing stuff to build back up

        # Build constant buttons on screen
        self.rebuildConstantButtons(constantLblRows['Operating Cash Flow:'])

        #Build interest labels, entries & buttons
        self.rebuildInvestingCash()
           
        #Build tax labels and entries
        self.rebuildFinancingCash()

        # Build constant labels and entries on screen
        self.rebuildConstantNames(constantLblRows['Operating Cash Flow:'])

        # Update the totals of everything on the screen
        self.updateAllTotals()
        #----------------------------------------------------- End: Build new screen

       if field[:5] == '> OC:':
        expenseName = field
        nextValueFlagOper = 'X'         #Flag initiated to get the next field value

       #Investing cash If statements   
       if nextValueFlagInves == 'X':
        nextValueFlagInves = ''         #Reset for next field
        
        #Save new label and txt field
        investingCash.append(expenseName)      #Add expense name to list
        investingCashRows[expenseName] = constantBtnRows[1] #Put label where button is located

        #----------------------------------------------------- Begin: destroying everything under
        #                                                      new expense to build screen back up
        self.destroyConstantNames(constantLblRows['Investing Cash Flow:'], 'Move Down')   # Destroy constant labels & entries
        self.destroyConstantButtons(constantLblRows['Investing Cash Flow:'], 'Move Down') # Destroy constant buttons

        self.destroyFinancingCash('Move Down')      # Destroy all things related to tax expenses
       
        #----------------------------------------------------- End: destroying everything under
        #                                                      new expense to build screen back up

        #----------------------------------------------------- Begin: Build new screen   
        # Build new label, entry & button on screen
        self.buildNewInvestingCash(expenseName, field)

        # Build buttons on screen
        self.rebuildConstantButtons(constantLblRows['Investing Cash Flow:'])

        #Build tax labels and entries
        self.rebuildFinancingCash() 
     
        # Build constant labels and entries on screen
        self.rebuildConstantNames(constantLblRows['Investing Cash Flow:'])
        
        # Update the totals of everything on the screen
        self.updateAllTotals()
        #----------------------------------------------------- End: Build new screen 

       if field[:5] == '> IC:':
        expenseName = field
        nextValueFlagInves = 'X'        #Flag initiated to get the next field value

       #Investing cash If statements   
       if nextValueFlagFinan == 'X':
        nextValueFlagFinan = ''         #Reset for next field
        
        #Save new label and txt field
        financingCash.append(expenseName)      #Add expense name to list
        financingCashRows[expenseName] = constantBtnRows[2] #Put label where button is located

        #----------------------------------------------------- Begin: destroying everything under
        #                                                      new expense to build screen back up
        self.destroyConstantNames(constantLblRows['Financing Cash Flow:'], 'Move Down')   # Destroy constant labels & entries
        self.destroyConstantButtons(constantLblRows['Financing Cash Flow:'], 'Move Down') # Destroy constant buttons
        #----------------------------------------------------- End: destroying everything under
        #                                                      new expense to build screen back up
      
        #----------------------------------------------------- Begin: Build new screen   
        # Build new label, entry & button on screen
        self.buildNewFinancingCash(expenseName, field)
     
        # Build buttons on screen
        self.rebuildConstantButtons(constantLblRows['Financing Cash Flow:'])

        # Build constant labels and entries on screen
        self.rebuildConstantNames(constantLblRows['Financing Cash Flow:'])
        
        # Update the totals of everything on the screen
        self.updateAllTotals()
        #----------------------------------------------------- End: Build new screen

       if field[:5] == '> FC:':
        expenseName = field
        nextValueFlagFinan = 'X'        #Flag initiated to get the next field value
     
     # Close connection
     c.close()         

  def updateAllTotals(self):
    self.setOperatingCash()  # Set Operating Cash Label
    self.setInvestingCash()  # Set Investing Cash Label
    self.setFinancingCash()  # Set Finacing  Cash Label
    self.setNetIncrease()    # Set Net Increase Label
    self.setBeginBalance()   # Set Beginning Balance Label
    self.setEndBalance()     # Set Ending    Balance Label

  def setOperatingCash(self):
     OC = float(0)               # Assign value before using it
     for name in operatingCash:   # Loop through OE's and add them up to find total
       # User could not put in value in entry they add, so we assign value zero
       if (operatingEntries[name].get()) == '':
         e = operatingEntries[name]
         e.insert(END, '0.0')

       operatingEntryValues[name] = float(operatingEntries[name].get()) # Save the value
       OC = (OC + float(operatingEntries[name].get()))         # Add on to our total  
     constantEntries["Operating Cash Flow:"]["text"] = float(OC) # Assign our final value

  def setInvestingCash(self):
     IC = float(0)               # Assign value before using it
     for name in investingCash:  # Loop through IE's and add them up to find total
       # User could not put in value in entry they add, so we assign value zero
       if (investingEntries[name].get()) == '':
         e = investingEntries[name]
         e.insert(END, '0.0')
         
       investingEntryValues[name] = float(investingEntries[name].get()) # Save the value  
       IC = (IC + float(investingEntries[name].get()))           # Add on to our total
     constantEntries["Investing Cash Flow:"]["text"] = float(IC) # Assign our final value

  def setFinancingCash(self):
     FC = float(0)                  # Assign value before using it
     for name in financingCash:     # Loop through TE's and add them up to find total
       # User could not put in value in entry they add, so we assign value zero
       if (financingEntries[name].get()) == '':
         e = financingEntries[name]
         e.insert(END, '0.0')

       financingEntryValues[name] = float(financingEntries[name].get()) # Save the value
       FC = (FC + float(financingEntries[name].get()))          # Add on to our total
     constantEntries["Financing Cash Flow:"]["text"] = float(FC) # Assign our final value

  def setNetIncrease(self):
     #if constantEntries["Net Increase in Cash:"].get() == '':
     # e = constantEntries["Net Increase in Cash:"]
     # e.insert(END, (float(constantEntries["Operating Cash Flow:"]["text"]) - float(constantEntries["Investing Cash Flow:"]["text"]) - float(constantEntries["Financing Cash Flow:"]["text"])))
     constantEntries["Net Increase in Cash:"]["text"] = (float(constantEntries["Operating Cash Flow:"]["text"])
                                                       - float(constantEntries["Investing Cash Flow:"]["text"])
                                                       - float(constantEntries["Financing Cash Flow:"]["text"]))
     
  def setBeginBalance(self):
     if (constantEntries["Beginning Balance:"].get() == ''):  # If this value isn't filled, give
       e = constantEntries["Beginning Balance:"]              # it the value of 0 for 
       e.insert(END, '0.0')                                   # calculation purposes

  def setEndBalance(self):
     if (constantEntries["Ending Balance:"]["text"] == ''):   # If this value isn't filled, give
       constantEntries["Ending Balance:"]["text"] == ''       # it the value of 0 for 
                                                              # calculation purposes

     constantEntries["Ending Balance:"]["text"] =  (float(constantEntries["Beginning Balance:"].get()) + (float(constantEntries["Net Increase in Cash:"]["text"])))
   
        
  #------------------------------------------------------ End: Methods that calculate totals   

  #------------------------------------------------------ Begin: Methods for formatting labels
  def formatLabel(self, labelString): # We want all of our labels to have a max of 24 characters
     formatLbl = True
     counter = 0
     countMax = (24 - len( labelString )) #Calculate how many spaces we need to make label 24 characters
     # Loop through and only allow labels to be length of 24
     while formatLbl == True:
      counter = (counter + 1)
      labelString = (' ' + labelString)
             
      if (counter == countMax):
        formatLbl = False
        
     return labelString    # Return formatted label text
  #------------------------------------------------------ End: Methods for formatting labels  

  #------------------------------------------------------ Begin: Methods for assigning action to new buttons
  def buttonMethodOperating(self, keyString):   
    btn = Button(self.frame, text = '<  Delete OC', font = ("Helvetica", "8"),
                 command = lambda: self.operatingBtnClick(keyString))
    btn.grid(row = operatingCashRows[keyString], column = 2)
    operatingBtns[keyString] = btn

  def buttonMethodInvesting(self, keyString):   
    btn = Button(self.frame, text = '<  Delete IC', font = ("Helvetica", "8"),
                 command = lambda: self.investingBtnClick(keyString))
    btn.grid(row = investingCashRows[keyString], column = 2)
    investingBtns[keyString] = btn

  def buttonMethodFinancing(self, keyString):   
    btn = Button(self.frame, text = '<  Delete FC', font = ("Helvetica", "8"),
                 command = lambda: self.financingBtnClick(keyString))
    btn.grid(row = financingCashRows[keyString], column = 2)
    financingBtns[keyString] = btn  
  #------------------------------------------------------ End: Methods for assigning action to new buttons

  #------------------------------------------------------ Begin: Methods for popups
  def runAddExpensePopup(self, expenseNameBeginning): 
    displayPopup = True
    popUp = finPopup()

    #Loop through popup and dont continue until data is recieved
    while(displayPopup == True):
     popUp.update()                    #Keeps popup looping, but not infinitely
     
     if(popUp.getExpenseName() != ''): # User has typed in expense name and pressed continue
      self.__expenseName = (expenseNameBeginning + popUp.getExpenseName()) # Bring strings together
      popUp.destroy()
      displayPopup = False     # Leave loop

    return self.__expenseName  # Return back the expense name that the user typed in
  #------------------------------------------------------ End: Methods for popups

  #------------------------------------------------------ Begin: Methods for destroying screen
  def destroyConstantNames(self, lowestRow, rowAction):
    # Loop through constantNames to delete labels lower than newly added expense
    count = -1
    for name in constantNames:
     count = (count + 1)  
     if (constantLblRows[name] > lowestRow):         # We only want labels lower than newly added expense
      if rowAction == 'Move Down':
        constantLblRows[name] = (constantLblRows[name] + 1) # Rows need to be shifted down one
      elif rowAction == 'Move Up':
        constantLblRows[name] = (constantLblRows[name] - 1) # Rows need to be shifted up one

      lb = constantLabels[name]      # Aquire label  
      lb.destroy()                   # Destroy label
      
      # Spaces shouldn't have entry boxs next to them
      if (name != 'Space'  and name != 'Space2' and
          name != 'Space3' and name != 'Space4' and
          name != 'Space5' and name != 'Space6' and name != 'Space7'):
       e  = constantEntries[name]    # Destroy all txt entries past Operating Expenses
       e.destroy()                   # Destroys entry

  def destroyConstantButtons(self, lowestRow, rowAction):
    # Loop through destroying buttons past new expense label
    count = -1
    for name in constantBtns:
     count = (count + 1)
     # We only want buttons past new expense label to get deleted
     if (constantBtnRows[count] > lowestRow):
      if rowAction == 'Move Down':
        constantBtnRows[count] = (constantBtnRows[count] + 1)    # Move buttons down one   
      elif rowAction == 'Move Up':
        constantBtnRows[count] = (constantBtnRows[count] - 1)    # Move buttons up one
        
      btn = constantButtonObject[name]                         # Aquire button
      btn.destroy()                                            # Destroy button

  def destroySpecialOperatingCash(self, btnId):
     #Destroy labels from operating expenses that could be below whatever are deleting
     count = -1
     for name in operatingCash:
      if (name == btnId): #Destroy actual label itself
       lb = operatingLabels[name]      # Load label from screen
       lb.destroy()                    # Delete label on screen

       e  = operatingEntries[name]     # Load Entry from screen 
       e.destroy()                     # Delete entry on screen

       btn = operatingBtns[name]       # Btn for label getting deleted
       btn.destroy()                   # Delete button on screen
       
      else:
       if((operatingCashRows[name]) > (operatingCashRows[btnId])):
        lb = operatingLabels[name]     # Aquire label
        operatingCashRows[name] = (operatingCashRows[name] - 1) # Rows need to moved up
        lb.destroy()                   # Destroy label
        
       else:
        lb = operatingLabels[name]     # Aquire label
        operatingCashRows[name] = (operatingCashRows[name])     # Rows need to be moved up
        lb.destroy()                   # Destroy label


       e  = operatingEntries[name]     # Aquire entry
       e.destroy()                     # Destroy entry

       btn = operatingBtns[name]       # Aquire button
       btn.destroy()                   # Destroy button

  def destroyFromOperatingLists(self, btnId):
    del operatingCashRows[btnId]     # Delete from dictionary 
    del operatingLabels[btnId]       # Delete from dictionary
    del operatingEntries[btnId]      # Delete from dictionary
    del operatingBtns[btnId]         # Delete from dictionary
    del operatingEntryValues[btnId]  # Delete from dictionary
    operatingCash.remove(btnId)  # Delete from list


  def destroyInvestingCash(self, rowAction):
    # Destroy all labels, entries, & buttons from interest expenses
    for name in investingCash:
      if rowAction == 'Move Down':
        investingCashRows[name] = (investingCashRows[name] + 1) # Rows need to be shifted down one
      elif rowAction == 'Move Up':
        investingCashRows[name] = (investingCashRows[name] - 1) # Rows need to be shifted up one

      lb = investingLabels[name]     # Aquire label        
      lb.destroy()                  # Destroy label

      e  = investingEntries[name]    # Aquire entry
      e.destroy()                   # Destroy entry

      btn = investingBtns[name]      # Aquire button
      btn.destroy()                 # Destroy button

  def destroySpecialInvestingCash(self, btnId):
     #Destroy labels from operating expenses that could be below whatever are deleting
     count = -1
     for name in investingCash:
      if (name == btnId):              #Destroy actual label itself
       lb = investingLabels[name]       # Load label from screen
       lb.destroy()                    # Delete label on screen

       e  = investingEntries[name]      # Load Entry from screen 
       e.destroy()                     # Delete entry on screen

       btn = investingBtns[name]        # Btn for label getting deleted
       btn.destroy()                   # Delete button on screen
       
      else:
       if((investingCashRows[name]) > (investingCashRows[btnId])):
        lb = investingLabels[name]      # Aquire label
        investingCashRows[name] = (investingCashRows[name] - 1) # Rows need to moved up
        lb.destroy()                   # Destroy label
        
       else:
        lb = investingLabels[name]      # Aquire label
        investingCashRows[name] = (investingCashRows[name])     # Rows need to be moved up
        lb.destroy()                   # Destroy label


       e  = investingEntries[name]      # Aquire entry
       e.destroy()                     # Destroy entry

       btn = investingBtns[name]        # Aquire button
       btn.destroy()                   # Destroy button

  def destroyFromInvestingLists(self, btnId):
    del investingCashRows[btnId]  # Delete from dictionary 
    del investingLabels[btnId]       # Delete from dictionary
    del investingEntries[btnId]      # Delete from dictionary
    del investingBtns[btnId]         # Delete from dictionary
    del investingEntryValues[btnId]  # Delete from dictionary
    investingCash.remove(btnId)  # Delete from list     

  def destroyFinancingCash(self, rowAction):
    # Destroy all labels, entries, & buttons from interest expenses
    for name in financingCash:
      if rowAction == 'Move Down':
        financingCashRows[name] = (financingCashRows[name] + 1) # Rows need to be shifted down one
      elif rowAction == 'Move Up':
        financingCashRows[name] = (financingCashRows[name] - 1) # Rows need to be shifted up one
      
      lb = financingLabels[name]         # Aquire label
      lb.destroy()                 # Destroy label
 
      e  = financingEntries[name]        # Aquire entry
      e.destroy()                  # Destroy entry

      btn = financingBtns[name]          # Aquire button
      btn.destroy()                # Destroy button

  def destroySpecialFinancingCash(self, btnId):
     #Destroy labels from operating expenses that could be below whatever are deleting
     count = -1
     for name in financingCash:
      if (name == btnId):              #Destroy actual label itself
       lb = financingLabels[name]            # Load label from screen
       lb.destroy()                    # Delete label on screen

       e  = financingEntries[name]           # Load Entry from screen 
       e.destroy()                     # Delete entry on screen

       btn = financingBtns[name]             # Btn for label getting deleted
       btn.destroy()                   # Delete button on screen
       
      else:
       if((financingCashRows[name]) > (financingCashRows[btnId])):
        lb = financingLabels[name]           # Aquire label
        financingCashRows[name] = (financingCashRows[name] - 1) # Rows need to moved up
        lb.destroy()                   # Destroy label
        
       else:
        lb = financingLabels[name]           # Aquire label
        financingCashRows[name] = (financingCashRows[name])     # Rows need to be moved up
        lb.destroy()                   # Destroy label


       e  = financingEntries[name]           # Aquire entry
       e.destroy()                     # Destroy entry

       btn = financingBtns[name]             # Aquire button
       btn.destroy()                   # Destroy button

  def destroyFromFinancingLists(self, btnId):
    del financingCashRows[btnId]  # Delete from dictionary 
    del financingLabels[btnId]       # Delete from dictionary
    del financingEntries[btnId]      # Delete from dictionary
    del financingBtns[btnId]         # Delete from dictionary
    del financingEntryValues[btnId]  # Delete from dictionary
    financingCash.remove(btnId)  # Delete from list         
  #------------------------------------------------------ End: Methods for destroying screen

  #------------------------------------------------------ Begin: Methods for new screen widjets
  def buildNewOperatingCash(self, operatingCashName, value = 0.0):
    # Build new Label
    lb = Label(self.frame, text = (self.formatLabel(operatingCashName)), font = ("Helvetica", "13"))
    lb.grid(row = operatingCashRows[operatingCashName], column = 0)
    operatingLabels[operatingCashName] = lb

    # Build new entry 
    e = Entry(self.frame)
    e.grid(row = operatingCashRows[operatingCashName], column = 1)
    e.insert(END, value)
    operatingEntries[operatingCashName] = e

    # Build new button that goes next to entry
    self.buttonMethodOperating(operatingCashName)

  def buildNewInvestingCash(self, investingCashName, value = 0.0):
    # Build new Label
    lb = Label(self.frame, text = (self.formatLabel(investingCashName)), font = ("Helvetica", "13"))
    lb.grid(row = investingCashRows[investingCashName], column = 0)
    investingLabels[investingCashName] = lb

    # Build new entry 
    e = Entry(self.frame)
    e.grid(row = investingCashRows[investingCashName], column = 1)
    e.insert(END, value)
    investingEntries[investingCashName] = e

    # Build new button that goes next to entry
    self.buttonMethodInvesting(investingCashName)

  def buildNewFinancingCash(self, financingCashName, value = 0.0):
    # Build new Label
    lb = Label(self.frame, text = (self.formatLabel(financingCashName)), font = ("Helvetica", "13"))
    lb.grid(row = financingCashRows[financingCashName], column = 0)
    financingLabels[financingCashName] = lb

    # Build new entry 
    e = Entry(self.frame)
    e.grid(row = financingCashRows[financingCashName], column = 1)
    e.insert(END, value)
    financingEntries[financingCashName] = e

    # Build new button that goes next to entry
    self.buttonMethodFinancing(financingCashName)  
  #------------------------------------------------------ End: Methods for new screen widjets

  #------------------------------------------------------ Begin: Methods for rebuilding screen
  def rebuildConstantNames(self, lowestRow):
    # Build constant labels and entries on screen
    count = -1
    for name in constantNames:
     count = (count + 1)
     if (constantLblRows[name] > lowestRow):         # We only want to rebuild the things we deleted
      if (name != 'Space' and name != 'Space2' and name != 'Space3' and
          name != 'Space4' and name != 'Space5' and name != 'Space6' and name != 'Space7'): # Big space in between everything else    
       lb = Label(self.frame, text = (self.formatLabel(constantNames[count])), font = ("Helvetica", "16"))
       lb.grid(row = constantLblRows[name], column = 0)
       constantLabels[name] = lb
       
       #Some entry fields need to be non enterable with data
       if (name == 'Operating Cash Flow:' or name == 'Investing Cash Flow:' or 
           name == 'Financing Cash Flow:' or name == 'Net Increase in Cash:' or
           name == 'Ending Balance:'):
        e = Label(self.frame, bg = "#fff", anchor = "w", relief = "groove", width = 17)
        e.grid(row = constantLblRows[name], column = 1)
        constantEntries[name] = e
        
       #Other entry fields need to have enterable txt fields
       else:
        e = Entry(self.frame)
        e.grid(row = constantLblRows[name], column = 1)
        constantEntries[name] = e

      #These are for the large spaces on the screen 
      else:
       lb = Label(self.frame, text = ' ', font = ("Helvetica", "14"))                     
       lb.grid(row = constantLblRows[name], columnspan = 2)
       constantLabels[name] = lb    

  def rebuildConstantButtons(self, lowestRow):
    # Build buttons on screen 
    count = -1
    for name in constantBtns:                      # Loop through all the constant buttons 
     count = (count + 1)
     if (constantBtnRows[count] > lowestRow):
      btn = Button(self.frame, text = constantBtns[count], font = ("Helvetica", "8"))
      btn.grid(row = constantBtnRows[count], column = 1) 
     
      if (name == "+ Add Operating Cash"):      
       btn["command"] = self.addOperatingCash
      elif (name == "+ Add Investing Cash"):
       btn["command"] = self.addInvestingCash
      elif (name == "+ Add Financing Cash"):
       btn["command"] = self.addFinancingCash
      elif (name == "Update All Totals"):
       btn.destroy()                               # Special button, it is bigger than others (has to be destroyed)
       btn = Button(self.frame, text = constantBtns[count], font = ("Helvetica", "13")) 
       btn["command"] = self.updateAllTotals       # Assign button command
       btn.grid(row = constantBtnRows[count], column = 1)
      elif (name == "Save To Database"):
       btn.destroy()
       btn = Button(self.frame, text = constantBtns[count], font = ("Helvetica", "13")) 
       btn["command"] = self.saveToDatabase
       btn.grid(row = constantBtnRows[count], column = 1) 
      
      constantButtonObject[name] = btn             # Save object in dictionary
      
  def rebuildOperatingCash(self):
    #Build operating labels, entries & buttons
    count = -1
    for name in operatingCash:                  # Loop through all operating expenses
       count = (count + 1)
       
       #Build label
       lb = Label(self.frame, text = (self.formatLabel(operatingCash[count])), font = ("Helvetica", "12"))
       lb.grid(row = operatingCashRows[name], column = 0)
       operatingLabels[name] = lb

       #Build entry
       e = Entry(self.frame)
       e.grid(row = operatingCashRows[name], column = 1)
       e.insert(END, operatingEntryValues[name]) 
       operatingEntries[name] = e

       #Build button
       self.buttonMethodOperating(name)


  def rebuildInvestingCash(self):
    #Build interest labels, entries & buttons
    count = -1
    for name in investingCash:                  # Loop through all interest expenses
       count = (count + 1)
       
       #Build label
       lb = Label(self.frame, text = (self.formatLabel(investingCash[count])), font = ("Helvetica", "12"))
       lb.grid(row = investingCashRows[name], column = 0)
       investingLabels[name] = lb

       #Build entry
       e = Entry(self.frame)
       e.grid(row = investingCashRows[name], column = 1)
       e.insert(END, investingEntryValues[name])
       investingEntries[name] = e

       #Build button
       self.buttonMethodInvesting(name)

  def rebuildFinancingCash(self):
    #Build tax labels and entries
    count = -1
    for name in financingCash:                       # Loop through all tax expenses
       count = (count + 1)

       # Build label
       lb = Label(self.frame, text = (self.formatLabel(financingCash[count])), font = ("Helvetica", "12"))
       lb.grid(row = financingCashRows[name], column = 0)
       financingLabels[name] = lb

       # Build entry
       e = Entry(self.frame)
       e.grid(row = financingCashRows[name], column = 1)
       e.insert(END, financingEntryValues[name])
       financingEntries[name] = e

       # Build button
       self.buttonMethodFinancing(name)
  #------------------------------------------------------ End: Methods for rebuilding screen

  #------------------------------------------------------ Begin: Methods for user adding new expenses when they hit an add button
  # Event that is triggered when continue button is pushed
  def addOperatingCash(self):
    # Bring up popup for user to enter in expense name
    expenseName = self.runAddExpensePopup('> OC: ')

    # Save new label and txt field from expense name
    operatingCash.append(expenseName)      #Add expense name to list
    operatingCashRows[expenseName] = constantBtnRows[0]  

    #----------------------------------------------------- Begin: destroying everything under
    #                                                      new expense to build screen back up
    self.destroyConstantNames(constantLblRows['Operating Cash Flow:'], 'Move Down')   # Destroy constant labels & entries
    self.destroyConstantButtons(constantLblRows['Operating Cash Flow:'], 'Move Down') # Destroy constant buttons

    self.destroyInvestingCash('Move Down') # Destroy all things related to interest expenses
    self.destroyFinancingCash('Move Down')      # Destroy all things related to tax expenses
    
    #----------------------------------------------------- End: destroying everything under
    #                                                      new expense to build screen back up

    #----------------------------------------------------- Begin: Build new screen 
    # Build new label, entry & button on screen
    self.buildNewOperatingCash(expenseName)

    #-------------------- Pre-existing stuff to build back up

    # Build constant buttons on screen
    self.rebuildConstantButtons(constantLblRows['Operating Cash Flow:'])

    #Build interest labels, entries & buttons
    self.rebuildInvestingCash()
       
    #Build tax labels and entries
    self.rebuildFinancingCash()

    # Build constant labels and entries on screen
    self.rebuildConstantNames(constantLblRows['Operating Cash Flow:'])

    # Update the totals of everything on the screen
    self.updateAllTotals()
    #----------------------------------------------------- End: Build new screen 
    
  def addInvestingCash(self):
     # Bring up popup for user to enter in expense name
     expenseName = self.runAddExpensePopup('> IC: ')

     #Save new label and txt field
     investingCash.append(expenseName)      #Add expense name to list
     investingCashRows[expenseName] = constantBtnRows[1] #Put label where button is located

     #----------------------------------------------------- Begin: destroying everything under
     #                                                      new expense to build screen back up
     self.destroyConstantNames(constantLblRows['Investing Cash Flow:'], 'Move Down')   # Destroy constant labels & entries
     self.destroyConstantButtons(constantLblRows['Investing Cash Flow:'], 'Move Down') # Destroy constant buttons

     self.destroyFinancingCash('Move Down')      # Destroy all things related to tax expenses

     #----------------------------------------------------- End: destroying everything under
     #                                                      new expense to build screen back up

     #----------------------------------------------------- Begin: Build new screen   
     # Build new label, entry & button on screen
     self.buildNewInvestingCash(expenseName)

     # Build buttons on screen
     self.rebuildConstantButtons(constantLblRows['Investing Cash Flow:'])

     #Build tax labels and entries
     self.rebuildFinancingCash() 
     
     # Build constant labels and entries on screen
     self.rebuildConstantNames(constantLblRows['Investing Cash Flow:'])

     # Update the totals of everything on the screen
     self.updateAllTotals()
     #----------------------------------------------------- End: Build new screen 

     
  def addFinancingCash(self):
     # Bring up popup for user to enter in expense name
     expenseName = self.runAddExpensePopup('> FC: ')

     #Save new label and txt field
     financingCash.append(expenseName)      #Add expense name to list
     financingCashRows[expenseName] = constantBtnRows[2] #Put label where button is located

     #----------------------------------------------------- Begin: destroying everything under
     #                                                      new expense to build screen back up
     self.destroyConstantNames(constantLblRows['Financing Cash Flow:'], 'Move Down')   # Destroy constant labels & entries
     self.destroyConstantButtons(constantLblRows['Financing Cash Flow:'], 'Move Down') # Destroy constant buttons
     #----------------------------------------------------- End: destroying everything under
     #                                                      new expense to build screen back up
      
     #----------------------------------------------------- Begin: Build new screen   
     # Build new label, entry & button on screen
     self.buildNewFinancingCash(expenseName)
     
     # Build buttons on screen
     self.rebuildConstantButtons(constantLblRows['Financing Cash Flow:'])

     # Build constant labels and entries on screen
     self.rebuildConstantNames(constantLblRows['Financing Cash Flow:'])

     # Update the totals of everything on the screen
     self.updateAllTotals()
     #----------------------------------------------------- End: Build new screen
     
  def saveToDatabase(self):
     
     #Build connection to database
     conn = sqlite3.connect("cashFlowDatabase.db")
     c = conn.cursor()

     #--------------------------------------------- Get header data from program
     #create a table
     c.execute("""CREATE TABLE IF NOT EXISTS cfht
                 (company       VARCHAR(20),
                  fiscal_year   VARCHAR(4),
                  beg_balance   VARCHAR(10),
                  PRIMARY KEY (company, fiscal_year))""")
     
     for name in constantNames:
      if name == "Beginning Balance:":
       begBalance  = (constantEntries[name].get()) # Store locally for use in insert statement

     # Save everything to the header table
     somethingExists = ''
     existingData = c.execute("SELECT * FROM cfht where company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))
     for record in existingData:
      somethingExists = 'X'
      
     if somethingExists == '':
      c.execute("INSERT INTO cfht VALUES (?, ?, ?)",
               (self.companyName, self.fiscalYear, begBalance))
      
     else: 
      c.execute("DELETE FROM cfht WHERE company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))
      c.execute("INSERT INTO cfht VALUES (?, ?, ?)",
               (self.companyName, self.fiscalYear, begBalance))
     #---------------------------------------------- End of Header Data
      
     #---------------------------------------------- Begin getting Item Data
     #create a table
     c.execute("""CREATE TABLE IF NOT EXISTS cfit
                 (company        VARCHAR(20),
                  fiscal_year    VARCHAR(4),
                  expenseName    VARCHAR(24),
                  valueOfExpense VARCHAR(10),
                  PRIMARY KEY (company, fiscal_year, expenseName))""")
     
     # Get rid of everything because we will rebuild database
     c.execute("DELETE FROM cfit WHERE company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))

     # Add operating cash to database
     for name in operatingCash:   # Loop through
       # Save the value in the database
       c.execute("INSERT INTO cfit VALUES (?, ?, ?, ?)",
               (self.companyName, self.fiscalYear, name, operatingEntries[name].get()))

     # Add investing cash to database
     for name in investingCash:   # Loop through 
       # Save the value in the database
       c.execute("INSERT INTO cfit VALUES (?, ?, ?, ?)",
               (self.companyName, self.fiscalYear, name, investingEntries[name].get()))  
     
     # Add financing cash to database
     for name in financingCash:     # Loop through 
       # Save the value in the database
       c.execute("INSERT INTO cfit VALUES (?, ?, ?, ?)",
               (self.companyName, self.fiscalYear, name, financingEntries[name].get()))
     #---------------------------------------------- End getting Item Data

     # Make changes permanent  
     conn.commit()
     c.close()    
     
  def operatingBtnClick(self, btnId):
     #----------------------------------------------------- Begin: destroying everything under
     #                                                      expense to build screen back up
     self.destroyConstantNames(constantLblRows['Operating Cash Flow:'], 'Move Up')   # Destroy constant labels & entries
     self.destroyConstantButtons(constantLblRows['Operating Cash Flow:'], 'Move Up') # Destroy constant buttons

     self.destroySpecialOperatingCash(btnId)
        
     self.destroyInvestingCash('Move Up') # Destroy all things related to interest expenses
     self.destroyFinancingCash('Move Up')      # Destroy all things related to tax expenses

     # Delete out of list and dictionaries
     self.destroyFromOperatingLists(btnId)
     #----------------------------------------------------- End: destroying everything under
     #                                                      new expense to build screen back up
    
     #----------------------------------------------------- Begin: Build new screen 
     # Rebuild constant buttons on screen
     self.rebuildConstantButtons(constantLblRows['Operating Cash Flow:'])

     # Build operating labels, entries, and buttons
     self.rebuildOperatingCash()

     # Build interest labels, entries, and buttons
     self.rebuildInvestingCash()
      
     # Build tax labels, entries, and buttons   
     self.rebuildFinancingCash()

     # Build constant labels and entries on screen
     self.rebuildConstantNames(constantLblRows['Operating Cash Flow:'])

     # Update the totals of everything on the screen
     self.updateAllTotals()
     #----------------------------------------------------- End: Build new screen 
           
  def investingBtnClick(self, btnId):
     #----------------------------------------------------- Begin: destroying everything under
     #                                                      expense to build screen back up
     self.destroyConstantNames(constantLblRows['Investing Cash Flow:'], 'Move Up')   # Destroy constant labels & entries
     self.destroyConstantButtons(constantLblRows['Investing Cash Flow:'], 'Move Up') # Destroy constant buttons

     self.destroySpecialInvestingCash(btnId) # Destroy certain interest expenses 
        
     self.destroyFinancingCash('Move Up')         # Destroy all things related to tax expenses

     # Delete out of list and dictionaries
     self.destroyFromInvestingLists(btnId)
     #----------------------------------------------------- End: destroying everything under
     #                                                      new expense to build screen back up

     #----------------------------------------------------- Begin: Build new screen 
     # Rebuild constant buttons on screen
     self.rebuildConstantButtons(constantLblRows['Investing Cash Flow:'])

     # Build interest labels, entries, and buttons
     self.rebuildInvestingCash()
      
     # Build tax labels, entries, and buttons   
     self.rebuildFinancingCash()

     # Build constant labels and entries on screen
     self.rebuildConstantNames(constantLblRows['Investing Cash Flow:'])

     # Update the totals of everything on the screen
     self.updateAllTotals()
     #----------------------------------------------------- End: Build new screen 
      
  def financingBtnClick(self, btnId):
     #----------------------------------------------------- Begin: destroying everything under
     #                                                      expense to build screen back up
     self.destroyConstantNames(constantLblRows['Financing Cash Flow:'], 'Move Up')   # Destroy constant labels & entries
     self.destroyConstantButtons(constantLblRows['Financing Cash Flow:'], 'Move Up') # Destroy constant buttons

     self.destroySpecialFinancingCash(btnId)        # Destroy certain interest expenses 
        
     # Delete out of list and dictionaries
     self.destroyFromFinancingLists(btnId)
     #----------------------------------------------------- End: destroying everything under
     #                                                      new expense to build screen back up

     #----------------------------------------------------- Begin: Build new screen 
     # Rebuild constant buttons on screen
     self.rebuildConstantButtons(constantLblRows['Financing Cash Flow:'])
      
     # Build tax labels, entries, and buttons   
     self.rebuildFinancingCash()

     # Build constant labels and entries on screen
     self.rebuildConstantNames(constantLblRows['Financing Cash Flow:'])

     # Update the totals of everything on the screen
     self.updateAllTotals()
     #----------------------------------------------------- End: Build new screen
     

        
def main():
  myGui = cashFlowApp()                  # Instantiate myGUI object to begin building GUI
 
  myGui.mainloop()


#Run main function
if(__name__ == "__main__"):
  main()

