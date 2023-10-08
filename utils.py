from datetime import date
from constants import *
import csv
from datetime import datetime
from statistics import mean


def calculate_five_years_from_date(d):
    # Fix date day in order to fit %7 == 0
    new_day = d.day-2 if d.day > 2 else d.day+5
    return date(d.year+5, d.month, new_day)


def calculate_five_years_first_of_month(d):
    return date(d.year + 5, 1, 1)


def calculate_months_delta(first_d, second_d):
    return 12 * (second_d.year - first_d.year) + (second_d.month - first_d.month)


def process_index_data(index_name):
    data_dict = {}
    calc_date = {SP500: calculate_five_years_first_of_month, NASDAQ: calculate_five_years_from_date}
    with open(f'data/{index_name}.csv', mode='r', encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            date = datetime.strptime(row[0], "%Y-%m-%d").date()
            data_dict[date] = {
                'index_rate': round(float(row[INDEX_RATE_COLUMN[index_name]]), DECIMAL_DIGITS),
                'date_in_5_years': calc_date[index_name](date),
                'percentage_change_in_5_years': None,
                'first_100p_profit_date': None,
                'months_to_100p_profit': None,
            }

    for date, data in data_dict.items():
        date_in_5_years = data['date_in_5_years']
        if date_in_5_years in data_dict:
            percent = round(100 * data_dict[date_in_5_years]['index_rate'] / data['index_rate'],
                            DECIMAL_DIGITS) - 100
            data['percentage_change_in_5_years'] = percent
        for otherDate in sorted(data_dict):
            if otherDate > date and data_dict[otherDate]['index_rate'] / data['index_rate'] >= 2:
                data['first_100p_profit_date'] = otherDate
                data['months_to_100p_profit'] = calculate_months_delta(date, otherDate)
                break

    filtered_data_dict = {date: data for date, data in data_dict.items() if
                          data_dict[date]['percentage_change_in_5_years'] is not None}
    
    date_and_percent_dict = {str(date): filtered_data_dict[date]['percentage_change_in_5_years'] for date in
                             filtered_data_dict.keys()}
    
    number_of_total_days = len(filtered_data_dict)
    earning_entry_points = sum(x > 0 for x in date_and_percent_dict.values())
    losing_entry_points = sum(x < 0 for x in date_and_percent_dict.values())

    earning_days_percentage = 100 * round(earning_entry_points / number_of_total_days, DECIMAL_DIGITS)
    losing_days_percentage = 100 - earning_days_percentage

    at_least_100_percent_profit_days = sum(x >= 100 for x in date_and_percent_dict.values())
    ave_num_of_months_for_100p_profit = mean(
        [data["months_to_100p_profit"] for data in data_dict.values() if data["months_to_100p_profit"]])
    ave_percentage_change_in_5_years = mean(
        [data["percentage_change_in_5_years"] for data in data_dict.values() if
         data["percentage_change_in_5_years"]])
    
    print(f'-----Index name: {index_name} -----')
    print('-----Entry points (days) data-----')
    print(f'Total entry points (days) tested: {number_of_total_days}')
    print(f'Earning entry points (days): {earning_entry_points}')
    print(f'Earning 100%+ Profit entry points: {at_least_100_percent_profit_days}')
    print(f'Losing entry points: {losing_entry_points}')
    print(f'Percentage: Earning: {earning_days_percentage}%')
    print(f'Earning 100%+: {100 * round(at_least_100_percent_profit_days/number_of_total_days, DECIMAL_DIGITS)}%')
    print(f'Losing: {losing_days_percentage}%')
    print('\n')


    insights = {
        'num_total_days': number_of_total_days,
        'earning_points': earning_entry_points,
        'losing_points': losing_entry_points,
        'earning_percent': earning_days_percentage,
        'losing_percent': losing_days_percentage,
        '100p_profit_days': at_least_100_percent_profit_days,
        'ave_num_of_months_for_100p_profit': round(ave_num_of_months_for_100p_profit, DECIMAL_DIGITS),
        'ave_percentage_change_in_5_years': round(ave_percentage_change_in_5_years, DECIMAL_DIGITS)
    }
    return data_dict, insights
