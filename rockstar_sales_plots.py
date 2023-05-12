import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox as messagebox


# Define the products
products = ['Drink1', 'Drink2', 'Drink3', 'Drink4', 'Drink5', 'Drink6', 'Drink7']

# Create the main window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Display welcome message
messagebox.showinfo("Welcome", "Welcome to Drink Analytics! Please select the file with sales data needed to be analyzed.")

# Prompt user to select CSV file
file_path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
if not file_path:
    messagebox.showerror("Error", "No file selected.")
    exit()

# Load the sales data from the selected CSV file
sales_data = pd.read_csv(file_path)
weeks = sales_data['Week'].nunique()

def plot_data(data, store_name, ax1, ax2):
    # Calculate the weekly sales totals for all drinks combined
    weekly_totals = data[products].sum(axis=1)

    # Calculate the total cases sold for each drink
    product_totals = data[products].sum(axis=0)

    # Round the limits of the y-axis to a multiple of 5
    y_max = round(weekly_totals.max() + 5, -1)
    y_min = round(weekly_totals.min() - 5, -1)

    # Set the number of ticks on the y-axis
    num_ticks = 8

    # Set the title if store_name is provided
    if store_name:
        ax1.set_title(store_name)

    # Plot the weekly sales trend for all drinks combined
    ax1.plot(range(1, weeks + 1), weekly_totals)
    ax1.set_xlabel("Week")
    ax1.set_ylabel("Sales by case")
    ax1.set_ylim(y_min, y_max)
    ax1.set_yticks(range(y_min, y_max + 1, int((y_max - y_min) / (num_ticks - 1))))

    # Plot the total cases sold for each drink in a bar plot
    ax2.bar(products, product_totals)
    for i, value in enumerate(product_totals):
        ax2.text(i, value, str(value), ha='center', va='bottom')
    ax2.set_xlabel("Product")
    ax2.set_ylabel("Sales by case")

"""
def plot_growth():

1. Calculate the total weekly sales: This is done by summing the sales of all 
   drinks for each week. This is the weekly_totals line in the function.

2. Calculate the growth rate: This is done using the pct_change function in pandas 
   which computes the percentage change from the immediately previous row by default. 
   This calculates the week-over-week growth rate of the total sales. This is then multiplied
    by 100 to convert it to a percentage. This is the growth_rate line in the function.

3. Plot the growth rate: The growth rate is then plotted with the week number on the 
   x-axis and the growth rate on the y-axis. Note that the first week is excluded when 
   plotting since there is no growth rate for the first week (as there is no previous week
   to compare it to). This is done by using slicing [1:] on growth_rate.

This process is done for each store if store information is available in the dataset, 
or for the entire dataset if no store information is provided.

"""

def plot_growth(data, ax):
    # Calculate the weekly sales totals for all drinks combined
    weekly_totals = data[products].sum(axis=1)
    
    # Calculate the growth rate
    growth_rate = weekly_totals.pct_change() * 100  # percent change from previous week

    # Set the title
    ax.set_title("Sales growth rate")
    
    # Plot the growth rate
    ax.plot(range(2, weeks + 1), growth_rate[1:])  # exclude the first week because it has no previous week to compare to
    ax.set_xlabel("Week")
    ax.set_ylabel("Growth rate (%)")

# Check if the "Store" column exists in the dataset
if 'Store' in sales_data.columns:
    # Get the unique store names
    stores = sales_data['Store'].unique()

    # Create a new figure
    plt.figure()

    # Loop through each store and create a separate plot
    for idx, store in enumerate(stores):
        # Filter the data for the current store
        store_data = sales_data[sales_data['Store'] == store].set_index('Week')

        # Create subplot axes
        ax1 = plt.subplot(len(stores), 3, 3 * idx + 1)
        ax2 = plt.subplot(len(stores), 3, 3 * idx + 2)
        ax3 = plt.subplot(len(stores), 3, 3 * idx + 3)

        # Plot the data for the current store
        plot_data(store_data, store, ax1, ax2)
        plot_growth(store_data, ax3)

    # Adjust layout and display the plots
    plt.tight_layout()
    plt.show()
else:
    # Set the index to 'Week' column
    sales_data.set_index('Week', inplace=True)

    # Create a new figure
    plt.figure(figsize=(15,5))

    # Create subplot axes
    ax1 = plt.subplot(1, 3, 1)
    ax2 = plt.subplot(1, 3, 2)
    ax3 = plt.subplot(1, 3, 3)

    # Plot the data for the entire dataset without store information
    plot_data(sales_data, None, ax1, ax2)
    plot_growth(sales_data, ax3)

    # Adjust layout and display the plots
    plt.tight_layout()
    plt.show()
