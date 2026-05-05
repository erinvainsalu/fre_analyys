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

# Kasuta laia paigutust
#st.set_page_config(layout='wide')

# Asenda väheste vastajate arvuga maakonnad valikuga muu
data_puhastatud = data.copy()
data_puhastatud['K5_elukoht'] = data['K5_elukoht'].replace([2, 3, 5, 6, 7, 8, 10, 11, 13, 15], 16)

st.title('Tarbijate teadlikkus')

st.write('Teadlikkus annab ülevaate tarbijate teadmistest, hoiakutest ja käitumisest, mis on seotud nende ostuotsuste ja tarbimisviiside mõjuga keskkonnale ning ühiskonnale. ' \
'See hõlmab arusaamist toodete elutsüklist, nende tootmise ja tarbimise tagajärgedest ning valikuid, mis aitavad vähendada jäätmeid ja soodustada ringmajandust. ' \
'Tekstiilide ja rõivaste kontekstis väljendub tarbijateadlikkus eelkõige valmisolekus teha teadlikke otsuseid rõivaste ostmisel, kasutamisel ja nende eluea lõpus vastutustundlikult käitlemises.')

###################################################
# TEADLIKKUS SEADUSEST                            #
###################################################

st.write('## Teadlikkus 2025. aastal Eestis kehtima hakanud seadusest')

st.write('Uuringus osalejatelt küsiti nende teadlikkust seoses 2025. aasta 1. jaanuaril algul jõustunud seadusega. ' \
'Jõustunud seadusest oli teadlik 252 vastajat (39%), kusjuures 1% nendest leidis, et tegemist on valitsuse ja KOV-ide, mitte tarbijate probleemiga. ' \
'Ülejäänud 61% vastanutest jagunesid nendeks, eks ei ole seadusest teadlikud (28%) ning nendeks, kes on küll seadusest kuulnud, aga ei ole teadlikud detailidest.')

st.write('**Vastajate jaotus teadlikkuse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])
# Leia vastajate arv teadlikkuse alusel
teadlikkus = sagedustabel(data_puhastatud, koodid, 'K11_teadlikkus').sort_values(by='protsent', ascending=False)

# Kuva tulpdiagramm
fig, ax = loo_hor_tulpdiagramm(
    teadlikkus,
    '',
    style,
    sort=True
)
tab1.pyplot(fig)
tab2.dataframe(teadlikkus,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

st.write('Seadusest on kõige teadlikumad vastajad vanuses 30+. Nooremate vastajate seas on teadlikkus kõige madalam. Vanusegruppides 18-29 ning <17 on neid, kes ei ole seadusest üldse teadlikud 41-52%. ' \
'Kõigis vanusegruppides on üsna võrdselt kolmandik neid, kes on seadusest küll kuulnud, kuid ei tea täpsemalt selle sisu.')

st.write('**Vastajate teadlikkus vanusegruppide lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Teadlikkus vanusegruppide alusel
teadlikkus_vanus = loo_risttabel(data_puhastatud, koodid, 'K3_vanus', 'K11_teadlikkus', normalize=True)

# Kuva tulpdiagramm
fig, ax = loo_stacked_tulpdiagramm(
    teadlikkus_vanus,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(teadlikkus_vanus,
    column_config={'K3_vanus': ''}
)

st.write('**Vastajate teadlikkus maakondade lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Teadlikkus vanusegruppide alusel
teadlikkus_elukoht = loo_risttabel(data_puhastatud, koodid, 'K5_elukoht', 'K11_teadlikkus', normalize=True)

# Kuva tulpdiagramm
fig, ax = loo_stacked_tulpdiagramm(
    teadlikkus_elukoht,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(teadlikkus_elukoht,
    column_config={'K5_elukoht': ''}
)

###################################################
# HINNANG TEADMISTELE                             #
###################################################

st.write('## Hinnang üldistele teadmistele jätkusuutlike valikute tegemisel')
st.write('Tarbijate teadlikkus rõivaste tarbimisega seotud keskkonna ja sotsiaalsetest mõjudest on oluline aspekt nende ostukäitumise ja tekstiilide tarbimisharjumuste kujundamisel. ' \
'Uuringu kohaselt peab antud teemal enda teadmisi väga madalaks või pigem madalaks 12% vastajatest. Enda teadmisi pigem heaks või väga heaks hindab 52% vastajatest. ' \
'Tulemuste hindamisel tuleb arvesse võtta, et kuna küsitlust jagati kanalites, mille kaudu tarbivad infot pigem keskmisest teadlikumad tarbijad, ' \
'siis vastused ei peegelda Eesti keskmist inimest.')

st.write('**Vastajate jaotus teadmiste hinnangu lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate hinnang oma teadmistele
teadmiste_hinnang = sagedustabel(data_puhastatud, koodid, 'K8_teadmiste_hinnang')

# Loo tulpdiagramm
fig, ax = loo_tulpdiagramm(
    teadmiste_hinnang,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(teadmiste_hinnang,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

st.write('Võib järeldada, et enamik vastanuid peab end rõivaste ja tekstiilide jätkusuutlikkuse teemadel mõõdukalt teadlikuks. Kuigi ligi pooltel on olemas teatud teadmised, mis võimaldavad teha teadlikumaid tarbimisotsuseid, viitab vähene väga heaks hinnatud teadlikkuse osakaal vajadusele süvendada tarbijate arusaama rõivatootmise ja -tarbimise keskkonna- ning sotsiaalsetest mõjudest. See näitab, et tarbijate teadlikkuse tõstmine on jätkuvalt oluline suund jätkusuutlike tarbimisharjumuste kujundamisel.')
st.write(':red[*To-be-done*]')
st.write('Kuna enda teadmiseid on madalamalt hinnanud eelkõige nooremad kasutajagrupid, siis tuleks teadmiseid tõsta just nendes vanusegruppides.')
st.write(':red[*To-be-done*]')

st.write('**Vastajate teadmiste hinnang vanusegruppide lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Teadmiste hinnang vanuse alusel
teadmised_vanus = loo_risttabel(data_puhastatud, koodid, 'K3_vanus', 'K8_teadmiste_hinnang', normalize=True)

# Kuva tulpdiagramm
fig, ax = loo_stacked_tulpdiagramm(
    teadmised_vanus,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(teadmised_vanus,
    column_config={'K3_vanus': ''}
)

st.write(':red[*To-be-done*]')
st.write('Graafikult on näha selge seos enda teadmiste hinnangu ning teadlikkuse vahel. ' \
'Inimestest, kes hindavad oma teadmisi kui **"Väga hea"**, on 64% teadlikud uuest seadusest. ' \
'Inimeste hulgas, kes hindavad oma teadmisi kui **"Väga madal"**, ei ole 63% uuest seadusest teadlikud ning nende hulgas on 0% seadusest teadlikke.')
st.write('Kõigis enesehinnangu gruppides leidub 25-37% neid, kes on seadusest kuulnud, kuid ei ole täpsemalt kursis selle sisuga.')
st.write('Nende hulgas, kes hindasin oma teadmiseid väga madalaks või pigem madalaks on 53-63% neid, kes ei ole uuest seadusest teadlikud.')
st.write('**Vastajate hinnang teadmistele vs teadlikkus uuest seadusest**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Hinnang enda teadmistele × teadlikkus seadusest
teadmised_teadlikkus = loo_risttabel(data_puhastatud, koodid, 'K8_teadmiste_hinnang', 'K11_teadlikkus', normalize=True)
# Statistiline analüüs: korrelatsioon teadlikkuse ja enesehinnangu vahel

# Loo heatmap
fig, ax = loo_heatmap(
    teadmised_teadlikkus,
    title=''
)
tab1.pyplot(fig)
tab2.dataframe(teadmised_teadlikkus,
    column_config={'K8_teadmiste_hinnang': ''}
)

###################################################
# HINNANG PROBLEEMI TÕSIDUSELE                    #
###################################################
st.write('## Tekstiilijäätmete probleemi tõsiduse hinnang')
st.write('Tarbijatel paluti hinnata tekstiilijäätmete probleemi tõsidust Eestis ja globaalses mastaabis')
st.write(':red[*To-be-done*]')

st.write('**Vastajate jaotus probleemi tõsiduse hinnangu lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate hinnang oma teadmistele
probleemi_hinnang = sagedustabel(data_puhastatud, koodid, 'K9_probleemi_tosidus')

# Loo tulpdiagramm
fig, ax = loo_tulpdiagramm(
    probleemi_hinnang,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(probleemi_hinnang,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

st.write(':red[*To-be-done*]')

st.write('**Probleemi tõsiduse hinnang vanusegruppide lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Probleemi tõsiduse hinnang vanuse alusel
probleem_vanus = loo_risttabel(data_puhastatud, koodid, 'K3_vanus', 'K9_probleemi_tosidus', normalize=True)

# Loo tulpdiagramm
fig, ax = loo_stacked_tulpdiagramm(
    probleem_vanus,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(teadmised_vanus,
    column_config={'K3_vanus': ''}
)

st.write(':red[*To-be-done*]')
st.write('Inimestest, kes hindavad oma teadmisi kui ...')
st.write('Graafikult on näha seos enda probleemi tõsiduse hinnangu ning teadlikkuse vahel. ' \
'Inimestest, kes hindavad probleemi tõsiseks või pigem tõsiseks on 36-46% teadlikud uuest seadusest.')

st.write('**Vastajate hinnang probleemi tõsidusele vs teadmised uuest seadusest**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Hinnang probleemi tõsidusele × teadlikkus seadusest
probleem_teadlikkus = loo_risttabel(data_puhastatud, koodid, 'K9_probleemi_tosidus', 'K11_teadlikkus', normalize=True)
# Statistiline analüüs: korrelatsioon teadlikkuse ja enesehinnangu vahel

# Loo heatmap
fig, ax = loo_heatmap(
    probleem_teadlikkus,
    title=''
)
tab1.pyplot(fig)
tab2.dataframe(probleem_teadlikkus,
    column_config={'K9_probleemi_tosidus': ''}
)

###################################################
# KOMMUNIKATSIOONI SELGUS                         #
###################################################
st.write('## KOV kommunikatsiooni selgus')
st.write(':red[*To-be-done*]')

st.write('**Vastajate jaotus kommunikatsiooni selguse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv kommunikatsiooni selguse alusel
kommunikatsiooni_selgus = sagedustabel(data_puhastatud, koodid, 'K13_kommunikatsiooni_selgus')

# Kommunikatsiooni selguse jaotuse tulpdiagramm
fig, ax = loo_tulpdiagramm(
    kommunikatsiooni_selgus,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(kommunikatsiooni_selgus,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)
st.write(':red[*To-be-done*]')

st.write('**Kommunikatsiooni selgus maakondade lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Kommunikatsiooni selgus elukoha alusel risttabel
kommunikatsioon_elukoht = loo_risttabel(data_puhastatud, koodid, 'K5_elukoht', 'K13_kommunikatsiooni_selgus', normalize=True)

# Loo tulpdiagramm
fig, ax = loo_stacked_tulpdiagramm(
    kommunikatsioon_elukoht,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(kommunikatsioon_elukoht,
    column_config={'K5_elukoht': ''}
)

st.write(':red[*To-be-done*]')
st.write('Inimestest, kes hindavad oma teadmisi kui ...')

st.write('**Kommunikatsiooni selgus vs teadlikkus uuest seadusest**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Hinnang probleemi tõsidusele × teadlikkus seadusest
kommunikatsioon_teadlikkus = loo_risttabel(data_puhastatud, koodid, 'K13_kommunikatsiooni_selgus', 'K11_teadlikkus', normalize=True)
# Statistiline analüüs: korrelatsioon teadlikkuse ja enesehinnangu vahel

# Loo heatmap
fig, ax = loo_heatmap(
    kommunikatsioon_teadlikkus,
    title=''
)
tab1.pyplot(fig)
tab2.dataframe(kommunikatsioon_teadlikkus,
    column_config={'K13_kommunikatsiooni_selgus': ''}
)

# Leia vastuste jaotus - teabe allikate eelistused
teabe_allikad = mitmikvastuse_sagedustabel(data, koodid, 'K32_teabe_allikad')

fig, ax = loo_hor_tulpdiagramm(
    teabe_allikad,
    'Teabeallikad',
    style,
    sort=True   
)

st.pyplot(fig)

teabeallikad = data[[
    'K3_vanus',
    'K32_teabe_allikad_1',
    'K32_teabe_allikad_2',
    'K32_teabe_allikad_3',
    'K32_teabe_allikad_4',
    'K32_teabe_allikad_5',
    'K32_teabe_allikad_6',
    'K32_teabe_allikad_7',
    'K32_teabe_allikad_8',
    'K32_teabe_allikad_9',
    'K32_teabe_allikad_10']].groupby('K3_vanus').agg('sum').rename(
        columns={
            'K32_teabe_allikad_1': 'Raadio',
            'K32_teabe_allikad_2': 'Televisioon',
            'K32_teabe_allikad_3': 'Ajalehed, ajakirjad',
            'K32_teabe_allikad_4': 'Artiklid veebiväljaannetes',
            'K32_teabe_allikad_5': 'Raamatud',
            'K32_teabe_allikad_6': 'Sotsiaalmeedia',
            'K32_teabe_allikad_7': 'Uuringud ja teadusartiklid',
            'K32_teabe_allikad_8': 'Sõbrad/tuttavad',
            'K32_teabe_allikad_9': 'Ei huvitu sellest infost teadlikult',
            'K32_teabe_allikad_10': 'Muu'
        }
    ).T

st.dataframe(teabeallikad,column_config={
        '1': '<17',
        '2': '18-29',
        '3': '30-49',
        '4': '50-64',
        '5': '65>'
    })

fig, ax = loo_hor_stacked_tulpdiagramm(
    teabeallikad,
    '',
    style
)
st.pyplot(fig)

###################################################
# RIIKLIKE JUHISTE SELGUS                         #
###################################################
st.write('## Riiklike juhiste selgus')
st.write(':red[*To-be-done*]')

st.write('**Vastajate jaotus riiklike juhiste selguse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv kommunikatsiooni selguse alusel
juhise_selgus = sagedustabel(data_puhastatud, koodid, 'K28_riikliku_juhise_selgus').sort_values(by='protsent', ascending=False)

# Kommunikatsiooni selguse jaotuse tulpdiagramm
fig, ax = loo_hor_tulpdiagramm(
    juhise_selgus,
    '',
    style,
    sort=True
)
tab1.pyplot(fig)
tab2.dataframe(juhise_selgus,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)
st.write(':red[*To-be-done*]')

st.write('**Riiklike juhiste selgus maakondade lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Kommunikatsiooni selgus elukoha alusel risttabel
juhis_elukoht = loo_risttabel(data_puhastatud, koodid, 'K5_elukoht', 'K28_riikliku_juhise_selgus', normalize=True)

# Loo tulpdiagramm
fig, ax = loo_stacked_tulpdiagramm(
    juhis_elukoht,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(juhis_elukoht,
    column_config={'K5_elukoht': ''}
)

st.write(':red[*To-be-done*]')

st.write('**Kommunikatsiooni selgus vs riiklike juhiste selgus**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Hinnang probleemi tõsidusele × teadlikkus seadusest
kommunikatsioon_juhis = loo_risttabel(data_puhastatud, koodid, 'K13_kommunikatsiooni_selgus', 'K28_riikliku_juhise_selgus', normalize=True)
# Statistiline analüüs: korrelatsioon teadlikkuse ja enesehinnangu vahel

# Loo heatmap
fig, ax = loo_heatmap(
    kommunikatsioon_juhis,
    title=''
)
tab1.pyplot(fig)
tab2.dataframe(kommunikatsioon_juhis,
    column_config={'K13_kommunikatsiooni_selgus': ''}
)