import sys
import os

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Leia peakaust
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Impordi tabelite ja graafikute joonistamiseks vajalikud funktsioonid
from Python.visuaalide_abilised import maara_raporti_stiil
from Python.visuaalide_abilised import sagedustabel, mitmikvastuse_sagedustabel, loo_risttabel
from Python.visuaalide_abilised import loo_tulpdiagramm, loo_hor_tulpdiagramm, loo_stacked_tulpdiagramm, loo_hor_stacked_tulpdiagramm, loo_heatmap

# Määra graafikute stiil
style = maara_raporti_stiil()

# Impordi andmed puhastamise käigus loodud CVS-st
data = pd.read_csv('data/cleaned_data.csv')

# Impordi vastuste koodid
koodid = pd.read_csv('data/vastuste_koodid.csv')

# Asenda väheste vastajate arvuga maakonnad valikuga muu
data_puhastatud = data.copy()
data_puhastatud['K5_elukoht'] = data['K5_elukoht'].replace([2, 3, 5, 6, 7, 8, 10, 11, 13, 15], 16)

st.title('Tänane tarbijakäitumine tekstiilidest loobumise osas')
st.write(':red[*To-be-done*]')

###################################################
# SORTEERIMISKÄITUMINE                            #
###################################################
st.write('## Tänane sorteerimiskäitumine')
st.write(':red[*To-be-done*]')
st.write('Kategooriad: segaolmejäätmed, biojäätmed, vanapaber ja papp, pakendid, ohtlikud jäätmed, tekstiilijäätmed (kasutuskõlblikud/kasutuskõlbmatud)')
st.write('Mitte-sorteerijaid 4% (30) vastanutest. Mitte-sorteerijaid nii vähe, et selle alusel ei ole võimalik mingeid järeldusi teha.')
st.write('**Vastajate jaotus sorteerimiskäitumise lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])
# Leia vastajate arv teadlikkuse alusel
sorteerimiskaitumine = sagedustabel(data_puhastatud, koodid, 'K7_sorteerimiskaitumine')

# Kuva tulpdiagramm
fig, ax = loo_tulpdiagramm(
    sorteerimiskaitumine,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(sorteerimiskaitumine,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

st.write(':red[*To-be-done*]')
st.write('Kõige rohkem sorteeritakse vanusegrupis 30-49 ja Harju, Tartu ja Pärnu maakondades')
st.write('Järgnevatelt graafikutelt välja jäetud null-kulu ja muu')

st.write('**Vastajate sorteerimiskäitumine vanusegruppide lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Eemalda sorteerimiskäitumine, kus valikuks Null-kulu eluviis, muu
sorteerimine_puhas = data_puhastatud[data_puhastatud['K7_sorteerimiskaitumine'].isin([1, 2, 3, 4])]

# sorteerimiskaitumine_grupeeritud = sagedustabel(sorteerimine_puhas, sort_koodid, 'K7_sorteerimiskaitumine', use_full_codebook=False)
#print(f'Vastanutest {sorteerimiskaitumine_grupeeritud.loc[sorteerimiskaitumine_grupeeritud['kood']==3, 'protsent_str'].to_string(index=False)} sorteerib 3-s või enamas kategoorias')

# Käitumine vanuse alusel
kaitumine_vanus = loo_risttabel(sorteerimine_puhas, koodid, 'K3_vanus', 'K7_sorteerimiskaitumine', normalize=True)

# Kuva tulpdiagramm
fig, ax = loo_stacked_tulpdiagramm(
    kaitumine_vanus,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(kaitumine_vanus,
    column_config={'K3_vanus': ''}
)

st.write(':red[*To-be-done*]')

st.write('**Vastajate sorteerimiskäitumine maakondade lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Käitumine elukoha alusel
kaitumine_elukoht = loo_risttabel(sorteerimine_puhas, koodid, 'K5_elukoht', 'K7_sorteerimiskaitumine', normalize=True)

# Kuva tulpdiagramm
fig, ax = loo_stacked_tulpdiagramm(
    kaitumine_elukoht,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(kaitumine_elukoht,
    column_config={'K5_elukoht': ''}
)

st.write(':red[*To-be-done*]')
st.write('**Vastajate hinnang teadmistele vs sorteerimiskäitumine**')
tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])
# Hinnang enda teadmistele × teadlikkus seadusest
teadmised_sorteerimine = loo_risttabel(sorteerimine_puhas, koodid, 'K8_teadmiste_hinnang', 'K7_sorteerimiskaitumine', normalize=True)
# Statistiline analüüs: korrelatsioon teadlikkuse ja enesehinnangu vahel

# Loo heatmap
fig, ax = loo_heatmap(
    teadmised_sorteerimine,
    title=''
)
tab1.pyplot(fig)
tab2.dataframe(teadmised_sorteerimine,
    column_config={'K8_teadmiste_hinnang': ''}
)

fig, ax = plt.subplots()
sns.heatmap(
    teadmised_sorteerimine,
    cmap='coolwarm_r',
    linewidths=1,
    #linecolor='gray',
    annot=True
    #square= True
)
plt.xticks(rotation=45)
ax.set(xlabel=None)
ax.set(ylabel=None)

# Display the plot in Streamlit
st.pyplot(fig)

teadlikkus_sorteerimine = loo_risttabel(sorteerimine_puhas, koodid, 'K11_teadlikkus', 'K7_sorteerimiskaitumine', normalize=True)
# Statistiline analüüs: korrelatsioon teadlikkuse ja enesehinnangu vahel

# Loo heatmap
fig, ax = loo_heatmap(
    teadlikkus_sorteerimine,
    title=''
)
tab1.pyplot(fig)
tab2.dataframe(teadlikkus_sorteerimine,
    column_config={'K11_teadlikkus': ''}
)

fig, ax = plt.subplots()
sns.heatmap(
    teadlikkus_sorteerimine,
    cmap='coolwarm_r',
    linewidths=1,
    #linecolor='gray',
    annot=True
    #square= True
)
plt.xticks(rotation=45)
ax.set(xlabel=None)
ax.set(ylabel=None)

# Display the plot in Streamlit
st.pyplot(fig)

st.write(':red[*To-be-done*]')
st.write('**Vastajate hinnang probleemi tõsidusele vs sorteerimiskäitumine**')
tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])
# Hinnang enda teadmistele × teadlikkus seadusest
tosidus_sorteerimine = loo_risttabel(sorteerimine_puhas, koodid, 'K9_probleemi_tosidus', 'K7_sorteerimiskaitumine', normalize=True)
# Statistiline analüüs: korrelatsioon teadlikkuse ja enesehinnangu vahel

# Loo heatmap
fig, ax = plt.subplots()
sns.heatmap(
    tosidus_sorteerimine,
    cmap='coolwarm_r',
    linewidths=1,
    #linecolor='gray',
    annot=True
    #square= True
)
plt.xticks(rotation=45)
ax.set(xlabel=None)
ax.set(ylabel=None)

# Display the plot in Streamlit
tab1.pyplot(fig)
tab2.dataframe(tosidus_sorteerimine,
    column_config={'K9_probleemi_tosidus': ''}
)


###################################################
# TEKSTIILIDE KOGUS                               #
###################################################
st.write('## Loobutud tekstiilide kogus ühes kalendriaastas')
st.write(':red[*To-be-done*]')

st.write('**Vastajate jaotus loobutud tekstiilide koguse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])
# Leia vastajate arv teadlikkuse alusel
loobutud_tekstiilid = sagedustabel(data_puhastatud, koodid, 'K14_tekstiilide_kogus')

# Kuva tulpdiagramm
fig, ax = loo_tulpdiagramm(
    loobutud_tekstiilid,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(loobutud_tekstiilid,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

###################################################
# MITEEVAJALIKUD TEKSTIILID                       #
###################################################
st.write('## Mittevajalikud tekstiilid')
st.write('Mida võtad peamiselt ette rõivaste või kodutekstiilidega, mida enam ei vaja?')
st.write(':red[*To-be-done*]')

st.write('**Käitumine mittevajalikest tekstiilidest loobumisel**')
tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

mittevajalikud_tekstiilid = mitmikvastuse_sagedustabel(data_puhastatud, koodid, 'K15_mittevajalikud_tekstiilid').sort_values(by='protsent', ascending=False)

fig, ax = loo_hor_tulpdiagramm(
    mittevajalikud_tekstiilid,
    '',
    style,
    sort=True   
)
tab1.pyplot(fig)
tab2.dataframe(mittevajalikud_tekstiilid,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

###################################################
# LOOBUMISE PÕHJUSED                              #
###################################################
st.write('## Loobumise põhjused')
st.write(':red[*To-be-done*]')

st.write('**Tekstiilidest loobumise põhjused**')
tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

loobumise_pohjused = mitmikvastuse_sagedustabel(data_puhastatud, koodid, 'K19_loobumise_pohjused').sort_values(by='protsent', ascending=False)

fig, ax = loo_hor_tulpdiagramm(
    loobumise_pohjused,
    '',
    style,
    sort=True   
)
tab1.pyplot(fig)
tab2.dataframe(loobumise_pohjused,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

###################################################
# KASUTUSKÕLBMATUD TEKSTIILID                     #
###################################################
st.write('## Kasutuskõlbmatud tekstiilid')
st.write(':red[*To-be-done*]')

st.write('**Käitumine kasutuskõlbmatute tekstiilidega**')
tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

kolbmatud = mitmikvastuse_sagedustabel(data_puhastatud, koodid, 'K23_kasutuskolbmatud_tekstiilid').sort_values(by='protsent', ascending=False)

fig, ax = loo_hor_tulpdiagramm(
    kolbmatud,
    '',
    style,
    sort=True   
)
tab1.pyplot(fig)
tab2.dataframe(kolbmatud,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

###################################################
# SOBIMATUD TEKSTIILID                            #
###################################################
st.write('## Korduskasutuseks sobimatud tekstiilid')