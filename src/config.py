COlUMNS = {
    'Регистационный номер пробы': "lab_nomer",
    'Номер колбы_Масса возд. сух. навески, г': 'kolba/naveska_s_rast',
    'Номер колбы_Масса возд. сух. навески, г с учетом РО': "kolba/naveska",
    'Номер ареометра': 'areometr',
    '1 замер_Температура, °С': '1_zamer/temp',
    '2 замер_Температура, °С': '2_zamer/temp',
    '3 замер_Температура, °С': '3_zamer/temp',
    'Содержание растительных остатков': 'rast_ost',
    'Масса фракций, г_>10': 'gran_10',
    'Масса фракций, г_5-10': 'gran_5-10',
    'Масса фракций, г_5-2': 'gran_5-2',
    'Масса фракций, г_2-1': 'gran_2-1',
    'Масса фракций, г_1-0,5': 'gran_1-0,5',
    'Масса фракций, г_0,5-0,25': 'gran_0,5-0,25',
    'Масса фракций, г_0,25-0,10': 'gran_0,25-0,10',
}

COLS_GRAN = [
    'gran_10_first', 'gran_5-10_first',
    'gran_5-2_first', 'gran_2-1_first',
    'gran_1-0,5_first', 'gran_0,5-0,25_first',
    'gran_0,25-0,10_first'
]

COLS_GRAN_KOEF_K = [
    'gran_10_first',
    'gran_5-10_first',
    'gran_5-2_first',
    'gran_2-1_first',
]

agg_dict = {
    'kolba/naveska_s_rast': 'last',
    'kolba/naveska': 'last',
    'areometr': 'first',
    'rast_ost': 'first',
    'gran_10': 'first',
    'gran_5-10': 'first',
    'gran_5-2': 'first',
    'gran_2-1': 'first',
    'gran_1-0,5': 'first',
    'gran_0,5-0,25': 'first',
    'gran_0,25-0,10': 'first',
}

temp_agg = {
    '1_zamer/temp': ['first', 'last'],
    '2_zamer/temp': ['first', 'last'],
    '3_zamer/temp': ['first', 'last'],
}

cols_prozent_vse = [
    'lab_nomer',
    'gran_10_%',
    'gran_5-10_%',
    'gran_5-2_%',
    'gran_2-1_%',
    'gran_1-0,5_%',
    'gran_0,5-0,25_%',
    'gran_0,25-0,10_%',
    'gran_0,10-0,05_%',
    'gran_0.05-0.01_%',
    'gran_0.01-0.002_%',
    'gran_0.002_%'
]

cols_kr_prozent = [
    'gran_10_%',
    'gran_5-10_%',
    'gran_5-2_%',
    'gran_2-1_%',
    'gran_1-0,5_%',
    'gran_0,5-0,25_%',
    'gran_0,25-0,10_%'
]

cols_melk_prozent = [
    'gran_0.05-0.01_%',
    'gran_0.01-0.002_%',
    'gran_0.002_%'
]