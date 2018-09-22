

import sqlite3 as sql
import datetime
import random

CMD_create_table = "CREATE TABLE {tablename} ({newfield} {fieldtype} PRIMARY KEY)"

#future command needs mapping string
CMD_insert_item_data = "INSERT OR IGNORE INTO Items (Unique_ID, Item_Desc) VALUES ({item_ID}, '{item_desc}')"
CMD_insert_item_price = "INSERT OR IGNORE INTO Items_Price_History (Item_Unique_ID, Date, Item_Price) VALUES ({item_ID}, '{date}', {item_price})"
## may not need to do an innerjoin just do two selects?
## also need to sort on datetime
CMD_get_item_price_history = "SELECT Date, Item_Price FROM Items_Price_History WHERE Item_Unique_ID = {item_ID} ORDER BY Date DESC;"
CMD_get_item_info = "SELECT Item_Desc FROM Items WHERE Unique_ID = {item_ID};"

db_location = 'C:\\sqllite\\Databases\\Menards_Data.db'

def insert_item_desc(conn, ID, desc):
    c = conn.cursor()
    try:
        c.execute(CMD_insert_item_data.format(item_ID=ID, item_desc=desc))
        conn.commit()
    except Exception:
        print('ERROR occurred in: insert_item_desc(conn, ID, desc):')
    finally:
        c.close()


## add logic to only update price on same day if price is different
def insert_item_price(conn, ID, price, date='default'):
    
    # used for testing purposes to simulate entries gathered at earlier dates
    if date is 'default':
        date_entry = datetime.datetime.now()
    else:
        date_entry = date
        
    c = conn.cursor()
    try:
        c.execute(CMD_insert_item_price.format(item_ID=ID, date=str(date_entry), item_price=price))
        conn.commit()
    except Exception as e:
        print('ERROR occurred in: def insert_item_price(conn, ID, desc):')
        print(e)
    finally:
        c.close()

def get_item_data(conn, ID):
    '''
    Searches Database using item's ID and returns a  containing, (item ID, item desc, list[all item's price history])
    '''
    c = conn.cursor()
    try:
        c.execute(CMD_get_item_info.format(item_ID=ID))
        
        Item_from_Items_table = c.fetchone()

        # make sure item has valid entry, maybe through exception in future?
        if Item_from_Items_table is None:
            print("ID# {} was not found in database".format(ID))
            exit

        print("Why does c.fetchone() return this object:", Item_from_Items_table)
        item_desc = Item_from_Items_table[0]
        
        c.execute(CMD_get_item_price_history.format(item_ID=ID))
        item_price_history = c.fetchall()

        for i in item_price_history:
            print(i)

        return (ID, item_desc, item_price_history)
    except Exception as e:
        print(e)
    finally:
        c.close()

def connect_to_sql():
    print("Connecting to database...")
    with sql.connect(db_location) as connection:
        return connection

def create_fake_data(conn, num_points):
    fake_ID = 1234567
    fake_desc = "fake tool"
    insert_item_desc(conn=conn, ID=fake_ID, desc=fake_desc)

    # create a week of past days
    entry_list = [datetime.datetime(2018, 9, 15, 10, 46, 22, 617403) - datetime.timedelta(days=random.uniform(-100, 100)) for x in range(num_points)]
    prev_price = 500.00
    for e in entry_list:
        insert_item_price(conn=conn, ID=fake_ID, price=prev_price, date=e)
        prev_price = round((prev_price + random.uniform(-25.00, 25.0)), 2)

if __name__ == '__main__':

    conn = connect_to_sql()

    
    ##item = get_item_data(conn, ID = 1234567)
    #print(item)

    create_fake_data(conn, num_points=50)




