import menards_selenium as mse
import menards_sql as msq

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# variables used for indexing into object structure returned from msq.get_item_data
date = 0
price = 1
price_history = 2



def get_plot():

    fake_id = 1234567
    menards_db = msq.connect_to_sql()
    item_data = msq.get_item_data(conn=menards_db, ID=fake_id)

    dates = [x[date] for x in item_data[price_history]]
    prices = [x[price] for x in item_data[price_history]]

    ts = pd.Series(prices, index=dates)

    ts.plot()
    plt.title("Price history for " + item_data[1])
    plt.ylabel("Prices")
    plt.xlabel("Date")
    #plt.show()


    return dates, prices

if __name__ == '__main__':
    get_plot()
    
    
    