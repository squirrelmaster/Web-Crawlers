from bs4 import BeautifulSoup
import requests
import time
import re
import os;
print os.getcwd()
os.chdir('/Users/sunjiaxuan/Documents/Py')
import csv
with open('AllQuotes.csv', 'rb') as f:
    reader = csv.reader(f)
    QS = list(reader)
resultFile = open("output.csv",'wb')
wr = csv.writer(resultFile, dialect='excel')

for i in range(0,len(QS)):
    print(i)
    wr.writerow(''.join(QS[i]))
    url = "https://sg.finance.yahoo.com/q/ao?s=" + ''.join(QS[i])
    try:
        r = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        continue
    bf = BeautifulSoup(r.text,"lxml")
    ####For first part
    try:
        tarth = bf.findAll('th', text = re.compile('Recommendation Summary*'))
        tarthre = (tarth[0].find_parent("tr").find_parent("table").find_next_sibling("table"))
    except:
        continue
    tartrs = tarthre.find_all("tr")
    for tartr in tartrs:
        #print("".join(tartr.text.encode('ascii', 'ignore')))
        #print(type(tartr.text.encode('ascii', 'ignore')))
        wr.writerow("".join(tartr.text.encode('ascii', 'ignore')))
    ####For second part
    tarth = bf.findAll('th', text = re.compile('Price Target Summary'))
    tarthre = (tarth[0].find_parent("tr").find_parent("table").find_next_sibling("table"))
    tartrs = tarthre.find_all("tr")
    for tartr in tartrs:
        wr.writerow(tartr.text.encode('ascii', 'ignore').decode('ascii'))
    ####For Third part
    tarth = bf.findAll('th', text = re.compile('Upgrades & Downgrades History'))
    tarthre = (tarth[0].find_parent("tr").find_parent("table").find_next_sibling("table"))
    tartrs = tarthre.find_all("tr")
    for tartr in tartrs:
        tds = tartr.find_all("td")
        tdsout = ''
        for td in tds:
            if td.text:
            #tdsout = tdsout + td.text 
                wr.writerow(td.text.encode('ascii', 'ignore').decode('ascii'))
    ####For Last part
    tarth = bf.findAll('th', text = re.compile('Recommendation Trends'))
    tarthre = (tarth[0].find_parent("tr").find_parent("table").find_next_sibling("table"))
    #print(tarthre.text)
    #Find the columns of the table
    ths = tarthre.find_all("th",{'scope',"col"})
    #for th in ths:
        #print(th.text)
    tartrs = tarthre.find_all("tr")
    for tartr in tartrs:
        tds = tartr.find_all("td")
        tdsout = ''
        for td in tds:
            if td.text:
            #tdsout = tdsout + td.text 
                wr.writerow(td.text.encode('ascii', 'ignore').decode('ascii'))
resultFile.close()
with open("output.csv") as infile, open("outfile.csv", "w") as outfile:
    for line in infile:
        outfile.write(line.replace(",", ""))
        
import AnalyseYahooResult
import YahooGetPrice
import YahooStrategyMain