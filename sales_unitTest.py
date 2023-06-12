import unittest
import pandas as pd
import numpy as np
from navigate_stores_sales import calculate_weekly_totals, calculate_product_totals, calculate_growth_rate

class TestPlotFunctions(unittest.TestCase):
    def setUp(self):
        # Create a mock data frame for testing
        self.data = pd.DataFrame({
            'Week': np.repeat(np.arange(1, 5), 7),
            'Store': np.repeat(['Store1', 'Store2', 'Store3', 'Store4'], 7),
            'Drink1': np.random.randint(1, 100, 28),
            'Drink2': np.random.randint(1, 100, 28),
            'Drink3': np.random.randint(1, 100, 28),
            'Drink4': np.random.randint(1, 100, 28),
            'Drink5': np.random.randint(1, 100, 28),
            'Drink6': np.random.randint(1, 100, 28),
            'Drink7': np.random.randint(1, 100, 28),
        })
        self.products = ['Drink1', 'Drink2', 'Drink3', 'Drink4', 'Drink5', 'Drink6', 'Drink7']

    def test_calculate_weekly_totals(self):
        data_store1 = self.data[self.data['Store'] == 'Store1']
        weekly_totals = data_store1[self.products].sum(axis=1)
        
        # Call your function with data_store1 and check if the output matches expected results
        result_weekly_totals = calculate_weekly_totals(data_store1)
        self.assertTrue((result_weekly_totals == weekly_totals).all())

    def test_calculate_product_totals(self):
        data_store1 = self.data[self.data['Store'] == 'Store1']
        product_totals = data_store1[self.products].sum(axis=0)
        
        # Call your function with data_store1 and check if the output matches expected results
        result_product_totals = calculate_product_totals(data_store1)
        self.assertTrue((result_product_totals == product_totals).all())

    def test_calculate_growth_rate(self):
        data_store1 = self.data[self.data['Store'] == 'Store1']
        weekly_totals = data_store1[self.products].sum(axis=1)
        
        # percent change from previous week
        growth_rate = weekly_totals.pct_change() * 100 

        # Call your function with data_store1 and check if the output matches expected results
        result_growth_rate = calculate_growth_rate(data_store1)
        self.assertTrue((result_growth_rate[1:] == growth_rate[1:]).all())

if __name__ == '__main__':
    unittest.main()
