Key links:

* http://www.kibot.com/free_historical_data.aspx

* http://www.kibot.com/data_format.aspx

------------------------

Kibot data format for historical text files
For maximum compatibility we store all of our data as standard, comma delimited text files. To see how our data files are formatted, you can download complete tick, aggregate bid/ask and 1 minute history for some of the instruments from the Free historical data samples section on our Buy page.

Other data formats and instrument types
This page focuses on the daily and minute format for stocks and ETFs. You can find out more about our futures, forex, tick and aggregate bid/ask data format on the support web page.

Intraday and daily (end-of-day) data format
Order of fields
Our files are standard comma-delimited text files. We use a separate file for every instrument. This is the order of fields:

Date, Time, Open, High, Low, Close, Volume

In daily files, the Time field is omitted. Every file is named using an instrument's symbol and a txt extension. For example, we keep our historical data for Microsoft Corporation in the MSFT.txt file.

Date and time format
Date values are recorded in the “mm/dd/yyyy” format. Time values are in the US Eastern Time (ET) time zone in the “hh:mm” format. Date and time values are separated by comma character. Daily (end of day) files have only Date value.

More information about the time zone issues is available here.

Market sessions
Intraday data records have a time stamp indicating the time when the bar opened. For example, a time stamp of 10:00 AM is for a period between 10:00 AM and 10:01 AM. All records with a time stamp between 9:30 AM and 3:59 PM represent the regular US trading session. Our stock and etf data includes pre-market (8:00-9:30 a.m. ET), regular (9:30 a.m. -4:00 p.m. ET.) and after market (4:00-6:30 p.m. ET.) sessions. Data records for SPY and some other liquid ETFs and stocks usually start at 4 a.m and ends at 8 p.m.

Splits and Dividends
All intraday and daily data is adjusted for stock splits and dividends. Since most of our customers are already familiar with Yahoo Finance historical daily data and are frequently comparing our data with Yahoo, we use the adjustment method as explained at this page

Volume is adjusted for splits and dividends in both intraday and daily files. In intraday files, volume field contains the number of shares exchanged during the duration of a specific bar. In our daily files, Volume field represents the number of all shares from both pre/after market sessions and the regular market session.

The Volume is adjusted in such a way so that the (price * volume) formula always gives the exact dollar amount exchanged during a specific time period. For example, let's say that a stock price is $10 and the volume is 100 shares. After a 2:1 split the price becomes $5 and volume 200. The total dollar amount remains the same.

For more information about our adjustment method please visit this web page.

Periods with no activity
If there were no transactions during a specific time interval, the data is not recorded. In our standard data files, the next bar is included after the next transaction and the whole period since the previous bar is ignored. You will find this situation often during pre/after market sessions and with less liquid stocks.

For more information, please visit this web page.

Daily close price
In our daily data files the closing price for the day is the last price before 16:00 or the close price of the 15:59 bar in the intraday file. For less liquid stocks, this can be before 15:59, but it is always the last intraday bar during the regular market session. If you use both intraday and daily data in your analysis, this increases the accuracy of your calculations.

We discuss some of the data format issues in greater detail on our support web page.

Exponential values
Some values are formatted with an exponent. For example, 1E-06 value represents 0.000001. Basically all prices below zero and with 5 or more decimal places are using the same format.

Please click here to see the list of all our products

