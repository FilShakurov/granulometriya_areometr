import pandas as pd
import config

def zagr_file(path):
    df = pd.read_excel(path, skiprows=4, header=[0, 1, 2], na_values="-")

    df.columns = [process_multiheader_column(col) for col in df.columns]

    df = df.rename(columns=config.COlUMNS)
    df = df[config.COlUMNS.values()]

    return df


def process_multiheader_column(col):
    if isinstance(col, tuple):
        clean_parts = []
        for part in col:
            if pd.isna(part):
                continue
            part_str = str(part)
            if part_str.startswith("Unnamed:"):
                continue
            if part_str.strip() and part_str != "nan":
                clean_parts.append(part_str.strip())
        return "_".join(clean_parts) if clean_parts else f"column_{hash(col) % 1000}"
    return str(col).strip()


def obrabotka_df_posle_zagr(df):
    df['lab_nomer'] = df['lab_nomer'].ffill()

    df_agg = df.groupby('lab_nomer').agg({**config.agg_dict, **config.temp_agg})

    df_agg.columns = [process_multiheader_column(col) for col in df_agg.columns]
    df_agg = df_agg.reset_index()

    df_agg[config.COLS_GRAN] = df_agg[config.COLS_GRAN].fillna(0)

    return df_agg


def zagr_tarirovki(path):
    df_tarirovk = pd.read_excel(path)
    df_tarirovk = df_tarirovk.set_index('№')

    return df_tarirovk


def rashet_popravki_areometr(df_agg, df_tarirovk):
    df_agg['popravka_t1'] = df_agg.apply(get_value1, axis=1, ref_df=df_tarirovk, col_temp='1_zamer/temp_last')
    df_agg['popravka_t2'] = df_agg.apply(get_value1, axis=1, ref_df=df_tarirovk, col_temp='2_zamer/temp_last')
    df_agg['popravka_t3'] = df_agg.apply(get_value1, axis=1, ref_df=df_tarirovk, col_temp='3_zamer/temp_last')

    df_agg['zamer_1'] = df_agg['1_zamer/temp_first'] + df_agg['popravka_t1']
    df_agg['zamer_2'] = df_agg['2_zamer/temp_first'] + df_agg['popravka_t2']
    df_agg['zamer_3'] = df_agg['3_zamer/temp_first'] + df_agg['popravka_t3']

    return df_agg


def get_value1(row, ref_df, col_temp):
    idx = row['areometr_first']
    col = row[col_temp]
    # .at работает быстро для одиночного доступа по метке
    return ref_df.at[idx, col] if idx in ref_df.index and col in ref_df.columns else None


def rashet_x1_x2_x3(df_agg, udelka):
    df_agg['udelka'] = udelka

    df_agg['koef_K'] = (df_agg['gran_10_first'] + df_agg['gran_5-10_first'] + df_agg['gran_5-2_first'] + df_agg[
        'gran_2-1_first'])

    df_agg = df_agg.dropna(subset=['3_zamer/temp_first'])

    df_agg['X1'] = df_agg['udelka'] * df_agg['zamer_1'] / (df_agg['udelka'] - 1) / df_agg[
        'kolba/naveska_s_rast_last'] * (100 - df_agg['koef_K'])
    df_agg['X2'] = df_agg['udelka'] * df_agg['zamer_2'] / (df_agg['udelka'] - 1) / df_agg[
        'kolba/naveska_s_rast_last'] * (100 - df_agg['koef_K'])
    df_agg['X3'] = df_agg['udelka'] * df_agg['zamer_3'] / (df_agg['udelka'] - 1) / df_agg[
        'kolba/naveska_s_rast_last'] * (100 - df_agg['koef_K'])

    return df_agg


def itog_raschet_gran(df_agg):
    df_agg['m_probi_bez_krupn'] = df_agg['kolba/naveska_last'] - df_agg[config.COLS_GRAN_KOEF_K].sum(axis=1)

    df_agg['gran_10_%'] = df_agg['gran_10_first'] / df_agg['kolba/naveska_last'] * 100
    df_agg['gran_5-10_%'] = df_agg['gran_5-10_first'] / df_agg['kolba/naveska_last'] * 100
    df_agg['gran_5-2_%'] = df_agg['gran_5-2_first'] / df_agg['kolba/naveska_last'] * 100
    df_agg['gran_2-1_%'] = df_agg['gran_2-1_first'] / df_agg['kolba/naveska_last'] * 100

    df_agg['gran_1-0,5_%'] = df_agg['gran_1-0,5_first'] / df_agg['m_probi_bez_krupn'] * (100 - df_agg['koef_K'])
    df_agg['gran_0,5-0,25_%'] = df_agg['gran_0,5-0,25_first'] / df_agg['m_probi_bez_krupn'] * (100 - df_agg['koef_K'])
    df_agg['gran_0,25-0,10_%'] = df_agg['gran_0,25-0,10_first'] / df_agg['m_probi_bez_krupn'] * (100 - df_agg['koef_K'])

    df_agg['gran_0.05-0.01_%'] = df_agg['X1'] - df_agg['X2']
    df_agg['gran_0.01-0.002_%'] = df_agg['X2'] - df_agg['X3']
    df_agg['gran_0.002_%'] = df_agg['X3']

    df_agg['gran_0,10-0,05_%'] = 100 - df_agg[config.cols_kr_prozent].sum(axis=1) - df_agg[
        config.cols_melk_prozent].sum(axis=1)

    return df_agg


def rashet_gran(df_agg, df_tarirovk, udelka):
    df_agg = rashet_popravki_areometr(df_agg, df_tarirovk)
    df_agg = rashet_x1_x2_x3(df_agg, udelka)
    df_agg = itog_raschet_gran(df_agg)

    return df_agg