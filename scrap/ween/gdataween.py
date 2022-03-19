from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options

cluster = MongoClient(
    "mongodb+srv://aichamabrouk:WSUzGbuQTTT8FMWn@cluster0.3ekil.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["wemove"]
collection1 = db["ween"]
chrome_options = Options()
chrome_options.add_extension("extension_4_0_141_0.crx")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get(
    "https://ween.tn/recherche?q=Sport+-+Salles+De&ou=")
time.sleep(2)
Salle = []  # List to store name of the gym
Adresse = []  # List to store the exact address
Ville = []  # List to store the city
PN = []
Email = []
home = driver.current_url
elements = []
while True:
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    for i in soup.findAll("a", attrs={"class": "truncate"}):
        elements.append("https://ween.tn"+i["href"])
    try:
        butt = driver.find_element_by_partial_link_text("Suivant")
        butt.click()
        time.sleep(2)
    except:
        break
print(elements)
for a in elements:
    driver.get(a)
    time.sleep(3)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    try:
        address = driver.find_element_by_css_selector(
            "#page > section > div.post-meta-info > div > div > div.col-md-7.col-sm-7.col-xs-12 > div > div.text-info > p").text
    except:
        address = "None"
    try:
        name = driver.find_element_by_css_selector(
            "#page > section > div.post-meta-info > div > div > div.col-md-7.col-sm-7.col-xs-12 > div > div.text-info > h1").text
    except:
        name = "none"
    try:
        phone = ''
        for i in soup.findAll(
                "a", attrs={"data-target": "#myNum"}):
            phone = phone + '/' + i.text
    except:
        phone = "None"
    Salle.append(name)
    Adresse.append(address)
    PN.append(phone)
    gym = {"Name": name, "Address": address,
           "Phone Number": phone}
    collection1.insert_one(gym)

df = pd.DataFrame({'weenSalles': Salle, 'Adresse': Adresse,
                  'Numéro de téléphone': PN})
df.to_csv('salles3.csv', index=False, encoding='utf-8', sep=";")
