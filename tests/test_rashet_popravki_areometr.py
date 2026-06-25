from core import rashet_popravki_areometr, rashet_x1_x2_x3, itog_raschet_gran
import pandas as pd
import pytest

def test_rashet_popravki_areometr(dfs_popravki_test):
    df_input = dfs_popravki_test['df_input']
    df_tarirovk_test = dfs_popravki_test['df_tarirovk_test']
    expected = dfs_popravki_test['df_expected']

    result = rashet_popravki_areometr(df_input, df_tarirovk_test)

    pd.testing.assert_frame_equal(result, expected)

def test_rashet_x1_x2_x3(dfs_X1_X2_X3_test):
    df_input = dfs_X1_X2_X3_test['df_input']
    df_expected = dfs_X1_X2_X3_test['df_expected']
    udelka = 2.7

    result = rashet_x1_x2_x3(df_input, udelka)

    pd.testing.assert_frame_equal(result, df_expected)

def test_itog_rashet_gran(dfs_itog_test):
    df_input = dfs_itog_test['df_input']
    df_expected = dfs_itog_test['df_expected']

    result = itog_raschet_gran(df_input)
    pd.testing.assert_frame_equal(result, df_expected)
