"""CSCA08: Assignment 3: Hypertension and Low Income

Starter code.

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) Jacqueline Smith, David Liu, and Anya Tafliovich

"""

from typing import TextIO
import statistics

from constants import (CityData, ID, HT, TOTAL, LOW_INCOME,
                       SEP, HT_ID_COL, LI_ID_COL,
                       HT_NBH_NAME_COL, LI_NBH_NAME_COL,
                       HT_20_44_COL, NBH_20_44_COL,
                       HT_45_64_COL, NBH_45_64_COL,
                       HT_65_UP_COL, NBH_65_UP_COL,
                       POP_COL, LI_POP_COL,
                       HT_20_44_IDX, HT_45_64_IDX, HT_65_UP_IDX,
                       NBH_20_44_IDX, NBH_45_64_IDX, NBH_65_UP_IDX
                       )
SAMPLE_DATA = {
    'West Humber-Clairville': {
        'id': 1,
        'hypertension': [703, 13291, 3741, 9663, 3959, 5176],
        'total': 33230, 'low_income': 5950},
    'Mount Olive-Silverstone-Jamestown': {
        'id': 2,
        'hypertension': [789, 12906, 3578, 8815, 2927, 3902],
        'total': 32940, 'low_income': 9690},
    'Thistletown-Beaumond Heights': {
        'id': 3,
        'hypertension': [220, 3631, 1047, 2829, 1349, 1767],
        'total': 10365, 'low_income': 2005},
    'Rexdale-Kipling': {
        'id': 4,
        'hypertension': [201, 3669, 1134, 3229, 1393, 1854],
        'total': 10540, 'low_income': 2140},
    'Elms-Old Rexdale': {
        'id': 5,
        'hypertension': [176, 3353, 1040, 2842, 948, 1322],
        'total': 9460, 'low_income': 2315}
}
SECOND_DATA = {
    'West Humber-Clairville': {
        'id': 1,
        'hypertension': [700, 7000, 3300, 8000, 4000, 5000],
        'total': 36000, 'low_income': 6000},
    'Mount Olive-Silverstone-Jamestown': {
        'id': 2,
        'hypertension': [800, 12000, 4000, 9000, 3000, 4000],
        'total': 33000, 'low_income': 10000},
    'Thistletown-Beaumond Heights': {
        'id': 3,
        'hypertension': [200, 4000, 1000, 3000, 1000, 2000],
        'total': 10000, 'low_income': 2000},
    'Rexdale-Kipling': {
        'id': 4,
        'hypertension': [200, 4500, 1500, 3500, 500, 2000],
        'total': 10000, 'low_income': 2000}
}
THIRD_DATA = {
    'West Humber-Clairville': {
        'id': 1,
        'hypertension': [700, 7000, 3300, 8000, 4000, 5000],
        'total': 36000, 'low_income': 6000},
    'Mount Olive-Silverstone-Jamestown': {
        'id': 2,
        'hypertension': [800, 12000, 4000, 9000, 3000, 4000],
        'total': 36000, 'low_income': 10000},
    'Thistletown-Beaumond Heights': {
        'id': 3,
        'hypertension': [200, 4000, 1000, 3000, 1000, 2000],
        'total': 10000, 'low_income': 2000},
    'Rexdale-Kipling': {
        'id': 4,
        'hypertension': [200, 4500, 1500, 3500, 500, 2000],
        'total': 10000, 'low_income': 2000}
}
EPSILON = 0.005


# This function is provided for use in Task 3. You do not need to
# change it.  Note the use of EPSILON constant (similar to what we had
# in asisgnment 2) for testing.
def get_age_standardized_ht_rate(city_data: CityData, nbh_name: str) -> float:
    """Return the age standardized hypertension rate from the
    neighbourhood in city_data with neighbourhood name nbh_name.

    Precondition: nbh_name is in city_data

    >>> abs(get_age_standardized_ht_rate(SAMPLE_DATA, 'Elms-Old Rexdale') -
    ...     24.44627) < EPSILON
    True
    >>> abs(get_age_standardized_ht_rate(SAMPLE_DATA, 'Rexdale-Kipling') -
    ...     24.72562) < EPSILON
    True

    """

    rates = calculate_ht_rates_by_age_group(city_data, nbh_name)

    # These rates are normalized for only 20+ ages, using the census data
    # that our datasets are based on.
    canada_20_44 = 11_199_830 / 19_735_665   # Number of 20-44 / Number of 20+
    canada_45_64 = 5_365_865 / 19_735_665    # Number of 45-64 / Number of 20+
    canada_65_plus = 3_169_970 / 19_735_665  # Number of 65+ / Number of 20+

    return (rates[0] * canada_20_44 + rates[1] * canada_45_64 +
            rates[2] * canada_65_plus)


def get_hypertension_data(data: dict[CityData], file: TextIO) -> None:
    """Modify the data so that it contains the hypertension data in the file.
    """
    content = file.readlines()
    for i in range(len(content)):
        if i == 0:
            continue
        line_list = content[i].strip().split(SEP)
        data_list = []
        for i in range(HT_20_44_COL, NBH_65_UP_COL + 1):
            data_list.append(int(line_list[i]))
        if line_list[HT_NBH_NAME_COL] in data:
            data[line_list[HT_NBH_NAME_COL]][HT] = \
                data_list
        else:
            data[line_list[HT_NBH_NAME_COL]] = \
                {ID: int(line_list[HT_ID_COL]), HT: data_list}


def get_low_income_data(data: dict, file: TextIO) -> None:
    """The new dictionary contain key/value pairs whose keys are
    the names of every neighbourhood in the file, and whose values
    are dictionaries which contain at least the keys ID and HT for
    those neighbourhoods.
    """
    content = file.readlines()
    for i in range(len(content)):
        if i == 0:
            continue
        line_list = content[i].strip().split(SEP)
        if line_list[LI_NBH_NAME_COL] in data:
            data[line_list[LI_NBH_NAME_COL]][TOTAL] = \
                int(line_list[POP_COL])
            data[line_list[LI_NBH_NAME_COL]][LOW_INCOME] = \
                int(line_list[LI_POP_COL])
        else:
            data[line_list[LI_NBH_NAME_COL]] = \
                {ID: int(line_list[LI_ID_COL]),
                 TOTAL: int(line_list[POP_COL]), LOW_INCOME: int(line_list[
                        LI_POP_COL])}


def get_bigger_neighbourhood(city: CityData, nei_1: str, nei_2: str) -> str:
    """Return the name of the neighborhood which has higher population
    in the city, given neigh_1 and neigh_2
    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'West Humber-Clairville', \
'Mount Olive-Silverstone-Jamestown')
    'West Humber-Clairville'
    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'Elms-Old Rexdale', \
'West Humber-Clairville')
    'West Humber-Clairville'
    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'Elms-Old Rexdale', 'awefbik')
    'Elms-Old Rexdale'
    """
    if nei_1 in city:
        if nei_2 in city:
            return compare_neibourhood(city, nei_1, nei_2)
        return nei_1
    if nei_2 in city:
        return nei_2
    return nei_1


def compare_neibourhood(city: CityData, nei_1: str, nei_2: str) -> str:
    """compare the populations between nei_1 and nei_2 from the given city
    """
    if city[nei_1][TOTAL] < city[nei_2][TOTAL]:
        return nei_2
    if city[nei_1][TOTAL] == city[nei_2][TOTAL]:
        return nei_1
    return nei_1


def get_high_hypertension_rate(city: CityData,
                               threshold: float) -> list[tuple[str, float]]:
    """Return a list of tuples representing all neighbourhoods in city \
    with a hypertension rate greater than or equal to the threshold.
    >>> get_high_hypertension_rate(SAMPLE_DATA, 0.3)
    [('Thistletown-Beaumond Heights', 0.31797739151574084), \
('Rexdale-Kipling', 0.3117001828153565)]
    >>> get_high_hypertension_rate(SAMPLE_DATA, 0.4)
    []
    >>> get_high_hypertension_rate(SAMPLE_DATA, 0.29)
    [('West Humber-Clairville', 0.2987202275151084), \
('Thistletown-Beaumond Heights', 0.31797739151574084), \
('Rexdale-Kipling', 0.3117001828153565)]
    """
    result = []
    for element in compute_hyper_rate(city):
        if element[1] >= threshold:
            result.append(element)
    return result
# helper function of get_high_hypertension_rate


def compute_hyper_rate(city: CityData) -> list[tuple[str, float]]:
    """return the hyper rate from the given city
    """
    result = []
    for neighbourhood in city:
        adult_pop = city[neighbourhood][HT][NBH_20_44_IDX] + \
            city[neighbourhood][HT][NBH_45_64_IDX] + \
            city[neighbourhood][HT][NBH_65_UP_IDX]
        hyper_total = city[neighbourhood][HT][HT_20_44_IDX] + \
            city[neighbourhood][HT][HT_45_64_IDX] + \
            city[neighbourhood][HT][HT_65_UP_IDX]
        rate = hyper_total / adult_pop
        result.append((neighbourhood, rate))
    return result


def get_ht_to_low_income_ratios(city: CityData) -> dict[str, float]:
    """Return a dictionary where the keys are the same as in the city,
    and the values are the ratio of the hypertension rate to the low income
    rate for that neighbourhood.
    >>> get_ht_to_low_income_ratios(SAMPLE_DATA)
    {'West Humber-Clairville': 1.6683148168616895, \
'Mount Olive-Silverstone-Jamestown': 0.9676885451091314, \
'Thistletown-Beaumond Heights': 1.6438083107534431, \
'Rexdale-Kipling': 1.5351962275111484, 'Elms-Old Rexdale': 1.1763941257986577}
    >>> get_ht_to_low_income_ratios(SECOND_DATA)
    {'West Humber-Clairville': 2.4000000000000004, \
'Mount Olive-Silverstone-Jamestown': 1.0296, \
'Thistletown-Beaumond Heights': 1.222222222222222, \
'Rexdale-Kipling': 1.0999999999999999}
    """
    result = {}
    for i in range(len(city)):
        rate = compute_hyper_rate(city)[i][1] / income_rate(city)[i][1]
        hood = compute_hyper_rate(city)[i][0]
        result[hood] = rate
    return result
# helper functions of get_ht_to_low_income_ratio


def income_rate(city: CityData) -> list[tuple[str, float]]:
    """return the income rate of the given city
    """
    result = []
    for hood in city:
        rate = city[hood][LOW_INCOME] / city[hood][TOTAL]
        result.append((hood, rate))
    return result


def calculate_ht_rates_by_age_group(city: CityData,
                                    hood: str) -> tuple[float, float, float]:
    """Returns a tuple of three values, representing the hypertension rate \
    for each of the three age groups in the hood of the city as a percentage.
    >>> calculate_ht_rates_by_age_group(SAMPLE_DATA, 'Elms-Old Rexdale')
    (5.24903071875932, 36.593947923997185, 71.70953101361573)
    >>> calculate_ht_rates_by_age_group(SAMPLE_DATA, 'West Humber-Clairville')
    (5.289293506884358, 38.71468488047191, 76.48763523956723)
    """
    rate1 = city[hood][HT][HT_20_44_IDX] / city[hood][HT][NBH_20_44_IDX] * 100
    rate2 = city[hood][HT][HT_45_64_IDX] / city[hood][HT][NBH_45_64_IDX] * 100
    rate3 = city[hood][HT][HT_65_UP_IDX] / city[hood][HT][NBH_65_UP_IDX] * 100
    return (rate1, rate2, rate3)


def get_correlation(city: CityData) -> float:
    """Return the correlation between age standardised hypertension rates \
    and low income rates across all neighbourhoods in the city.
    >>> get_correlation(SAMPLE_DATA)
    0.28509539188554994
    >>> get_correlation(SECOND_DATA)
    0.21203002137332072
    """
    return statistics.correlation(stand_ht_rate_list(city),
                                  low_income_list(city))
# helper functions of get_correlation


def stand_ht_rate_list(city: CityData) -> list[float]:
    """return the list of standard hypertension rate of the given city
    """
    result = []
    for hood in city:
        result.append(get_age_standardized_ht_rate(city, hood))
    return result


def low_income_list(city: CityData) -> list[float]:
    """return the low income list of the given city
    """
    result = []
    for hood in city:
        result.append(city[hood][LOW_INCOME] / city[hood][TOTAL])
    return result


def order_by_ht_rate(city: CityData) -> list[str]:
    """Return a list of the names of the neighbourhoods in the city, ordered \
    from lowest to highest age-standardised hypertension rate.
    >>> order_by_ht_rate(SAMPLE_DATA)
    ['Elms-Old Rexdale', 'Rexdale-Kipling', 'Thistletown-Beaumond Heights', \
'West Humber-Clairville', 'Mount Olive-Silverstone-Jamestown']
    >>> order_by_ht_rate(SECOND_DATA)
    ['Rexdale-Kipling', 'Thistletown-Beaumond Heights', \
'Mount Olive-Silverstone-Jamestown', 'West Humber-Clairville']
    """
    sorted_list = []
    result = []
    for hood in city:
        sorted_list.append((get_age_standardized_ht_rate(city, hood), hood))
    sorted_list.sort()
    for my_variable in sorted_list:
        result.append(my_variable[1])
    return result


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    small_data = {}
    with open('hypertension_data_small.csv') as ht_small_f:
        get_hypertension_data(small_data, ht_small_f)
    with open('low_income_small.csv') as li_small_f:
        get_low_income_data(small_data, li_small_f)

    print('Did we build the dict correctly?', small_data == SAMPLE_DATA)
    print('Correlation in small data file:', get_correlation(small_data))

    example_neighbourhood_data = {}
    with open('hypertension_data_2016.csv') as ht_example_f:
        get_hypertension_data(example_neighbourhood_data, ht_example_f)
    with open('low_income_2016.csv') as li_example_f:
        get_low_income_data(example_neighbourhood_data, li_example_f)
    print('Correlation in example data file:',
          get_correlation(example_neighbourhood_data))
