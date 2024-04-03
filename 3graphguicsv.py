import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class VibrationAnalyzerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Vibration Analyzer")
        self.master.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.graph_frame = ttk.Frame(self.master)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(3, 1, figsize=(6, 6))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.load_csv1_button = ttk.Button(self.master, text="Load CSV for Graph 1", command=lambda: self.load_csv(0))
        self.load_csv1_button.pack()

        self.load_csv2_button = ttk.Button(self.master, text="Load CSV for Graph 2", command=lambda: self.load_csv(1))
        self.load_csv2_button.pack()

        self.load_csv3_button = ttk.Button(self.master, text="Load CSV for Graph 3", command=lambda: self.load_csv(2))
        self.load_csv3_button.pack()

        self.select_button = ttk.Button(self.master, text="Select Part", command=self.select_part)
        self.select_button.pack()

    def load_csv(self, idx):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                # Assume the first column is time and the rest are data columns
                time = df.iloc[:, 0]
                data_col = df.iloc[:, 1]

                self.ax[idx].plot(time, data_col)

                self.canvas.draw()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def select_part(self):
        try:
            for ax in self.ax:
                ax.set_xlim(auto=True)
                ax.set_ylim(auto=True)
                ax.patches.clear()

            self.canvas.draw()

            messagebox.showinfo("Select Part", "Select the part by clicking and dragging on the graph.")

            def onselect(eclick, erelease):
                x0, y0 = eclick.xdata, eclick.ydata
                x1, y1 = erelease.xdata, erelease.ydata

                for ax in self.ax:
                    rect = ax.add_patch(plt.Rectangle((min(x0, x1), min(y0, y1)), abs(x1 - x0), abs(y1 - y0),
                                                      facecolor='yellow', alpha=0.5))
                self.canvas.draw()

            self.fig.canvas.mpl_connect('button_press_event', onselect)
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = VibrationAnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()