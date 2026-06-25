from core import zagr_file, zagr_tarirovki, obrabotka_df_posle_zagr, rashet_gran
import config

PATH_NAMIV = "test_namiv2.xlsx"
PATH_TARIROVKI = "tarirovki.xlsx"
udelka = 2.7

df = zagr_file(PATH_NAMIV)
df_tarirovk = zagr_tarirovki(PATH_TARIROVKI)

df_agg = obrabotka_df_posle_zagr(df)

df_agg = rashet_gran(df_agg, df_tarirovk, udelka)

df_agg.to_excel('test2.xlsx')

df_itog = df_agg[config.cols_prozent_vse].copy()

print(df_itog)