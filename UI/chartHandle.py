import seaborn as sns
import matplotlib.pyplot as plt

class ChartHandle:
    def __init__(self, connector=None):
        self.connector = connector
    def getExplode(self,df, columnLabel):
        explode = [0.1]
        for i in range(len(df[columnLabel]) - 1):
            explode.append(0)
        return explode

    def visualizeDistribution(self, figure, canvas, df, column, xlabel, title):
        figure.clear()
        ax = figure.add_subplot(111)
        ax.ticklabel_format(useOffset=False, style="plain")
        ax.grid()
        ax.bar(df[column], df["Status 0 Count"], label="status 0")
        ax.bar(df[column], df["Status 1 Count"], label="status 1")
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Count")
        ax.legend()
        canvas.draw()
