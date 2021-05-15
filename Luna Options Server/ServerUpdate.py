"""
Script for server updates, can change based on needs
"""
import APICallScript as api
import LunaOptionsDB as db
import SandP500List as snp


def update():
    luna = db.LunaDB()
    api_obj = api.APICalls()
    for ticker in snp.ticker_list:
        ticker.lower()
        table = luna.get_table(ticker, '_options')
        print(table)
        print(ticker)
        if table:
            if table == [] or len(table[0]) == 4:
                print('ADDING COLUMN')
                luna.add_column(ticker, '_options', 'historicalVolatility', 'varchar(32)')

        hv = api_obj.historical_volatility_call(ticker)
        if hv and 'indicator' in hv.keys():
            historical_volatility = hv['indicator'][0][0]
            historical_volatility = float(historical_volatility)
            historical_volatility = historical_volatility * 100
            historical_volatility = round(historical_volatility, 2)

        else:
            historical_volatility = 'N/A'
        try:
            luna.update_column_conditional(ticker, '_options', 'historicalVolatility', str(historical_volatility), 'id', '1')
        except:
            print('PASSED: ', ticker)

    print('Update Complete!')


update()
