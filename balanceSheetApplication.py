#Developer: Tyler Smith
#Date:      11.06.16
#Purpose:   The balance sheet application is the GUI 
#           and logic behind the popup that is displayed
#           when the user clicks the balance sheet button 
#           on the main program.

from tkinter import *            # Import tkinter library 

from balanceSheetPopups import * # Import BalanceSheetPopups library

import sqlite3                   # SQL Database

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
constantNames   = ["                Balance Sheet               ", "(Values represented in $)",
                   "Space",                                        "Current Assets:",
                   "Space2",                                       "Current Liabilities:",
                   "Space3",                                       "Owner's Equity:",
                   "Space4",                                       "Space5"]
constantEntries = {}
constantLabels  = {}
constantLblRows = {}
constantBtns    = ["+ Add Current Asset", "+ Add Current Liability",
                   "Update All Totals", "Save To Database"]
constantButtonObject = {}
constantBtnRows = [4, 7, 11, 13]

# Operating Lists and Dictionaries (these dynamically change upon user actions)
currentAssets = []
assetLabels   = {}
assetEntries  = {}
assetRows     = {}
assetBtns     = {}
assetEntryValues = {}

# Interest Lists and Dictionaries (these dynamically change upon user actions)
currentLiabilities  = []
liabilityLabels = {}
liabilityEntries = {}
liabilityRows = {}
liabilityBtns = {}
liabilityEntryValues = {}
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
  elif (count > 5 and count < 9): 
   constantLblRows[name] = (count + 2)
  elif (count > 8):  
   constantLblRows[name] = (count + 3) 
#-------------------------------------------------------------- End: Build up of rows for constant labels  

#-------------------------------------------------------------- Begin: Class of actual screen building
#                                                               and reacting to user activity
class balanceSheetApp(Tk):        
  def __init__(self, companyName, fiscalYear):   # Constructor for GUI class
    Tk.__init__(self)
    self.companyName = companyName # Set variables for database use
    self.fiscalYear  = fiscalYear   # Set variables for database use

    #------------------------------------------- Begin: Frame building to get scrollbar in program
    vscrollbar = AutoScrollbar(self)
    vscrollbar.grid(row=0, column=3, sticky=N+S)

    canvas = Canvas(self, yscrollcommand=vscrollbar.set, width = 515, height = 600)
    canvas.grid(row=0, column = 1, sticky=N+S+E+W)

    vscrollbar.config(command=canvas.yview)

    # make the canvas expandable
    #self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=3)
    self.grid_columnconfigure(0, weight=1)

    # create canvas contents
    self.frame = Frame(canvas, width = 200,height = 2000)
    self.frame.rowconfigure(1, weight=1)
    self.frame.columnconfigure(1, weight=1)

    canvas.create_window(0, 0, anchor=NW, window=self.frame)
    self.frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    #-------------------------------------------- End: Frame building to get scrollbar in program
 
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
      if (name == 'Space'  or name == 'Space2' or
          name == 'Space3' or name == 'Space4' or name == 'Space5'):   # Big space in between everything else    
       lb = Label(self.frame, text = ' ', font = ("Helvetica", "14"))                     
       lb.grid(row = constantLblRows[name], columnspan = 2)
       constantLabels[name] = lb
       
      else:
       lb = Label(self.frame, text = (self.formatLabel(constantNames[count])), font = ("Helvetica", "16"))
       lb.grid(row = constantLblRows[name], column = 0)
       constantLabels[name] = lb
       
       #Some entry fields need to be non enterable with data
       if (name == 'Current Assets:' or name == 'Current Liabilities:' or 
           name == "Owner's Equity:"):
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
     if (name == "+ Add Current Asset"):      
      btn["command"] = self.addCurrentAsset
     elif (name == "+ Add Current Liability"):
      btn["command"] = self.addCurrentLiability
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
    conn = sqlite3.connect("balanceSheetDatabase.db")
    c = conn.cursor()

    #create a table
    c.execute("""CREATE TABLE IF NOT EXISTS bsit
                 (company        VARCHAR(20),
                  fiscal_year    VARCHAR(4),
                  name    VARCHAR(24),
                  valueOfName VARCHAR(10),
                  PRIMARY KEY (company, fiscal_year, name))""")

    # Get everything from the item table
    nextValueFlagAsset     = '' # Reference the values before if statements
    nextValueFlagLiability = '' # Reference the values before if statements

    #Insert default values for user to have as guide to each fin. statement
    defaultFound = ''
    defaultLoad = c.execute("SELECT * FROM bsit where company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))
    for record in defaultLoad:
     defaultFound = 'X'

    # Company hasn't ever before entered data, preload data for them 
    if defaultFound == '':
     # Purge pre-existing data
     c.execute("DELETE FROM bsit WHERE company = '' and fiscal_year = ''")
     
     # Insert data to be preloaded
     c.execute("INSERT INTO bsit VALUES (?, ?, ?, ?)",('', '', '> CA: Cash on Hand', '23000'))
     c.execute("INSERT INTO bsit VALUES (?, ?, ?, ?)",('', '', '> CA: Accounts Rec.', '2000'))
     c.execute("INSERT INTO bsit VALUES (?, ?, ?, ?)",('', '', '> CA: Inventory', '10000'))
     c.execute("INSERT INTO bsit VALUES (?, ?, ?, ?)",('', '', '> CA: Equipment', '25000'))

     c.execute("INSERT INTO bsit VALUES (?, ?, ?, ?)",('', '', '> CL: Accounts Payable', '5000'))
     c.execute("INSERT INTO bsit VALUES (?, ?, ?, ?)",('', '', '> CL: Taxes Payable', '2000'))
     c.execute("INSERT INTO bsit VALUES (?, ?, ?, ?)",('', '', '> CL: Bank Loan', '20000'))

     result = c.execute("SELECT * FROM bsit where company = '' and fiscal_year = ''")
    else: 
     result = c.execute("SELECT * FROM bsit where company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))

    # Build screen
    for record in result:
     for field in record:
      if nextValueFlagAsset == 'X':
        nextValueFlagAsset = ''          #Reset for next field

        # Save new label and txt field from expense name
        currentAssets.append(assetName)      #Add expense name to list
        assetRows[assetName] = constantBtnRows[0]  

        #----------------------------------------------------- Begin: destroying everything under
        #                                                      new expense to build screen back up
        self.destroyConstantNames(constantLblRows['Current Assets:'], 'Move Down')   # Destroy constant labels & entries
        self.destroyConstantButtons(constantLblRows['Current Assets:'], 'Move Down') # Destroy constant buttons

        self.destroyCurrentLiabilities('Move Down') # Destroy all things related to current liabilities
        #----------------------------------------------------- End: destroying everything under
        #                                                      new expense to build screen back up
          
        #----------------------------------------------------- Begin: Build new screen 
        # Build new label, entry & button on screen
        self.buildNewCurrentAsset(assetName, field)

        #-------------------- Pre-existing stuff to build back up

        # Build constant buttons on screen
        self.rebuildConstantButtons(constantLblRows['Current Assets:'])

        #Build liabilities labels, entries & buttons
        self.rebuildCurrentLiabilities()

        # Build constant labels and entries on screen
        self.rebuildConstantNames(constantLblRows['Current Assets:'])
        #----------------------------------------------------- End: Build new screen
            
      if field[:5] == '> CA:':
        nextValueFlagAsset = 'X'  
        assetName = field

      if nextValueFlagLiability == 'X':
        nextValueFlagLiability = ''     #Reset for next field
        #Save new label and txt field
        currentLiabilities.append(liabilityName)          #Add expense name to list
        liabilityRows[liabilityName] = constantBtnRows[1] #Put label where button is located

        #----------------------------------------------------- Begin: destroying everything under
        #                                                      new expense to build screen back up
        self.destroyConstantNames(constantLblRows['Current Liabilities:'], 'Move Down')   # Destroy constant labels & entries
        self.destroyConstantButtons(constantLblRows['Current Liabilities:'], 'Move Down') # Destroy constant buttons
        #----------------------------------------------------- End: destroying everything under
        #                                                      new expense to build screen back up

        #----------------------------------------------------- Begin: Build new screen   
        # Build new label, entry & button on screen
        self.buildNewCurrentLiability(liabilityName, field)

        # Build buttons on screen
        self.rebuildConstantButtons(constantLblRows['Current Liabilities:'])
     
        # Build constant labels and entries on screen
        self.rebuildConstantNames(constantLblRows['Current Liabilities:'])
        #----------------------------------------------------- End: Build new screen

      if field[:5] == '> CL:':
        nextValueFlagLiability = 'X'  
        liabilityName = field
          

  def updateAllTotals(self):
    self.setCurrentAssets()       # Set Current Assets Label
    self.setCurrentLiabilities()  # Set Current Liabilities Label
    self.setOwnersEquity()        # Set Owner's Equity Label

  def setCurrentAssets(self):
     CA = float(0)                   # Assign value before using it
     for name in currentAssets:   # Loop through CA's and add them up to find total
       # User could not put in value in entry they add, so we assign value zero
       if (assetEntries[name].get()) == '':
         e = assetEntries[name]
         e.insert(END, '0.0')

       assetEntryValues[name] = float(assetEntries[name].get()) # Save the value in dictionary
       CA = (CA + float(assetEntries[name].get()))          # Add on to our total
     constantEntries["Current Assets:"]["text"] = float(CA) # Assign our final value

  def setCurrentLiabilities(self):
     CL = float(0)                  # Assign value before using it
     for name in currentLiabilities:  # Loop through CL's and add them up to find total
       # User could not put in value in entry they add, so we assign value zero
       if (liabilityEntries[name].get()) == '':
         e = liabilityEntries[name]
         e.insert(END, '0.0')
         
       liabilityEntryValues[name] = float(liabilityEntries[name].get()) # Save the value in dictionary
       CL = (CL + float(liabilityEntries[name].get()))           # Add on to our total
     constantEntries["Current Liabilities:"]["text"] = float(CL) # Assign our final value

  def setOwnersEquity(self):         
     constantEntries["Owner's Equity:"]["text"] = (float(constantEntries["Current Assets:"]["text"])
                                                 - float(constantEntries["Current Liabilities:"]["text"]))
     
  #------------------------------------------------------ End: Methods that calculate totals   

  #------------------------------------------------------ Begin: Methods for formatting labels
  def formatLabel(self, labelString): # We want all of our labels to have a max of 24 characters
     formatLbl = True
     counter   = 0
     countMax  = (24 - len( labelString )) #Calculate how many spaces we need to make label 24 characters
     # Loop through and only allow labels to be length of 24
     while formatLbl == True:
      counter = (counter + 1)
      labelString = (' ' + labelString)
             
      if (counter == countMax):
        formatLbl = False
        
     return labelString    # Return formatted label text
  #------------------------------------------------------ End: Methods for formatting labels  

  #------------------------------------------------------ Begin: Methods for assigning action to new buttons
  def buttonMethodAssets(self, keyString):   
    btn = Button(self.frame, text = '<  Delete CA', font = ("Helvetica", "8"),
                 command = lambda: self.assetBtnClick(keyString))
    btn.grid(row = assetRows[keyString], column = 2)
    assetBtns[keyString] = btn

  def buttonMethodLiabilities(self, keyString):   
    btn = Button(self.frame, text = '<  Delete CL', font = ("Helvetica", "8"),
                 command = lambda: self.liabilityBtnClick(keyString))
    btn.grid(row = liabilityRows[keyString], column = 2)
    liabilityBtns[keyString] = btn
  #------------------------------------------------------ End: Methods for assigning action to new buttons

  #------------------------------------------------------ Begin: Methods for popups
  def runAddAssetPopup(self, assetNameBeginning): 
    displayPopup = True
    popUp = assetPopup()

    #Loop through popup and dont continue until data is recieved
    while(displayPopup == True):
     popUp.update()                    #Keeps popup looping, but not infinitely
     
     if(popUp.getAssetName() != ''): # User has typed in expense name and pressed continue
      self.__assetName = (assetNameBeginning + popUp.getAssetName()) # Bring strings together
      popUp.destroy()
      displayPopup = False     # Leave loop

    return self.__assetName  # Return back the name that the user typed in

  def runAddLiabilityPopup(self, liabilityNameBeginning): 
    displayPopup = True
    popUp = liabilityPopup()

    #Loop through popup and dont continue until data is recieved
    while(displayPopup == True):
     popUp.update()                    #Keeps popup looping, but not infinitely
     
     if(popUp.getLiabilityName() != ''): # User has typed in expense name and pressed continue
      self.__liabilityName = (liabilityNameBeginning + popUp.getLiabilityName()) # Bring strings together
      popUp.destroy()
      displayPopup = False     # Leave loop

    return self.__liabilityName  # Return back the name that the user typed in
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
          name != 'Space3' and name != 'Space4'
          and name != 'Space5'):
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

  def destroySpecialCurrentAssets(self, btnId):
     #Destroy labels from operating expenses that could be below whatever are deleting
     count = -1
     for name in currentAssets:
      if (name == btnId): #Destroy actual label itself
       lb = assetLabels[name]      # Load label from screen
       lb.destroy()                # Delete label on screen

       e  = assetEntries[name]     # Load Entry from screen 
       e.destroy()                 # Delete entry on screen

       btn = assetBtns[name]       # Btn for label getting deleted
       btn.destroy()               # Delete button on screen
       
      else:
       if((assetRows[name]) > (assetRows[btnId])):
        lb = assetLabels[name]     # Aquire label
        assetRows[name] = (assetRows[name] - 1) # Rows need to moved up
        lb.destroy()               # Destroy label
        
       else:
        lb = assetLabels[name]     # Aquire label
        assetRows[name] = (assetRows[name])     # Rows need to be moved up
        lb.destroy()               # Destroy label


       e  = assetEntries[name]     # Aquire entry
       e.destroy()                 # Destroy entry

       btn = assetBtns[name]       # Aquire button
       btn.destroy()               # Destroy button

  def destroyFromAssetLists(self, btnId):
    del assetRows[btnId]         # Delete from dictionary 
    del assetLabels[btnId]       # Delete from dictionary
    del assetEntries[btnId]      # Delete from dictionary
    del assetBtns[btnId]         # Delete from dictionary
    del assetEntryValues[btnId]   # Delete from dictionary                                      
    currentAssets.remove(btnId)  # Delete from list

  def destroyCurrentLiabilities(self, rowAction):
    # Destroy all labels, entries, & buttons from interest expenses
    for name in currentLiabilities:
      if rowAction == 'Move Down':
        liabilityRows[name] = (liabilityRows[name] + 1) # Rows need to be shifted down one
      elif rowAction == 'Move Up':
        liabilityRows[name] = (liabilityRows[name] - 1) # Rows need to be shifted up one

      lb = liabilityLabels[name]     # Aquire label        
      lb.destroy()                  # Destroy label

      e  = liabilityEntries[name]    # Aquire entry
      e.destroy()                   # Destroy entry

      btn = liabilityBtns[name]      # Aquire button
      btn.destroy()                 # Destroy button

  def destroySpecialCurrentLiabilities(self, btnId):
     #Destroy labels from operating expenses that could be below whatever are deleting
     count = -1
     for name in currentLiabilities:
      if (name == btnId):              #Destroy actual label itself
       lb = liabilityLabels[name]       # Load label from screen
       lb.destroy()                    # Delete label on screen

       e  = liabilityEntries[name]      # Load Entry from screen 
       e.destroy()                     # Delete entry on screen

       btn = liabilityBtns[name]        # Btn for label getting deleted
       btn.destroy()                   # Delete button on screen
       
      else:
       if((liabilityRows[name]) > (liabilityRows[btnId])):
        lb = liabilityLabels[name]      # Aquire label
        liabilityRows[name] = (liabilityRows[name] - 1) # Rows need to moved up
        lb.destroy()                   # Destroy label
        
       else:
        lb = liabilityLabels[name]      # Aquire label
        liabilityRows[name] = (liabilityRows[name])     
        lb.destroy()                   # Destroy label


       e  = liabilityEntries[name]      # Aquire entry
       e.destroy()                     # Destroy entry

       btn = liabilityBtns[name]        # Aquire button
       btn.destroy()                   # Destroy button

  def destroyFromLiabilityLists(self, btnId):
    del liabilityRows[btnId]         # Delete from dictionary 
    del liabilityLabels[btnId]       # Delete from dictionary
    del liabilityEntries[btnId]      # Delete from dictionary
    del liabilityBtns[btnId]         # Delete from dictionary
    del liabilityEntryValues[btnId]  # Delete from dictionary
    currentLiabilities.remove(btnId) # Delete from list       
  #------------------------------------------------------ End: Methods for destroying screen

  #------------------------------------------------------ Begin: Methods for new screen widjets
  def buildNewCurrentAsset(self, currentAssetName, value = 0.0):
    # Build new Label
    lb = Label(self.frame, text = (self.formatLabel(currentAssetName)), font = ("Helvetica", "13"))
    lb.grid(row = assetRows[currentAssetName], column = 0)
    assetLabels[currentAssetName] = lb

    # Build new entry 
    e = Entry(self.frame)
    e.grid(row = assetRows[currentAssetName], column = 1)
    e.insert(END, value)
    assetEntries[currentAssetName] = e

    # Build new button that goes next to entry
    self.buttonMethodAssets(currentAssetName)

  def buildNewCurrentLiability(self, currentLiabilityName, value = 0.0):
    # Build new Label
    lb = Label(self.frame, text = (self.formatLabel(currentLiabilityName)), font = ("Helvetica", "13"))
    lb.grid(row = liabilityRows[currentLiabilityName], column = 0)
    liabilityLabels[currentLiabilityName] = lb

    # Build new entry 
    e = Entry(self.frame)
    e.grid(row = liabilityRows[currentLiabilityName], column = 1)
    e.insert(END, value)
    liabilityEntries[currentLiabilityName] = e

    # Build new button that goes next to entry
    self.buttonMethodLiabilities(currentLiabilityName) 
  #------------------------------------------------------ End: Methods for new screen widjets

  #------------------------------------------------------ Begin: Methods for rebuilding screen
  def rebuildConstantNames(self, lowestRow):
    # Build constant labels and entries on screen
    count = -1
    for name in constantNames:
     count = (count + 1)
     if (constantLblRows[name] > lowestRow):         # We only want to rebuild the things we deleted
      if (name != 'Space' and name != 'Space2' and
          name != 'Space3' and name != 'Space4'
          and name != 'Space5'):    # If it isn't a space do this 
       lb = Label(self.frame, text = (self.formatLabel(constantNames[count])), font = ("Helvetica", "16"))
       lb.grid(row = constantLblRows[name], column = 0)
       constantLabels[name] = lb
       
       #Some entry fields need to be non enterable with data
       if (name == 'Current Assets:' or name == 'Current Liabilities:' or 
           name == "Owner's Equity:"):
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
     
      if   (name == "+ Add Current Asset"):    # Different buttons require different command
       btn["command"] = self.addCurrentAsset   # Assign button command
      elif (name == "+ Add Current Liability"):
       btn["command"] = self.addCurrentLiability   # Assign button command
      elif (name == "Update All Totals"):
       btn.destroy()                           # Special button, it is bigger than others (has to be destroyed)
       btn = Button(self.frame, text = constantBtns[count], font = ("Helvetica", "13")) 
       btn["command"] = self.updateAllTotals   # Assign button command
       btn.grid(row = constantBtnRows[count], column = 1)
      elif (name == "Save To Database"):
       btn.destroy()
       btn = Button(self.frame, text = constantBtns[count], font = ("Helvetica", "13")) 
       btn["command"] = self.saveToDatabase
       btn.grid(row = constantBtnRows[count], column = 1) 
      
      constantButtonObject[name] = btn         # Save object in dictionary
      
  def rebuildCurrentAssets(self):
    #Build operating labels, entries & buttons
    count = -1
    for name in currentAssets:                  # Loop through all current assets
       count = (count + 1)
       
       #Build label
       lb = Label(self.frame, text = (self.formatLabel(currentAssets[count])), font = ("Helvetica", "12"))
       lb.grid(row = assetRows[name], column = 0)
       assetLabels[name] = lb

       #Build entry
       e = Entry(self.frame)
       e.grid(row = assetRows[name], column = 1)
       e.insert(END, assetEntryValues[name])
       assetEntries[name] = e

       #Build button
       self.buttonMethodAssets(name)


  def rebuildCurrentLiabilities(self):
    #Build interest labels, entries & buttons
    count = -1
    for name in currentLiabilities:              # Loop through all 
       count = (count + 1)
       
       #Build label
       lb = Label(self.frame, text = (self.formatLabel(currentLiabilities[count])), font = ("Helvetica", "12"))
       lb.grid(row = liabilityRows[name], column = 0)
       liabilityLabels[name] = lb

       #Build entry
       e = Entry(self.frame)
       e.grid(row = liabilityRows[name], column = 1)
       e.insert(END, liabilityEntryValues[name])
       liabilityEntries[name] = e

       #Build button
       self.buttonMethodLiabilities(name)
  #------------------------------------------------------ End: Methods for rebuilding screen

  #------------------------------------------------------ Begin: Methods for user adding new expenses when they hit an add button
  # Event that is triggered when calculate button is pushed
  def addCurrentAsset(self):
    # Bring up popup for user to enter in expense name
    assetName = self.runAddAssetPopup('> CA: ')

    # Save new label and txt field from expense name
    currentAssets.append(assetName)      #Add expense name to list
    assetRows[assetName] = constantBtnRows[0]  

    #----------------------------------------------------- Begin: destroying everything under
    #                                                      new expense to build screen back up
    self.destroyConstantNames(constantLblRows['Current Assets:'], 'Move Down')   # Destroy constant labels & entries
    self.destroyConstantButtons(constantLblRows['Current Assets:'], 'Move Down') # Destroy constant buttons

    self.destroyCurrentLiabilities('Move Down') # Destroy all things related to current liabilities
    #----------------------------------------------------- End: destroying everything under
    #                                                      new expense to build screen back up
      
    #----------------------------------------------------- Begin: Build new screen 
    # Build new label, entry & button on screen
    self.buildNewCurrentAsset(assetName)

    #-------------------- Pre-existing stuff to build back up

    # Build constant buttons on screen
    self.rebuildConstantButtons(constantLblRows['Current Assets:'])

    #Build liabilities labels, entries & buttons
    self.rebuildCurrentLiabilities()

    # Build constant labels and entries on screen
    self.rebuildConstantNames(constantLblRows['Current Assets:'])

    # Update the totals of everything on the screen
    self.updateAllTotals()
    #----------------------------------------------------- End: Build new screen 

    
  def addCurrentLiability(self):
     # Bring up popup for user to enter in expense name
     liabilityName = self.runAddLiabilityPopup('> CL: ')

     #Save new label and txt field
     currentLiabilities.append(liabilityName)          #Add expense name to list
     liabilityRows[liabilityName] = constantBtnRows[1] #Put label where button is located

     #----------------------------------------------------- Begin: destroying everything under
     #                                                      new expense to build screen back up
     self.destroyConstantNames(constantLblRows['Current Liabilities:'], 'Move Down')   # Destroy constant labels & entries
     self.destroyConstantButtons(constantLblRows['Current Liabilities:'], 'Move Down') # Destroy constant buttons
     #----------------------------------------------------- End: destroying everything under
     #                                                      new expense to build screen back up

     #----------------------------------------------------- Begin: Build new screen   
     # Build new label, entry & button on screen
     self.buildNewCurrentLiability(liabilityName)

     # Build buttons on screen
     self.rebuildConstantButtons(constantLblRows['Current Liabilities:'])
     
     # Build constant labels and entries on screen
     self.rebuildConstantNames(constantLblRows['Current Liabilities:'])

     # Update the totals of everything on the screen
     self.updateAllTotals()
     #----------------------------------------------------- End: Build new screen
     
  def saveToDatabase(self):
     #Build connection to database
     conn = sqlite3.connect("balanceSheetDatabase.db")
     c = conn.cursor()
      
     #---------------------------------------------- Begin getting Item Data
     #create a table
     c.execute("""CREATE TABLE IF NOT EXISTS bsit
                 (company        VARCHAR(20),
                  fiscal_year    VARCHAR(4),
                  name    VARCHAR(24),
                  valueOfName VARCHAR(10),
                  PRIMARY KEY (company, fiscal_year, name))""")
     
     # Get rid of everything because we will rebuild database
     c.execute("DELETE FROM bsit WHERE company = ? and fiscal_year = ?", (self.companyName, self.fiscalYear))

     # Add current assets to database
     for name in currentAssets:   # Loop through OE's and add them up to find total
       # Save the value in the database
       c.execute("INSERT INTO bsit VALUES (?, ?, ?, ?)",
               (self.companyName, self.fiscalYear, name, assetEntries[name].get()))

     # Add current liabilities to database
     for name in currentLiabilities:   # Loop through OE's and add them up to find total
       # Save the value in the database
       c.execute("INSERT INTO bsit VALUES (?, ?, ?, ?)",
               (self.companyName, self.fiscalYear, name, liabilityEntries[name].get()))  
     #---------------------------------------------- End getting Item Data

     # Make changes permanent  
     conn.commit()
     c.close() 
  
  def assetBtnClick(self, btnId):
     #----------------------------------------------------- Begin: destroying everything under
     #                                                      expense to build screen back up
     self.destroyConstantNames(constantLblRows['Current Assets:'], 'Move Up')   # Destroy constant labels & entries
     self.destroyConstantButtons(constantLblRows['Current Assets:'], 'Move Up') # Destroy constant buttons

     self.destroySpecialCurrentAssets(btnId)
        
     self.destroyCurrentLiabilities('Move Up') # Destroy all things related to interest expenses

     # Delete out of list and dictionaries
     self.destroyFromAssetLists(btnId)
     #----------------------------------------------------- End: destroying everything under
     #                                                      new expense to build screen back up
    
     #----------------------------------------------------- Begin: Build new screen 
     # Rebuild constant buttons on screen
     self.rebuildConstantButtons(constantLblRows['Current Assets:'])

     # Build asset labels, entries, and buttons
     self.rebuildCurrentAssets()

     # Build liabilty labels, entries, and buttons
     self.rebuildCurrentLiabilities()

     # Build constant labels and entries on screen
     self.rebuildConstantNames(constantLblRows['Current Assets:'])

     # Update the totals of everything on the screen
     self.updateAllTotals()
     #----------------------------------------------------- End: Build new screen 
           
  def liabilityBtnClick(self, btnId):
     #----------------------------------------------------- Begin: destroying everything under
     #                                                      expense to build screen back up
     self.destroyConstantNames(constantLblRows['Current Liabilities:'], 'Move Up')   # Destroy constant labels & entries
     self.destroyConstantButtons(constantLblRows['Current Liabilities:'], 'Move Up') # Destroy constant buttons

     self.destroySpecialCurrentLiabilities(btnId) # Destroy certain current liabilities 

     # Delete out of list and dictionaries
     self.destroyFromLiabilityLists(btnId)
     #----------------------------------------------------- End: destroying everything under
     #                                                      new expense to build screen back up

     #----------------------------------------------------- Begin: Build new screen 
     # Rebuild constant buttons on screen
     self.rebuildConstantButtons(constantLblRows['Current Liabilities:'])

     # Build liability labels, entries, and buttons
     self.rebuildCurrentLiabilities()

     # Build constant labels and entries on screen
     self.rebuildConstantNames(constantLblRows['Current Liabilities:'])

     # Update the totals of everything on the screen
     self.updateAllTotals()
     #----------------------------------------------------- End: Build new screen 
      
def main():
  myGui = balanceSheetApp()                  # Instantiate myGUI object to begin building GUI
 
  myGui.mainloop()


#Run main function
if(__name__ == "__main__"):
  main()

