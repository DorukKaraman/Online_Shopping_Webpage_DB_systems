import sqlite3
from datetime import datetime
import PySimpleGUI as sg

# --- Database connection ---
con = sqlite3.connect('shopping_db.db')
cur = con.cursor()

sg.theme('DarkTeal9')

# --- Global variables ---
login_user_id = -1
login_user_name = -1
login_user_type = -1


# --- Window functions ---
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
    active_auctionsNo = [row for row in cur.execute('SELECT * FROM auction_categorizes')]
    layout = [
        [sg.Text('Active Auctions:'), sg.Combo(active_auctionsNo, size=(25, 7), key='auctionNo'), sg.Button('Bid')],
        [sg.Button('Return to Main')],
        [sg.Button('Logout')]]
    return sg.Window('Active Auctions Window', layout)


def window_auctions():
    auctionsNo = [row for row in cur.execute(
        '''SELECT a.description, a.status, a.auctionNo
           FROM owns o, auction_categorizes a
           WHERE a.auctionNo = o.auctionNo AND o.SellerID = ?''',
        (login_user_id,)
    )]
    layout = [
        [sg.Text('Your Auctions:'), sg.Combo(auctionsNo, size=(25, 7), key='auctions'),
         sg.Button('List Bidders')],
        [sg.Button('Delete Auction')],
        [sg.Button('Show Bill')],
        [sg.Listbox([], size=(40, 10), key='bidders')],
        [sg.Button('Return to Main')],
        [sg.Button('Logout')]]
    return sg.Window('Auctions Window', layout)


def window_create_auctions():
    category = [row for row in cur.execute('SELECT categoryName FROM Category')]
    layout = [
        [sg.Text('Create New Auctions:')],
        [sg.Text('Start Price: ', size=(15, 1)), sg.Input(key='startPrice')],
        [sg.Text('Description: ', size=(15, 1)), sg.Input(key='description')],
        [sg.Text('Title: ', size=(15, 1)), sg.Input(key='title')],
        [sg.Text('End Date (dd-mm-yyyy): ', size=(15, 1)), sg.Input(key='endDate')],
        [sg.Text('Buy It Price: ', size=(15, 1)), sg.Input(key='buyitprice')],
        [sg.Text('Category Name: ', size=(15, 1)), sg.Combo(category, size=(25, 7), key='catName')],
        [sg.Button('Press to Create Auction')],
        [sg.Button('Return to Main')],
        [sg.Button('Logout')]]
    return sg.Window('Create Auctions Window', layout)


def window_bills():
    Bills = [row for row in cur.execute(
        '''SELECT tranNo, auctionNo, finalBidID, netAmount
           FROM bill_Generates_Payday
           WHERE SellerID = ?''',
        (login_user_id,)
    )]
    layout = [
        [sg.Text('Your Bills:'), sg.Combo(Bills, size=(25, 7), key='Bills')],
        [sg.Button('Return to Main')],
        [sg.Button('Logout')]]
    return sg.Window('Bills Window', layout)


def window_update_information():
    layout = [
        [sg.Text('Your Info:')],
        [sg.Text('First Name: ', size=(15, 1)), sg.Input(key='firstName'), sg.Button('Save Name')],
        [sg.Text('Last Name: ', size=(15, 1)), sg.Input(key='lastName'), sg.Button('Save Surname')],
        [sg.Text('IBAN: ', size=(15, 1)), sg.Input(key='IBAN'), sg.Button('Save IBAN')],
        [sg.Text('Password: ', size=(15, 1)), sg.Input(key='password'), sg.Button('Save Password')],
        [sg.Button('Return to Main')],
        [sg.Button('Logout')]]
    return sg.Window('Update Info Window', layout)


# --- Button handlers ---
def button_delete_auction(values):
    if not values['auctions']:
        sg.popup('Select an auction')
        return
    auction = values['auctions'][2]
    if values['auctions'][1] != 'OnGoing':
        sg.popup('Select an ongoing auction to delete')
    else:
        cur.execute('DELETE FROM auction_categorizes WHERE auctionNo = ?', (auction,))
        con.commit()
        sg.popup(f'Auction {auction} deleted successfully.')


def button_show_bill(values):
    if not values['auctions']:
        sg.popup('Select an auction')
        return
    auction = values['auctions'][2]
    if values['auctions'][1] != 'Ended':
        sg.popup('Select a finished auction')
    else:
        cur.execute('SELECT tranNo, netAmount FROM bill_Generates_Payday WHERE auctionNo = ?', (auction,))
        row = cur.fetchone()
        if row is None:
            sg.popup('No bill found for this auction')
        else:
            sg.popup(f'Transaction No: {row[0]} | Amount: {row[1]}')


def button_update_username_information(values):
    Name = values['firstName']
    if not Name:
        sg.popup('Name cannot be empty!')
    else:
        cur.execute('UPDATE User SET firstName = ? WHERE ssn = ?', (Name, login_user_id))
        con.commit()
        sg.popup('First name updated successfully!')


def button_update_usersurname_information(values):
    Surname = values['lastName']
    if not Surname:
        sg.popup('Surname cannot be empty!')
    else:
        cur.execute('UPDATE User SET lastName = ? WHERE ssn = ?', (Surname, login_user_id))
        con.commit()
        sg.popup('Surname updated successfully!')


def button_update_seller_IBAN_information(values):
    IBAN = values['IBAN']
    if not IBAN:
        sg.popup('IBAN cannot be empty!')
    else:
        cur.execute('UPDATE Seller SET IBAN = ? WHERE SellerID = ?', (IBAN, login_user_id))
        con.commit()
        sg.popup('IBAN updated successfully!')


def button_update_password_information(values):
    password = values['password']
    if not password:
        sg.popup('Password cannot be empty!')
    else:
        cur.execute('UPDATE User SET password = ? WHERE ssn = ?', (password, login_user_id))
        con.commit()
        sg.popup('Password updated successfully!')


def button_create_auctions(values, window):
    startPrice = values['startPrice']
    description = values['description']
    title = values['title']
    endDate = values['endDate']
    buyitprice = values['buyitprice']
    catName = values['catName'][0] if values['catName'] else None

    try:
        datetime.strptime(endDate, "%d-%m-%Y")
    except Exception:
        sg.popup('Invalid date format. Please use dd-mm-yyyy.')
        return

    if not startPrice or not startPrice.isnumeric():
        sg.popup('Start price must be numeric and not empty.')
        return
    if not buyitprice or not buyitprice.isnumeric():
        sg.popup('Buy it price must be numeric and not empty.')
        return
    if not description or not title or not catName:
        sg.popup('Description, title, and category cannot be empty.')
        return

    startPrice = int(startPrice)
    buyitprice = int(buyitprice)
    if startPrice < 0:
        sg.popup('Start price cannot be negative')
        return

    cur.execute('SELECT MAX(auctionNo) FROM auction_categorizes')
    row = cur.fetchone()
    new_auction_no = (row[0] + 1) if row and row[0] else 1

    currentPrice = startPrice
    startDate = datetime.today().strftime('%Y-%m-%d')
    state = "OnGoing"

    cur.execute('''INSERT INTO auction_categorizes 
                   VALUES (?,?,?,?,?,?,?,?,null,?,?)''',
                (startPrice, description, title, catName,
                 currentPrice, state, endDate, startDate,
                 new_auction_no, buyitprice))
    cur.execute('INSERT INTO owns VALUES (?,?)', (new_auction_no, login_user_id))
    con.commit()

    sg.popup(f'Successfully created auction "{title}" with number {new_auction_no}')

    # clear inputs
    for key in ['startPrice', 'description', 'title', 'endDate', 'buyitprice']:
        window[key].update(value='')


def button_login(values):
    global login_user_id, login_user_name, login_user_type, window

    uid = values['id']
    upass = values['password']
    if not uid or not upass:
        sg.popup('ID and password cannot be empty')
        return

    cur.execute('SELECT ssn, firstName FROM User WHERE ssn = ? AND password = ?', (uid, upass))
    row = cur.fetchone()

    if row is None:
        sg.popup('ID or password is wrong!')
        return

    login_user_id, login_user_name = row[0], row[1]

    cur.execute('SELECT SellerID FROM Seller WHERE SellerID = ?', (uid,))
    row_seller = cur.fetchone()

    if row_seller:
        login_user_type = 'Seller'
        sg.popup(f'Welcome, {login_user_name} (Seller)')
        window.close()
        window = window_seller()
    else:
        cur.execute('SELECT BuyerID FROM Buyer WHERE BuyerID = ?', (uid,))
        row_buyer = cur.fetchone()
        if row_buyer:
            login_user_type = 'Buyer'
            sg.popup(f'Welcome, {login_user_name} (Buyer)')
            window.close()
            window = window_buyer()
        else:
            sg.popup('User type error! Please contact the admin.')


def button_list_bidders(values, window):
    auctions = values['auctions']
    if not auctions:
        sg.popup('Please choose an auction to list bidders.')
        return
    if auctions[1] == 'Ended':
        sg.popup('Please choose an ongoing auction to list bidders.')
        return

    aNo = auctions[2]
    bidders = [row for row in cur.execute(
        '''SELECT B.BuyerID, U.firstName, U.lastName, T.biddingPrice
           FROM Buyer B, TakesBids T, User U
           WHERE B.BuyerID = U.ssn
             AND B.BuyerID = T.buyerSsn
             AND T.auctionNo = ?
           ORDER BY T.biddingPrice ASC''',
        (aNo,)
    )]

    window['bidders'].update(values=bidders)


# --- Main Loop ---
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
        button_create_auctions(values, window)
    elif event == 'List Bidders':
        button_list_bidders(values, window)
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
        window.close()
        if login_user_type == 'Seller':
            window = window_seller()
        elif login_user_type == 'Buyer':
            window = window_buyer()
        else:
            window = window_login()
    elif event == 'Logout':
        login_user_id = login_user_name = login_user_type = -1
        window.close()
        window = window_login()
    elif event == sg.WIN_CLOSED:
        break

window.close()
con.commit()
con.close()
