from tkinter import SEPARATOR
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from pymongo import MongoClient
cluster = MongoClient(
    "mongodb+srv://aichamabrouk:WSUzGbuQTTT8FMWn@cluster0.3ekil.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["wemove"]
collection1 = db["pagesport"]
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(
    "https://www.pagesport.tn/etablissement-category/salles-de-sports/#s=1")
time.sleep(3)
Salle = []  # List to store name of the gym
Adresse = []  # List to store the exact address
Ville = []  # List to store the city$
PN = []
Email = []
home = driver.current_url
c = 0
elements = []
elements2 = []
while True:
    c = c+1
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    for i in soup.findAll(
            "a", attrs={"class": "job_listing-clickbox"}):
        elements.append(i["href"])
    time.sleep(2)
    try:
        if c >= 2:
            butt = driver.find_element_by_css_selector(
                "#main > div > nav > ul > li:nth-child(9) > a")
        else:
            butt = driver.find_element_by_css_selector(
                "#main > div > nav > ul > li:nth-child(8) > a")

        butt.click()
        time.sleep(3)
    except:
        break

driver.get(
    "https://www.pagesport.tn/etablissement-category/academies-et-terrains-de-football/")
time.sleep(3)
c2 = 3
while True:
    c2 = c2+1
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    for i in soup.findAll(
            "a", attrs={"class": "job_listing-clickbox"}):
        elements2.append(i["href"])
    time.sleep(2)
    try:
        if c2 == 4:
            butt = driver.find_element_by_css_selector(
                "#main > div > nav > ul > li:nth-child(4) > a")
        else:
            butt = driver.find_element_by_css_selector(
                "#main > div > nav > ul > li:nth-child(5) > a")

        butt.click()
        time.sleep(3)
    except:
        break

for a in elements:
    driver.get(a)
    time.sleep(1)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    try:
        address = driver.find_element_by_class_name(
            "job_listing-location").text
    except:
        address = "None"
    try:
        name = driver.find_element_by_class_name("job_listing-title").text
    except:
        name = "none"
    try:
        phone = soup.find(
            "span", attrs={"itemprop": "telephone"}).find("a").text
    except:
        phone = "None"
    try:
        mail = soup.find(
            "a", attrs={"itemprop": "email"}).text
    except:
        mail = "None"
    Salle.append(name)
    Adresse.append(address)
    PN.append(phone)
    Email.append(mail)

    gym = {"Name": name, "Address": address,
           "Phone Number": phone, "E-mail": mail, "Type": "Club de sport"}
    collection1.insert_one(gym)

for a in elements2:
    driver.get(a)
    time.sleep(1)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    try:
        address = driver.find_element_by_class_name(
            "job_listing-location").text
    except:
        address = "None"
    try:
        name = driver.find_element_by_class_name("job_listing-title").text
    except:
        name = "none"
    try:
        phone = soup.find(
            "span", attrs={"itemprop": "telephone"}).find("a").text
    except:
        phone = "None"
    try:
        mail = soup.find(
            "a", attrs={"itemprop": "email"}).text
    except:
        mail = "None"
    Salle.append(name)
    Adresse.append(address)
    PN.append(phone)
    Email.append(mail)

    gym = {"Name": name, "Address": address,
           "Phone Number": phone, "E-mail": mail, "Type": "Académie de sport"}
    collection1.insert_one(gym)

df = pd.DataFrame({'Salle': Salle, 'Adresse': Adresse,
                  'Numéro de téléphone': PN, 'Email': Email, "Type": "Salles de sport"})
df.to_csv('pagesportsalles.csv', index=False, encoding='utf-8', sep=";")
