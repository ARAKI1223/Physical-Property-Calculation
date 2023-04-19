import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


# Composition
COMPOSE_DICT = {"h2": "C1333740", "o2": "C7782447", "n2": "C7727379", "h2o": "C7732185",
                "ch4": "C74828", "c2h6": "C74840", "c3h8": "C74986", "c4h10": "C106978"}
COMPOSE_LIST = list(COMPOSE_DICT.keys())

# Property
# Density[kg/m3]
# Thermal Conductivity[W/m-k]
# Specific Heat[J/kg-s]
# Viscosity[Pa-s]
# PROPERTY_LIST = ["density", "thermal_conductivity", "specific_heat", "viscosity"]

"---"
st.title("ガス物性計算アプリ")
st.text("更新日：2023/4/19")
"---"

zero_data = np.zeros(shape=(1, len(COMPOSE_LIST)))
volf = pd.DataFrame(zero_data, columns=COMPOSE_LIST)

# input volume fraction
with st.sidebar:
    st.text("組成[vol%]を入力")
    for i in COMPOSE_LIST:
        volf[i] = st.number_input(i, format="%f")
    total = volf.sum(axis=1)
    st.text(f"Total={total}%")

# display volume fraction
st.text("ガス組成")
volf
"---"

# set temperature list
with st.sidebar:
    "---"
    prop_col1, prop_col2 = st.columns(2)
    # with prop_col1:
    temp_min, temp_max = st.slider(
        "温度範囲", min_value=0, max_value=2000, value=(0, 1000), step=100)
    # with prop_col2:
    temp_interval = st.slider("温度刻み", min_value=10,
                              max_value=100, value=50, step=10)
    pressure = float(st.text_input('圧力[MPa]', value=0.1))

# get thermophysic
thermophysic_lists = []

for species, ID in COMPOSE_DICT.items():
    print(species, ID)
    html = f"https://webbook.nist.gov/cgi/fluid.cgi?P={pressure:.1f}&TLow={temp_min}&THigh={temp_max}&TInc={temp_interval}&Digits=5&ID={ID}&Action=Load&Type=IsoBar&TUnit=C&PUnit=MPa&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm&RefState=DEF"

    res = requests.get(html)
    soup = BeautifulSoup(res.content, "html.parser")

    table = soup.find("table", {"class": "small"})
    rows = table.findAll("tr")

    columns = []
    values_list = []
    for row in rows:
        throws = row.findAll("th")
        tdrows = row.findAll("td")
        if bool(throws) == True:
            for throw in throws:
                column = throw.get_text()
                columns.append(column)
        elif bool(tdrows) == True:
            values = []
            for tdrow in tdrows:
                value = tdrow.get_text()
                values.append(value)
            values_list.append(values)

    thermophysic_list = pd.DataFrame(values_list, columns=columns)
    thermophysic_lists.append(thermophysic_list)

# display thermophysic
print(thermophysic_lists)
"---"
