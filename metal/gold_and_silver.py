import requests
import json
import pandas as pd
import datetime
import bs4

def getDataAndSave(metalType, fromYear, toYear):
    dates = []
    prices = []
    for year in range(fromYear, toYear + 1):
        baseUrl = f'http://www.usagold.com/reference/{metalType}prices/{year}.html'
        if(year >= 2017):
            baseUrl = f"http://www.usagold.com/reference/prices/{metalType}history.php?ddYears={year}"
        html = requests.get(baseUrl).content
        bs = bs4.BeautifulSoup(html, "lxml")
        div = bs.find(id = "quotes")
        table = div.find("table")
        trs = table.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            if len(tds) != 2:
                print(f"header tr, skip")
                continue

            dates.append(tds[0].text)
            prices.append(tds[1].text)
        print(f"get:{baseUrl}")
    pf = pd.DataFrame({"date":dates, "price":prices})
    pf.to_csv(f"./{metalType}.csv")

if __name__ == "__main__":
    
    getDataAndSave("gold", 1994, 2019)
    getDataAndSave("silver", 1994, 2019)