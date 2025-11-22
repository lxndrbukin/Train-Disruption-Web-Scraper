import os
import pandas as pd

class Scraper:
	def __init(self, href):
		self.href = href
		self.db = DataBase()

class DataBase:
	def __init__(
			self, columns=["date", "title"], 
			file_path=os.path.join(os.path.dirname(__file__), "disruptions.csv")
		):
		self._file_path = file_path
		self._data = self.fetch_data()

	@property
	def file_path(self):
		return self._file_path

	@file_path.setter
	def file_path(self, path):
		self._file_path = path

	@property
	def data(self):
		return self._data

	def fetch_data(self):
		if not os.path.exists(self.file_path):
			return pd.DataFrame()
		return pd.read_csv(self.file_path)
	
	def save_data(self):
		pass
