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

init_data = np.zeros(shape=(1, len(COMPOSE_LIST)))
volf = pd.DataFrame(init_data, columns=COMPOSE_LIST)

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
        "温度範囲", min_value=0, max_value=100, value=(0, 100), step=10)
    # with prop_col2:
    temp_interval = st.slider("温度刻み", min_value=10,
                              max_value=100, value=50, step=10)
    pressure = float(st.text_input('圧力[MPa]', value=0.1))

# get thermophysic
thermophysic_lists = {}

for species, ID in COMPOSE_DICT.items():
    html = f"https://webbook.nist.gov/cgi/fluid.cgi?P={pressure:.1f}&TLow={temp_min}&THigh={temp_max}&TInc={temp_interval}&Digits=5&ID={ID}&Action=Load&Type=IsoBar&TUnit=C&PUnit=MPa&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm&RefState=DEF"

    res = requests.get(html)
    soup = BeautifulSoup(res.content, "html.parser")

    table = soup.find("table", {"class": "small"})
    rows = table.findAll("tr")

    labels = []
    values_list = []
    for row in rows:
        throws = row.findAll("th")
        tdrows = row.findAll("td")
        if bool(throws) == True:
            for throw in throws:
                label = throw.get_text()
                labels.append(label)
        elif bool(tdrows) == True:
            values = []
            for tdrow in tdrows:
                value = tdrow.get_text()
                values.append(value)
            values_list.append(values)

    thermophysic_list = pd.DataFrame(values_list, columns=labels)
    thermophysic_list.drop(
        columns=thermophysic_list.columns[[1, 2, 3, 4, 5, 6, 7, 9, 10, 13]], inplace=True)
    thermophysic_lists.setdefault(species, thermophysic_list)

# calculate mixture values
mix_list = thermophysic_list.copy()
mix_list[:] = 0
# minlen = 1000000
# maxlen = 0
for species, list in thermophysic_lists.items():
    vf = volf.at[0, species]
    list1 = list.astype('float64')
    list2 = list1.applymap(lambda x: x*vf)
    # minlen = min(minlen, len(list.index))
    # maxlen = max(maxlen, len(list.index))
    mix_list.add(list2)

# display thermophysic
mix_list
"---"
