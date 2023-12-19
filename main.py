from constants import *
import matplotlib.pyplot as plt
from utils import process_index_data


def time_to_100_percent_plot(nasdaq_data, nasdaq_insights, snoopy_data, snoopy_insights):
    plt.plot(nasdaq_data.keys(), [data[MONTHS_TO_100P_PROFIT] for data in nasdaq_data.values()], 'c-', label='Nasdaq')
    plt.plot(snoopy_data.keys(), [data[MONTHS_TO_100P_PROFIT] for data in snoopy_data.values()], 'm-',
             label='S&P 500')
    plt.xlabel('Date')
    plt.ylabel('Months to 100% profit')
    plt.title(f'Nasdaq & S&P500 Indices - Number of months needed to double an investment \n'
              f'Nasdaq average: {nasdaq_insights[AVG_NUM_OF_MONTHS_FOR_100P_PROFIT]} \n'
              f'S&P500 average: {snoopy_insights[AVG_NUM_OF_MONTHS_FOR_100P_PROFIT]} ')
    plt.legend()
    plt.show()


def five_years_investment_plot(nasdaq_data, nasdaq_insights, snoopy_data, snoopy_insights):
    plt.plot(nasdaq_data.keys(), [data[PERCENTAGE_CHANGE_IN_5_YEARS] for data in nasdaq_data.values()], 'c-',
             label='Nasdaq')
    plt.plot(snoopy_data.keys(), [data[PERCENTAGE_CHANGE_IN_5_YEARS] for data in snoopy_data.values()], 'm-',
             label='S&P 500')
    plt.xlabel('Date')
    plt.ylabel('Percentage change in 5 years')
    plt.title(f'Nasdaq & S&P500 Indices - Percentage change in 5 years \n'
              f'Nasdaq average: {nasdaq_insights[AVG_PERCENTAGE_CHANGE_IN_5_YEARS]} \n'
              f'S&P500 average: {snoopy_insights[AVG_PERCENTAGE_CHANGE_IN_5_YEARS]} ')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    nasdaq_data, nasdaq_insights = process_index_data(NASDAQ)
    snoopy_data, snoopy_insights = process_index_data(SP500)
    time_to_100_percent_plot(nasdaq_data, nasdaq_insights, snoopy_data, snoopy_insights)
    five_years_investment_plot(nasdaq_data, nasdaq_insights, snoopy_data, snoopy_insights)


