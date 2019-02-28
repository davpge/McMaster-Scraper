# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 11:18:28 2019

@author: david.page
"""

# import libraries
import urllib
import re
from urllib.request import urlopen

from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import itertools
import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()
root.update()

file_list = []
file_count = 0
filename = []

print('Save HTML of the McMaster Cart, right click->save as on browser page')
print('Choose the html file you saved onto the desktop')
print('A CSV file will be created in the same folder the .exe was run from')

while True:
    file_path = filedialog.askopenfilename()                # Open window to pick file until cancel
    if len(file_path) > 0:
        break
    file_list.append(file_path)                             # add file path to list
    file_count += 1
    

# specify the url      
quote_page = (file_path)

# query the website and return the html to the variable ‘page’
page = open(quote_page)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page.read())

#Getting the item description

item_description = soup.find_all('div', attrs={'class':"title-text"})
item_description_stripped = []
for item in item_description: item_description_stripped.append(item.get_text())

for items in item_description_stripped:
    if items =='Length, ft.':
        print(items)
        
for count, i in enumerate(item_description_stripped):
    if i=='Length, ft.':
#        print(i)
        item_description_stripped.pop(count)
        

#item_description_stripped.remove('Length, ft.')

item_description_string =','.join(str(e) for e in item_description_stripped)

print (item_description_string)


#Getting the item quantity##################################################################################
quantity = soup.find_all('div', attrs={"class":"line-section line-quantity"})

quantity_string = []
for sections in quantity:
    quantity_string.append(str(sections))
 
number = []       
for strings in quantity_string:
 #   print(strings)
    number.append(re.findall('\d+', strings ))

for count, i in enumerate(number):
#    if len(i)>1:
 #       print(i[0])
        number[count] = i[0]
 

for items in number:
    print(*items, sep =",")

number_string = (",".join([item for sublist in number for item in sublist]))


#Getting item price##################################################################################

price = soup.find_all('div', attrs={'class':"line-section line-unit-price"})
price_stripped = []
for items in price:
    price_stripped.append(str(items))

price_ea = []       
for strings in price_stripped:
 #   print(strings)
    price_ea.append(re.findall('[0-9\.]+', strings ))
    
price_string =(",".join([item for sublist in price_ea for item in sublist]))


for items in price_ea:
   
    print(*items, sep = ",")


##################################################################################

vendor_part = soup.find_all(attrs={'class':"line-part-number-input"})
vendor_stripped = []
for items in vendor_part:
    vendor_stripped.append(str(items))
    

vendor_text_store = ""   

for items in vendor_stripped:
    vendor_text_split = items.split("value=")[1]
    vendor_text_split= vendor_text_split.split("/>")[0]
    vendor_text_split= vendor_text_split.split('"')[1]
    vendor_text_store += vendor_text_split + ","

print (vendor_text_store)

 

print (vendor_text_store)
print (item_description_string)
print (price_string)
print (number_string)

data_list = [vendor_text_store,item_description_string,price_string,number_string]

data_list =zip_longest(vendor_text_store.split(','),item_description_string.split(','),price_string.split(','),number_string.split(','))

with open('numbers.csv', 'a',newline="") as csvFile:   
    writer = csv.writer(csvFile,delimiter=',')
    writer.writerow(['Part#','Description','Price','Quantity'])
    for values in data_list:
        print(values)
        writer.writerow([values[0],values[1],values[2],values[3]])
        

page.close()




