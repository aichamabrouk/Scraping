from tkinter import SEPARATOR
from tkinter.ttk import Separator
from attr import attrs
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Firefox()

driver.get(
    "https://www.ecoles.com.tn/sport?titreville=&ville=All&activites=All&type%5Bprive%5D=prive")
time.sleep(3)
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")
Salle = []  # List to store name of the gym
Adresse = []  # List to store the exact address
Ville = []  # List to store the city
for a in soup.findAll('div', attrs={'class': 'col-md-4 col-xs-6'}):
    name = a.find('div', attrs={'class': 'title-content'})
    address = a.find('div', attrs={'class': 'box-desc'})
    ville = a.find('ul', attrs={'class': 'location'})
    Salle.append(name.text)
    Adresse.append(address.text)
    Ville.append(ville.find('a').text)

df = pd.DataFrame({'Salle': Salle, 'Adresse': Adresse,
                  'Ville': Ville})
df.to_csv('salle.csv', index=False, encoding='utf-8', sep="#")
