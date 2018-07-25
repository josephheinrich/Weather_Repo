#Import Statements
import urllib.request, re
from bs4 import BeautifulSoup
import requests
import pandas
import csv
from datetime import date
from datetime import datetime

#Ten Day Forecast URL
page = requests.get('https://weather.com/weather/tenday/l/USIN0046:1:US')

#Parse URL
soup = BeautifulSoup(page.text, 'html.parser')

#Find Table Containing Weather Data Via HTML Tags
days = soup.table.tbody.find_all(class_="day-detail clearfix")
temp = soup.table.tbody.find_all(class_="temp")
precip = soup.table.tbody.find_all(class_="precip")
descrip = soup.table.tbody.find_all(class_="description")

#Find Day, Temp, Precip, Descrip in HTML Table
day_script = re.findall('(?<=day-detail clearfix">).+?(?=</span>)', str(days)) 
temp_script = re.findall('(?<=<span class="">).+?(?=<sup>)', str(temp))
precip_script = re.findall('(?<=<span>).+?(?=<span class="Percentage-8191)', str(precip))
descrip_script = re.findall('(?<="><span>).+?(?=</span>)', str(descrip))

#Add in Current Temp

#Hi/Low URL
hilo_page = requests.get('https://weather.com/weather/today/l/USIN0046:1:US')

#Parse URL
hilo = BeautifulSoup(hilo_page.text, 'html.parser')

#Find Table Containing Weather Data Via HTML Tags
current_hilo = hilo.body.find_all(class_="today_nowcard-hilo")

#Find Hi-Lo in HTML Class
hilo_script = re.findall('(?<=<span class="">).+?(?=<sup>)', str(current_hilo))

#Export Hi-Lo to CSV

#Check if Temp List has 30 Values
if len(temp_script) != 30:
    temp_script.insert(0, 0)

#Print Title and Hi-Lo
print("Fifteen Day Weather Forecast - Bloomington, IN\n")
print("Today's High:", hilo_script[0], "\nToday's Low:", hilo_script[1], "\n")

#Print Formatted Weather Data
for i in range(len(day_script)):
    print(day_script[i] + (" " * (8-len(day_script[i]))),
    str(temp_script[i*2]) + (" " * (2-len(str(temp_script[i*2])))),
    str(temp_script[(i*2)+1]) + (" " * (4-len(str(temp_script[(i*2)+1])))),
    str(precip_script[i] + "% CoR") + (" " * (11-len(str(descrip_script[i] + "% CoR")))),
    descrip_script[i])

#Pair Temperature List
pairs = zip(temp_script[::2], temp_script[1::2])
result_list = list(pairs)

#Month
MONTH = datetime.now()
month = MONTH.strftime("%B")

#Today's Date
now = datetime.now()
now_format = now.strftime("%x")
today = now_format.replace("/", "-")
today = "./Weather/" + month + "/" + today + ".csv"

#Export Output
print("\nYour 15 Day Weather Forecast Has Been Exported To:", today)

#Format Data for CSV Export
df = pandas.DataFrame(data={"Day": day_script,
                            "Description": descrip_script,
                            "Precipitation": precip_script,
                            "Temperature": result_list})

#Export Weather Data to CSV
df.to_csv(today, sep=',', index=False)









