import os
import pandas as pd
from datetime import datetime, timezone
from typing import List
import requests
from bs4 import BeautifulSoup

class Scraper:
	def __init__(self, href, city="London"):
		self.href = href
		self.city = city
		self.db = DataBase()

	def scrape_headlines(self):
		html = requests.get(self.href)
		soup = BeautifulSoup(html.text, "html.parser")
		urls = soup.find_all("a", class_="sc-efcddfe6-3")
		titles = soup.find_all("p", class_="sc-7e8228e1-1")
		for i, url in enumerate(urls):
			if self.city in titles[i].get_text().strip():
				self.db.create_entry({"title": titles[i], "url": url})

class DataBase:
	def __init__(
			self, columns=["date", "title", "url"], 
			file_path=os.path.join(os.path.dirname(__file__), "disruptions.csv")
		):
		self._file_path = file_path
		self._columns = columns
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

	@property
	def columns(self):
		return self._columns

	@staticmethod
	def clean_data(df: pd.DataFrame):
		df_copy = df.copy()
		df_copy["date"] = pd.to_datetime(df["date"], errors="coerce")
		return df_copy

	def create_df(self, entries: List[dict]):
		return pd.DataFrame(entries, columns=self.columns)

	def fetch_data(self):
		if not os.path.exists(self.file_path):
			return pd.DataFrame(columns=self.columns)
		return self.clean_data(pd.read_csv(self.file_path))
	
	def save_data(self):
		return self.data.to_csv(self.file_path, index=False)

	def create_entry(self, entry: dict):
		new_row = {
			"date": datetime.now(tz=timezone.utc),
			"title": entry["title"],
			"url": entry["url"]
		}
		self.create_df([new_row]).to_csv(self.file_path, mode="a", header=False, index=False)
		self.data = pd.concat(self.data, self.create_df([new_row]), ignore_index=True)