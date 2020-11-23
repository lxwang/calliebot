#%%
import json 
import time

with open('callie_scripts/options_chains_list.json') as f:
    option_chains_list = json.load(f) 

option_dates = list(option_chains_list[0]['callExpDateMap'].keys())
print(option_dates)


option_short_list= []
option_long_list=[]

if len(option_dates) == 3:
    for option in option_chains_list:
        try:
            ## reinitilize empty dict
            option_short_dict ={}
            option_long_dict={}

            name = option['underlying']['symbol']
            option = option['callExpDateMap']
            first_date = option[option_dates[0]]
            second_date = option[option_dates[1]]
            third_date = option[option_dates[2]]
            strikes = list( first_date.keys() ) ## list of strikes  given date
            
            ## dictionary varaible stuff ...

            option_short_dict['ticker']  = name
            option_short_dict['strikes'] = []
            option_short_dict['goldenRatio'] = []

            option_long_dict['ticker']  = name
            option_long_dict['strikes'] = []
            option_long_dict['goldenRatio'] = []
            for strike in strikes:
                # variables to filter calendar 
                first_date_strike = first_date[strike][0]
                second_date_strike = second_date[strike][0]
                third_date_strike = third_date[strike][0]

                golden_ratio = first_date_strike['mark'] / second_date_strike['mark'] ## bid, ask, mark, last ['']
                totalVolume = first_date_strike['totalVolume'] + second_date_strike['totalVolume']
                openInterest = first_date_strike['openInterest'] + second_date_strike['openInterest']

                golden_ratio1 = second_date_strike['mark'] / third_date_strike['mark'] ## bid, ask, mark, last ['']
                totalVolume1 = second_date_strike['totalVolume'] + third_date_strike['totalVolume']
                openInterest1 = third_date_strike['openInterest'] + third_date_strike['openInterest']

                volatiltiy = first_date_strike['volatility']
                theoreticalOptionValue = first_date_strike['theoreticalOptionValue']

                # this week filter 
                if golden_ratio >= .65 and golden_ratio <= .9 and totalVolume >= 500 and openInterest >= 1000: 
                    option_short_dict['strikes'].append(strike) 
                    option_short_dict['goldenRatio'].append(golden_ratio) 
                    option_short_dict['dates'] = [option_dates[0], option_dates[1]]
                # next week filter
                if golden_ratio1 >= .65 and golden_ratio1 <= .9 and totalVolume1 >= 500 and openInterest1 >= 1000: 
                    option_long_dict['strikes'].append(strike) 
                    option_long_dict['goldenRatio'].append(golden_ratio1) 
                    option_long_dict['dates'] = [option_dates[1], option_dates[2]]
            ## only append to list when there are strikes present from the filter
            if option_short_dict['strikes']:
                option_short_list.append(option_short_dict)

            if option_long_dict['strikes']:
                option_long_list.append(option_long_dict)
        except: 
            pass

### save option_short_list and optino_long_list
with open('callie_scripts/option_short_filter.json', 'w') as f:
    json.dump(option_short_list, f)
with open('callie_scripts/option_long_filter.json', 'w') as f:
    json.dump(option_long_list, f)