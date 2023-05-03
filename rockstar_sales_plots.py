import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk

# Define the products and weeks
products = ['Drink1', 'Drink2', 'Drink3', 'Drink4', 'Drink5', 'Drink6', 'Drink7']
weeks = range(1, 9)

# Create the main window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Prompt the user to select a CSV file with sales data
file_path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
if not file_path:
    print("No file selected.")
    exit()

# Load the sales data from the selected CSV file
sales_data = pd.read_csv(file_path, index_col=0)

# Calculate the weekly sales totals for all drinks combined
weekly_totals = sales_data.sum(axis=1)

# Calculate the total cases sold for each drink
product_totals = sales_data.sum(axis=0)

# Round the limits of the y-axis to a multiple of 5
y_max = round(weekly_totals.max() + 5, -1)
y_min = round(weekly_totals.min() - 5, -1)

# Set the number of ticks on the y-axis
num_ticks = 8

# Plot the weekly sales trend for all drinks combined
plt.subplot(2, 1, 1)
plt.plot(weeks, weekly_totals)
plt.title("Weekly Sales Trend")
plt.xlabel("Week")
plt.ylabel("Sales by case")
plt.ylim(y_min, y_max)
plt.yticks(range(y_min, y_max + 1, int((y_max - y_min) / (num_ticks - 1))))

# Plot the total cases sold for each drink in a bar plot
plt.subplot(2, 1, 2)
plt.bar(products, product_totals)
for i, value in enumerate(product_totals):
    plt.text(i, value, str(value), ha='center', va='bottom')
plt.title("Total Cases Sold")
plt.xlabel("Product")
plt.ylabel("Sales by case")

plt.tight_layout()
plt.show()