from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from pymongo import MongoClient
cluster = MongoClient(
    "mongodb+srv://aichamabrouk:WSUzGbuQTTT8FMWn@cluster0.3ekil.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")  # connect with mongodb
db = cluster["wemove"]  # get to database
collection = db["ecole"]  # get to collection in database
driver = webdriver.Chrome()
driver.get("https://www.ecoles.com.tn/sport?titreville=&ville=All&activites=All")
time.sleep(3)
Salle = []  # List to store name of the gym
Adresse = []  # List to store the exact address
Ville = []  # List to store the city
PN = []  # List to store the phone number
Email = []   # List to store the email
Type = []   # List to store the type
while True:
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    time.sleep(3)
    for a in soup.findAll('div', attrs={'class': 'col-md-4 col-xs-6'}):
        bl = []
        name = a.find('div', attrs={'class': 'title-content'})
        block = a.find('div', attrs={'class': 'box-desc'})
        b = block.findAll("span")
        for j in b:
            bl.append(j.text)
        address = bl[0]
        if len(bl) == 0:
            address = "null"
            phone = "null"
            mail = "null"
        if len(bl) == 1:
            phone = "null"
            mail = "null"
        elif len(bl) == 2:
            phone = bl[1]
            mail = "null"
        elif len(bl) == 3:
            phone = bl[1]
            mail = bl[2]
        try:
            type = a.find('span', attrs={'class': 'info'}).text
        except:
            type = "null"
        ville = a.find('ul', attrs={'class': 'location'})
        Salle.append(name.find('a').text)
        Adresse.append(address)
        PN.append(phone)
        Email.append(mail)
        Ville.append(ville.find('a').text)
        Type.append(type)
        gym = {"Name": name.find('a').text, "Address": address, "City": ville.find(
            'a').text, "Phone Number": phone, "E-mail": mail, "Type": type}
        collection.insert_one(gym)
    try:
        bot = driver.find_element_by_css_selector(
            'body > div.dialog-off-canvas-main-canvas > main > section.flat-map-zoom-in.ecoles-list-section > div > div > div.col-lg-9.mt-55 > div:nth-child(2) > div > div > div > ul > li.pager__item.pager__item--next > a > span:nth-child(2)')
        bot.click()
        time.sleep(3)
    except:
        break


df = pd.DataFrame({'Salle': Salle, 'Adresse': Adresse,
                  'Ville': Ville, 'Numéro de téléphone': PN, 'Email': Email, 'Type': Type})
df.to_csv('ecolesalles.csv', index=False, encoding='utf-8', sep=";")
