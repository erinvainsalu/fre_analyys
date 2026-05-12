# Vajalike pakettide impordid ja seadistused
import sys
import os

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Impordi tabelite ja graafikute joonistamiseks vajalikud funktsioonid
from Python.visuaalide_abilised import maara_raporti_stiil
from Python.visuaalide_abilised import sagedustabel, mitmikvastuse_sagedustabel, loo_risttabel, loo_mitmikvastuse_risttabel
from Python.visuaalide_abilised import loo_hor_tulpdiagramm, loo_hor_stacked_tulpdiagramm, loo_heatmap

# Määra graafikute stiil
style = maara_raporti_stiil()

app_path = 'http://localhost:8502'
praegune_leht = 'eelistused'

# Sidebar linkidega
#st.sidebar.markdown(f'<a href="{app_path}/{praegune_leht}#olulised-tegurid-roivastest-loobumisel" target="_self">Loobumisel olulised tegurid</a>', unsafe_allow_html=True)
#st.sidebar.markdown(f'<a href="{app_path}/{praegune_leht}#eelistatud-kogumisviisid" target="_self">Eelistatud kogumisviisid</a>', unsafe_allow_html=True)
#st.sidebar.markdown(f'<a href="{app_path}/{praegune_leht}#valmisolek-esemete-eraldi-sorteerimiseks" target="_self">Valmisolek sorteerimiseks</a>', unsafe_allow_html=True)
#st.sidebar.markdown(f'<a href="{app_path}/{praegune_leht}#sorteerimist-julgustavad-tegurid" target="_self">Julgustavad tegurid</a>', unsafe_allow_html=True)

# Leia peakaust
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

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

st.write('Tarbijate eelistused ja valmisolek tekstiilide liigiti kogumiseks annavad ülevaate sellest, millised tegurid mõjutavad inimeste otsuseid rõivastest ja kodutekstiilidest loobumisel ning milliseid lahendusi peetakse kõige mugavamaks ja usaldusväärsemaks. ' \
'Tekstiilide kogumise ja sorteerimise kontekstis uuriti tarbijate eelistusi eelkõige valmisolekus tekstiile liigiti eraldada, kasutada erinevaid kogumislahendusi ning toetada süsteeme, mis tagavad esemetele võimalikult jätkusuutliku edasise kasutuse.')

###################################################
# LOOBUMISEL OLULINE                              #
###################################################
st.write('## Olulised tegurid rõivastest loobumisel')

st.write('Rõivastest loobumisel lähtuvad tarbijad erinevatest kaalutlustest. ' \
'Uuringus küsiti, mida vastajad peavad oluliseks kui nad oma rõivastest loobuvad. Vastajatel oli võimalik valida mitu vastusevarianti.')

st.write('Enamik vastanutest (76%) peab kõige olulisemaks, et rõivaesemele oleks tagatud uus elu. ' \
'Selle kõrval peetakse samuti oluliseks heategevuslikku eesmärki, mille valis 55% vastajatest. ' \
'Eelneva kahe valiku järel olid ühtmoodi populaarsed valikud "ese läheb re-disainimisele" (36%) ja "organisatsiooni läbipaistvus" (35%). ' \
'Kõige sagedamini märgiti korraga 2-3 olulist mõjutajat, mis näitab, et rõivastest loobumisel peetakse samaaegselt oluliseks mitut erinevat tegurit. ' \
'Kusjuures sagedamini valiti koos variante "rõivale on tagatud uus elu" ja "ese läheb re-disainimisele" ning "heategevuslik aspekt" ja "rõivale on tagatud uus elu".')

st.write('Ka küsimuse vabatekstilistest vastustest mainiti, et rõivaste annetamisel jälgitakse nende sihtkohta ning eelistatakse keskkonnahoidlikke lahendusi ja tootjavastutuse põhimõtete rakendamist. ' \
'Ehk oluliseks peetakse, mis kujul rõivas uue elu saab ning milline on selle edasine saatus.')

st.write('**Vastajate jaotus loobumisel oluliste tegurite lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv oluliste tegurite alusel
oluline_loobumisel = mitmikvastuse_sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K25_loobumisel_oluline'
).sort_values(by='protsent', ascending=False)

# Loo tulpdiagramm
fig, ax = loo_hor_tulpdiagramm(
    df=oluline_loobumisel,
    title='',
    style_config=style,
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
plt.close(fig)

st.write('### Probleemi tõsiduse tajumise mõju loobumisel olulistele teguritele')

st.write('Vastajad, kes on hinnanud, et tekstiilijäätmete probleem puudub või on väike, märkisid sagedamini, et neid ei huvita esemete edasine saatus (vastavalt 23% ja 26%). ' \
'Vastajate hulgas, kes ei tunnistanud probleemi olemasolu, oli teiste gruppidega võrreldes ka rohkem neid, kes soovisid rõivaste loobumisest saada isiklikku kasu (15%). ' \
'Samas näiteks need, kes hindavad probleemi väga tõsiseks, peavad rõivastest loobumisel teistest olulisemaks vastuvõtva organisatsiooni läbipaistvust (18%).')

st.write('**Probleemi tõsidus vs loobumisel olulised tegurid**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Probleemi tõsidus x loobumisel oluline
tosidus_oluline = loo_mitmikvastuse_risttabel(
    df_data=data_puhastatud,
    df_koodid=koodid,
    tunnus_single='K9_probleemi_tosidus', 
    tunnus_multiselect='K25_loobumisel_oluline', 
    normalize=True
)

# Loo heatmap
fig, ax = loo_heatmap(
    df=tosidus_oluline,
    title=''
)
tab1.pyplot(fig)
tab2.dataframe(
    #valjakutsed_kaitumine.style.background_gradient(axis=0, cmap='Blues', low=0, high=1.0).format(precision=0),
    tosidus_oluline.reindex(tosidus_oluline.index[::-1]),
    column_config={'K9_probleemi_tosidus': ''}
)
plt.close(fig)

###################################################
# SOBIV KOGUMISVIIS                               #
###################################################
st.write('## Eelistatud kogumisviisid')

st.write('Kogumisvõrgustiku loomiseks on oluline välja selgitada, millised on tarbijate poolt eelistatud kogumisviisid, võttes arvesse vastaja tänast elukorraldust ja -stiili. ' \
'Vastajatel paluti valida endale sobivaim viis rõivastest loobumiseks eeldusel, et kõik järgnevad valikud on võrdselt võimalikud, kättesaadavad ja tasuta.')

st.write('Valikvastustest joonistub välja, et nõuetekohane variant kasutuskõlbmatud tekstiilid jäätmejaama viia ei ole tarbijate esmane valik. Selle variandi valis vaid 10% vastajatest. ' \
'See viitab tõsisele lõhele hetkel pakutava ja tarbijate soovitud lahenduse vahel.')

st.write('Kõige populaarsemad on linnas paiknevad püsivad kogumispunktid, mida eelistas 39% vastajatest. Suur toetus (30%) oli ka kaubanduspindadel asuvatele kogumispunktidele. ' \
'Need kaks varianti kokku moodustavad 69% eelistustest, mis näitab, et eelistatakse kogumispunkte, mis on lihtsalt ligipääsetavad ning asuvad igapäevategevuste käigus tihti külastatavas asukohas. ' \
'Regulaarsed kogunädalad kodukandis said 12% toetust, mobiilsed ukselt-uksele kogumisautod 6% ja muud variandid 3%.')

st.write('**Vastajate jaotus eelistatud kogumisviiside lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv kogumisviiside eelistuse alusel
kogumisviisid = sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K29_sobiv_kogumisviis'
).sort_values(by='protsent', ascending=False)

# Kuva tulpdiagramm
fig, ax = loo_hor_tulpdiagramm(
    df=kogumisviisid,
    title='',
    style_config=style,
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

#plt.savefig('Documentation/kogumisviisi_eelistused.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

st.write('### Vanuselised erinevused eelistustes')

st.write('Vanuserühmade võrdlus paljastab olulisi erinevusi. Vanuserühmad 18-64 näitavad kõige suuremat huvi linnas paiknevate püsivate kogumispunktide vastu, ' \
'kusjuures vanusegrupis 18-29 oli see eelistus ülekaalukalt suurim (50%). Kõige vanem vanuserühm (64+) eristub selgelt, kuna eelistab oluliselt rohkem mobiilseid ukselt-uksele kogumisautosid (31%) võrreldes teiste vanuserühmadega, ' \
'kus see näitaja jääb 5-14% vahele. See viitab vanemaealiste suuremale vajadusele mugavuse ja ligipääsetavuse järele.')

st.write('**Eelistatud kogumisviisid vanuse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Kogumisviisid vanuse alusel
vanus_kogumisviis = loo_risttabel(
    df_data=data, 
    df_koodid=koodid, 
    tunnus_rida='K3_vanus', 
    tunnus_veerg='K29_sobiv_kogumisviis', 
    normalize=True
)

# Kuva tulpdiagramm
fig, ax = loo_hor_stacked_tulpdiagramm(
    df=vanus_kogumisviis,
    title='',
    style_config=style,
    sort=False
)
tab1.pyplot(fig)
tab2.dataframe(
    vanus_kogumisviis,
    column_config={'K3_vanus': ''}
)

#plt.savefig('Documentation/kogumisviis_vanus.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

st.write('### Sorteerimiskäitumise mõju eelistustele')

st.write('Inimesed, kes juba sorteerivad tekstiile rohkem kui viie kategooria järgi, eelistavad veidi enam linnas paiknevaid püsipunkte (37%) ja jäätmejaama (13%) võrreldes mitte-sorteerijatega. ' \
'See võib viidata, et aktiivsemad sorteerijad on valmis rohkem vaeva nägema. Seda kinnitab ka see, et mitte-sorteerijate hulgas on rohkem neid, kes eelistavad ukselt-ukselt kogumislahendust.')

st.write('**Eelistatud kogumisviisid sorteerimiskäitumise lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Sobiv kogumisviis sorteerimiskäitumise alusel
kaitumine_kogumisviis = loo_risttabel(
    df_data=data,
    df_koodid=koodid,
    tunnus_rida='K7_sorteerimiskaitumine',
    tunnus_veerg='K29_sobiv_kogumisviis',
    normalize=True
)

# Kuva tulpdiagramm
fig, ax = loo_hor_stacked_tulpdiagramm(
    df=kaitumine_kogumisviis,
    title='',
    style_config=style,
    sort=False
)

tab1.pyplot(fig)
tab2.dataframe(
    kaitumine_kogumisviis,
    column_config={'K7_sorteerimiskaitumine': ''}
)
plt.close(fig)

###################################################
# VALMISOLEK KATEGORISEERIMISEKS                  #
###################################################
st.write('## Valmisolek esemete eraldi sorteerimiseks')

st.write('Rõivaste edasise müügi ja ümbertöötluse edukus sõltub esmasest sorteerimisest ehk sellest, kas tarbija on valmis tekstiile enne loobumist sorteerima. ' \
'Seetõttu uuriti, kas vastajad oleksid valmis kasutama mitut erinevat konteinerit või kogumispunkti sõltuvalt eseme kategooriast (nt kasutuskõlblik, parandatav, kasutuskõlmatu). ' \
'86% vastajatest väljendas valmisolekut tekstiile sorteerida: 38% oleks valmis sorteerima juhul, kui juhised on selged, 25% kui kogumispunktid on mugavas asukohas, 23% on juba praegu valmis sorteerima ilma tingimusteta. ' \
'Vaid 10% märkis, et nad eelistavad ühe konteineri lahendust. 3% ei osanud enda eelistust välja tuua. Need tulemused viitavad, et suurem osa takistustest ei ole tarbijate motivatsioonis, vaid pigem süsteemi mugavuses ja selguses.')

st.write('**Vastajate jaotus valmisoleku lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv valmisoleku alusel
valmisolek = sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K30_valmisolek_kategoriseerimiseks'
).sort_values(by='protsent', ascending=False)

# Kuva tulpdiagramm
fig, ax = loo_hor_tulpdiagramm(
    df=valmisolek,
    title='',
    style_config=style,
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

#plt.savefig('Documentation/valmisolek.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

st.write('### Sorteerimiskäitumise mõju valmisolekule')

st.write('Kõige kõrgem valmisolek sorteerida ilma tingimusteta on nende vastajate seas, kes sorteerivad jäätmeid enam kui viide kategooriasse või järgivad nullkulu eluviisi. ' \
'Vähematesse kategooriatesse sorteerijate seas muutuvad tingimused olulisemaks. Näiteks 3-5 kategoorias sorteerijatest 41%-le on oluline, et juhised oleksid selged ja '
'<3 kategoorias sorteerijatest 36% sorteeriks tekstiile eraldi siis, kui kogumispunktid on mugavas asukohas. ')

st.write('Ka mittesorteerijate hulgas sõltub valmisolek peamiselt mugavusest ja selgusest - võrdselt 27% tõi välja vajaduse selgete juhiste ja mugavate kogumispunktide järele. ' \
'Samas oli mittesorteerijate hulgas ka 27% neid, kes ei ole nõus tekstiile sorteerima ning eelistavad hoopis ühte universaalset konteinerit. ' \
'Sellest saab järeldada, et keskkonnateadlikumad tarbijad on valmis uusi jätkusuutlikke lahendusi kiiremini omaks võtma.')

st.write('**Valmisolek sorteerimiskäitumise lõikes**')

# Eemalda sorteerimiskäitumine, kus valikuks Null-kulu eluviis, muu
sorteerimine_puhas = data_puhastatud[data_puhastatud['K7_sorteerimiskaitumine'].isin([1, 2, 3, 4])]

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Valmisolek sorteerimiskäitumise alusel
valmisolek_kaitumine = loo_risttabel(
    df_data=sorteerimine_puhas,
    df_koodid=koodid, 
    tunnus_rida='K7_sorteerimiskaitumine', 
    tunnus_veerg='K30_valmisolek_kategoriseerimiseks', 
    normalize=True
)

# Kuva tulpdiagramm
fig, ax = loo_hor_stacked_tulpdiagramm(
    df=valmisolek_kaitumine,
    title='',
    style_config=style
)
tab1.pyplot(fig)
tab2.dataframe(valmisolek_kaitumine,
    column_config={'K7_sorteerimiskaitumine': ''}
)

#plt.savefig('Documentation/sorteerimine_valmisolek.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

st.write('### Probleemi tajumise mõju valmisolekule')

st.write('Selge juhise vajadus on ühtlaselt kõrge kõigis probleemi tõsiduse tajumise gruppides (22-43%). Isegi probleemi mittetajujate seas eelistab 33% vastajatest selget juhendit. ' \
'Ilma lisatingimusteta sorteerijate osakaal on nende seas, kes probleemi tõsiseks või väga tõsiseks peavad, suurem kui probleemi tõsidust madalamalt hindavate gruppide seas. ' \
'Probleemi pigem tõsiseks või väga tõsiseks hindajate seas on nende osakaal 21-27%, probleemi väikeseks või üldse puuduvaks hindajate seas 11-13%.')
st.write('Ühe konteineri eelistajate trend on samas vastupidine. See valik on oluliselt populaarsem nende hulgas, kes peavad probleemi keskmiseks või madalamaks (22-23%) ning kaob peaaegu täielikult nende hulgas, kes peavad probleemi väga tõsiseks (5%). ' \
'Ka nende vastajate hulk, kes ei oska enda eelistust sorteerimise osas välja tuua, on probleemi mittetajujate hulgas oluliselt suurem kui probleemi tõsiseks hindajate hulgas - vastavalt 22% ja 1%.')

st.write('**Valmisolek probleemi tõsiduse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Valmisolek probleemi tõsiduse alusel
valmisolek_kaitumine = loo_risttabel(
    df_data=data_puhastatud,
    df_koodid=koodid, 
    tunnus_rida='K9_probleemi_tosidus', 
    tunnus_veerg='K30_valmisolek_kategoriseerimiseks', 
    normalize=True
)

# Kuva tulpdiagramm
fig, ax = loo_hor_stacked_tulpdiagramm(
    df=valmisolek_kaitumine,
    title='',
    style_config=style
)
tab1.pyplot(fig)
tab2.dataframe(valmisolek_kaitumine,
    column_config={'K9_probleemi_tosidus': ''}
)
plt.close(fig)

###################################################
# JULGUSTAVAD TEGURID                             #
###################################################
st.write('## Sorteerimist julgustavad tegurid')

st.write('Mõistmaks paremini vastajate soove tekstiilide kogumiseks ja ringluse korraldamiseks, uuriti, millised tegurid julgustaksid inimesi tekstiile sorteerima hetkest, mil neist loobutakse. Vastajatel oli võimalik valida mitu vastusevarianti.')

st.write('Sorteerimist julgustavate tegurite seas domineerivad kaks aspekti: kogumispunktide lähedus elukohale ja ligipääsetavus (76% vastajatest) ning selged juhised (71%). ' \
'Need kaks tegurit on märgatavalt olulisemad kui teised. Neile järgnevad võimalus teha head (48%), teave keskkonnamõjude kohta (38%) ja soodustused/allahindlused 21%. ' \
'Vaid 14% peab oluliseks ukselt-uksele kogumise meetodit, mis on kooskõlas ka kogumisviiside eelistustega. Kõige sagedamini märgiti korraga 2-3 olulist mõjutajat, mis näitab, et ühe inimese puhul on julgustavaid tegureid pigem mitu. ' \
'Kusjuures sagedamini valiti koos variante “võimalus teha head" ja “teave keskkonnamõjude kohta", mis viitab selle, et tarbijad soovivad teada, et nende kogutud tekstiil jõuab õigesse kohta ning sellest sünnib tegelik kasu.')

st.write('Küsimuse vabatekstilistes täpsustustes rõhutati mitmel korral vajadust usaldusväärse ja läbipaistva süsteemi järele. ' \
'Need tulemused näitavad, et eduka kogumissüsteemi alustalad on praktiline ligipääsetavus, kommunikatsiooni selgus ning arusaadav süsteem, mitte niivõrd majanduslikud stiimulid või ukselt-uksele teenused.')

st.write('**Vastajate jaotus julgustavate tegurite lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv väljakutsete alusel
tegurid = mitmikvastuse_sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K33_julgustavad_tegurid'
).sort_values(by='protsent', ascending=False)

# Kuva tulpdiagramm
fig, ax = loo_hor_tulpdiagramm(
    df=tegurid,
    title='',
    style_config=style,
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
plt.close(fig)