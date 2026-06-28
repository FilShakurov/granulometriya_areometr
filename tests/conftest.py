import sys

import pytest
import pandas as pd


@pytest.fixture
def dfs_popravki_test():
    data1 = {
        'areometr_first': [882],
        '1_zamer/temp_first': [15],
        '1_zamer/temp_last': [20.5],
        '2_zamer/temp_first': [5],
        '2_zamer/temp_last': [20.5],
        '3_zamer/temp_first': [-0.1],
        '3_zamer/temp_last': [21],
    }
    df_input = pd.DataFrame(data1)

    data2 = {
        'popravka_t1': [1.4],
        'popravka_t2': [1.4],
        'popravka_t3': [1.5],
        'zamer_1': [16.4],
        'zamer_2': [6.4],
        'zamer_3': [1.4],
    }

    df_expected = pd.DataFrame({**data1, **data2})

    df_tarirovk_test = pd.DataFrame({
        '№': [882],
        20.5: [1.4],
        21: [1.5],
    })
    df_tarirovk_test = df_tarirovk_test.set_index('№')


    return {
        'df_input': df_input,
        'df_expected': df_expected,
        'df_tarirovk_test': df_tarirovk_test,
    }

@pytest.fixture
def dfs_X1_X2_X3_test():
    data1 = {
        'kolba/naveska_s_rast_last': [30.13],
        'gran_10_first': [0],
        'gran_5-10_first': [0],
        'gran_5-2_first': [0],
        'gran_2-1_first': [0.03],
        '3_zamer/temp_first': [-0.1],
        'zamer_1': [16.4],
        'zamer_2': [6.4],
        'zamer_3': [1.4],
    }

    df_agg_input = pd.DataFrame(data1)

    data2 = {
        'udelka': [2.7],
        'koef_K': [0.03],
        'X1': [86.4229827609769],
        'X2': [33.7260420530642],
        'X3': [7.37757169910779],
    }

    df_expected = pd.DataFrame({**data1, **data2})

    return {
        'df_input': df_agg_input,
        'df_expected': df_expected,
    }

@pytest.fixture
def dfs_itog_test():
    data1 = {
        'kolba/naveska_last': [30.13],
        'koef_K': [0.03],
        'gran_10_first': [0.0],
        'gran_5-10_first': [0.0],
        'gran_5-2_first': [0.0],
        'gran_2-1_first': [0.03],
        'gran_1-0,5_first': [0.04],
        'gran_0,5-0,25_first': [0.1],
        'gran_0,25-0,10_first': [0.23],
        'X1': [86.4229827609769],
        'X2': [33.7260420530642],
        'X3': [7.37757169910779],
    }

    df_agg_input = pd.DataFrame(data1)

    data2 = {
        'm_probi_bez_krupn': [30.1],
        'gran_10_%': [0.0],
        'gran_5-10_%': [0.0],
        'gran_5-2_%': [0.0],
        'gran_2-1_%': [0.1],
        'gran_1-0,5_%': [0.1],
        'gran_0,5-0,25_%': [0.3],
        'gran_0,25-0,10_%': [0.8],

        'gran_0.05-0.01_%': [52.7],
        'gran_0.01-0.002_%': [26.3],
        'gran_0.002_%': [7.4],
        'gran_0,10-0,05_%': [12.3],
    }

    df_expected = pd.DataFrame({**data1, **data2})

    return {
        'df_input': df_agg_input,
        'df_expected': df_expected,
    }