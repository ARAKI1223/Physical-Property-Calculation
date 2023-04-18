import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def NIST_Date_Tracking():

    html = f"https://webbook.nist.gov/cgi/fluid.cgi?P={pressure:.1f}&TLow={temp_min}&THigh={temp_max}&TInc={temp_interval}&Digits=5&ID={ID}&Action=Load&Type=IsoBar&TUnit=C&PUnit=MPa&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm&RefState=DEF"

    res = requests.get(html)
    soup = BeautifulSoup(res.content, "html.parser")

    table = soup.find("table", {"class": "small"})
    rows = table.findAll("tr")  # Type: bs4.element.ResultSet

    columns = []
    values_list = []
    for row in rows:  # Type: bs4.element.Tag
        throws = row.findAll("th")  # Type: bs4.element.ResultSet
        tdrows = row.findAll("td")  # Type: bs4.element.ResultSet
        if bool(throws) == True:
            for throw in throws:  # Type: bs4.element.Tag
                column = throw.get_text()  # Type: str
                columns.append(column)
        elif bool(tdrows) == True:
            values = []
            for tdrow in tdrows:
                value = tdrow.get_text()
                values.append(value)
            values_list.append(values)

    thermophysic_list = pd.DataFrame(values_list, columns=columns)
    print(thermophysic_list)
    # thermophysic_list.to_csv('thermophysic_list.csv')


ID = "C7727379"  # H2O
# ID_list = ["C1333740","C7782447","C7727379","C7732185","C74828","C74840","C74986","C106978"]
# COMPOSE_LIST = ["h2","o2","n2","h2o","ch4","c2h6","c3h8","c4h10"]
temp_min = 100
temp_max = 200
temp_interval = 10
pressure = 10.0
NIST_Date_Tracking()
