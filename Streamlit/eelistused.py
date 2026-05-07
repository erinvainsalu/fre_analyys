import sys
import os

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Leia peakaust
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Impordi tabelite ja graafikute joonistamiseks vajalikud funktsioonid
from Python.visuaalide_abilised import maara_raporti_stiil, leia_sildi_mapping
from Python.visuaalide_abilised import sagedustabel, mitmikvastuse_sagedustabel, loo_risttabel, loo_mitmikvastuse_risttabel
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

st.title('Tarbijate eelistused')

###################################################
# LOOBUMISEL OLULINE                              #
###################################################
st.write('## Loobumisel oluline')
st.write(':red[*To-be-done*]')
st.write('**Vastajate jaotus loobumisel oluliste tunnuste lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv väljakutsete alusel
oluline_loobumisel = mitmikvastuse_sagedustabel(data_puhastatud, koodid, 'K25_loobumisel_oluline').sort_values(by='protsent', ascending=False)

fig, ax = loo_hor_tulpdiagramm(
    oluline_loobumisel,
    '',
    style,
    sort=True   
)
tab1.pyplot(fig)
tab2.dataframe(oluline_loobumisel,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

valjakutsed_kaitumine = loo_mitmikvastuse_risttabel(data_puhastatud, koodid, 'K25_loobumisel_oluline', 'K7_sorteerimiskaitumine')
valjakutsed_kaitumine

##################################
# Uuri vastusevariante

valjakutsed_veerud = [
    col for col in data.columns 
    if col.startswith('K25_loobumisel_oluline') 
    and not col.endswith('_muu_tekst')  # Välista tekstvastustega veerud
]

st.write('Tunnuste koos esinemise sagedus:')
# Kui sageli mingid valikud koos esinevad?
fig, ax = plt.subplots()
corr_matrix = data[valjakutsed_veerud].corr()
# Loo heatmap
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
st.pyplot(fig)

# Leia 10 kõige tugevama korrelatsiooniga tunnust
# Set diagonal to NaN (ignore self-correlation)
import numpy as np
corr_no_diag = corr_matrix.where(~np.eye(len(corr_matrix), dtype=bool))

# 3. Get top correlations
corr_pairs = corr_no_diag.unstack().sort_values(ascending=False)
st.write('Tugevaimad korrelatsioonid:')
st.write(corr_pairs[corr_pairs < 1.0].head(10))  # Top 10 pairs

# Kui mitu väljakutset iga inimene korraga valis?
test = data.copy()
kokku = test[valjakutsed_veerud].sum(axis=1)
st.write(kokku.value_counts())
##################################

st.write('K25 x K7_sorteerimiskaitumine')
st.write('K25 x K23_kasutuskolbmatud_tekstiilid')

###################################################
# SOBIV KOGUMISVIIS                               #
###################################################
st.write('## Sobivad kogumisviisid')
st.write(':red[*To-be-done*]')
st.write('**Vastajate jaotus sobivate kogumisviiside lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv kogumisviiside eelistuse alusel
kogumisviisid = sagedustabel(data_puhastatud, koodid, 'K29_sobiv_kogumisviis')

# Kuva tulpdiagramm
fig, ax = loo_hor_tulpdiagramm(
    kogumisviisid,
    '',
    style,
    sort=True   
)
tab1.pyplot(fig)
tab2.dataframe(kogumisviisid,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

st.write(':red[*To-be-done*]')

st.write('**Sobivad kogumisviisid maakondade lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Käitumine vanuse alusel
kogumisviis_elukoht = loo_risttabel(data_puhastatud, koodid, 'K5_elukoht', 'K29_sobiv_kogumisviis', normalize=True)

# Kuva tulpdiagramm
fig, ax = loo_stacked_tulpdiagramm(
    kogumisviis_elukoht,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(kogumisviis_elukoht,
    column_config={'K5_elukoht': ''}
)

risttabel_k29_vanus = loo_risttabel(
    df=data,
    df_koodid=koodid,
    tunnus_rida='K29_sobiv_kogumisviis',
    tunnus_veerg='K3_vanus',
    normalize=True  # Show percentages within age groups
)

st.write(risttabel_k29_vanus)

# Visualize
fig, ax = loo_hor_stacked_tulpdiagramm(
    df=risttabel_k29_vanus.T,  # Transpose: age groups as rows
    title='Sobiv kogumisviis vanuse järgi',
    style_config=style,
    normalize=True,
    sort=False
)

st.pyplot(fig)

st.write('Kas inimesed, kes sorteerivad, eelistavad mingeid meetodeid?')
risttabel_k29_sort = loo_risttabel(
    df=data,
    df_koodid=koodid,
    tunnus_rida='K29_sobiv_kogumisviis',
    tunnus_veerg='K7_sorteerimiskaitumine',
    normalize=True
)

st.write(risttabel_k29_sort)

fig, ax = loo_hor_stacked_tulpdiagramm(
    df=risttabel_k29_sort.T,  # Transpose: age groups as rows
    title='Sobiv kogumisviis sorteerimiskäitumise järgi',
    style_config=style,
    normalize=True,
    sort=False
)

st.pyplot(fig)

st.write('Võrdlus K22_peamised_valjakutsed')

###################################################
# VALMISOLEK KATEGORISEERIMISEKS                  #
###################################################
st.write('## Valmisolek esemete eraldi sorteerimiseks')
st.write(':red[*To-be-done*]')
st.write('**Vastajate jaotus valmisoleku lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv kogumisviiside eelistuse alusel
valmisolek = sagedustabel(data_puhastatud, koodid, 'K30_valmisolek_kategoriseerimiseks')

# Kuva tulpdiagramm
fig, ax = loo_hor_tulpdiagramm(
    valmisolek,
    '',
    style,
    sort=True   
)
tab1.pyplot(fig)
tab2.dataframe(valmisolek,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

st.write(':red[*To-be-done*]')

st.write('**Sobivad kogumisviisid sorteerimiskäitumise lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Käitumine vanuse alusel
valmisolek_kaitumine = loo_risttabel(data_puhastatud, koodid, 'K7_sorteerimiskaitumine', 'K30_valmisolek_kategoriseerimiseks', normalize=True)

# Kuva tulpdiagramm
fig, ax = loo_hor_stacked_tulpdiagramm(
    valmisolek_kaitumine,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(valmisolek_kaitumine,
    column_config={'K7_sorteerimiskaitumine': ''}
)

###################################################
# JULGUSTAVAD TEGURID                             #
###################################################
st.write('## Sorteerimist julgustavad tegurid')
st.write(':red[*To-be-done*]')
st.write('Neid, kes sorteerivad, peavad julgustavateks teguriteks kogumispunktide lähedus ja selged juhised. Ka mitte-sorteerijad samu tegureid maininud.')
st.write('**Vastajate jaotus julgustavate tegurite lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv väljakutsete alusel
tegurid = mitmikvastuse_sagedustabel(data_puhastatud, koodid, 'K33_julgustavad_tegurid').sort_values(by='protsent', ascending=False)

fig, ax = loo_hor_tulpdiagramm(
    tegurid,
    '',
    style,
    sort=True   
)
tab1.pyplot(fig)
tab2.dataframe(tegurid,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

tegurid_kaitumine = loo_mitmikvastuse_risttabel(data_puhastatud, koodid, 'K33_julgustavad_tegurid', 'K7_sorteerimiskaitumine')
tegurid_kaitumine

##################################
# Uuri vastusevariante

valjakutsed_veerud = [
    col for col in data.columns 
    if col.startswith('K33_julgustavad_tegurid') 
    and not col.endswith('_muu_tekst')  # Välista tekstvastustega veerud
]

st.write('Tunnuste koos esinemise sagedus:')
# Kui sageli mingid valikud koos esinevad?
fig, ax = plt.subplots()
corr_matrix = data[valjakutsed_veerud].corr()
# Loo heatmap
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
st.pyplot(fig)

# Leia 10 kõige tugevama korrelatsiooniga tunnust
# Set diagonal to NaN (ignore self-correlation)
import numpy as np
corr_no_diag = corr_matrix.where(~np.eye(len(corr_matrix), dtype=bool))

# 3. Get top correlations
corr_pairs = corr_no_diag.unstack().sort_values(ascending=False)
st.write('Tugevaimad korrelatsioonid:')
st.write(corr_pairs[corr_pairs < 1.0].head(10))  # Top 10 pairs

# Kui mitu väljakutset iga inimene korraga valis?
test = data.copy()
kokku = test[valjakutsed_veerud].sum(axis=1)
st.write(kokku.value_counts())
##################################

st.write('K33_julgustavad_tegurid x K22_peamised_valjakutsed - kas julgustavad tegurid on sellised, mis aitaks lahendada peamisi väljakutseid?')