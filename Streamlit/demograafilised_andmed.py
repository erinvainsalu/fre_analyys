import sys
import os

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Leia peakaust
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Impordi tabelite ja graafikute joonistamiseks vajalikud funktsioonid
from Python.visuaalide_abilised import maara_raporti_stiil
from Python.visuaalide_abilised import sagedustabel, mitmikvastuse_sagedustabel, loo_risttabel
from Python.visuaalide_abilised import loo_tulpdiagramm, loo_hor_tulpdiagramm, loo_stacked_tulpdiagramm, loo_hor_stacked_tulpdiagramm

# Määra graafikute stiil
style = maara_raporti_stiil()

# Impordi andmed puhastamise käigus loodud CVS-st
data = pd.read_csv('data/cleaned_data.csv')

# Impordi vastuste koodid
koodid = pd.read_csv('data/vastuste_koodid.csv')

# Asenda väheste vastajate arvuga maakonnad valikuga muu
data_puhastatud = data.copy()
data_puhastatud['K5_elukoht'] = data['K5_elukoht'].replace([2, 3, 5, 6, 7, 8, 10, 11, 13, 15], 16)

st.title('Vastajate demograafilised andmed')

###################################################
# VANUS                                           #
###################################################

st.write('## Vastajate vanus')
st.write('Erinevad vanusegrupid tarbivad rõivaid ja kodutekstiile erinevalt. ' \
'Samuti erinevad vanusegrupiti ka rõivastest ja tekstiilidest loobumise motiivid. Seetõttu küsiti uuringus vastajate vanusegruppi.')
st.write('668-st vastanust moodustasid enam kui poole ehk 55% 30-49-aastased vastajad. ' \
'Suurim vastanute hulk vahemikus 30-49 eluaastat on tõenäoliselt tingitud küsimustiku jagamise kanalist, milleks oli suurel määral sotsiaalmeedia erinevad platvormid ja kanalid. ' \
'Lisaks jagati küsimustikku ka Harjumaa valla paberväljaandes, mis tõi eelduslikult küsimustikule vastajaid vanusest 65 ja vanemad.')

st.write('**Vastajate jaotus vanusegruppide lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv vanusegrupiti
vanus_sagedus = sagedustabel(data, koodid, 'K3_vanus')

# Loo tulpdiagramm
fig, ax = loo_tulpdiagramm(
    vanus_sagedus,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(vanus_sagedus,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

st.write('Peamine kiirmoe tarbija globaalses vaates on vanuses 26-35, mistõttu võib eeldada, et see vanusegrupp ostab ja seetõttu ka loobub kõige enam rõivastest ning kodutekstiilidest ja seda ka Eestis.')

###################################################
# SUGU                                            #
###################################################

st.write('## Vastajate sugu')
st.write('Käesolevale küsimustikule andsid enim vastuseid naised (88%). ' \
'Mehi vastas küsimustikule 11% ning 1% vastanutest ei soovinud enda sugu avaldada. ' \
'Vastuste kogumise perioodil prooviti meeste vastuste osakaalu suurendada, kuid tekstiile ja rõivaid puudutavad teemakäsitlused jäävad sageli meestele kaugeks.')

st.write('**Vastajate jaotus soo lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv soo alusel
sugu_sagedus = sagedustabel(data, koodid, 'K4_sugu').sort_values(by='protsent', ascending=False)

# Loo tulpdiagramm
fig, ax = loo_tulpdiagramm(
    sugu_sagedus,
    '',
    style,
    sort=True
)
tab1.pyplot(fig)
tab2.dataframe(sugu_sagedus,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

st.write('Kuna vastajate sooline jaotus on tugevalt naiste poole kaldu, siis edasise analüüsi käigus ei vaadelda vastuste jaotust soolise kuuluvuse alusel.')

###################################################
# ELUKOHT                                         #
###################################################

st.write('## Vastajate peamine elukoht')
st.write('Uuringus osalesid inimesed üle Eesti, kuid kõige suurem osa vastajatest elab Harjumaal (61%), moodustades selge enamuse. ' \
'Tartumaalt ja Pärnumaalt oli samuti märkimisväärne hulk vastajaid - vastavalt 13% ja 8%. ' \
'Lisaks olid esindatud Järvamaa (5%) ning Viljandimaa (3%) elanikud. ' \
'Ülejäänud maakondades ning välismaal elavate vastajate osakaal on 9%.')

st.write('**Vastajate jaotus maakonna lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv elukoha alusel
elukoht_sagedus = sagedustabel(data, koodid, 'K5_elukoht').sort_values(by='protsent', ascending=False)

# Loo tulpdiagramm
fig, ax = loo_hor_tulpdiagramm(
    elukoht_sagedus,
    '',
    style,
    sort=True
)
tab1.pyplot(fig)
tab2.dataframe(elukoht_sagedus,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

st.write('Kuna vastajate esindatus enamuses Eesti maakondades on madal, siis edasises analüüsi käigus koondatakse vähese vastajate hulgaga maakonnad vastusevariandi "Muu" alla.')

st.write('**Vastajate vanuseline jaotus maakonna lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Vanuseline jaotus elukoha alusel
vanus_elukoht = loo_risttabel(data_puhastatud, koodid, 'K5_elukoht', 'K3_vanus', normalize=True)

# Loo tulpdiagramm
fig, ax = loo_stacked_tulpdiagramm(
    vanus_elukoht,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(vanus_elukoht,
    column_config={'K5_elukoht': ''}
)

st.write('Vastajate vanuseline jaotus erinevates maakondades on maakondade lõikes sarnane. ' \
'Kõige enam vastajaid on vanusegrupis 30-49 (48-65%). Järgnevad vastajad vanusegruppides 18-29 ja 50-64. ' \
'Erandiks on Järvamaa, kus enamus vastajaid on vanusegrupist <17 (74%).')

###################################################
# KEEL                                            #
###################################################

st.write('## Vastajate peamine kodune keel')
st.write('Valdav enamus (96%) küsitlusele vastanutest märkis enda koduseks keeleks eesti keele. ' \
'15 vastanu ehk 2% kodune keel on vene keel. Vähemuses olid vastajad, kelle kodune keel on inglise või mõni muu keel. ' \
'Kuna küsimustikku oli võimalik täita vaid eesti keeles, siis see selgitab miks suure osa vastajate peamiseks koduseks keeleks on eesti keel.')

st.write('**Vastajate jaotus koduse keele lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv keele alusel
keel_sagedus = sagedustabel(data, koodid, 'K6_keel').sort_values(by='protsent', ascending=False)

fig, ax = loo_tulpdiagramm(
    keel_sagedus,
    '',
    style,
    sort=True
)
tab1.pyplot(fig)
tab2.dataframe(keel_sagedus,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)