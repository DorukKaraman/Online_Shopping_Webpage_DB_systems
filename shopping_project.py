import sqlite3
from datetime import datetime
from datetime import timedelta
import PySimpleGUI as sg

con = sqlite3.connect('database1.db')
cur = con.cursor()

sg.theme('DarkTeal9')
# global variables
login_user_id = -1
login_user_name = -1
login_user_type = -1


# window functions
def window_login():
    layout = [[sg.Text('Welcome to eBAY Auction System. Please enter your information.')],
              [sg.Text('ID:', size=(10, 1)), sg.Input(size=(10, 1), key='id')],
              [sg.Text('Password:', size=(10, 1)), sg.Input(size=(10, 1), key='password')],
              [sg.Button('Login')]]

    return sg.Window('Login Window', layout, background_color='#FF0000')


def window_seller():
    layout = [[sg.Text('Welcome ' + login_user_name)],
              [sg.Button('View Auctions')],
              [sg.Button('Create Auction')],
              [sg.Button('Bills')],
              [sg.Button('Update Information')],
              [sg.Button('Logout')]]

    return sg.Window('Seller Window', layout)


def window_buyer():
    layout = [[sg.Text('Welcome ' + login_user_name)],
              [sg.Button('View Active Auctions')],
              [sg.Button('Logout')]]

    return sg.Window('Buyer Window', layout)


def window_active_auctions():
    active_auctionsNo = []

    for row in cur.execute('''SELECT *
                                  FROM auction_categorizes'''):
        active_auctionsNo.append(row)

    layout = [
        [sg.Text('Active Auctions:'), sg.Combo(active_auctionsNo, size=(25, 7), key='auctionNo'), sg.Button('Bid')],
        [sg.Button('Return to Main')],
        [sg.Button('Logout')]]

    return sg.Window('Active Auctions Window', layout)


def window_auctions():
    auctionsNo = []

    for row in cur.execute('''SELECT a.description, a.status, a.auctionNo
                              FROM owns o, auction_categorizes a
                              WHERE a.auctionNo = o.auctionNo and o.SellerID = ?''', (login_user_id,)):
        auctionsNo.append(row)

    layout = [
        [sg.Text('Your Auctions:'), sg.Combo(auctionsNo, size=(25, 7), key='auctions'), sg.Button('List Bidders')],
        [sg.Button('Delete Auction')],
        [sg.Button('Show Bill')],
        [sg.Button('Return to Main')],
        [sg.Button('Logout')]]

    return sg.Window('Auctions Window', layout)


def window_create_auctions():
    category = []

    for row in cur.execute('''SELECT categoryName
                              FROM Category'''):
        category.append(row)
        
    layout = [
        [sg.Text('Create New Auctions:')],
        [sg.Text('Start Price: ', size=(10,1)), sg.Input(key='startPrice', size=(10,1))],
        [sg.Text('Description: ', size=(10,1)), sg.Input(key='description', size=(10,1))],
        [sg.Text('Title: ', size=(10,1)), sg.Input(key='title', size=(10,1))],
        [sg.Text('End Date (dd-mm-yyyy): ', size=(10,1)), sg.Input(key='endDate', size=(10,1))],
        [sg.Text('Buy It Price: ', size=(10,1)), sg.Input(key='buyitprice', size=(10,1))],
        [sg.Text('Category Name: ', size=(10,1)), sg.Combo(category, size=(25, 7), key='catName')],
        [sg.Button('Press to Create Auction')],
        [sg.Button('Return to Main')],
        [sg.Button('Logout')]]

    return sg.Window('Create Auctions Window', layout)


def window_bills():
    Bills = []

    for row in cur.execute('''SELECT tranNo, auctionNo, finalBidID, netAmount
                              FROM bill_Generates_Payday
                              WHERE SellerID = ?''', (login_user_id,)):
        Bills.append(row)

    layout = [
        [sg.Text('Your Bills:'), sg.Combo(Bills, size=(25, 7), key='Bills')],
        [sg.Button('Return to Main')],
        [sg.Button('Logout')]]

    return sg.Window('Bills Window', layout)


def window_update_information():
    layout = [
        [sg.Text('Your Info:')],
        [sg.Text('First Name: ', size=(10,1)), sg.Input(key='firstName', size=(10,1)), sg.Button('Save Name')],
        [sg.Text('Last Name: ', size=(10,1)), sg.Input(key='lastName', size=(10,1)), sg.Button('Save Surname')],
        [sg.Text('IBAN: ', size=(10,1)), sg.Input(key='IBAN', size=(10,1)), sg.Button('Save IBAN')],
        [sg.Text('Password: ', size=(10,1)), sg.Input(key='password', size=(10,1)), sg.Button('Save Password')],
        [sg.Button('Return to Main')],
        [sg.Button('Logout')]]

    return sg.Window('Update Bill Window', layout)


def button_delete_auction(values):
    auction = values['auctions'][2]
    if auction == '':
        sg.popup('Select an auction')
    elif values['auctions'][1] != 'OnGoing':
        sg.popup('Select a finished auction')
    else:
        cur.execute('DELETE FROM auction_categorizes WHERE auctionNo = ?',((auction),))
    
    
def button_show_bill(values):
    auction = values['auctions'][2]
    if auction == '':
        sg.popup('Select an auction')
    elif values['auctions'][1] != 'Ended':
        sg.popup('Select a finished auction')
    else:
        cur.execute('SELECT tranNo FROM bill_Generates_Payday WHERE auctionNo = ?',((auction),))
        transactionNo = cur.fetchone()[0]
        cur.execute('SELECT netAmount FROM bill_Generates_Payday WHERE auctionNo = ?',((auction),))
        billamount = cur.fetchone()[0]
        sg.popup(('The Transaction No is: ' + str(transactionNo) + ' with the amount: ' + str(billamount)))
         

def button_update_username_information(values):
    global login_user_id
    Name = values['firstName']
    if Name == '':
        sg.popup('Name cannot be empty!')
    else:
        cur.execute('UPDATE User SET firstName = ? WHERE ssn = ?',
                        (Name, login_user_id))


def button_update_usersurname_information(values):
    global login_user_id
    Surname = values['lastName']
    if Surname == '':
        sg.popup('Surname cannot be empty!')
    else:
        cur.execute('UPDATE User SET lastName = ? WHERE ssn = ?',
                        (Surname, login_user_id))
    
    
def button_update_seller_IBAN_information(values):
    global login_user_id
    IBAN = values['IBAN']
    if IBAN == '':
        sg.popup('IBAN cannot be empty!')
    else:
        cur.execute('UPDATE Seller SET IBAN = ? WHERE SellerID = ?',
                        (IBAN, login_user_id))
    
    
def button_update_password_information(values):
    global login_user_id
    password = values['password']
    if password == '':
        sg.popup('password cannot be empty!')
    else:
        cur.execute('UPDATE User SET password = ? WHERE ssn = ?',
                        (password, login_user_id))


def button_create_auctions(values):
    global login_user_id
    startPrice = values['startPrice']
    description = values['description']
    title = values['title']
    endDate = values['endDate']
    buyitprice = values['buyitprice']
    catName = values['catName'][0]

    
    if startPrice == '':
        sg.popup('Start price cannot be empty!')
    elif not startPrice.isnumeric():
        sg.popup('Start price should be numeric.')
    elif description == '':
        sg.popup('Descripton cannot be empty')
    elif title == '':
        sg.popup('Title cannot be empty')
    elif endDate == '':
        sg.popup('End date cannot be empty')
    elif buyitprice == '':
        sg.popup('Buy it price cannot be empty')
    elif not buyitprice.isnumeric():
        sg.popup('Buy it price should be numeric.')
    else:
        startPrice = int(startPrice)
        if startPrice < 0:
            sg.popup('Start price cannot be negative')
        else:
            # for this auction we should find the next available auction no
            cur.execute('SELECT MAX(auctionNo) FROM auction_categorizes')
            row = cur.fetchone()

            if row is None:
                # this is when there is no auction in the system
                new_auction_no = 1
            else:
                new_auction_no = row[0] + 1  # burda row[0]ydu ama ben 9 yaptım indexi öyle diye

            currentPrice = startPrice
            startDate = datetime.today().strftime('%Y-%m-%d')
            state = "OnGoing"
            

            # first insert to the auction table
            cur.execute('INSERT INTO auction_categorizes VALUES (?,?,?,?,?,?,?,?,null,?,?)',
                        (startPrice, description, title, catName, currentPrice, state, endDate, startDate, new_auction_no, buyitprice))

            sg.popup('Successfully inserted ' + title + ' with auction number: ' + str(new_auction_no))

            cur.execute('INSERT INTO owns VALUES (?,?)',
                        (new_auction_no, login_user_id))
            
            # clear inputs
            window.Element('startPrice').Update(value='')
            window.Element('description').Update(value='')
            window.Element('title').Update(value='')
            window.Element('endDate').Update(value='')
            window.Element('buyitprice').Update(value='')


def button_login(values):
    global login_user_id
    global login_user_name
    global login_user_type
    global window

    uid = values['id']
    upass = values['password']
    if uid == '':
        sg.popup('ID cannot be empty')
    elif upass == '':
        sg.popup('Password cannot be empty')
    else:
        # first check if this is a valid user
        cur.execute('SELECT ssn, firstName FROM User WHERE ssn = ? AND password = ?', (uid, upass))
        row = cur.fetchone()

        if row is None:
            sg.popup('ID or password is wrong!')
        else:
            # this is some existing user, let's keep the ID of this user in the global variable
            login_user_id = row[0]

            # we will use the name in the welcome message
            login_user_name = row[1]

            # now let's find which type of user this login_user_id belongs to
            # let's first check if this is a student
            cur.execute('SELECT SellerID FROM Seller WHERE SellerID = ?', (uid,))
            row_seller = cur.fetchone()

            if row_seller is None:
                # this is not a student, let's check for teacher
                cur.execute('SELECT BuyerID FROM Buyer WHERE BuyerID = ?', (uid,))
                row_buyer = cur.fetchone()
                if row_buyer is None:
                    # this is not a teacher also, then there should be some problem with the DB
                    # since we expect a user to be either a student or a teacher
                    sg.popup('User type error! Please contact the admin.')
                else:
                    login_user_type = 'Buyer'
                    sg.popup('Welcome, ' + login_user_name + ' (Buyer)')
                    window.close()
                    window = window_buyer()
            else:
                login_user_type = 'Seller'
                sg.popup('Welcome, ' + login_user_name + ' (Seller)')
                window.close()
                window = window_seller()
                
                
def button_list_bidders(values):
    
    auctions = values['auctions']
    if auctions == '':
        sg.popup('Please choose an auction to list bidders.')
    elif auctions[1] == 'Ended':
        sg.popup('Please choose an ongoing auction to list bidders.')
    else:
        adescription = auctions[0]
        aNo = auctions[2]
        
        bidders = []
        
        # here in SQL, we need to specify which SID we are using, otherwise it will say "ambiguous column name"
        for row in cur.execute('''SELECT B.BuyerID, U.firstName, U.lastName, T.biddingPrice
                                  FROM Buyer B, TakesBids T, User U
                                  WHERE B.BuyerID = U.ssn
                                  AND B.BuyerID = T.buyerSsn
                                  AND T.auctionNo = ?
                                  ORDER BY T.biddingPrice ASC''', (aNo,)):
            bidders.append(row)
        
        window.Element('bidders').Update(values=bidders)


# open the first window
window = window_login()

while True:
    event, values = window.read()
    if event == 'Login':
        button_login(values)
    elif event == 'View Auctions':
        window.close()
        window = window_auctions()
    elif event == 'Create Auction':
        window.close()
        window = window_create_auctions()
    elif event == 'Bills':
        window.close()
        window = window_bills()
    elif event == 'View Active Auctions':
        window.close()
        window = window_active_auctions()
    elif event == 'Update Information':
        window.close()
        window = window_update_information()
    elif event == 'Press to Create Auction':
        button_create_auctions(values)
    elif event == 'List Bidders':
        button_list_bidders(values)
    elif event == 'Create Auction':
        button_create_auctions(values)
    elif event == 'Save Name':
        button_update_username_information(values)
    elif event == 'Save Surname':
        button_update_usersurname_information(values)
    elif event == 'Save IBAN':
        button_update_seller_IBAN_information(values)
    elif event == 'Save Password':
        button_update_password_information(values)
    elif event == 'Delete Auction':
        button_delete_auction(values)
    elif event == 'Show Bill':
        button_show_bill(values)
    elif event == 'Return to Main':
        if login_user_type == 'Seller':
            window.close()
            window = window_seller()
        elif login_user_type == 'Buyer':
            window.close()
            window = window_buyer()
        else:
            # this should not happen, bu in case happens let's return to login window
            window.close()
            window = window_login()
    elif event == 'Logout':
        # set login user global parameters
        login_user_id = -1
        login_user_name = -1
        login_user_type = -1
        window.close()
        window = window_login()
    elif event == sg.WIN_CLOSED:
        break

window.close()

con.commit()
con.close()
