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
from Python.visuaalide_abilised import maara_raporti_stiil, leia_sildi_mapping
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
# Hinnang enda teadmistele × sorteerimiskäitumine
teadmised_sorteerimine = loo_risttabel(sorteerimine_puhas, koodid, 'K8_teadmiste_hinnang', 'K7_sorteerimiskaitumine', normalize=True)

# Loo heatmap
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

tab1.pyplot(fig)
tab2.dataframe(teadmised_sorteerimine,
    column_config={'K8_teadmiste_hinnang': ''}
)

st.write(':red[*To-be-done*]')
st.write('Kas vastajad käituvad vastavalt oma väärtushinnangutele?')
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
# ULTRAKIIRMOE OSTMINE                            #
###################################################
st.write('## Ultrakiirmoe ostmise harjumus')
st.write(':red[*To-be-done*]')
st.write('Lisaküsimusena oli vastajatel võimalik täpsustada kas nad ostavad ultrakiirmoodi. Vastuseid kokku ???')

st.write('**Vastajate jaotus loobutud ultrakiirmoe soetamise lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])
# Leia vastajate arv teadlikkuse alusel
kiirmood = sagedustabel(data_puhastatud, koodid, 'K41_ultrakiirmoe_ostmine')

# Kuva tulpdiagramm
fig, ax = loo_tulpdiagramm(
    kiirmood,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(kiirmood,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

st.write(':red[*To-be-done*]')

st.write('**Ultrakiirmoe ostmise sagedus vanusegruppide lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Eemalda sorteerimiskäitumine, kus valikuks Null-kulu eluviis, muu
# sorteerimine_puhas = data_puhastatud[data_puhastatud['K7_sorteerimiskaitumine'].isin([1, 2, 3, 4])]

# sorteerimiskaitumine_grupeeritud = sagedustabel(sorteerimine_puhas, sort_koodid, 'K7_sorteerimiskaitumine', use_full_codebook=False)
#print(f'Vastanutest {sorteerimiskaitumine_grupeeritud.loc[sorteerimiskaitumine_grupeeritud['kood']==3, 'protsent_str'].to_string(index=False)} sorteerib 3-s või enamas kategoorias')

# Käitumine vanuse alusel
kiirmood_vanus = loo_risttabel(data_puhastatud, koodid, 'K3_vanus', 'K41_ultrakiirmoe_ostmine', normalize=True)

# Kuva tulpdiagramm
fig, ax = loo_stacked_tulpdiagramm(
    kiirmood_vanus,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(kiirmood_vanus,
    column_config={'K3_vanus': ''}
)

###################################################
# RÕIVASTE OSTMISSAGEDUS                          #
###################################################
st.write('## Uute rõivaste ostmissagedus')
st.write(':red[*To-be-done*]')
st.write('Lisaküsimusena oli vastajatel võimalik täpsustada kui sageli nad ostavad uusi rõivaid. Vastuseid kokku ???')

st.write('**Vastajate jaotus loobutud rõivaste soetamise sageduse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])
# Leia vastajate arv teadlikkuse alusel
ostmissagedus = sagedustabel(data_puhastatud, koodid, 'K40_ostmissagedus')

# Kuva tulpdiagramm
fig, ax = loo_tulpdiagramm(
    ostmissagedus,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(ostmissagedus,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

st.write(':red[*To-be-done*]')

st.write('**Uute rõivaste ostmise sagedus vanusegruppide lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Eemalda sorteerimiskäitumine, kus valikuks Null-kulu eluviis, muu
# sorteerimine_puhas = data_puhastatud[data_puhastatud['K7_sorteerimiskaitumine'].isin([1, 2, 3, 4])]

# sorteerimiskaitumine_grupeeritud = sagedustabel(sorteerimine_puhas, sort_koodid, 'K7_sorteerimiskaitumine', use_full_codebook=False)
#print(f'Vastanutest {sorteerimiskaitumine_grupeeritud.loc[sorteerimiskaitumine_grupeeritud['kood']==3, 'protsent_str'].to_string(index=False)} sorteerib 3-s või enamas kategoorias')

# Käitumine vanuse alusel
sagedus_vanus = loo_risttabel(data_puhastatud, koodid, 'K3_vanus', 'K40_ostmissagedus', normalize=True)

# Kuva tulpdiagramm
fig, ax = loo_stacked_tulpdiagramm(
    sagedus_vanus,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(sagedus_vanus,
    column_config={'K3_vanus': ''}
)

###################################################
# MITTEVAJALIKUD TEKSTIILID                       #
###################################################
st.write('## Mittevajalikud tekstiilid')
st.write('Mida võtad peamiselt ette rõivaste või kodutekstiilidega, mida enam ei vaja?')
st.write(':red[KES VIIB OLMEPRÜGISSE???]')
st.write(':red[KAS OLMEJÄÄTMESSE need, kes viivad olmejäätmetesse, ES VIIB OLMEPRÜGISSE???]')
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

st.write('Kasutuskülbmatud tekstiilid tuleks viia jäätmejaama. ' \
'Paljud need, kes on teadlikuse seadusest märkinud kõrgeks, viskavad siiski rõivad olmejäätmetesse või viivad riidekonteinerisse.')

# Segaolmejäätmete konteinerisse viijad vs teadlikkus
social_proof_receptive = data_puhastatud[
    (data_puhastatud['K23_kasutuskolbmatud_tekstiilid_2'].isin([1])) &
    (data_puhastatud['K11_teadlikkus'].isin([1]))
].shape[0]

st.write(f'Segaolmejäätmete konteinerisse viib kasutuskõlbmatuid tekstiile {social_proof_receptive} teadlikest kasutajatest')

veerud = {
    'K23_kasutuskolbmatud_tekstiilid_1': 'Rõivakonteiner',
    'K23_kasutuskolbmatud_tekstiilid_2': 'Segaolmejäätmete konteiner',
    'K23_kasutuskolbmatud_tekstiilid_3': 'Jäätmejaam',
    'K23_kasutuskolbmatud_tekstiilid_4': 'Põletamine (kodus)',
    'K23_kasutuskolbmatud_tekstiilid_5': 'Matmine',
    'K23_kasutuskolbmatud_tekstiilid_6': 'Ei tea (kuna ei vastuta)',
    'K23_kasutuskolbmatud_tekstiilid_7': 'Muu'
}

labelid = leia_sildi_mapping(koodid, 'K11_teadlikkus')

teabeallikad = (
    data_puhastatud[['K11_teadlikkus', *veerud]]
    .groupby('K11_teadlikkus')
    .sum()
    .rename(columns=veerud)
    .T # transponeeri
)
st.dataframe(teabeallikad, column_config=labelid)

###################################################
# SOBIMATUD TEKSTIILID                            #
###################################################
st.write('## Korduskasutuseks sobimatud tekstiilid')

st.write(':red[*To-be-done*]')
st.write('Uuringus küsiti, kas vastajad on teadlikult viinud tekstiilikonteineritesse rõivaid, mis korduskasutuseks ei sobi.')
st.write('**Vastajate jaotus teadliku käitumise lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])
# Leia vastajate arv teadlikkuse alusel
sobimatu_kaitumine = sagedustabel(data_puhastatud, koodid, 'K26_korduskasutuseks_sobimatud_tekstiilid')

# Kuva tulpdiagramm
fig, ax = loo_tulpdiagramm(
    sobimatu_kaitumine,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(sobimatu_kaitumine,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)