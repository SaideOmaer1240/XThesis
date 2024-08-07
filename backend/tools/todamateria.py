import requests
from bs4 import BeautifulSoup
import re

class TodaMateria:
    def __init__(self):
        self.queryset = []
    
    def request(self, query):
        url = f"https://www.todamateria.com.br/?s={query}" 
        
        response = requests.get(url)