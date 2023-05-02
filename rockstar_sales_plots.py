import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.gridspec as gridspec

def import_csv_data():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)
            if not set(products).issubset(df.columns):
                messagebox.showerror("Invalid CSV", "The CSV file must contain the required product columns.")
                return

            sales_data = {product: df[product].tolist() for product in products}
            plot_sales_data_from_dict(sales_data)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the CSV file: {str(e)}")


# Function to validate user input
def validate_input(input_str):
    try:
        value = int(input_str)
        if value < 0:
            raise ValueError("The value must be a non-negative integer.")
        return value
    except ValueError as e:
        messagebox.showerror("Invalid input", e)
        return None

# Function to plot the sales data
def plot_sales_data():
    # Retrieve the sales data
    sales_data = {}
    for i, product in enumerate(products):
        sales = []
        for day in range(num_days.get()):
            sale_str = product_entries[i][day].get()
            sale = validate_input(sale_str)
            if sale is not None:
                sales.append(sale)
            else:
                return
        sales_data[product] = sales

    # Calculate the weekly sales totals
    weekly_totals = [sum(sales) for sales in sales_data.values()]

    # Calculate the total sales for each product
    product_totals = [sum(sales) for sales in sales_data.values()]

    # Create the figure and the gridspec
    fig = plt.figure(figsize=(10, 5))  # Adjust the figure size to fit the side-by-side plots
    gs = gridspec.GridSpec(1, 2, figure=fig)  # Change the number of rows to 1 and the number of columns to 2

    # Plot the weekly sales trends
    ax1 = fig.add_subplot(gs[0, 0])  # Use the first column
    ax1.plot(weekly_totals)
    ax1.set_title("Weekly Sales Trends")
    ax1.set_xlabel("Week")
    ax1.set_ylabel("Sales by case")

    # Create a bar chart of the product sales
    ax2 = fig.add_subplot(gs[0, 1])  # Use the second column
    ax2.bar(products, product_totals)
    for i, value in enumerate(product_totals):
        ax2.text(i, value, str(value), ha='center', va='bottom')
    ax2.set_title("Select Rockstar Energy Drinks Sales")
    ax2.set_xlabel("Product")
    ax2.set_ylabel("Sales by case")

    # Adjust the x label spacing
    plt.xticks(rotation=45, ha='right')
    gs.tight_layout(fig)

    # Display the plot in the GUI
    chart = FigureCanvasTkAgg(fig, master=root)
    #chart.get_tk_widget().grid(row=len(products) + 2, columnspan=num_days.get())
    chart.get_tk_widget().grid(row=1, column=num_days.get() + 1, rowspan=len(products))

def plot_sales_data_from_dict(sales_data):
    # Calculate the weekly sales totals
    weekly_totals = [sum(sales) for sales in sales_data.values()]

    # Calculate the total sales for each product
    product_totals = [sum(sales) for sales in sales_data.values()]

    # Create the figure and the gridspec
    fig = plt.figure(figsize=(10, 5))  # Adjust the figure size to fit the side-by-side plots
    gs = gridspec.GridSpec(1, 2, figure=fig)  # Change the number of rows to 1 and the number of columns to 2

    # Plot the weekly sales trends
    ax1 = fig.add_subplot(gs[0, 0])  # Use the first column
    ax1.plot(weekly_totals)
    ax1.set_title("Weekly Sales Trends")
    ax1.set_xlabel("Week")
    ax1.set_ylabel("Sales by case")

    # Create a bar chart of the product sales
    ax2 = fig.add_subplot(gs[0, 1])  # Use the second column
    ax2.bar(products, product_totals)
    for i, value in enumerate(product_totals):
        ax2.text(i, value, str(value), ha='center', va='bottom')
    ax2.set_title("Select Rockstar Energy Drinks Sales")
    ax2.set_xlabel("Product")
    ax2.set_ylabel("Sales by case")

    # Adjust the x label spacing
    plt.xticks(rotation=45, ha='right')
    gs.tight_layout(fig)

    # Display the plot in the GUI
    chart = FigureCanvasTkAgg(fig, master=root)
    chart.get_tk_widget().grid(row=1, column=num_days.get() + 1, rowspan=len(products))

# Create the main window
root = tk.Tk()
root.title("Sales Data")


# Create the number of days input
num_days = tk.IntVar()
tk.Label(root, text="Enter the number of days for analysis: ").grid(row=0, column=0)
tk.Entry(root, textvariable=num_days).grid(row=0, column=1)

# Create the submit button
submit_button = tk.Button(root, text="Submit", command=plot_sales_data)

products = ['Rockstar Original', 'Rockstar Sugar Free', 'Rockstar Punched Fruit Punch', 'Rockstar TMGS', 'Rockstar Recovery Orange', 'Rockstar Recover Lemonade', 'Rockstar Pure Zero Fruit Punch']

# Initialize product_entries as an empty list
product_entries = []

def create_sales_data_input(*args):
    global product_entries
    
    for entries in product_entries:
        for entry in entries:
            entry.destroy()

    product_entries = []

    for i, product in enumerate(products):
        tk.Label(root, text=product).grid(row=i + 1, column=0)
        entries = [tk.Entry(root) for _ in range(num_days.get())]
        product_entries.append(entries)
        for j, entry in enumerate(entries):
            entry.grid(row=i + 1, column=j + 1)


columnspan_value = max(1, num_days.get())  # Ensure columnspan is at least 1
submit_button.grid(row=len(products) + 1, column=0, columnspan=columnspan_value)

# Create the import CSV button
import_csv_button = tk.Button(root, text="Import CSV", command=import_csv_data)
import_csv_button.grid(row=len(products) + 1, column=1, columnspan=columnspan_value)

# Bind the create_sales_data_input function to the num_days variable
num_days.trace_add("write", create_sales_data_input)


def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main loop
root.mainloop()


