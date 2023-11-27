import tkinter as tk
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import sqrt
from graphs import *

class ErrorBarPlotterGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Error Bar Plotter")

        self.data_for_plots_path_label = tk.Label(master, text="Path to data_for_plots CSV:")
        self.data_for_plots_path_label.pack()
        self.data_for_plots_path_entry = tk.Entry(master)
        self.data_for_plots_path_entry.pack()
        self.data_for_plots_button = tk.Button(master, text="Browse", command=self.browse_data_for_plots)
        self.data_for_plots_button.pack()

        self.data_for_errorbars_path_label = tk.Label(master, text="Path to data_for_errorbars CSV:")
        self.data_for_errorbars_path_label.pack()
        self.data_for_errorbars_path_entry = tk.Entry(master)
        self.data_for_errorbars_path_entry.pack()
        self.data_for_errorbars_button = tk.Button(master, text="Browse", command=self.browse_data_for_errorbars)
        self.data_for_errorbars_button.pack()

        self.labels_label = tk.Label(master, text="Labels:")
        self.labels_label.pack()
        self.x_label_entry = tk.Entry(master, text="x-axis label")
        self.x_label_entry.pack()
        self.y_label_entry = tk.Entry(master, text="y-axis label")
        self.y_label_entry.pack()
        self.title_entry = tk.Entry(master, text="Plot Title")
        self.title_entry.pack()

        self.generate_plot_button = tk.Button(master, text="Generate Plot", command=self.generate_plot)
        self.generate_plot_button.pack()

    def browse_data_for_plots(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.data_for_plots_path_entry.delete(0, tk.END)
        self.data_for_plots_path_entry.insert(0, file_path)

    def browse_data_for_errorbars(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.data_for_errorbars_path_entry.delete(0, tk.END)
        self.data_for_errorbars_path_entry.insert(0, file_path)

    def generate_plot(self):
        data_for_plots_path = self.data_for_plots_path_entry.get()
        data_for_errorbars_path = self.data_for_errorbars_path_entry.get()

        # Load data from CSV files
        data_for_plots = pd.read_csv(data_for_plots_path)
        data_for_errorbars = pd.read_csv(data_for_errorbars_path)

        # Extracting x and y labels and plot title from text boxes
        x_label = self.x_label_entry.get()
        y_label = self.y_label_entry.get()
        title = self.title_entry.get()

        # Creating an instance of ErrorBarPlotterOverlay and generating the overlay plot
        error_bar_plotter_overlay = ErrorBarPlotterOverlay([data_for_errorbars], [data_for_plots], [(x_label, y_label, title)])
        error_bar_plotter_overlay.make_graph()

if __name__ == "__main__":
    root = tk.Tk()
    app = ErrorBarPlotterGUI(root)
    root.mainloop()
