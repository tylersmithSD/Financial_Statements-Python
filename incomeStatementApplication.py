#Developer: Tyler Smith
#Date:      11.06.16
#Purpose:   The income statement application is the GUI 
#           and logic behind the popup that is displayed
#           when the user clicks the income button on the 
#           main program.

from tkinter import *       # Import tkinter library 

from incomeSatementPopup import * # Import incomeStatementPopup library

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
constantNames = ["                Income Statement               ", "(Values represented in $)",
                 "Space", "Net Revenue:", "Cost of Goods:","Space2", "Gross Profit:",
                 "Operating Expenses:", "Space3", "Operating Income:", "Interest Expenses:",
                 "Tax Expenses:", "Space4", "Net Income:", "Space5", "Space6"] 
constantEntries = {}
constantLabels  = {}
constantLblRows = {}
constantBtns = ["+ Add Operating Expense", "+ Add Interest Expense",
                "+ Add Tax Expense", "Update All Totals", "Save To Database"]
constantButtonObject = {}
constantBtnRows = [8, 12, 14, 18, 20]

# Operating Lists and Dictionaries (these dynamically change upon user actions)
operatingExpenses    = []
operatingLabels      = {}
operatingEntries     = {}
operatingExpenseRows = {}
operatingBtns        = {}
operatingEntryValues = {}

# Interest Lists and Dictionaries (these dynamically change upon user actions)
interestExpenses     = []
interestLabels       = {}
interestEntries      = {}
interestExpenseRows  = {}
interestBtns         = {}
interestEntryValues  = {}

# Tax Lists and Dictionaries (these dynamically change upon user actions)
taxExpenses    = []
taxLabels      = {}
taxEntries     = {}
taxExpenseRows = {}
taxBtns        = {}
taxEntryValues = {}
#-------------------------------------------------------------- End: Lists & Dictionaries

#-------------------------------------------------------------- Begin: Build up of rows for constant labels
# Build up the rows for the labels and entries on the screen
# when we initially load the program/screen
count = -1
for name in constantNames:
  count = (count + 1)
  if (count <= 7):
   constantLblRows[name] = count  
  elif (count > 7 and count < 11):
   constantLblRows[name] = (count + 1)
  elif (count > 10 and count < 12):
   constantLblRows[name] = (count + 2)
  elif (count > 11 and count < 15):
   constantLblRows[name] = (count + 3)
  elif (count > 14):
   constantLblRows[name] = (count + 4)
#-------------------------------------------------------------- End: Build up of rows for constant labels  


#-------------------------------------------------------------- Begin: Class of actual screen building
#                                                               and reacting to user activity
class incomeStatementApp(Tk):        
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
          or name == 'Space4' or name == 'Space5' or name == 'Space6'): # Big space in between everything else    
       lb = Label(self.frame, text = ' ', font = ("Helvetica", "14"))                     
       lb.grid(row = constantLblRows[name], columnspan = 2)
       constantLabels[name] = lb
       
      else:
       lb = Label(self.frame, text = (self.formatLabel(constantNames[count])), font = ("Helvetica", "16"))
       lb.grid(row = constantLblRows[name], column = 0)
       constantLabels[name] = lb
       
       #Some entry fields need to be non enterable with data
       if (name == 'Gross Profit:' or name == 'Operating Expenses:' or 
           name == 'Operating Income:' or name == 'Interest Expenses:' or
           name == 'Tax Expenses:' or name == 'Net Income:'):
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
     if (name == "+ Add Operating Expense"):      
      btn["command"] = self.addOperatingExpense
     elif (name == "+ Add Interest Expense"):
      btn["command"] = self.addInterestExpense
     elif (name == "+ Add Tax Expense"):
      btn["command"] = self.addTaxExpense
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
    self.getDatabaseData()       # Set Net Revenue and cost of goods from database
    self.updateAllTotals()  
  #----------------------------------------------- End: Intialization of class
     
  #----------------------------------------------- Begin: Methods that calculate all totals on our screen
  def getDatabaseData(self):
     # Build connection to database
     conn = sqlite3.connect("incomeStatementDatabase.db")
     c = conn.cursor()

     #create a table
     c.execute("""CREATE TABLE IF NOT EXISTS isht
                 (company       VARCHAR(20),
                  fiscal_year   VARCHAR(4),
                  net_revenue   VARCHAR(10),
                  cost_of_goods VARCHAR(10),
                  PRIMARY KEY (company, fiscal_year))""")
     
     # Get everything from the header table
     existingData = c.execute("SELECT * FROM isht where company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))
     count = 0
     for record in existingData:
      for field in record:
       count = count + 1
       # Prefill fields on selection screen
       if   count == 3:
        e = constantEntries["Net Revenue:"]             
        e.insert(END, field)
       elif count == 4:
        e = constantEntries["Cost of Goods:"]             
        e.insert(END, field)

     # If table doesnt exist, build it. 
     c.execute("""CREATE TABLE IF NOT EXISTS isit
                 (company        VARCHAR(20),
                  fiscal_year    VARCHAR(4),
                  expenseName    VARCHAR(24),
                  valueOfExpense VARCHAR(10),
                  PRIMARY KEY (company, fiscal_year, expenseName))""")   

     # Get everything from the item table
     nextValueFlagOper  = '' # Reference the values before if statements
     nextValueFlagInter = '' # Reference the values before if statements
     nextValueFlagTax   = '' # Reference the values before if statements

     # Insert default values for user to have as guide to each fin. statement
     defaultFound = ''
     defaultLoad = c.execute("SELECT * FROM isit where company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))
     for record in defaultLoad:
      defaultFound = 'X'
 
     # Company hasn't ever before entered data, preload data for them 
     if defaultFound == '':
      # Purge pre-existing data
      c.execute("DELETE FROM isit WHERE company = '' and fiscal_year = ''")
      
      # Insert data to be preloaded
      c.execute("INSERT INTO isit VALUES (?, ?, ?, ?)",('', '', '> OE: Selling Expenses', '23000'))
      c.execute("INSERT INTO isit VALUES (?, ?, ?, ?)",('', '', '> OE: Admin Expenses', '2000'))
     
      c.execute("INSERT INTO isit VALUES (?, ?, ?, ?)",('', '', '> IE: Deposits', '5000'))
      c.execute("INSERT INTO isit VALUES (?, ?, ?, ?)",('', '', '> IE: Trading Account', '20000'))

      c.execute("INSERT INTO isit VALUES (?, ?, ?, ?)",('', '', '> TE: Property Tax', '10000'))
      c.execute("INSERT INTO isit VALUES (?, ?, ?, ?)",('', '', '> TE: Income Tax', '8000'))


      result = c.execute("SELECT * FROM isit where company = '' and fiscal_year = ''")
     else: 
      result = c.execute("SELECT * FROM isit where company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))

     # Build screen
     for record in result:
      for field in record:
       # Operating Expense If statements   
       if nextValueFlagOper == 'X':
        nextValueFlagOper = ''          #Reset for next field
        
        # Save new label and txt field from expense name
        operatingExpenses.append(expenseName)      #Add expense name to list
        operatingExpenseRows[expenseName] = constantBtnRows[0]  

        #----------------------------------------------------- Begin: destroying everything under
        #                                                      new expense to build screen back up
        self.destroyConstantNames(constantLblRows['Operating Expenses:'], 'Move Down')   # Destroy constant labels & entries
        self.destroyConstantButtons(constantLblRows['Operating Expenses:'], 'Move Down') # Destroy constant buttons

        self.destroyInterestExpenses('Move Down') # Destroy all things related to interest expenses
        self.destroyTaxExpenses('Move Down')      # Destroy all things related to tax expenses
    
        #----------------------------------------------------- End: destroying everything under
        #                                                      new expense to build screen back up
      
        #----------------------------------------------------- Begin: Build new screen 

        # Build new label, entry & button on screen
        self.buildNewOperatingExpense(expenseName, field)

        #-------------------- Pre-existing stuff to build back up

        # Build constant buttons on screen
        self.rebuildConstantButtons(constantLblRows['Operating Expenses:'])

        #Build interest labels, entries & buttons
        self.rebuildInterestExpenses()
           
        #Build tax labels and entries
        self.rebuildTaxExpenses()

        # Build constant labels and entries on screen
        self.rebuildConstantNames(constantLblRows['Operating Expenses:'])

        # Update the totals of everything on the screen
        self.updateAllTotals()
        #----------------------------------------------------- End: Build new screen
            
       if field[:5] == '> OE:':
        expenseName = field
        nextValueFlagOper = 'X'         #Flag initiated to get the next field value
       #---------------------------------- End of operating expense if statements

       #---------------------------------- Interest Expense If statements   
       if nextValueFlagInter == 'X':
        nextValueFlagInter = ''          #Reset for next field

        #Save new label and txt field
        interestExpenses.append(expenseName)      #Add expense name to list
        interestExpenseRows[expenseName] = constantBtnRows[1] #Put label where button is located

        #----------------------------------------------------- Begin: destroying everything under
        #                                                      new expense to build screen back up
        self.destroyConstantNames(constantLblRows['Interest Expenses:'], 'Move Down')   # Destroy constant labels & entries
        self.destroyConstantButtons(constantLblRows['Interest Expenses:'], 'Move Down') # Destroy constant buttons

        self.destroyTaxExpenses('Move Down')      # Destroy all things related to tax expenses

        #----------------------------------------------------- End: destroying everything under
        #                                                      new expense to build screen back up

        #----------------------------------------------------- Begin: Build new screen   
        # Build new label, entry & button on screen
        self.buildNewInterestExpense(expenseName, field)

        # Build buttons on screen
        self.rebuildConstantButtons(constantLblRows['Interest Expenses:'])

        #Build tax labels and entries
        self.rebuildTaxExpenses() 
     
        # Build constant labels and entries on screen
        self.rebuildConstantNames(constantLblRows['Interest Expenses:'])

        # Update the totals of everything on the screen
        self.updateAllTotals()
        #----------------------------------------------------- End: Build new screen 
        
       if field[:5] == '> IE:':
        expenseName = field
        nextValueFlagInter = 'X'         #Flag initiated to get the next field value
       #--------------------------------- End of interest expense if statements

       #---------------------------------- Interest Expense If statements   
       if nextValueFlagTax == 'X':
        nextValueFlagTax = ''          #Reset for next field
        #Save new label and txt field
        taxExpenses.append(expenseName)      #Add expense name to list
        taxExpenseRows[expenseName] = constantBtnRows[2] #Put label where button is located

        #----------------------------------------------------- Begin: destroying everything under
        #                                                      new expense to build screen back up
        self.destroyConstantNames(constantLblRows['Tax Expenses:'], 'Move Down')   # Destroy constant labels & entries
        self.destroyConstantButtons(constantLblRows['Tax Expenses:'], 'Move Down') # Destroy constant buttons


        #----------------------------------------------------- End: destroying everything under
        #                                                      new expense to build screen back up
      
        #----------------------------------------------------- Begin: Build new screen   
        # Build new label, entry & button on screen
        self.buildNewTaxExpense(expenseName, field)
     
        # Build buttons on screen
        self.rebuildConstantButtons(constantLblRows['Tax Expenses:'])

        # Build constant labels and entries on screen
        self.rebuildConstantNames(constantLblRows['Tax Expenses:'])

        # Update the totals of everything on the screen
        self.updateAllTotals()
        #----------------------------------------------------- End: Build new screen

       if field[:5] == '> TE:':
        expenseName = field
        nextValueFlagTax = 'X'         #Flag initiated to get the next field value
       #--------------------------------- End of interest expense if statements 
        
      
     # Close connection
     c.close()      
      
  def updateAllTotals(self):
    self.setGrossProfit()      # Set Gross Profit Label
    self.setOperatingExpense() # Set Operating Expenses Label
    self.setOperatingIncome()  # Set Operating Income Label
    self.setInterestExpense()  # Set Interest Expense Label
    self.setTaxExpense()       # Set Tax Expense Label
    self.setNetIncome()        # Set Net Income Label
    
  def setGrossProfit(self):  
     # If statements serve as fail safe if user doesnt enter in value
     if(constantEntries["Net Revenue:"].get() == ''):   # If this value isn't filled, give    
       e = constantEntries["Net Revenue:"]              # it the value of 0 for 
       e.insert(END, '0.0')                             # calculation purposes
       
     if(constantEntries["Cost of Goods:"].get() == ''): # If this value isn't filled, give
       e = constantEntries["Cost of Goods:"]            # it the value of 0 for 
       e.insert(END, '0.0')                             # calculation purposes
       
     # Assign Gross Profit label a value  
     constantEntries["Gross Profit:"]["text"] = (float(constantEntries["Net Revenue:"].get())
                                                - float(constantEntries["Cost of Goods:"].get()))
  def setOperatingExpense(self):
     OPE = float(0)                   # Assign value before using it
     for name in operatingExpenses:   # Loop through OE's and add them up to find total
       # User could not put in value in entry they add, so we assign value zero
       if (operatingEntries[name].get()) == '':
         e = operatingEntries[name]
         e.insert(END, '0.0')

       operatingEntryValues[name] = float(operatingEntries[name].get()) # Save the value
       OPE = (OPE + float(operatingEntries[name].get()))         # Add on to our total  
     constantEntries["Operating Expenses:"]["text"] = float(OPE) # Assign our final value

  def setOperatingIncome(self):
     # Assign our final Value
     constantEntries["Operating Income:"]["text"] = (float((constantEntries["Gross Profit:"]["text"])) -
                                                     float((constantEntries["Operating Expenses:"]["text"])))

  def setInterestExpense(self):
     IE = float(0)                  # Assign value before using it
     for name in interestExpenses:  # Loop through IE's and add them up to find total
       # User could not put in value in entry they add, so we assign value zero
       if (interestEntries[name].get()) == '':
         e = interestEntries[name]
         e.insert(END, '0.0')
         
       interestEntryValues[name] = float(interestEntries[name].get()) # Save the value  
       IE = (IE + float(interestEntries[name].get()))          # Add on to our total
     constantEntries["Interest Expenses:"]["text"] = float(IE) # Assign our final value

  def setTaxExpense(self):
     TE = float(0)                  # Assign value before using it
     for name in taxExpenses:       # Loop through TE's and add them up to find total
       # User could not put in value in entry they add, so we assign value zero
       if (taxEntries[name].get()) == '':
         e = taxEntries[name]
         e.insert(END, '0.0')

       taxEntryValues[name] = float(taxEntries[name].get()) # Save the value  
       TE = (TE + float(taxEntries[name].get()))          # Add on to our total
     constantEntries["Tax Expenses:"]["text"] = float(TE) # Assign our final value

  def setNetIncome(self):  
     constantEntries["Net Income:"]["text"] = (float(constantEntries["Operating Income:"]["text"])
                                             - float(constantEntries["Interest Expenses:"]["text"])
                                             - float(constantEntries["Tax Expenses:"]["text"]))
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
  def buttonMethod(self, keyString):   
    btn = Button(self.frame, text = '<  Delete OE', font = ("Helvetica", "8"),
                 command = lambda: self.operatingBtnClick(keyString))
    btn.grid(row = operatingExpenseRows[keyString], column = 2)
    operatingBtns[keyString] = btn

  def buttonMethodInterest(self, keyString):   
    btn = Button(self.frame, text = '<  Delete IE', font = ("Helvetica", "8"),
                 command = lambda: self.interestBtnClick(keyString))
    btn.grid(row = interestExpenseRows[keyString], column = 2)
    interestBtns[keyString] = btn

  def buttonMethodTax(self, keyString):   
    btn = Button(self.frame, text = '<  Delete TE', font = ("Helvetica", "8"),
                 command = lambda: self.taxBtnClick(keyString))
    btn.grid(row = taxExpenseRows[keyString], column = 2)
    taxBtns[keyString] = btn  
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
      if (name != 'Space3' and name != 'Space4' and
          name != 'Space5' and name != 'Space6'):
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

  def destroySpecialOperatingExpenses(self, btnId):
     #Destroy labels from operating expenses that could be below whatever are deleting
     count = -1
     for name in operatingExpenses:
      if (name == btnId): #Destroy actual label itself
       lb = operatingLabels[name]      # Load label from screen
       lb.destroy()                    # Delete label on screen

       e  = operatingEntries[name]     # Load Entry from screen 
       e.destroy()                     # Delete entry on screen

       btn = operatingBtns[name]       # Btn for label getting deleted
       btn.destroy()                   # Delete button on screen
       
      else:
       if((operatingExpenseRows[name]) > (operatingExpenseRows[btnId])):
        lb = operatingLabels[name]     # Aquire label
        operatingExpenseRows[name] = (operatingExpenseRows[name] - 1) # Rows need to moved up
        lb.destroy()                   # Destroy label
        
       else:
        lb = operatingLabels[name]     # Aquire label
        operatingExpenseRows[name] = (operatingExpenseRows[name])     # Rows need to be moved up
        lb.destroy()                   # Destroy label


       e  = operatingEntries[name]     # Aquire entry
       e.destroy()                     # Destroy entry

       btn = operatingBtns[name]       # Aquire button
       btn.destroy()                   # Destroy button

  def destroyFromOperatingLists(self, btnId):
    del operatingExpenseRows[btnId]  # Delete from dictionary 
    del operatingLabels[btnId]       # Delete from dictionary
    del operatingEntries[btnId]      # Delete from dictionary
    del operatingBtns[btnId]         # Delete from dictionary
    del operatingEntryValues[btnId]  # Delete from dictionary
    operatingExpenses.remove(btnId)  # Delete from list

  def destroyInterestExpenses(self, rowAction):
    # Destroy all labels, entries, & buttons from interest expenses
    for name in interestExpenses:
      if rowAction == 'Move Down':
        interestExpenseRows[name] = (interestExpenseRows[name] + 1) # Rows need to be shifted down one
      elif rowAction == 'Move Up':
        interestExpenseRows[name] = (interestExpenseRows[name] - 1) # Rows need to be shifted up one

      lb = interestLabels[name]     # Aquire label        
      lb.destroy()                  # Destroy label

      e  = interestEntries[name]    # Aquire entry
      e.destroy()                   # Destroy entry

      btn = interestBtns[name]      # Aquire button
      btn.destroy()                 # Destroy button

  def destroySpecialInterestExpenses(self, btnId):
     #Destroy labels from operating expenses that could be below whatever are deleting
     count = -1
     for name in interestExpenses:
      if (name == btnId):              #Destroy actual label itself
       lb = interestLabels[name]       # Load label from screen
       lb.destroy()                    # Delete label on screen

       e  = interestEntries[name]      # Load Entry from screen 
       e.destroy()                     # Delete entry on screen

       btn = interestBtns[name]        # Btn for label getting deleted
       btn.destroy()                   # Delete button on screen
       
      else:
       if((interestExpenseRows[name]) > (interestExpenseRows[btnId])):
        lb = interestLabels[name]      # Aquire label
        interestExpenseRows[name] = (interestExpenseRows[name] - 1) # Rows need to moved up
        lb.destroy()                   # Destroy label
        
       else:
        lb = interestLabels[name]      # Aquire label
        interestExpenseRows[name] = (interestExpenseRows[name])     # Rows need to be moved up
        lb.destroy()                   # Destroy label


       e  = interestEntries[name]      # Aquire entry
       e.destroy()                     # Destroy entry

       btn = interestBtns[name]        # Aquire button
       btn.destroy()                   # Destroy button

  def destroyFromInterestLists(self, btnId):
    del interestExpenseRows[btnId]  # Delete from dictionary 
    del interestLabels[btnId]       # Delete from dictionary
    del interestEntries[btnId]      # Delete from dictionary
    del interestBtns[btnId]         # Delete from dictionary
    del interestEntryValues[btnId]  # Delete from dictionary
    interestExpenses.remove(btnId)  # Delete from list     

  def destroyTaxExpenses(self, rowAction):
    # Destroy all labels, entries, & buttons from interest expenses
    for name in taxExpenses:
      if rowAction == 'Move Down':
        taxExpenseRows[name] = (taxExpenseRows[name] + 1) # Rows need to be shifted down one
      elif rowAction == 'Move Up':
        taxExpenseRows[name] = (taxExpenseRows[name] - 1) # Rows need to be shifted up one
      
      lb = taxLabels[name]         # Aquire label
      lb.destroy()                 # Destroy label
 
      e  = taxEntries[name]        # Aquire entry
      e.destroy()                  # Destroy entry

      btn = taxBtns[name]          # Aquire button
      btn.destroy()                # Destroy button

  def destroySpecialTaxExpenses(self, btnId):
     #Destroy labels from operating expenses that could be below whatever are deleting
     count = -1
     for name in taxExpenses:
      if (name == btnId):              #Destroy actual label itself
       lb = taxLabels[name]            # Load label from screen
       lb.destroy()                    # Delete label on screen

       e  = taxEntries[name]           # Load Entry from screen 
       e.destroy()                     # Delete entry on screen

       btn = taxBtns[name]             # Btn for label getting deleted
       btn.destroy()                   # Delete button on screen
       
      else:
       if((taxExpenseRows[name]) > (taxExpenseRows[btnId])):
        lb = taxLabels[name]           # Aquire label
        taxExpenseRows[name] = (taxExpenseRows[name] - 1) # Rows need to moved up
        lb.destroy()                   # Destroy label
        
       else:
        lb = taxLabels[name]           # Aquire label
        taxExpenseRows[name] = (taxExpenseRows[name])     # Rows need to be moved up
        lb.destroy()                   # Destroy label


       e  = taxEntries[name]           # Aquire entry
       e.destroy()                     # Destroy entry

       btn = taxBtns[name]             # Aquire button
       btn.destroy()                   # Destroy button

  def destroyFromTaxLists(self, btnId):
    del taxExpenseRows[btnId]  # Delete from dictionary 
    del taxLabels[btnId]       # Delete from dictionary
    del taxEntries[btnId]      # Delete from dictionary
    del taxBtns[btnId]         # Delete from dictionary
    del taxEntryValues[btnId]  # Delete from dictionary
    taxExpenses.remove(btnId)  # Delete from list         
  #------------------------------------------------------ End: Methods for destroying screen

  #------------------------------------------------------ Begin: Methods for new screen widjets
  def buildNewOperatingExpense(self, operatingExpenseName, value = 0.0):
    # Build new Label
    lb = Label(self.frame, text = (self.formatLabel(operatingExpenseName)), font = ("Helvetica", "13"))
    lb.grid(row = operatingExpenseRows[operatingExpenseName], column = 0)
    operatingLabels[operatingExpenseName] = lb

    # Build new entry 
    e = Entry(self.frame)
    e.grid(row = operatingExpenseRows[operatingExpenseName], column = 1)
    e.insert(END, value)
    operatingEntries[operatingExpenseName] = e

    # Build new button that goes next to entry
    self.buttonMethod(operatingExpenseName)

  def buildNewInterestExpense(self, interestExpenseName, value = 0.0):
    # Build new Label
    lb = Label(self.frame, text = (self.formatLabel(interestExpenseName)), font = ("Helvetica", "13"))
    lb.grid(row = interestExpenseRows[interestExpenseName], column = 0)
    interestLabels[interestExpenseName] = lb

    # Build new entry 
    e = Entry(self.frame)
    e.grid(row = interestExpenseRows[interestExpenseName], column = 1)
    e.insert(END, value)
    interestEntries[interestExpenseName] = e

    # Build new button that goes next to entry
    self.buttonMethodInterest(interestExpenseName)

  def buildNewTaxExpense(self, taxExpenseName, value = 0.0):
    # Build new Label
    lb = Label(self.frame, text = (self.formatLabel(taxExpenseName)), font = ("Helvetica", "13"))
    lb.grid(row = taxExpenseRows[taxExpenseName], column = 0)
    taxLabels[taxExpenseName] = lb

    # Build new entry 
    e = Entry(self.frame)
    e.grid(row = taxExpenseRows[taxExpenseName], column = 1)
    e.insert(END, value)
    taxEntries[taxExpenseName] = e

    # Build new button that goes next to entry
    self.buttonMethodTax(taxExpenseName)  
  #------------------------------------------------------ End: Methods for new screen widjets

  #------------------------------------------------------ Begin: Methods for rebuilding screen
  def rebuildConstantNames(self, lowestRow):
    # Build constant labels and entries on screen
    count = -1
    for name in constantNames:
     count = (count + 1)
     if (constantLblRows[name] > lowestRow):         # We only want to rebuild the things we deleted
      if (name != 'Space3' and name != 'Space4' and
          name != 'Space5' and name != 'Space6'):    # If it isn't a space do this 
       lb = Label(self.frame, text = (self.formatLabel(constantNames[count])), font = ("Helvetica", "16"))
       lb.grid(row = constantLblRows[name], column = 0)
       constantLabels[name] = lb
       
       #Some entry fields need to be non enterable with data
       if (name == 'Gross Profit:' or name == 'Operating Expenses:' or 
           name == 'Operating Income:' or name == 'Interest Expenses:' or
           name == 'Tax Expenses:' or name == 'Net Income:'):
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
     
      if (name == "+ Add Operating Expense"):      # Different buttons require different command
       btn["command"] = self.addOperatingExpense   # Assign button command
      elif (name == "+ Add Interest Expense"):
       btn["command"] = self.addInterestExpense    # Assign button command
      elif (name == "+ Add Tax Expense"):
       btn["command"] = self.addTaxExpense         # Assign button command
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
      
  def rebuildOperatingExpenses(self):
    #Build operating labels, entries & buttons
    count = -1
    for name in operatingExpenses:                  # Loop through all operating expenses
       count = (count + 1)
       
       #Build label
       lb = Label(self.frame, text = (self.formatLabel(operatingExpenses[count])), font = ("Helvetica", "12"))
       lb.grid(row = operatingExpenseRows[name], column = 0)
       operatingLabels[name] = lb

       #Build entry
       e = Entry(self.frame)
       e.grid(row = operatingExpenseRows[name], column = 1)
       e.insert(END, operatingEntryValues[name]) 
       operatingEntries[name] = e

       #Build button
       self.buttonMethod(name)


  def rebuildInterestExpenses(self):
    #Build interest labels, entries & buttons
    count = -1
    for name in interestExpenses:                  # Loop through all interest expenses
       count = (count + 1)
       
       #Build label
       lb = Label(self.frame, text = (self.formatLabel(interestExpenses[count])), font = ("Helvetica", "12"))
       lb.grid(row = interestExpenseRows[name], column = 0)
       interestLabels[name] = lb

       #Build entry
       e = Entry(self.frame)
       e.grid(row = interestExpenseRows[name], column = 1)
       e.insert(END, interestEntryValues[name])
       interestEntries[name] = e

       #Build button
       self.buttonMethodInterest(name)

  def rebuildTaxExpenses(self):
    #Build tax labels and entries
    count = -1
    for name in taxExpenses:                       # Loop through all tax expenses
       count = (count + 1)

       # Build label
       lb = Label(self.frame, text = (self.formatLabel(taxExpenses[count])), font = ("Helvetica", "12"))
       lb.grid(row = taxExpenseRows[name], column = 0)
       taxLabels[name] = lb

       # Build entry
       e = Entry(self.frame)
       e.grid(row = taxExpenseRows[name], column = 1)
       e.insert(END, taxEntryValues[name])
       taxEntries[name] = e

       # Build button
       self.buttonMethodTax(name)
  #------------------------------------------------------ End: Methods for rebuilding screen

  #------------------------------------------------------ Begin: Methods for user adding new expenses when they hit an add button
  # Event that is triggered when calculate button is pushed
  def addOperatingExpense(self):
    # Bring up popup for user to enter in expense name
    expenseName = self.runAddExpensePopup('> OE: ')

    # Save new label and txt field from expense name
    operatingExpenses.append(expenseName)      #Add expense name to list
    operatingExpenseRows[expenseName] = constantBtnRows[0]  

    #----------------------------------------------------- Begin: destroying everything under
    #                                                      new expense to build screen back up
    self.destroyConstantNames(constantLblRows['Operating Expenses:'], 'Move Down')   # Destroy constant labels & entries
    self.destroyConstantButtons(constantLblRows['Operating Expenses:'], 'Move Down') # Destroy constant buttons

    self.destroyInterestExpenses('Move Down') # Destroy all things related to interest expenses
    self.destroyTaxExpenses('Move Down')      # Destroy all things related to tax expenses
    
    #----------------------------------------------------- End: destroying everything under
    #                                                      new expense to build screen back up
      
    #----------------------------------------------------- Begin: Build new screen 

    # Build new label, entry & button on screen
    self.buildNewOperatingExpense(expenseName)

    #-------------------- Pre-existing stuff to build back up

    # Build constant buttons on screen
    self.rebuildConstantButtons(constantLblRows['Operating Expenses:'])

    #Build interest labels, entries & buttons
    self.rebuildInterestExpenses()
       
    #Build tax labels and entries
    self.rebuildTaxExpenses()

    # Build constant labels and entries on screen
    self.rebuildConstantNames(constantLblRows['Operating Expenses:'])

    # Update the totals of everything on the screen
    self.updateAllTotals()
    #----------------------------------------------------- End: Build new screen 

    
  def addInterestExpense(self):
     # Bring up popup for user to enter in expense name
     expenseName = self.runAddExpensePopup('> IE: ')

     #Save new label and txt field
     interestExpenses.append(expenseName)      #Add expense name to list
     interestExpenseRows[expenseName] = constantBtnRows[1] #Put label where button is located

     #----------------------------------------------------- Begin: destroying everything under
     #                                                      new expense to build screen back up
     self.destroyConstantNames(constantLblRows['Interest Expenses:'], 'Move Down')   # Destroy constant labels & entries
     self.destroyConstantButtons(constantLblRows['Interest Expenses:'], 'Move Down') # Destroy constant buttons

     self.destroyTaxExpenses('Move Down')      # Destroy all things related to tax expenses

     #----------------------------------------------------- End: destroying everything under
     #                                                      new expense to build screen back up

     #----------------------------------------------------- Begin: Build new screen   
     # Build new label, entry & button on screen
     self.buildNewInterestExpense(expenseName)

     # Build buttons on screen
     self.rebuildConstantButtons(constantLblRows['Interest Expenses:'])

     #Build tax labels and entries
     self.rebuildTaxExpenses() 
     
     # Build constant labels and entries on screen
     self.rebuildConstantNames(constantLblRows['Interest Expenses:'])

     # Update the totals of everything on the screen
     self.updateAllTotals()
     #----------------------------------------------------- End: Build new screen 

     
  def addTaxExpense(self):
     # Bring up popup for user to enter in expense name
     expenseName = self.runAddExpensePopup('> TE: ')

     #Save new label and txt field
     taxExpenses.append(expenseName)      #Add expense name to list
     taxExpenseRows[expenseName] = constantBtnRows[2] #Put label where button is located

     #----------------------------------------------------- Begin: destroying everything under
     #                                                      new expense to build screen back up
     self.destroyConstantNames(constantLblRows['Tax Expenses:'], 'Move Down')   # Destroy constant labels & entries
     self.destroyConstantButtons(constantLblRows['Tax Expenses:'], 'Move Down') # Destroy constant buttons


     #----------------------------------------------------- End: destroying everything under
     #                                                      new expense to build screen back up
      
       
     #----------------------------------------------------- Begin: Build new screen   
     # Build new label, entry & button on screen
     self.buildNewTaxExpense(expenseName)
     
     # Build buttons on screen
     self.rebuildConstantButtons(constantLblRows['Tax Expenses:'])

     # Build constant labels and entries on screen
     self.rebuildConstantNames(constantLblRows['Tax Expenses:'])

     # Update the totals of everything on the screen
     self.updateAllTotals()
     #----------------------------------------------------- End: Build new screen 

  def saveToDatabase(self):
     
     #Build connection to database
     conn = sqlite3.connect("incomeStatementDatabase.db")
     c = conn.cursor()

     #--------------------------------------------- Get header data from program
     #create a table
     c.execute("""CREATE TABLE IF NOT EXISTS isht
                 (company       VARCHAR(20),
                  fiscal_year   VARCHAR(4),
                  net_revenue   VARCHAR(10),
                  cost_of_goods VARCHAR(10),
                  PRIMARY KEY (company, fiscal_year))""")
     
     for name in constantNames:
      if name == "Net Revenue:":
       netRevenue  = (constantEntries[name].get()) # Store locally for use in insert statement
      elif name == "Cost of Goods:":
       costOfGoods = (constantEntries[name].get()) # Store locally for use in insert statement

     # Save everything to the header table
     somethingExists = ''
     existingData = c.execute("SELECT * FROM isht where company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))
     for record in existingData:
      somethingExists = 'X'
      
     if somethingExists == '':
      c.execute("INSERT INTO isht VALUES (?, ?, ?, ?)",
               (self.companyName, self.fiscalYear, netRevenue, costOfGoods))
      
     else: 
      c.execute("DELETE FROM isht WHERE company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))
      c.execute("INSERT INTO isht VALUES (?, ?, ?, ?)",
               (self.companyName, self.fiscalYear, netRevenue, costOfGoods))
     #---------------------------------------------- End of Header Data
      
     #---------------------------------------------- Begin getting Item Data
     #create a table
     c.execute("""CREATE TABLE IF NOT EXISTS isit
                 (company        VARCHAR(20),
                  fiscal_year    VARCHAR(4),
                  expenseName    VARCHAR(24),
                  valueOfExpense VARCHAR(10),
                  PRIMARY KEY (company, fiscal_year, expenseName))""")
     
     # Get rid of everything because we will rebuild database
     c.execute("DELETE FROM isit WHERE company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))

     # Add operating expenses to database
     for name in operatingExpenses:   # Loop through OE's and add them up to find total
       # Save the value in the database
       c.execute("INSERT INTO isit VALUES (?, ?, ?, ?)",
               (self.companyName, self.fiscalYear, name, operatingEntries[name].get()))

     # Add interest expenses to database
     for name in interestExpenses:   # Loop through OE's and add them up to find total
       # Save the value in the database
       c.execute("INSERT INTO isit VALUES (?, ?, ?, ?)",
               (self.companyName, self.fiscalYear, name, interestEntries[name].get()))  
     
     # Add interest expenses to database
     for name in taxExpenses:   # Loop through OE's and add them up to find total
       # Save the value in the database
       c.execute("INSERT INTO isit VALUES (?, ?, ?, ?)",
               (self.companyName, self.fiscalYear, name, taxEntries[name].get()))
     #---------------------------------------------- End getting Item Data

     # Make changes permanent  
     conn.commit()
     c.close() 
     
  def operatingBtnClick(self, btnId):
     #----------------------------------------------------- Begin: destroying everything under
     #                                                      expense to build screen back up
     self.destroyConstantNames(constantLblRows['Operating Expenses:'], 'Move Up')   # Destroy constant labels & entries
     self.destroyConstantButtons(constantLblRows['Operating Expenses:'], 'Move Up') # Destroy constant buttons

     self.destroySpecialOperatingExpenses(btnId)
        
     self.destroyInterestExpenses('Move Up') # Destroy all things related to interest expenses
     self.destroyTaxExpenses('Move Up')      # Destroy all things related to tax expenses

     # Delete out of list and dictionaries
     self.destroyFromOperatingLists(btnId)
     #----------------------------------------------------- End: destroying everything under
     #                                                      new expense to build screen back up
    
     #----------------------------------------------------- Begin: Build new screen 
     # Rebuild constant buttons on screen
     self.rebuildConstantButtons(constantLblRows['Operating Expenses:'])

     # Build operating labels, entries, and buttons
     self.rebuildOperatingExpenses()

     # Build interest labels, entries, and buttons
     self.rebuildInterestExpenses()
      
     # Build tax labels, entries, and buttons   
     self.rebuildTaxExpenses()

     # Build constant labels and entries on screen
     self.rebuildConstantNames(constantLblRows['Operating Expenses:'])

     # Update the totals of everything on the screen
     self.updateAllTotals()
     #----------------------------------------------------- End: Build new screen 
           
  def interestBtnClick(self, btnId):
     #----------------------------------------------------- Begin: destroying everything under
     #                                                      expense to build screen back up
     self.destroyConstantNames(constantLblRows['Interest Expenses:'], 'Move Up')   # Destroy constant labels & entries
     self.destroyConstantButtons(constantLblRows['Interest Expenses:'], 'Move Up') # Destroy constant buttons

     self.destroySpecialInterestExpenses(btnId) # Destroy certain interest expenses 
        
     self.destroyTaxExpenses('Move Up')         # Destroy all things related to tax expenses

     # Delete out of list and dictionaries
     self.destroyFromInterestLists(btnId)
     #----------------------------------------------------- End: destroying everything under
     #                                                      new expense to build screen back up

     #----------------------------------------------------- Begin: Build new screen 
     # Rebuild constant buttons on screen
     self.rebuildConstantButtons(constantLblRows['Interest Expenses:'])

     # Build interest labels, entries, and buttons
     self.rebuildInterestExpenses()
      
     # Build tax labels, entries, and buttons   
     self.rebuildTaxExpenses()

     # Build constant labels and entries on screen
     self.rebuildConstantNames(constantLblRows['Interest Expenses:'])

     # Update the totals of everything on the screen
     self.updateAllTotals()
     #----------------------------------------------------- End: Build new screen 
      
  def taxBtnClick(self, btnId):
     #----------------------------------------------------- Begin: destroying everything under
     #                                                      expense to build screen back up
     self.destroyConstantNames(constantLblRows['Tax Expenses:'], 'Move Up')   # Destroy constant labels & entries
     self.destroyConstantButtons(constantLblRows['Tax Expenses:'], 'Move Up') # Destroy constant buttons

     self.destroySpecialTaxExpenses(btnId)        # Destroy certain interest expenses 
        
     # Delete out of list and dictionaries
     self.destroyFromTaxLists(btnId)
     #----------------------------------------------------- End: destroying everything under
     #                                                      new expense to build screen back up

     #----------------------------------------------------- Begin: Build new screen 
     # Rebuild constant buttons on screen
     self.rebuildConstantButtons(constantLblRows['Tax Expenses:'])
      
     # Build tax labels, entries, and buttons   
     self.rebuildTaxExpenses()

     # Build constant labels and entries on screen
     self.rebuildConstantNames(constantLblRows['Tax Expenses:'])

     # Update the totals of everything on the screen
     self.updateAllTotals()
     #----------------------------------------------------- End: Build new screen
     
        
def main():
  myGui = incomeStatementApp()                  # Instantiate myGUI object to begin building GUI
 
  myGui.mainloop()


#Run main function
if(__name__ == "__main__"):
  main()

