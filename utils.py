from datetime import date
from constants import *
import csv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from statistics import mean


def calculate_five_years_from_date(dt):
    # Add 5 years to the input datetime, considering leap years
    new_datetime = dt + relativedelta(years=+5)
    return new_datetime


def calculate_five_years_first_of_month(d):
    return date(d.year + 5, 1, 1)


def calculate_months_delta(earlier_date, later_date):
    return 12 * (later_date.year - earlier_date.year) + (later_date.month - earlier_date.month)


def print_processed_data(index_name, insights):
    total_days = insights[NUMBER_OF_TOTAL_DAYS]
    earning_entry_points = insights[EARNING_ENTRY_POINTS]
    at_least_100_percent_profit_days = insights[AT_LEAST_100_PERCENT_PROFIT_DAYS]
    losing_entry_points = insights[LOSING_ENTRY_POINTS]
    earning_days_percentage = insights[EARNING_DAYS_PERCENTAGE]
    at_least_100_percent_profit_percentage = round(100 * (at_least_100_percent_profit_days / total_days), 2)
    losing_days_percentage = insights[LOSING_DAYS_PERCENTAGE]

    print(f'----- Index name: {index_name} -----')
    print('----- Entry points (days) data -----')
    print(f'Total entry points (days) tested: {total_days}')
    print(f'Earning entry points (days): {earning_entry_points}')
    print(f'Earning 100%+ Profit entry points: {at_least_100_percent_profit_days}')
    print(f'Losing entry points: {losing_entry_points}')
    print(f'Percentage: Earning: {earning_days_percentage}%')
    print(f'Earning 100%+: {at_least_100_percent_profit_percentage}%')
    print(f'Losing: {losing_days_percentage}%\n')


def process_index_data(index_name):
    data_dict = {}
    calc_date_functions_dict = {SP500: calculate_five_years_first_of_month, NASDAQ: calculate_five_years_from_date}
    file_name = f'data/{index_name}.csv'

    with open(file_name, mode='r', encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            date = datetime.strptime(row[0], "%Y-%m-%d").date()
            data_dict[date] = {
                INDEX_RATE: round(float(row[INDEX_RATE_COLUMN[index_name]]), DECIMAL_DIGITS),
                DATE_IN_5_YEARS: calc_date_functions_dict[index_name](date),
                PERCENTAGE_CHANGE_IN_5_YEARS: None,
                FIRST_100P_PROFIT_DATE: None,
                MONTHS_TO_100P_PROFIT: None,
            }

    # Calculate percentage change and profit dates
    for date, data in data_dict.items():
        date_in_5_years = data[DATE_IN_5_YEARS]
        # This variable is intended to fix cases where date_in_5_years is not a trading day
        date_normalizer = 1 
        while(date_in_5_years not in data_dict and date_normalizer < WEEK):
            date_in_5_years = date_in_5_years + timedelta(days = date_normalizer)        
            date_normalizer += 1
        if date_in_5_years in data_dict:
            index_rate_in_5_years = data_dict[date_in_5_years][INDEX_RATE]
            index_rate_in_date = data[INDEX_RATE]
            percent_change_in_5_years = round(100 * index_rate_in_5_years / index_rate_in_date, DECIMAL_DIGITS) - 100
            data[PERCENTAGE_CHANGE_IN_5_YEARS] = percent_change_in_5_years

        for other_date, other_data in data_dict.items():
            if other_date > date and other_data[INDEX_RATE] / data[INDEX_RATE] >= 2:
                data[FIRST_100P_PROFIT_DATE] = other_date
                data[MONTHS_TO_100P_PROFIT] = calculate_months_delta(date, other_date)
                break

    # Filter data and calculate insights
    filtered_data_dict = {date: data for date, data in data_dict.items() if data[PERCENTAGE_CHANGE_IN_5_YEARS] is not None}
    date_and_percent_dict = {str(date): data[PERCENTAGE_CHANGE_IN_5_YEARS] for date, data in filtered_data_dict.items()}

    number_of_total_days = len(filtered_data_dict)
    earning_entry_points = sum(percentage > 0 for percentage in date_and_percent_dict.values())
    losing_entry_points = number_of_total_days - earning_entry_points

    earning_days_percentage = 100 * earning_entry_points / number_of_total_days
    earning_days_percentage = round(earning_days_percentage, DECIMAL_DIGITS)

    losing_days_percentage = 100 - earning_days_percentage
    losing_days_percentage = round(losing_days_percentage, DECIMAL_DIGITS)

    at_least_100_percent_profit_days = sum(percentage >= 100 for percentage in date_and_percent_dict.values())

    avg_num_of_months_for_100p_profit = mean(data[MONTHS_TO_100P_PROFIT] for data in data_dict.values() if data[MONTHS_TO_100P_PROFIT])
    avg_num_of_months_for_100p_profit = round(avg_num_of_months_for_100p_profit, DECIMAL_DIGITS)
    
    avg_percentage_change_in_5_years = mean(data[PERCENTAGE_CHANGE_IN_5_YEARS] for data in data_dict.values() if data[PERCENTAGE_CHANGE_IN_5_YEARS])
    avg_percentage_change_in_5_years = round(avg_percentage_change_in_5_years, DECIMAL_DIGITS)

    insights = {
        NUMBER_OF_TOTAL_DAYS: number_of_total_days,
        EARNING_ENTRY_POINTS: earning_entry_points,
        LOSING_ENTRY_POINTS: losing_entry_points,
        EARNING_DAYS_PERCENTAGE: earning_days_percentage,
        LOSING_DAYS_PERCENTAGE: losing_days_percentage,
        AT_LEAST_100_PERCENT_PROFIT_DAYS: at_least_100_percent_profit_days,
        AVG_NUM_OF_MONTHS_FOR_100P_PROFIT: avg_num_of_months_for_100p_profit,
        AVG_PERCENTAGE_CHANGE_IN_5_YEARS: avg_percentage_change_in_5_years
    }

    print_processed_data(index_name, insights)

    return data_dict, insights
