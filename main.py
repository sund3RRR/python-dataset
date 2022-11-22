import sys, pandas, seaborn
from PyQt6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from scripts.dataset import Dataset
from form.form import Ui_MainWindow


def seaborndisplot(data):
    return seaborn.displot(data, kind = 'kde', height=3)


def seabornregplot(data):
    return seaborn.regplot(x = 'Energy', y = 'Danceability', data = data)


def read_csv(file_name :str) -> list[list]:
    df = pandas.read_csv(file_name, delimiter=',', encoding = "ISO-8859-1")
    data = [[row[col] for col in df.columns] for row in df.to_dict('records')]
    return data


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, plot):
        self.fig = plot.figure
        self.axes = plot.axes
        super().__init__(self.fig)

        
class App(Ui_MainWindow):
    def __init__(self, MainWindow) -> None:
        super().__init__()
        self.setupUi(MainWindow)
        self.dataset_table.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        data = read_csv("data/top50.csv")
        self.set_dataset_table_data(data)
        self.dataset = Dataset("data/top50.csv")

        self.load_button.clicked.connect(self.load)
        

    def load(self):
        self.set_dataset_to_sample(self.dataset.df_ed, self.sample_dataset_2)
        self.set_dataset_to_sample(self.dataset.df_ebd, self.sample_dataset_3)

        
        self.regression_graphic_1 = MplCanvas(plot=seabornregplot(self.dataset.df_ed))
        self.regression_layout_1.addWidget(self.regression_graphic_1)
        self.regression_layout_1.itemAt(1).widget().setMaximumSize(400, 250)


        self.distribution_graphic = MplCanvas(plot=seaborndisplot(self.dataset.x))
        self.distribution_layout_1.addWidget(self.distribution_graphic)
        self.distribution_layout_1.itemAt(1).widget().setMaximumSize(400, 250)

        self.count.setText(str(self.dataset.n))
        self.avg.setText(str(self.dataset.x_bar))
        self.standart_dev.setText(str(self.dataset.s))
        self.coeff_pirson.setText(str(self.dataset.r))
        self.correl.setText(str(self.dataset.is_correlation_significance))
        self.intercept_1.setText(str(self.dataset.intercept_1))
        self.coefficient_1.setText(str(self.dataset.coefficient_1))
        self.model_score_1.setText(str(self.dataset.model_score_1))
        
        self.intercept_2.setText(str(self.dataset.intercept_2))
        self.coefficient_2.setText(str(self.dataset.coefficient_2))
        self.model_score_2.setText(str(self.dataset.model_score_2))


    def set_dataset_to_sample(self, df, table):
        data = [[row[col] for col in df.columns] for row in df.to_dict('records')]
        table.setRowCount(len(data))

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                new_item = QtWidgets.QTableWidgetItem(str(item))
                table.setItem(i, j, new_item)
        
        header = table.horizontalHeader()   
        for i in range(0, header.count()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)


    def set_dataset_table_data(self, data):
        self.dataset_table.setRowCount(len(data))

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                new_item = QtWidgets.QTableWidgetItem(str(item))
                self.dataset_table.setItem(i, j, new_item)
        
        header = self.dataset_table.horizontalHeader()   
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        for i in range(4, header.count()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)



if __name__ == "__main__":    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = App(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())