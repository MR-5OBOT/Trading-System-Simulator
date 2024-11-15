import matplotlib.pyplot as plt
import pandas as pd


def data_ploter():
    with open(file_path) as file:
        data = pd.read_csv(file)
        columns = data.columns
        print(f"Columns: {', '.join(columns)}")  # clear output for the column by join() func
        # print(data)
        # inputs
        xlabel = input("X-axis: ")
        ylabel = input("Y-axis: ")
        chart_type = input("line or bar chart: ")

    # plots
    if chart_type == "line":
        plt.style.use("ggplot")
        plt.figure(figsize=(10, 6))
        plt.title("Performance")
        plt.plot(data[xlabel], data[ylabel])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        # plt.grid()
        plt.legend()
        plt.show()
    elif chart_type == "bar":
        plt.figure(figsize=(10, 6))
        plt.style.use("ggplot")
        plt.title("Performance")
        plt.bar(data[xlabel], data[ylabel])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        # plt.grid()
        plt.legend()
        plt.show()
    else:
        print("Invalid chart type")


file_path = input("CSV File (Full path): ")

data_ploter()
