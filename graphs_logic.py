import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import sqrt

class ErrorBarPlotterBase:
    def __init__(self, data_for_errorbars, data_for_plots, labels):
        self.data_for_errorbars = data_for_errorbars
        self.data_for_plots = data_for_plots
        self.labels = labels

        if self.data_for_plots is None:
            raise ValueError("data_for_plots cannot be None")

    def main_scatterplot(self, graph_data, label):
        df = pd.DataFrame(graph_data)
        try:
            x = label[0]
            y = label[1]
            title = label[2]
        except IndexError:
            x = "x"
            y = "y"
            title = ""
        sns.scatterplot(x=x, y=y, data=df, color="blue", label=y)

    def error_lineplot(self, error_data, main_data):
        df = pd.DataFrame(main_data)
        error_data = pd.DataFrame(error_data)
        error_data["Sstd"] = error_data.std(axis=1)
        error_data["Sins"] = 0.1
        error_data["S"] = sqrt((error_data["Sstd"]) ** 2 + (error_data["Sins"]) ** 2)
        error_data["error min"] = df["y"] - error_data["S"]
        error_data["error max"] = df["y"] + error_data["S"]
        error_data["x"] = df["x"]
        sns.lineplot(x="x", y="error min", data=error_data, color="black", label="error bars")
        sns.lineplot(x="x", y="error max", data=error_data, color="black")

    def plot_data(self, ax, graph_data, error_data, label):
        self.main_scatterplot(graph_data, label)
        if error_data is not None:
            try:
                self.error_lineplot(error_data, graph_data)
            except (IndexError, TypeError):
                print("Error plotting error bars")
        ax.set_xlabel(label[0])
        ax.set_ylabel(label[1])
        ax.legend()

class ErrorBarPlotterOverlay(ErrorBarPlotterBase):
    def make_graph(self):
        if self.data_for_errorbars is not None:
            for index, graph_data in enumerate(self.data_for_plots):
                self.main_scatterplot(graph_data, self.labels[index])
                try:
                    self.error_lineplot(self.data_for_errorbars[index], graph_data)
                except IndexError:
                    pass
            plt.xlabel(self.labels[0][0])
            plt.ylabel(self.labels[0][1])
            plt.title(self.labels[0][2])
            plt.legend()
        plt.show()

class ErrorBarPlotterSeparate(ErrorBarPlotterBase):
    def make_graph(self):
        num_datasets = len(self.data_for_plots)
        fig, axes = plt.subplots(nrows=num_datasets, figsize=(8, 4 * num_datasets))

        for index, (graph_data, error_data) in enumerate(zip(self.data_for_plots, self.data_for_errorbars)):
            try:
                label = self.labels[index]
            except IndexError:
                label = ["x", "y", ""]
            ax = axes[index]
            self.plot_data(ax, graph_data, error_data, label)
            ax.set_title(f"Dataset {index + 1}: {label[2]}")
        plt.tight_layout()
        plt.show()
