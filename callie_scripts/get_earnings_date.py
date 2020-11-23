import re, json, datetime
from datetime import date

from config import client_id, redirect_uri, option_price_threshold, calendar_ratio_threshold, spread_ratio_threshold, OTM_amount, date_delta
from yahoo_earnings_calendar import YahooEarningsCalendar

def get_front_date(date_delta):
    dates_list = []
    for i in range(0, date_delta):
        d = datetime.date.today()
        d += datetime.timedelta(i)
        if d.weekday() == 4:
            dates_list.append(str(d))
    #print(dates_list[-2])
    return dates_list[0]

def get_back_date(date_delta):
    dates_list = []
    for i in range(0, date_delta):
        d = datetime.date.today()
        d += datetime.timedelta(i)
        if d.weekday() == 4:
            dates_list.append(str(d))
    #print(dates_list[-1])
    return dates_list[-1]

front_date = get_front_date(date_delta)
back_date = get_back_date(date_delta)

# ========= check earnings calendar ==========
date_from = datetime.datetime.strptime(date.today().strftime('%Y-%m-%d') + " 05:00:00",  '%Y-%m-%d %X')
date_to = datetime.datetime.strptime(front_date + " " + "18:00:00", '%Y-%m-%d %X')
#print(date_from, date_to)


yec = YahooEarningsCalendar()
'''
    get earnings date and ticker from yahoo calendar library
    save as format:
    [
        {
        ticker: 'string',
        date: 'string',
        },
        ...
    ]


'''
#print('getting earnings dates from yahoo')
earnings_list= []
#print(yec.earnings_on(date_from))
#earnings_calendar = yec.earnings_between(date_from, date_to) # <-- get request for yahoo calendar ehre
earnings_calendar = yec.earnings_between(date_from, date_to)
#print(earnings_calendar)
if earnings_calendar:
    for company in earnings_calendar:
        earnings_dict = {}
        earnings_dict['ticker'] = company['ticker']
        earnings_dict['date'] = re.findall('\d\d\d\d-\d\d-\d\d',company['startdatetime'])[0]
        earnings_list.append(earnings_dict)

    with open('callie_scripts/companies_earnings.json', 'w') as f:
        json.dump(earnings_list, f)