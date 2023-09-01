import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox


# Create the main window
root = tk.Tk()
root.withdraw()  # Hide the root window

# welcome message
messagebox.showinfo("Welcome", "Welcome to Drink Analytics! Please select the file with sales data needed to be analyzed.")

# user to select CSV file
file_path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
if not file_path:
    messagebox.showerror("Error", "No file selected.")
    exit()

# Load the sales data from the selected CSV file
sales_data = pd.read_csv(file_path)


def select_products():
    # List all columns in the dataframe excluding 'Week' and 'Store'
    possible_products = [col for col in sales_data.columns if col not in ['Week', 'Store']]

    # new Tkinter window
    product_window = tk.Toplevel(root)
    product_window.title("Select Products")

    # Create a list of checkboxes for product selection
    product_vars = {product: tk.IntVar(value=1) for product in possible_products}  # dictionary to hold checkbox variables
    for product, var in product_vars.items():
        cb = tk.Checkbutton(product_window, text=product, variable=var)
        cb.pack()

    def confirm_selection():
        # Get the selected products
        selected_products = [product for product, var in product_vars.items() if var.get() == 1]
        if not selected_products:
            messagebox.showerror("Error", "No product selected.")
        else:
            global products
            products = selected_products  # Update the products global variable
            product_window.destroy()

    # button to confirm the selection
    btn_confirm = tk.Button(product_window, text="Confirm", command=confirm_selection)
    btn_confirm.pack()

    root.wait_window(product_window)

# user select the products
select_products()

weeks = sales_data['Week'].nunique()

def calculate_weekly_totals(data):
    # Calculate the weekly sales totals for all drinks combined
    weekly_totals = data[products].sum(axis=1)
    return weekly_totals

def calculate_product_totals(data):
    # Calculate the total cases sold for each drink
    product_totals = data[products].sum(axis=0)
    return product_totals

def calculate_growth_rate(data):
    # Calculate the weekly sales totals for all drinks combined
    weekly_totals = data[products].sum(axis=1)
    
    # Calculate the growth rate
    growth_rate = weekly_totals.pct_change() * 100  # percent change from previous week
    return growth_rate

def plot_data(data, store_name, ax1, ax2):
    # Use calculate_weekly_totals & calculate_product_totals functions
    weekly_totals = calculate_weekly_totals(data)
    product_totals = calculate_product_totals(data)

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

def plot_growth(data, ax):
    # Use calculate_growth_rate function
    growth_rate = calculate_growth_rate(data)

    # Set the title
    ax.set_title("Sales growth rate")
    
    # Plot the growth rate
    ax.plot(range(2, weeks + 1), growth_rate[1:])  # exclude the first week because it has no previous week to compare to
    ax.set_xlabel("Week")
    ax.set_ylabel("Growth rate (%)")

# Define the function to update the plots
def update_plots():
    select_products()
    # Check if any pages exist in the notebook, if yes remove all.
    for page in notebook.winfo_children():
        page.destroy()

    # Use the same code as before to build the pages
    for idx, store in enumerate(stores):
        store_data = sales_data[sales_data['Store'] == store].set_index('Week')

        page = tk.Frame(notebook)
        notebook.add(page, text=store)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
        plot_data(store_data, store, ax1, ax2)

        canvas = FigureCanvasTkAgg(fig, master=page)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, page)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Growth page
    growth_page = tk.Frame(notebook)
    notebook.add(growth_page, text="Sales Growth Rate for Each Store")

    fig_growth, ax_growth = plt.subplots(figsize=(8, 6))

    for store in stores:
        store_data = sales_data[sales_data['Store'] == store].set_index('Week')
        plot_growth(store_data, ax_growth)

    canvas_growth = FigureCanvasTkAgg(fig_growth, master=growth_page)
    canvas_growth.draw()
    canvas_growth.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    toolbar_growth = NavigationToolbar2Tk(canvas_growth, growth_page)
    toolbar_growth.update()
    canvas_growth.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    notebook.select(0)

# Check if the "Store" column exists in the dataset
if 'Store' in sales_data.columns:
    # Get the unique store names
    stores = sales_data['Store'].unique()
    num_stores = len(stores)

    # Create a new Tkinter window
    window = tk.Toplevel(root)

    # Set the window title
    window.title("Drink Analytics")

    # Create the notebook widget to hold the pages
    notebook = ttk.Notebook(window)
    notebook.pack(fill=tk.BOTH, expand=True)

    # refresh button
    btn_refresh = tk.Button(window, text="Refresh", command=update_plots)
    btn_refresh.pack()

    # Loop through each store and create a separate page for each store
    for idx, store in enumerate(stores):
        # Filter the data for the current store
        store_data = sales_data[sales_data['Store'] == store].set_index('Week')

        # Create a new page in the notebook for the current store
        page = tk.Frame(notebook)
        notebook.add(page, text=store)

        # Create subplot axes for sales data
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

        # Plot the data for the current store
        plot_data(store_data, store, ax1, ax2)

        # Create the FigureCanvasTkAgg object to display the plot in the page
        canvas = FigureCanvasTkAgg(fig, master=page)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add the navigation toolbar to the page
        toolbar = NavigationToolbar2Tk(canvas, page)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    if num_stores > 0:
        # Create a new page for the sales growth rate
        growth_page = tk.Frame(notebook)
        notebook.add(growth_page, text="Sales Growth Rate for Each Store")

        # Create subplot axes for the sales growth rate
        fig_growth, ax_growth = plt.subplots(figsize=(8, 6))

        # Plot the sales growth rate for each store
        for store in stores:
            store_data = sales_data[sales_data['Store'] == store].set_index('Week')
            plot_growth(store_data, ax_growth)

        # Create the FigureCanvasTkAgg object to display the plot in the growth page
        canvas_growth = FigureCanvasTkAgg(fig_growth, master=growth_page)
        canvas_growth.draw()
        canvas_growth.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add the navigation toolbar to the growth page
        toolbar_growth = NavigationToolbar2Tk(canvas_growth, growth_page)
        toolbar_growth.update()
        canvas_growth.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Select the first page in the notebook
    notebook.select(0)

    def close_window():
        window.destroy()
        root.quit()  # Exit the application

    # Bind the closing event of the window to close_window
    window.protocol("WM_DELETE_WINDOW", close_window)

    # Run the Tkinter event loop
    root.mainloop()
else:
    # Set the index to 'Week' column
    sales_data.set_index('Week', inplace=True)

    # Create a new figure
    plt.figure(figsize=(15, 5))

    # Create subplot axes
    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)

    # Plot the data for the entire dataset without store information
    plot_data(sales_data, None, ax1, ax2)

    plt.tight_layout()
    plt.show()
