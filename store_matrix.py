import random
import matplotlib.pyplot as plt

# Define the number of products and days
num_products = 7
num_days = 7

# Ask the user to input the sales data matrix
sales_data = []
for i in range(num_products):
    row = []
    for j in range(num_days):
        sale = int(input(f"Enter sales data (by case)for Rockstar drink {i+1} on week {j+1}: "))
        row.append(sale)
    sales_data.append(row)

# Display the matrix
print("Sales Data:")
for row in sales_data:
    print(row)

# Calculate the weekly sales totals
weekly_totals = [sum(row) for row in sales_data]

# Plot the weekly sales trends
plt.plot(weekly_totals)
plt.title("Weekly Sales Trends")
plt.xlabel("Week")
plt.ylabel("Sales by case")
plt.show()

# Calculate the total sales for each product
product_totals = [sum([row[i] for row in sales_data]) for i in range(num_days)]

# Create a bar chart of the product sales
products = ['Rockstar Original', 'Rockstar Sugar Free', 'Rockstar Punched Fruit Punch', 'Rockstar TMGS', 'Rockstar Recovery Orange', 'Rockstar Recover Lemonade', 'Rockstar Pure Zero Fruit Punch',]
plt.bar(products, product_totals)
plt.title("Select Rockstar Energy dr")
plt.xlabel("Product")
plt.ylabel("Sales by case")

# Adjust the x label spacing
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.3)

plt.show()
