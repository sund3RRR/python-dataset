# Импортируем библиотеки.
import pandas, numpy, seaborn, matplotlib, scipy

from math import sqrt
from sklearn.linear_model import LinearRegression

class Dataset:
    def __init__(self, data_file_name) -> None:
        self.init_df(data_file_name)
        self.init_df_ed()
        self.init_x_y()
        self.init_indicators()
        self.delete_anomaly()
        self.init_pirson_k()
        self.init_correlation_significance()
        self.init_icm_1()
        self.init_df_ebd()
        self.init_icm_2()


    def init_df(self, data_file_name):
        '''Загружаем датасэт.'''

        df = pandas.read_csv(data_file_name, encoding = 'ISO-8859-1', delimiter = ',').drop('Unnamed: 0', axis = 1)
        df.sample(10)

        self.df = df


    def init_df_ed(self):
        '''Создаём новый датасэт из двух переменных первого датасэта и выбираем данные для анализа, а также рисуем их распределение.'''

        self.df_ed = self.df[['Energy', 'Danceability']].copy()
        #
        #
        #
        #seaborn.displot(self.x, kind = 'kde')
        #
        #
        #


    def init_x_y(self):
        self.x = self.df_ed.iloc[:, 0].to_numpy()
        self.y = self.df_ed.iloc[:, -1].to_numpy()
    

    def init_indicators(self):
        '''Находим количество, среднее значение и стандартное отклонение данных.'''

        self.n = len(self.x) # count
        self.x_bar = sum(self.x) / self.n #avg
        self.s = sqrt(sum((x_i - self.x_bar) ** 2 for x_i in self.x) / self.n - 1) # standart distribution


    def is_normal(self):
        '''Проверяем данные на нормальное распределение по ассиметрии и эксцессу.'''

        a = (1 / (self.n * self.s ** 3)) * sum((x_i - self.x_bar) ** 3 for x_i in self.x)
        e = (1 / (self.n * self.s ** 4)) * sum((x_i - self.x_bar) ** 4 for x_i in self.x) - 3
        d_a = (6 * self.n - 1) / ((self.n + 1) * (self.n + 3))
        d_e = (24 * (self.n - 2) * (self.n - 3) * self.n) / ((self.n + 1) ** 2 * (self.n + 3) * (self.n + 5))
        if abs(a) <= 3 * sqrt(d_a) and abs(e) <= 5 * sqrt(d_e):
            return True
        else:
            return False


    def delete_anomaly(self):
        '''Начинаем удалять аномалии, если распределение не нормально и проверяем на нормальность.'''

        for x_i in self.x:
            if x_i > self.x_bar + 3 * self.s or x_i < self.x_bar - 3 * self.s:
                self.x = numpy.delete(self.x, numpy.where(self.x == x_i))
                self.n = len(self.x)
                self.x_bar = sum(self.x) / self.n
                self.s = sqrt(sum((x_i - self.x_bar) ** 2 for x_i in self.x) / self.n - 1)
        
        if  not self.is_normal():
            self.delete_anomaly()
    
    
    def init_pirson_k(self):
        '''Считаем коэффициент Пирсона (корреляцию).'''

        self.r = self.df_ed.corr(method = 'pearson').iloc[0, 1]

    
    def init_correlation_significance(self) -> bool:
        '''Two-tailed test.
            H0 - корреляция статистически не значима (r = 0).
            H1 - корреляция статистическа значима (r != 0).'''
            
        t_dist = scipy.stats.t.pdf(self.x, df = self.n - 1, loc = self.x_bar, scale = self.s)

        quantile = 1.676

        t_v = (self.r * sqrt(self.n - 2)) / sqrt(1 - self.r ** 2)
        t_t = quantile * (self.n - 1)

        if abs(t_v) > t_t:
            self.is_correlation_significance = True
        elif abs(t_v) < t_t:
            self.is_correlation_significance = False


    def init_icm_1(self):
        '''Строим линейную регрессию и находим коэффициенты b0 и b1.'''

        linear_regression = LinearRegression()
        linear_regression.fit(self.x.reshape(-1, 1), self.y.reshape(-1, 1))

        self.intercept_1 = linear_regression.intercept_[0]
        self.coefficient_1 = linear_regression.coef_.flatten()
        self.model_score_1 = linear_regression.score(self.x.reshape(-1, 1), self.y.reshape(-1, 1))
        #
        #
        #
        # seaborn.regplot(x = 'Energy', y = 'Danceability', data = self.df_ed)
        #
        #
        #
    

    def init_df_ebd(self):
        '''Создаём новый датасэт из трёх переменных.'''

        self.df_ebd = self.df[['Energy', 'Beats.Per.Minute', 'Danceability']].copy()

        self.x_ebd = self.df_ebd.drop('Danceability', axis = 1)
        self.y_ebd = self.df_ebd['Danceability']

        self.df_ebd.sample(10)


    def init_icm_2(self):
        '''Строим многофакторную линейную регрессию.'''
        linear_regression_ebd = LinearRegression()
        linear_regression_ebd.fit(self.x_ebd, self.y_ebd)

        self.intercept_2 = linear_regression_ebd.intercept_
        self.coefficient_2 = linear_regression_ebd.coef_.flatten()
        self.model_score_2 = linear_regression_ebd.score(self.x_ebd, self.y_ebd)

    def correlation(self):
        pass
        #
        #
        #
        # axes = matplotlib.pyplot.axes(projection = '3d')
        # axes.scatter3D(self.df_ebd['Energy'], self.df_ebd['Beats.Per.Minute'], self.df_ebd['Danceability'])
        #
        #
        #