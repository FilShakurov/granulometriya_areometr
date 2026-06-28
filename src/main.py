import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox)
import traceback
from core import zagr_file, zagr_tarirovki, obrabotka_df_posle_zagr, rashet_gran
import config
from database.database import DatabaseSample


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = DatabaseSample("database/database.db")

        self.initUI()


    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Шаблон')

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.btn = QPushButton("Загрузить намыв")
        self.btn.clicked.connect(self.zagr_namiv)
        main_layout.addWidget(self.btn)

    def zagr_namiv(self):
        try:
            path_namiv, _ = QFileDialog.getOpenFileName(
                self, "Выберите файл намыва", "", "Excel Files (*.xlsx *.xls)")
            if not path_namiv:
                return

            path_tarirovki, _ = QFileDialog.getOpenFileName(
                self, "Выберите файл тарировки", "", "Excel Files (*.xlsx *.xls)")
            if not path_tarirovki:
                return

            df = zagr_file(path_namiv)
            df_tarirovk = zagr_tarirovki(path_tarirovki)
            udelka = 2.7

            df_agg = obrabotka_df_posle_zagr(df)
            df_itog, spisok_otrizat_grani = rashet_gran(df_agg, df_tarirovk, udelka)

            if spisok_otrizat_grani:
                QMessageBox.warning(self, "Внимание", f"Есть отрицательные граны {spisok_otrizat_grani}")

            df_db = df_itog.rename(columns=config.cols_bd_rename)

            self.db.add_proby_and_granulometry_from_df(df_db)

            self.save_rashet_namiva(df_agg)

            QMessageBox.information(self, "Успех", "Граны расчитаны успешно")
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Ошибка", f"Ошибка {e}")
            traceback.print_exc()


    def save_rashet_namiva(self, df_agg):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить расчеты",
            "Расчет гранов после намыва",
            "Excel Files (*.xlsx *.xls)"
        )
        if not file_path:
            return

        df_agg.to_excel(file_path)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# db = DatabaseSample("database/database.db")
# PATH_NAMIV = "../test_namiv2.xlsx"
# PATH_TARIROVKI = "../tarirovki.xlsx"
# udelka = 2.7
#
# df = zagr_file(PATH_NAMIV)
# df_tarirovk = zagr_tarirovki(PATH_TARIROVKI)
#
# df_agg = obrabotka_df_posle_zagr(df)
#
# df_agg = rashet_gran(df_agg, df_tarirovk, udelka)
#
# df_agg.to_excel('test3.xlsx')
#
# df_itog = df_agg[config.cols_prozent_vse].copy()
#
# df_db = df_itog.rename(columns=config.cols_bd_rename)
#
# db.add_proby_and_granulometry_from_df(df_db)
#
# print(df_itog)