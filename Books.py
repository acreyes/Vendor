######################
'''
Software to manage sales, and generate sales reports
Author: Adam Reyes
'''
#####################

####LOAD LIBRARIES##
import glob
import os
import time
import datetime
import pickle

######CLASSES########
class SALE():
    def __init__(self, date, item, price):
        self.dos = date
        self.obj = item
        self.prc = price
#####FUNCTIONS#######

def choice_return(low, high):
    #this is a function to return a integer choice between low and high#
    choice = raw_input("Enter a Number:")
    while(True):
        try:
            val = int(choice)
            if val < low or val > high: #not in valid range
                print "That is not a valid number. Please enter and integer between " + str(low) + "and " +  str(high)
                choice = raw_input("Enter a Number:")
            else:
                break
        except ValueError: #Not an integer
            print "That is not a valid number. Please enter and integer between " + str(low) + "and " + str(high)
            choice = raw_input("Enter a Number:")
    return(val)

def get_date():
    now = datetime.datetime.today()
    now = now.strftime("%Y-%m-%d")
    return(now)

def find_all(core, check):
    #finds all instances of core in elements of check
    #returns the overlapping elements in an array
    overlap = []
    for name in check:
        if core in name:
            overlap.append(name)
    return(overlap)

def make_sale():
    now = get_date()
    object_options = ["Shirt", "Poster", "Book", "Sticker", "Other"]
    count = 1
    print "Please select an item type"
    for option in object_options:
        print str(count) + ") " + option 
        count += 1
    val = choice_return(1,len(object_options))
    if val == len(object_options): #choice is Other
        object = "Other-" + raw_input("Other-")
    else:
        object = object_options[val - 1]
    while(True):
        try:
            price = float(raw_input("Price of item: "))
            break
        except ValueError:
            print "Error: Please enter a valid number"
            price = float(raw_input("Price of item: "))
    item = SALE(now, object, price)
    return(item)

def load_file(file_name):
    path = "Records/" + file_name
    fid = open(path, "r")
    Sales = pickle.load(fid)
    fid.close()
    return(Sales)

##################MENUS##############
def Main_menu():
    #clear the terminal
    print "\n"*100

    print( "#"*75 + "\n")*3
    print "#"*31+" Welcome to "+"#"*32
    print "#"*31 + " Adam's Book " + "#"*31
    print "Main Menu\n What would you like to do?"

    #options#
    print '1) New Book'
    print '2) Load Book'
    print '3) Exit'
    val = choice_return(1,3) #returns integer 1 or 2
    if val == 1:
        option = "NEW"
    elif val == 2:
        option = "LOAD"
    elif val == 3:
        option = "EXIT"
    
    return(option)

def load_book(): 
    #book loading menu
    #all books should be in Records/ folder
    #filenames should be formatted "Books_[date].dat"
    print "\n"*100 #clear the screen
    try:
        print "Choose a book"
        files = os.listdir("Records/")
        count = 1
        for name in files: 
            #list options and remove trailing junk
            name = name.strip("Book_")
            name = name.strip(".dat")
            print str(count) + ") " + name
            count += 1
        print "Enter 0 to return to main menu"
        val = choice_return(0,len(files))
        if val == 0:
            return("MAIN")
        else:
            file_name = files[val-1]
            return(file_name)
    except OSError:
        print "There does not appear to be any valid files. Returning to main menu. Please make a new book"
        time.sleep(3)
        return("MAIN")
        

def new_book():
    #menu tree for making a new book
    now = datetime.datetime.today()
    now = now.strftime("%Y-%m-%d")
    file_core = "Book_" + now
    file_name = file_core + ".dat"
    files = os.listdir("Records/")
    old_files = find_all(now, files) #get the other books from today
    if any(x in file_name for x in files):
        print "You already have a Book for today."
        print "Would you like to..."
        print "1) Make a new one anyway"
        print "2) Load from today"
        print "3) Return to the main menu"
        val = choice_return(1,3)
        
        if val == 1:
            file_name = file_core + "_" + str(len(old_files)) + ".dat"
        elif val == 2:
            print "Please select a file from the list"
            count = 1
            for name in old_files:
                print str(count) + ") " + name 
                count += 1
            file_num = choice_return(1,len(old_files))
            file_name = "load " + old_files[file_num - 1]
        elif val == 3:
            file_name = "MAIN"
    return(file_name)

###########WORKSPACE#########            
def work_space(file_name, new_old):
    #this is the main work space environment
    if new_old == 'NEW': #this is a new book
        Sales = []
    elif new_old == 'OLD': #this is an old book
        Sales = load_file(file_name)
    print "\n"*100 #clear screen
    print "#"*30 + "BOOK: " + file_name + "#"*30
    file_path = "Records/" + file_name
         
    while(True):
        print "What do you want to do?"
        Options = ["New Sale", "List Today's Sales", "Change an item", "Exit"]
        for i in range(len(Options)):
            print str(i+1) + ") " + Options[i]
        val = choice_return(1, len(Options))

        if val == 1:
            new_item = make_sale()
            Sales.append(new_item)
            fid = open(file_path, "w")
            pickle.dump(Sales, fid) #write new items to file
            fid.close()
            print "\n"*100
        elif val == 2: #list today's sales
            print "\n"*100
            print "Today's Sales".center(80, "#")
            for sale in Sales:
                print sale.dos.ljust(20) + sale.obj.ljust(20) + "$%.02f" % sale.prc
            print "".center(80, "#")
        elif val == 3: #change an item
            print "Which item do you want to change?"
            count = 1
            for sale in Sales: #list the sales
                print str(count) + ") " + sale.dos.ljust(20) + sale.obj.ljust(20) + str(sale.prc)
                count += 1
            while(True):
                item_num = choice_return(1, len(Sales))
                item = make_sale()
                print "These are your changes"
                print item.dos.ljust(20) + item.obj.ljust(20) + "$%.02f" % item.prc
                confirm = raw_input("Confirm these changes (Y/N): ")
                if confirm.lower() == "y":
                    Sales[item_num - 1] = item
                    break
                #else:
        elif val == 4: #exit
            break
    fid = open(file_path, "w")
    pickle.dump(Sales,fid) #write any changes
    return('EXIT')
            
    

#####################

#######MAIN##########
menu_tree = 'MAIN' #sets the menu tree to load
while(True):
    if menu_tree == 'MAIN': #main menu
        menu_tree = Main_menu()
        print menu_tree
    elif menu_tree == 'EXIT': #exit the program
        break
    elif menu_tree == 'NEW': #create a new book in /Records
        file_name = new_book()
        if file_name == 'MAIN':#exit to main menu
            menu_tree = "MAIN"
        elif len(file_name.split()) == 1: #created new file
            menu_tree = work_space(file_name, 'NEW')
        elif len(file_name.split()) == 2: #load an old book
            menu_tree = work_space(file_name.split()[1], "OLD")
            
    elif menu_tree == 'LOAD': #load a book
        choice = load_book()
        if choice == "MAIN":
            menu_tree = "MAIN"
        else:
            menu_tree = work_space(choice, "OLD")
