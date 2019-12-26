
import pandas as pd
import datetime as datetime

# What is an order? Focus on one type of order
# What is an outcome? differentiate between real outcome and simulated outcome.
# What is a blended model?
# - input: available cash, order, time until markets close (?), max_transaction limit
# - output: authorization/non-authorization to execute the order.

# Type of order: buy one unit
# Stock: MSFT
# Start time: 1:00pm
# Expiration time at 1:05pm. 
# Initial buy at 11 USD 
# Keep interval: [10, 15] (if goes below 10 or above 15: sell)
# [if MSFT goes bellow]

class modelBlender():
	def __init__(self):
		self.blended_model = None
		return self

	def submit_order(self, order):
		# stores the submited order with additional data
		# returns wether the order  be executed or not! and how big should the transaction be.
		current_time = datetime.now()

	def submit_outcome(self, outcome, outcome_type='simulated'):
		# stores the submited outcome
		# it might be important to differentiate between a simulated and a real outcome
		current_time = datetime.now()

	def load_orders(self, startDate, endDate):
		# load the orders we had in a period of time

	def load_outcomes(self, startDate, endDate):
		# load the outcomes we had in a period of time

	def produce_blended_model(self, startDate, endDate):
		df_orders = self.load_orders(startDate, endDate)
		df_outcomes = self.load_outcomes(startDate, endDate)
		# (...)
		df = # dataframe with: model_name, order_time, execution_time, outcome_time, invested_cash, output_cash

		# the blended could also be a dictionary with the proportions of money we wish to have invested on each model
		# example: 
		# blended_model = {'model1':0, 'model2':0, 'model3':0.2, 'model4':0.3, 'model5':0.5}
		# blended_model_performance={} (??)
