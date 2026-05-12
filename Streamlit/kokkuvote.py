import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# Asenda väheste vastajate arvuga maakonnad valikuga muu
data_puhastatud = data.copy()
data_puhastatud['K5_elukoht'] = data['K5_elukoht'].replace([2, 3, 5, 6, 7, 8, 10, 11, 13, 15], 16)

st.title('Kokkuvõte uuringust')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label='Uuringu algus',
        value='10.03.2025'
    )

with col2:
    st.metric(
        label='Uuringu lõpp',
        value='30.03.2025'
    )

with col3:
    st.metric(
        label='Uuringus osalejaid',
        value=668
    )

st.divider()

st.write('Uuring „Tarbijate hoiakud tekstiilide liigiti kogumisel rõivastest ja kodutekstiilidest loobumisel“ kaardistas Eesti tarbijate teadlikkust, hoiakuid ja käitumist seoses 2025. aastal jõustunud tekstiilijäätmete liigiti kogumise nõudega.')

st.write('Keskmine uuringus osaleja: ')
st.write('- 30-49-aastane (56%)')
st.write('- Harjumaa elanik (61%)')
st.write('- naine (88%)')
st.write('- peamine kodune keel: eesti (96%)')

st.write('Tulemused näitavad, et tarbijate keskkonnateadlikkus on üldiselt kõrge ning tekstiilijäätmete probleemi tajutakse tõsisena. 81% vastanutest peab tekstiilijäätmete probleemi Eestis ja maailmas tõsiseks või väga tõsiseks. ' \
'Samuti sorteerib enamik vastanutest oma jäätmeid aktiivselt ning 86% on valmis tekstiile eraldi sorteerima, kui süsteem on piisavalt selge ja mugav.')

st.write('Samas ilmnevad olulised kitsaskohad teadlikkuses ja süsteemi toimimises. Uuring näitab, et kuigi enamik vastajatest on 2025. aastal jõustunud tekstiilijäätmete liigiti kogumise nõudest vähemalt kuulnud, on tegelik teadlikkus seaduse sisust ja praktilisest rakendamisest madal. ' \
'Vaid 39% vastanutest pidas end seadusest teadlikuks, samas kui 61% kas ei olnud seadusega kursis või teadis sellest vaid pealiskaudselt.')

st.write('**Vastajate jaotus teadlikkuse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])
# Leia vastajate arv teadlikkuse alusel
teadlikkus = sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K11_teadlikkus'
).sort_values(by='protsent', ascending=False)

highlight_categories = [
    'Olen kuulnud',
    'Ei ole teadlik'
]

# Kuva tulpdiagramm
fig, ax = loo_hor_tulpdiagramm(
    df=teadlikkus,
    title='',
    style_config=style,
    sort=True
)

colors = ['#8B0000' if row['vastus_lyhike'] in highlight_categories else '#808080' 
          for _, row in teadlikkus.iterrows()]

for bar, color in zip(ax.patches, colors):
    bar.set_color(color)

tab1.pyplot(fig)
tab2.dataframe(teadlikkus,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

#plt.savefig('Documentation/teadlikkus_seadusest.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

st.write('Tulemused viitavad selgele kommunikatsioonilüngale, mida kinnitab ka asjaolu, et 82% vastanutest hindas KOV-ide kommunikatsiooni puudulikuks või arusaamatuks ning riiklike juhiste osas ei tunne end piisavalt informeerituna ligi pooled vastajad.')

st.write('**Vastajate jaotus kommunikatsiooni selguse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv kommunikatsiooni selguse alusel
kommunikatsiooni_selgus = sagedustabel(data_puhastatud, koodid, 'K13_kommunikatsiooni_selgus')

highlight_categories = [
    'Puudulik',
    'Arusaamatu'
]

# Kommunikatsiooni selguse jaotuse tulpdiagramm
fig, ax = loo_tulpdiagramm(
    kommunikatsiooni_selgus,
    '',
    style
)

colors = ['#8B0000' if row['vastus_lyhike'] in highlight_categories else '#808080' 
          for _, row in kommunikatsiooni_selgus.iterrows()]

for bar, color in zip(ax.patches, colors):
    bar.set_color(color)

tab1.pyplot(fig)
tab2.dataframe(kommunikatsiooni_selgus,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

#plt.savefig('Documentation/kommunikatsiooni_selgus.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

st.write('Tarbijate käitumine näitab samas tugevat valmisolekut ringmajanduslikeks lahendusteks. Kasutuskõlblikke tekstiile viiakse enim kogumiskastidesse, antakse edasi tuttavatele või müüakse edasi veebiplatvormidel. ' \
'Tarbijad väärtustavad rõivaste „uue elu“ võimalust, süsteemi läbipaistvust ning heategevuslikku mõju. '
'Samas puudub inimestel selgus kasutuskõlbmatute tekstiilide korrektse käitlemise osas. Enam kui pooled vastanutest viskavad sellised tekstiilid jätkuvalt segaolmejäätmetesse ning paljud viivad need ekslikult rõivakonteineritesse. ' \
'Tulemused viitavad vajadusele parandada nii riiklikku kui ka kohaliku tasandi kommunikatsiooni ning muuta juhised selgemaks.')

st.write('**Vastajate jaotus kasutuskõlbmatutest tekstiilidest loobumise viiside alusel**')
tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

kolbmatud = mitmikvastuse_sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K23_kasutuskolbmatud_tekstiilid'
).sort_values(by='protsent', ascending=False)

highlight_categories = [
    'Segaolmejäätmete konteiner',
    'Rõivakonteiner',
    'Põletamine (kodus)',
    'Matmine'
]

fig, ax = loo_hor_tulpdiagramm(
    df=kolbmatud,
    title='',
    style_config=style,
    sort=True   
)

colors = ['#8B0000' if row['vastus_lyhike'] in highlight_categories else '#808080' 
          for _, row in kolbmatud.iterrows()]

for bar, color in zip(ax.patches, colors):
    bar.set_color(color)

tab1.pyplot(fig)
tab2.dataframe(kolbmatud,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

#plt.savefig('Documentation/kasutuskolbmatud_tekstiilid.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

st.write('Uuring toob selgelt esile, et peamised takistused ei ole seotud inimeste motivatsioonipuudusega, vaid süsteemi kasutusmugavuse ja info puudumisega. Suurimateks väljakutseteks peetakse kogumispunktide ebamugavat asukohta, ebaselgeid juhiseid ning teadmatust, mida teha kasutuskõlbmatute tekstiilidega.')

st.write('**Vastajate jaotus peamiste väljakutsete lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv väljakutsete alusel
valjakutsed = mitmikvastuse_sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K22_peamised_valjakutsed'
).sort_values(by='protsent', ascending=False)

fig, ax = loo_hor_tulpdiagramm(
    df=valjakutsed,
    title='',
    style_config=style,
    sort=True   
)

for bar in ax.patches:
    bar.set_color('#808080')

tab1.pyplot(fig)
tab2.dataframe(valjakutsed,
    column_order=('vastus_lyhike', 'vastuste_arv', 'protsent_str'),
    column_config={
        'vastus_lyhike': st.column_config.TextColumn('Vastus'),
        'vastuste_arv': st.column_config.NumberColumn('Vastuste arv', width=20),
        'protsent_str': st.column_config.TextColumn('Protsent', alignment='right', width=20)
    },
    hide_index=True)

#plt.savefig('Documentation/valjakutsed.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

st.write('**Järeldused:**')
st.write('- Eestis on olemas tugev tarbijate valmisolek tekstiilide liigiti kogumiseks ja ringluseks.')
st.write('- Eduka süsteemi peamised eeldused on selged juhised, mugavalt ligipääsetavad kogumispunktid ja usaldusväärne kommunikatsioon.')
st.write('- Praegune kommunikatsioon ei anna tarbijatele piisavalt praktilist infot tekstiilide seisukorra hindamise ning käitlemise kohta.')
st.write('- Tarbijad eelistavad igapäevases liikumisteekonnas paiknevaid kogumispunkte ning ei pea jäätmejaamu esmaseks lahenduseks.')
st.write('- Nooremad vanusegrupid vajavad sihitud teadlikkuse tõstmist, eriti seoses ultrakiirmoe tarbimise ja tekstiilijäätmete mõjuga.')

st.write('**Soovitused:**')
st.write('- Tõsta nooremate vanusegruppide teadlikkust läbi suunatud teavitustegevuse.')
st.write('- Kommunikeerida senisest oluliselt selgemalt ning praktiliste näidete varal tekstiiljäätmete eraldi sorteerimise ning kogumise nõude sisu ning juhiseid selle rakendamiseks.')
st.write('- Viia läbi kampaaniaid, mis pakuvad osalejale motiveerivat tasu (nt sooduskupong) rõivaste ja tekstiilide ringlusse saatmisel.')
st.write('- Kogumissüsteemi loomisel võtta arvesse tarbijate vajadust kodulähedaste ja/või sagedasti külastatavates asukohtades asuvate kogumispunktide järele.')