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

st.title('Tarbijate teadlikkus')

st.write('Teadlikkus annab ülevaate tarbijate teadmistest, hoiakutest ja käitumisest, mis on seotud nende ostuotsuste ja tarbimisviiside mõjuga keskkonnale ning ühiskonnale. ' \
'See hõlmab arusaamist toodete elutsüklist, nende tootmise ja tarbimise tagajärgedest ning valikuid, mis aitavad vähendada jäätmeid ja soodustada ringmajandust. ' \
'Tekstiilide ja rõivaste kontekstis väljendub tarbijateadlikkus eelkõige valmisolekus teha teadlikke otsuseid rõivaste ostmisel, kasutamisel ja nende eluea lõpus vastutustundlikult käitlemises.')

st.write('Aastal 2025 jõustunud seadus näeb ette tekstiilijäätmete liigiti kogumise olmeprügist eraldi, ' \
'ehk tarbijal ei ole enam seaduse järgi lubatud visata tekstiilijäätmeid, näiteks kulunud ja katkiseid rõivaid, olmeprügi hulka. ' \
'See on pannud KOV-idele kohustuse luua süsteem tarbijatelt tekstiilijäätmete eraldi kogumiseks.')

###################################################
# TEADLIKKUS SEADUSEST                            #
###################################################

st.write('## Teadlikkus 2025. aastal Eestis kehtima hakanud seadusest')

st.write('Uuringus osalejatelt küsiti nende teadlikkust 2025. aasta algul jõustunud seadusest. ' \
'Jõustunud seadusest oli teadlik 252 vastajat (39%), kusjuures 1% nendest leidis, et tegemist on valitsuse ja KOV-ide, mitte tarbijate probleemiga. ' \
'Ülejäänud 61% vastanutest jagunesid nendeks, kes ei ole seadusest teadlikud (28%) ning nendeks, kes on küll seadusest kuulnud, aga ei ole teadlikud detailidest (33%). ' \
'Kuigi 72% vastajatest on vähemalt ühel või teisel moel jõustunud seadusest kuulnud, siis siiski on palju teadmatust seoses seaduse ja selle täitmise üksikasjadega. ')

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

st.write('Seadusest on kõige teadlikumad vastajad vanuses 30+, kelle seas on seadusest teadlikke 40-46%. ' \
'Nooremate vastajate seas on seadusest teadlikke 21-30%. Nendes vanusegruppides on võrreldes teistega oluliselt rohkem neid, kes ei ole seadusest üldse teadlikud (41-52%). ' \
'Kõigis vanusegruppides on umbes kolmandik neid, kes on seadusest küll kuulnud, kuid ei tea täpsemalt selle sisu.')

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

st.write('Maakondade lõikes on näha, et teiste maakondadega võrreldes on Pärnumaal oluliselt rohkem vastajaid, kes on uuest seadusest teadlikud (62%). ' \
'Selles maakonnas on ka seadusest mitteteadlike hulk võrreldes teiste maakondadega pigem väiksem. ' \
'Ootuste vastaselt on Eesti suurimate maakondade (Harju, Tartu) puhul seadusest mitteteadlike vastajate hulk pigem kõrge - vastavalt 28% ja 31%.')

st.write('**Vastajate teadlikkus maakondade lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Teadlikkus elukoha alusel
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
'siis vastused ei pruugi peegeldada Eesti keskmist inimest.')

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

st.write('Vastustest võib järeldada, et enamik vastanuid peab end rõivaste ja tekstiilide jätkusuutlikkuse teemadel mõõdukalt teadlikuks. ' \
'Kuigi pooltel vastajatel on olemas teatud teadmised, mis võimaldavad teha teadlikumaid tarbimisotsuseid, viitab väike väga heade teadmistega vastajate hulk vajadusele süvendada tarbijate arusaama rõivatootmise ja -tarbimise keskkonna- ning sotsiaalsetest mõjudest. ' \
'See näitab, et tarbijate teadlikkuse tõstmine on jätkuvalt oluline suund jätkusuutlike tarbimisharjumuste kujundamisel.')

st.write('Enda teadmiseid on madalamalt hinnanud eelkõige nooremad kasutajagrupid (<18 ja 18-29). Nende seas on vastajaid, kes on oma teadmiseid väga heaks hinnanud, võrreldes teiste vanusepruppidega samuti pisut vähem (6-7%). ' \
'Samas neid, kes on on teadmiseid väga heaks hinnanud, on vähe ka vanusegruppides 30-49 (10%) ja 64> (8%). ' \
'Kõige paremaks on oma teadmiseid hinnanud vanusegrupp 50-64.')

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

st.write('Vastajatest, kes hindavad oma teadmisi väga heaks, on 64% teadlikud uuest seadusest. ' \
'Kõigis enesehinnangu gruppides leidub 25-37% neid, kes on seadusest kuulnud, kuid ei ole täpsemalt kursis selle sisuga.')

st.write('Vastanute hulgas, kes hindavad oma teadmisi väga madalaks või pigem madalaks, on uuest seadusest teadlikke 53-63%. ' \
'Kusjuures, väga madalate enesehinnanguliste teadmistega vastajate hulgas on 0% seadusest teadlikke.')

st.write('**Vastajate hinnang teadmistele vs teadlikkus uuest seadusest**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Liida kategooriad "Olen teadlik" ja "Olen teadlik (ei ole tarbija mure)"
vahetabel = data_puhastatud.copy()
vahetabel['K11_teadlikkus'] = vahetabel['K11_teadlikkus'].replace(2, 4)

# Loo analüüsitav tabel
analyys_table = pd.crosstab(vahetabel['K8_teadmiste_hinnang'], vahetabel['K11_teadlikkus'])

# Hinnang enda teadmistele × teadlikkus seadusest
teadmised_teadlikkus = loo_risttabel(vahetabel, koodid, 'K8_teadmiste_hinnang', 'K11_teadlikkus', normalize=True)
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

# Teosta hii-ruut test
chi2, p_value, dof, expected_freq = chi2_contingency(analyys_table)

#st.write(f"Chi-square: {chi2:.4f}")
#st.write(f"P-value: {p_value:.4f}")

st.write(f'Enesehinnatud teadmiste ja teadlikkuse vahelise seose hindamiseks viidi läbi hi-ruuttest. Tulemused näitavad statistiliselt olulist seost - hii-ruut-statistiku väärtuseks on {chi2:.4f} (p={p_value:.4f}). ' \
'Vastajad, kes on hinnanud oma teadmiseid kõrgemaks olid teadlikumad uues seadusest, samas kui madalama teadmiste hinnanguga vastajad olid sagedamini teadmatud. ' \
'Ehk on olemas selge seos üldiste teadmiste ning seadusest teadlikkuse vahel.')

###################################################
# HINNANG PROBLEEMI TÕSIDUSELE                    #
###################################################
st.write('## Tekstiilijäätmete probleemi tõsiduse hinnang')
st.write('Seoses ületootmise ja kiirmoe ärimudeliga on tekstiilijäätmete probleem on kasvav kogu maailmas, sh Eestis. ' \
'Sellega seoses paluti tarbijatel hinnata tekstiilijäätmete probleemi tõsidust Eestis ja globaalses mastaabis.')

st.write('Üle poole ehk 58% vastanutest peab tekstiilijäätmete probleemi väga tõsiseks ja 23% peab probleemi pigem tõsiseks. ' \
'Neid, kes probleemi üldse ei tunnistanud, oli vastajate seas vaid 9 (1%).' \
'Vastuste vabas vormis tuuakse välja rohkelt kommentaare, märksõnadeks tarbimishullus, rohepesu, ületarbimine, kiirmood, ümbertöötluse võimaluste puudus, arutu tarbimine, naftast riided jne. ' \
'Mitmed vastanud leiavad, et kiirmood on peamine "süüdlane". Kommunikatsiooni antud teemal peetakse väga kehvaks.')

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

st.write('Enamuses vanusegruppides hinnatakse probleemi tõsiseks või pigem tõsiseks.' \
'Erandiks on vanusegrupp <18, kelle hulgas on vaid 21% neid, kes hindavad probleemi väga tõsiseks ning sama palju probleemi pigem tõsiseks hindajaid.' \
'Samas vanusegrupis on 20% vastanuid, kes ei tunnista probleemi üldse või peab seda väikeseks. ' \
'Probleemi tõsidust hindavad madalamaks ka vastajad vanusegrupis 64>.')

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
tab2.dataframe(probleem_vanus,
    column_config={'K3_vanus': ''}
)

st.write('Vastajatest, kes tunnetavad, et tekstiilijäätmete probleem Eestis ja globaalses mastaabis on väga tõsine või pigem tõsine, on 36-47% teadlikud kehtima hakanud seadusest. ' \
'Enamuses probleemi tõsiduse hinnangu gruppides on 22-36% neid, kes kes on seadusest küll kuulnud, kuid ei tea täpsemalt selle sisu.' \
'Seadusest ei ole teadlikud need vastajad, kes on probleemi tõsidust hinnanud olematuks või väikeseks - esimeses grupis on seadusest mitteteadlikke 67%, teises 78%.')

st.write('**Vastajate hinnang probleemi tõsidusele vs teadmised uuest seadusest**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

analyys_table = pd.crosstab(vahetabel['K9_probleemi_tosidus'], vahetabel['K11_teadlikkus'])

# Hinnang probleemi tõsidusele × teadlikkus seadusest
probleem_teadlikkus = loo_risttabel(vahetabel, koodid, 'K9_probleemi_tosidus', 'K11_teadlikkus', normalize=True)

# Loo heatmap
fig, ax = loo_heatmap(
    probleem_teadlikkus,
    title=''
)
tab1.pyplot(fig)
tab2.dataframe(probleem_teadlikkus,
    column_config={'K9_probleemi_tosidus': ''}
)

# Statistiline analüüs: korrelatsioon teadlikkuse ja enesehinnangu vahel

# Teosta hii-ruut test
chi2, p_value, dof, expected_freq = chi2_contingency(analyys_table)

#st.write(f"Chi-square: {chi2:.4f}")
#st.write(f"P-value: {p_value:.4f}")

st.write(f'Probleemi tõsiduse ja teadlikkuse vahelise seose hindamiseks viidi läbi hi-ruuttest. Tulemused näitavad statistiliselt olulist seost - hii-ruut-statistiku väärtuseks on {chi2:.4f} (p={p_value:.4f}). ' \
'Vastajad, kes on hinnanud probleemi tõsisemaks olid teadlikumad uuest seadusest, seadusest ei olnud teadlikud vastajad, kes hindasin probleemi olematuks või väikeseks. ' \
'Ehk on olemas selge seos probleemi hinnangulise tõsiduse ning seadusest teadlikkuse vahel.')

st.write('On selge, et probleem Eestis eksisteerib ja vastustest selgub, et ka inimesed tunnetavad probleemi väga selgelt. ' \
'Olgugi, et probleem on suur ning probleemi nähakse vastanute seas tõsisena, ei ole see muutnud tarbijate tarbimisharjumusi ja rõivaste ning tekstiilide tarbimine on kasvanud ja kasvamas.')

###################################################
# KOMMUNIKATSIOONI SELGUS                         #
###################################################
st.write('## KOV kommunikatsiooni selgus')

st.write('Üle poole vastanutest ehk 436 inimest (65%) pidas KOV-ide kommunikatsiooni seoses 2025. aasta alguses kehtima hakanud tekstiilide liigiti kogumise nõudega puudulikuks. ' \
'116 vastajat (17%) pidas kommunikatsiooni arusaamatuks ning 102 (15%) leidis, et kommunikatsioon on olnud Selge, kuid mittetäielik. ' \
'Kõigest 14 inimest ehk 2% vastajatest peab KOV-ide kommunikatsiooni väga selgeks.')

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

st.write('Kui vaadelda kommunikatsiooni selgust maakondade lõikes, siis kõige selgema kommunikatsiooniga jääb silma Pärnu maakond. ' \
'Pärnu maakonnas on kokku 33% neid vastajaid, kes on leidnud, et kommunikatsioon on olnud väga selge või selge, kuid mittetäielik. ' \
'Pärnu maakonnas oli uuringu kohaselt ka kõige rohkem vastajaid, kes olid uuest seadusest teadlikud. ' \
'Kommunikatsiooni puudulikuks pidanud vastajate hulk on Pärnu maakonnas 46%. Teistes maakondades jääb see vahemikku 54-74%.')

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

st.write('Vastustest tuleneb, et vastajatest, kes on hinnanud kommunikatsiooni väga selgeks, on 71% öelnud, et nad on teadlikus 2025. aastal kehtima hakanud nõudest. ' \
'Samas on nende hulgas, kes pidasid kommunikatsiooni väga selgeks, 21% neid vastajaid, kes ei ole uuest nõudest teadlikud. ' \
'Siiski on suurem hulk neid vastajaid, kes on hinnanud kommunikatsiooni puudulikuks või arusaamatuks ning kes ei ole üldse teadlikud uuest nõudest. ' \
'Vastajate grupis, kes pidas kommunikatsiooni puudulikuks, on mitteteadlikke 37% ja kommunikatsiooni arusaamatuks pidanud grupis 19%.')

st.write('**Kommunikatsiooni selgus vs teadlikkus uuest seadusest**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

analyys_table = pd.crosstab(vahetabel['K13_kommunikatsiooni_selgus'], vahetabel['K11_teadlikkus'])

# Hinnang kommunikatsioonile × teadlikkus seadusest
kommunikatsioon_teadlikkus = loo_risttabel(vahetabel, koodid, 'K13_kommunikatsiooni_selgus', 'K11_teadlikkus', normalize=True)

# Loo heatmap
fig, ax = loo_heatmap(
    kommunikatsioon_teadlikkus,
    title=''
)
tab1.pyplot(fig)
tab2.dataframe(kommunikatsioon_teadlikkus,
    column_config={'K13_kommunikatsiooni_selgus': ''}
)

# Statistiline analüüs: korrelatsioon teadlikkuse ja enesehinnangu vahel

# Teosta hii-ruut test
chi2, p_value, dof, expected_freq = chi2_contingency(analyys_table)

#st.write(f"Chi-square: {chi2:.4f}")
#st.write(f"P-value: {p_value:.4f}")

st.write(f'Kommunikatsiooni selguse ja teadlikkuse vahelise seose hindamiseks viidi läbi hi-ruuttest. Tulemused näitavad statistiliselt olulist seost - hii-ruut-statistiku väärtuseks on {chi2:.4f} (p={p_value:.4f}). ' \
'Vastajad, kes pidasid kommunikatsiooni väga selgeks olid teadlikumad uuest seadusest, seadusest ei olnud teadlikud vastajad, kes pidasid kommunikatsiooni puudulikuks. ' \
'Ehk on olemas selge seos kommunikatsiooni selguse ning seadusest teadlikkuse vahel.')

st.write('## Eelistatud teabeallikad')
st.write(':red[*To-be-done*]')

# Leia vastuste jaotus - teabe allikate eelistused
teabe_allikad = mitmikvastuse_sagedustabel(data, koodid, 'K32_teabe_allikad')

fig, ax = loo_hor_tulpdiagramm(
    teabe_allikad,
    '',
    style,
    sort=True   
)

st.pyplot(fig)

veerud = {
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

labelid = leia_sildi_mapping(koodid, 'K3_vanus')

teabeallikad = (
    data_puhastatud[['K3_vanus', *veerud]]
    .groupby('K3_vanus')
    .sum()
    .rename(columns=veerud)
    .T # transponeeri
)
st.dataframe(teabeallikad, column_config=labelid)

###################################################
# RIIKLIKE JUHISTE SELGUS                         #
###################################################
st.write('## Riiklike juhiste selgus')
st.write('Suur osa vastajatest (46%) ei ole riiklike juhistega kursis või ei oska nende selgust hinnata. ' \
'Vastajaid, kes peavad riiklikke juhiseid piisavalt selgeks, on kõigest 4%. ' \
'See viitab, et märkimisväärne osa inimestest ei ole juhistega kokku puutunud või ei tunne end juhiste järgimisel pädevana. ' \
'Juhiste täielik arusaadavus on pigem erand, mis võib viidata kommunikatsiooniprobleemidele või info vähesele kättesaadavusele.')

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

st.write('Kõige rohkem vastajaid, kes ei ole riiklike juhistega kursis, on Tartu maakonnas (57%), millele järgnevad Viljandi (52%) ja Harju (47%). ' \
'Selguse hinnangutes on kõige enam valitud vahepealset kategooriat „osaliselt arusaadav“. ' \
'Kõige rohkem on selle valiku teinud vastajaid Järva maakonnas (40%) ja Pärnu maakonnas (35%), mis viitab, et sealsetele vastajatele on juhised küll mõistetavad, kuid mitte täielikult selged. ' \
'Samas on „täiesti arusaadav“ hinnangu osakaal kõikides maakondades üsna madal, jäädes vahemikku 3-9%. ' \
'Negatiivsemate hinnangute osas („täiesti arusaamatu“ ja „osaliselt arusaamatu“) paistab silma Harju maakond, kus vastavalt 12% ja 19% vastajatest leiavad, et juhised on raskesti mõistetavad. ' \
'Ka väiksemates maakondades kategoorias „muu“ on „täiesti arusaamatu“ osakaal suhteliselt kõrge (14%).')

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

st.write('Kõige rohkem on vastajaid, kes hindavad kommunikatsiooni „puudulikuks“ ning ei ole kursis riiklike juhistega (57%). ' \
'Nende hulgas on neid, kes on pidanud riiklikke juheiseid täiesti arusaadavaks kõigest 1%. ' \
'Vastajate hulgas, kes on öelnud, et kommunikatsioon on “arusaamatu” või “selge, kuid mittetäielik”, on samuti palju vastajaid, kes ei ole riiklike juhistega kursis (21-29%) või kes peavad juhiseid vaid osaliselt arusaadavaks (33-34%) või osaliselt arusaamatuks (23-28%). ' \
'See kinnitab, et segane kommunikatsioon ei toeta juhiste mõistmist. ' \
'Siiski ei ole „väga selge“ kommunikatsiooni puhul juhiste täielik arusaadavus ülekaalus - „täiesti arusaadav“ vastuste osakaal on selles grupis. ' \
'„Ei tea“ vastuseid on väga selge kommunikatsiooni puhul vähem (15%) kui teiste kommunikatsiooni hinnangute puhul. ' \
'Samas on “väga selge” kommunikatsiooni puhul suur osakaal neid, kes peavad juhiseid osaliselt arusaamatuks (38%).')

st.write('Üldiselt võib öelda, et kommunikatsiooni selguse hinnang mõjutab ka juhiste mõistetavust. ' \
'Mida selgemaks peetakse kommunikatsiooni, seda enam kaldutakse andma juhistele positiivsemaid hinnanguid. ' \
'Samas ei pruugi hästi tajutud kommunikatsioon tagada juhiste sisulist selgust.')

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

# vahetabel = data_puhastatud[data_puhastatud['K28_riikliku_juhise_selgus'] != 5]
# spearman_corr, p_value = spearmanr(vahetabel['K13_kommunikatsiooni_selgus'], vahetabel['K28_riikliku_juhise_selgus'])