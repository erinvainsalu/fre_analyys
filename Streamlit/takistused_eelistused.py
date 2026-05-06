import sys
import os

import streamlit as st
import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Leia peakaust
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Impordi tabelite ja graafikute joonistamiseks vajalikud funktsioonid
from Python.visuaalide_abilised import maara_raporti_stiil, leia_sildi_mapping
from Python.visuaalide_abilised import sagedustabel, mitmikvastuse_sagedustabel, loo_risttabel
from Python.visuaalide_abilised import loo_tulpdiagramm, loo_hor_tulpdiagramm, loo_stacked_tulpdiagramm, loo_hor_stacked_tulpdiagramm, loo_heatmap

# Määra graafikute stiil
style = maara_raporti_stiil()

# Impordi andmed puhastamise käigus loodud CVS-st
data = pd.read_csv('data/cleaned_data.csv')

# Impordi vastuste koodid
koodid = pd.read_csv('data/vastuste_koodid.csv')

# Kasuta laia paigutust
#st.set_page_config(layout='wide')

# Asenda väheste vastajate arvuga maakonnad valikuga muu
data_puhastatud = data.copy()
data_puhastatud['K5_elukoht'] = data['K5_elukoht'].replace([2, 3, 5, 6, 7, 8, 10, 11, 13, 15], 16)

st.title('pealkiri')

st.write('## Väljakutsed')

st.write('## Loobumise lihtsuse hinnang')

st.write('**Vastajate jaotus teadlikkuse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])
# Leia vastajate arv teadlikkuse alusel
lihtsus = sagedustabel(data_puhastatud, koodid, 'K21_loobumise_lihtsus').sort_values(by='protsent', ascending=False)

# Kuva tulpdiagramm
fig, ax = loo_hor_tulpdiagramm(
    lihtsus,
    '',
    style,
    sort=True
)
tab1.pyplot(fig)
tab2.dataframe(lihtsus,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

st.write('K21_loobumise_lihtsus')
st.write('K22_peamised_väljakutsed')