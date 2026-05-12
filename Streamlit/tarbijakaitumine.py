import sys
import os

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2_contingency

# Leia peakaust
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Impordi tabelite ja graafikute joonistamiseks vajalikud funktsioonid
from Python.visuaalide_abilised import maara_raporti_stiil
from Python.visuaalide_abilised import sagedustabel, mitmikvastuse_sagedustabel, loo_risttabel, loo_mitmikvastuse_risttabel
from Python.visuaalide_abilised import loo_tulpdiagramm, loo_hor_tulpdiagramm, loo_hor_stacked_tulpdiagramm, loo_heatmap

# Määra graafikute stiil
style = maara_raporti_stiil()

app_path = 'http://localhost:8501'
praegune_leht = 'tarbijakaitumine'

# Sidebar linkidega
#st.sidebar.markdown(f'<a href="{app_path}/{praegune_leht}#taenane-sorteerimiskaeitumine" target="_self">Tänane sorteerimiskäitumine</a>', unsafe_allow_html=True)
#st.sidebar.markdown(f'<a href="{app_path}/{praegune_leht}#peamised-vaeljakutsed-sorteerimisel" target="_self">Peamised väljakutsed</a>', unsafe_allow_html=True)
#st.sidebar.markdown(f'<a href="{app_path}/{praegune_leht}#loobutud-tekstiilide-kogus-uehes-kalendriaastas" target="_self">Loobutud tekstiilide kogused</a>', unsafe_allow_html=True)
#st.sidebar.markdown(f'<a href="{app_path}/{praegune_leht}#toimimine-mittevajalike-roivaste-ja-tekstiilidega" target="_self">Mittevajalike tekstiilidega toimimine</a>', unsafe_allow_html=True)
#st.sidebar.markdown(f'<a href="{app_path}/{praegune_leht}#loobumise-pohjused" target="_self">Loobumise põhjused</a>', unsafe_allow_html=True)
#st.sidebar.markdown(f'<a href="{app_path}/{praegune_leht}#kasutuskolbmatutest-tekstiilidest-loobumise-viisid" target="_self">Kasutuskõlbmatutest tekstiilidest loobumine</a>', unsafe_allow_html=True)
#st.sidebar.markdown(f'<a href="{app_path}/{praegune_leht}#ultrakiirmoe-ostmise-harjumused" target="_self">Ultrakiirmoe ostuharjumused</a>', unsafe_allow_html=True)
#st.sidebar.markdown(f'<a href="{app_path}/{praegune_leht}#uute-roivaste-ostmissagedus" target="_self">Uute rõivaste ostmissagedus</a>', unsafe_allow_html=True)

# Impordi andmed puhastamise käigus loodud CVS-st
data = pd.read_csv('data/cleaned_data.csv')

# Impordi vastuste koodid
koodid = pd.read_csv('data/vastuste_koodid.csv')

# Asenda väheste vastajate arvuga maakonnad valikuga muu
data_puhastatud = data.copy()
data_puhastatud['K5_elukoht'] = data['K5_elukoht'].replace([2, 3, 5, 6, 7, 8, 10, 11, 13, 15], 16)

st.title('Tänane tarbijakäitumine')

st.write('Oluline on mõista lähemalt tarbijate tänast tekstiilidega seotud käitumisharjumust. Uuringus püüti välja selgitada, mida teeb tarbija täna oma tekstiilidega, mis enam kasutust ei leia ning millised on peamised põhjused esemetest loobumisel.')

###################################################
# SORTEERIMISKÄITUMINE                            #
###################################################
st.write('## Tänane sorteerimiskäitumine')

st.write('Uue regulatsiooni kohaselt tuleb tekstiilijäätmeid koguda olmeprügist eraldi. Seetõttu on oluline, et tarbijad mõistaksid tekstiilide liigiti sorteerimise põhimõtteid ning tekstiilide muudest jäätmetest eraldamise vajalikkust. ' \
'Seetõttu uuriti vastanute harjumusi koduses majapidamises jäätmeid sorteerida.')

st.write('Uuring näitab, et vastajad sorteerivad jäätmeid üsna aktiivselt. Enamus vastanutest (63%) sorteerib jäätmeid 3-5 erinevas kategoorias ja viiendik (20%) sorteerib üle 5 kategoorias. ' \
'Vaid 4% vastanutest ei sorteeri jäätmeid üldse, mis on liiga väike grupp, et sellest täiendavaid järeldusi teha.')

st.write('**Vastajate jaotus sorteerimiskäitumise lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])

# Leia vastajate arv teadlikkuse alusel
sorteerimiskaitumine = sagedustabel(
    df_data=data_puhastatud,
    df_koodid=koodid,
    tunnus='K7_sorteerimiskaitumine'
)

# Kuva tulpdiagramm
fig, ax = loo_tulpdiagramm(
    df=sorteerimiskaitumine,
    title='',
    style_config=style
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

#plt.savefig('Documentation/sorteerimiskaitumine.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

st.write('Kuna null-kulu eluviisi harrastab vaid 1 vastanu ja ka "muu" vastajaid oli kõigest 1%, siis järgnevalt neid kahte kategeooriat süviti ei analüüsita.')

st.write('### Vanuselised erinevused sorteerimiskäitumises')

st.write('Vanusegruppide võrdlus paljastab selged erinevused sorteerimisaktiivsuses. Keskealised (30-64 aastat) sorteerivad kõige intensiivsemalt: 64-71% neist sorteerib jäätmeid 3-5 kategoorias ja 22-26% enamas kui viies kategoorias. ' \
'Nooremad (alla 18 ja 18-29) näitavad madalamat aktiivsust. Üle 64-aastased sorteerivad samuti aktiivselt (77% sorteerib 3-5 kategoorias), kuid nende hulgas on vähem intensiivseid sorteerijaid, vaid 8% sorteerib rohkemas kui viies kategoorias.')

st.write('**Sorteerimiskäitumine vanusegruppide lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Eemalda sorteerimiskäitumine, kus valikuks Null-kulu eluviis, muu
sorteerimine_puhas = data_puhastatud[data_puhastatud['K7_sorteerimiskaitumine'].isin([1, 2, 3, 4])]

# Käitumine vanuse alusel
kaitumine_vanus = loo_risttabel(
    df_data=sorteerimine_puhas, 
    df_koodid=koodid, 
    tunnus_rida='K3_vanus', 
    tunnus_veerg='K7_sorteerimiskaitumine', 
    normalize=True
)

# Kuva tulpdiagramm
fig, ax = loo_hor_stacked_tulpdiagramm(
    df=kaitumine_vanus,
    title='',
    style_config=style
)
tab1.pyplot(fig)
tab2.dataframe(kaitumine_vanus,
    column_config={'K3_vanus': ''}
)

#plt.savefig('Documentation/sorteerimiskaitumine_vanus.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

st.write('### Erinevused sorteerimiskäitumises maakondade vaates')
st.write('Sorteerimiskäitumises esinevad ka mõned regionaalsed erinevused. Kõige aktiivsemad sorteerijad on Harju, Pärnu ja Tartu maakondades, kus on 3-5 kateoorias sorteerijaid 63-64% ning rohkemas kui viies kategoorias sorteerijaid 20-25%. ' \
'Järva maakond eristub teistest - seal on suurem osakaal neid, kes sorteerivad vähem kui 3 kategoorias või ei sorteeri üldse (kokku 27%). Need erinevused võivad peegeldada infrastruktuuri kättesaadavust või kohalikku teadlikkuse taset.')

st.write('**Sorteerimiskäitumine maakondade lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Käitumine elukoha alusel
kaitumine_elukoht = loo_risttabel(
    df_data=sorteerimine_puhas, 
    df_koodid=koodid, 
    tunnus_rida='K5_elukoht', 
    tunnus_veerg='K7_sorteerimiskaitumine', 
    normalize=True
)

# Kuva tulpdiagramm
fig, ax = loo_hor_stacked_tulpdiagramm(
    df=kaitumine_elukoht,
    title='',
    style_config=style
)
tab1.pyplot(fig)
tab2.dataframe(kaitumine_elukoht,
    column_config={'K5_elukoht': ''}
)
plt.close(fig)

st.write('### Teadmiste hinnangu mõju sorteerimiskäitumisele')

st.write('Teadmiste taseme ja sorteerimiskäitumise vahel on selge seos. Nende hulgas, kes hindavad oma teadmisi väga madalaks, on mittesorteerijaid 26%, samas kui pigem heade või väga heade teadmiste juures on mittesorteerijaid vaid 1-2%. ' \
'Sama trend on ka nende vastajate puhul, kes sorteerivad jäätmeid vähem kui 3 kategooriasse: väga madala või pigem madala teadmiste hinnangu puhul on neid vastajaid 26-27%, samas kui "pigem hea" ja "väga hea" teadmistega vastajate puhul 8-9%. ' \
'Kolmes ja enamas kategoorias sorteerijate osakaal on pigem heade või väga heade teadmistega vastajate puhul 90%. Kusjuures, isegi need, kes hindavad end "keskmiseks", sorteerivad aktiivselt (84% sorteerib kolmes või enamas kategoorias), ' \
'mis näitab, et teadlikkuse tõstmine võib otseselt mõjutada sorteerimiskäitumist.')

st.write('**Hinnang teadmistele vs sorteerimiskäitumine**')
tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])
# Hinnang enda teadmistele × sorteerimiskäitumine
teadmised_sorteerimine = loo_risttabel(
    df_data=sorteerimine_puhas, 
    df_koodid=koodid, 
    tunnus_rida='K8_teadmiste_hinnang', 
    tunnus_veerg='K7_sorteerimiskaitumine', 
    normalize=True
)

# Loo heatmap
fig, ax = loo_heatmap(
    df=teadmised_sorteerimine,
    title=''
)
tab1.pyplot(fig)
tab2.dataframe(teadmised_sorteerimine.reindex(teadmised_sorteerimine.index[::-1]),
    column_config={'K8_teadmiste_hinnang': ''}
)
plt.close(fig)

analyys_table = pd.crosstab(data_puhastatud['K8_teadmiste_hinnang'], data_puhastatud['K7_sorteerimiskaitumine'])

# Teosta hii-ruut test
chi2, p_value, dof, expected_freq = chi2_contingency(analyys_table)

# Calculate Cramér's V (effect size)
#n = analyys_table.sum().sum()
#min_dim = min(analyys_table.shape) - 1
#cramers_v = np.sqrt(chi2 / (n * min_dim))

#st.write(f"Chi-square: {chi2:.4f}")
#st.write(f"P-value: {p_value:.4f}")
#st.write(f"Cramér's V: {cramers_v:.4f}")

st.write(f'Teadmiste hinnangu ja sorteerimiskäitumise vahelise seose hindamiseks viidi läbi hi-ruuttest. Tulemused näitavad statistiliselt olulist seost - hii-ruut-statistiku väärtuseks on {chi2:.4f} (p={p_value:.4f}). ' \
'See ei ole juhus, et vastajad, kes hindasin oma teadmiseid paremaks olid usinamad sorteerijad ning vähem sorteerisid need vastajad, kes hindasid oma teadmiseid madalamaks. ' \
'Ehk on olemas selge seos enesehinnanguliste teadmiste ning sorteerimiskäitumise vahel.')

st.write('### Probleemi tõsiduse taju mõju sorteerimiskäitumisele')

st.write('Nende hulgas, kes peavad jäätmeprobleemi tõsiseks või väga tõsiseks, on kõrgeim sorteerimisaktiivsus. Hinnangu "väga tõsine" andnutest sorteerib 27% rohkemas kui viies kategoorias ja 62% sorteerib jäätmeid 3-5 kategoorias. ' \
'3-5 kategoorias sorteerijate hulgas on suur osakaal ka neid, kes on hinnanud probleemi kas väikeseks, keskmiseks või pigem tõsiseks. Samas, nende hulgas, kes probleemi olemasolu üldse ei taju, ei ole ühtki rohkemas kui viies kategoorias sorteerijat. ' \
'Samal ajal on nende hulgas tervelt 56% mittesorteerijaid.')

st.write('**Hinnang probleemi tõsidusele vs sorteerimiskäitumine**')
tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])
# Probleemi tõsidus × sorteerimiskäitumine
tosidus_sorteerimine = loo_risttabel(
    df_data=sorteerimine_puhas, 
    df_koodid=koodid, 
    tunnus_rida='K9_probleemi_tosidus', 
    tunnus_veerg='K7_sorteerimiskaitumine', 
    normalize=True
)

# Loo heatmap
fig, ax = loo_heatmap(
    df=tosidus_sorteerimine,
    title=''
)
tab1.pyplot(fig)
tab2.dataframe(tosidus_sorteerimine.reindex(tosidus_sorteerimine.index[::-1]),
    column_config={'K9_probleemi_tosidus': ''}
)
plt.close(fig)

analyys_table = pd.crosstab(data_puhastatud['K9_probleemi_tosidus'], data_puhastatud['K7_sorteerimiskaitumine'])

# Teosta hii-ruut test
chi2, p_value, dof, expected_freq = chi2_contingency(analyys_table)

# Calculate Cramér's V (effect size)
#n = analyys_table.sum().sum()
#min_dim = min(analyys_table.shape) - 1
#cramers_v = np.sqrt(chi2 / (n * min_dim))

#st.write(f"Chi-square: {chi2:.4f}")
#st.write(f"P-value: {p_value:.4f}")
#st.write(f"Cramér's V: {cramers_v:.4f}")

st.write(f'Probleemi tõsiduse taju ja sorteerimiskäitumise vahelise seose hindamiseks viidi läbi hi-ruuttest. Tulemused näitavad statistiliselt olulist seost - hii-ruut-statistiku väärtuseks on {chi2:.4f} (p={p_value:.4f}). ' \
'See ei ole juhus, et vastajad, kes hindasin probleemi tõsisemaks olid usinamad sorteerijad ning vähem sorteerisid need vastajad, kes hindasid probleemi tõsidust väiksemaks. ' \
'Ehk on olemas selge seos probleemi tõsiduse taju ning sorteerimiskäitumise vahel.')

###################################################
# PEAMISED VÄLJAKUTSED                            #
###################################################
st.write('## Peamised väljakutsed sorteerimisel')

st.write('Väljakutsed indiviidi tasandil tekstiilide sorteerimisel on erinevad, kuid on oluline mõista põhjuseid, et parandada tekstiilide liigiti kogumist. ' \
'Seetõttu uuriti vastajatelt millised on nende peamised väljakutsed rõivaste ja tekstiilide sorteerimisel. Vastajal oli võimalik valida mitu vastusevarianti ning vajadusel märkida muu ning seda valikut selgitada. ' \
'Kõige sagedamini valiti korraga 1-2 takistust.')

st.write('Kõige suuremaks väljakutseks (46%) peavad vastajad kogumiskohtade puudumist mugavas asukohas. Sellele järgnes moraalne side, mis teeb loobumise keerukaks (35%). ' \
'Valiti ka ajapuudust (32%) ning transpordi keerukust (24%). Kusjuures tõenäoliselt võivad nii ajapuudus kui ka keerukas tranport olla seotud kogumispunktide ebamugava asukohaga. ' \
'Lisakas toodi välja ebakindlust tekstiilide seisukorra hindmisel (26%) ning keerukaid sorteerimisjuhendeid (18%).')

st.write('Vabatekstilistes vastustes mainiti sageli, et puudub teadmine, mida teha rõivastega, millel on küll palju kõlblikku materjali, kuid mida enam kanda ei saa - näiteks kulunud jalgevahega teksadega. ' \
'Samuti tõid vastajad välja murekohana, et täis riidekonteinerid takistavad asjade äraandmist ning nenditi, et teadmatus esemete saatuse üle on ebakindlust tekitav. ' \
'Enim aga toodi välja, et puudub konkreetne koht, kuhu viia kulunud, määrdunud ja kasutuskõlbmatud rõivad ja tekstiilid. ')

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

st.write('### Vanuselised erinevused peamiste väljakutsete osas')

st.write('Noorematel (alla 18 ja 18-29) on suurimaks väljakutseks ajapuudus (vastavalt 32% ja 20%), samas kui vanusegruppides 30-49 ja 50-64 peetakse suuremaks probleemiks kogumiskohtade puudumist mugavas asukohas (25-27%). ' \
'Transpordikeerukust on kõige rohkem välja toodud vanusegruppides 50-64 (23%) ja >64 (27%). Ka sorteerimisjuhiste keerukust peetakse vanemaealiste seas suuremaks probleemiks. ' \
'Samas näiteks esemete seisukorra hindamise ebakindlus on läbivaks väljakutseks kõigis vanusegruppides.')

st.write('**Peamised väljakutsed vanuse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Kogumisviisid vanuse alusel
vanus_valjakutse = loo_mitmikvastuse_risttabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus_single='K3_vanus', 
    tunnus_multiselect='K22_peamised_valjakutsed', 
    normalize=True
)

# Kuva tulpdiagramm
fig, ax = loo_hor_stacked_tulpdiagramm(
    df=vanus_valjakutse,
    title='',
    style_config=style,
    sort=False
)
tab1.pyplot(fig)
tab2.dataframe(
    vanus_valjakutse,
    column_config={'K3_vanus': ''}
)
plt.close(fig)

##################################
# Uuri vastusevariante

#valjakutsed_veerud = [
#    col for col in data.columns 
#    if col.startswith('K22_peamised_valjakutsed') 
#    and not col.endswith('_muu_tekst')  # Välista tekstvastustega veerud
#]

#st.write('Tunnuste koos esinemise sagedus:')
# Kui sageli mingid valikud koos esinevad?
#fig, ax = plt.subplots()
#corr_matrix = data[valjakutsed_veerud].corr()
# Loo heatmap
#sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
#st.pyplot(fig)

# Leia 10 kõige tugevama korrelatsiooniga tunnust
# Set diagonal to NaN (ignore self-correlation)
#import numpy as np
#corr_no_diag = corr_matrix.where(~np.eye(len(corr_matrix), dtype=bool))

# 3. Get top correlations
#corr_pairs = corr_no_diag.unstack().sort_values(ascending=False)
#st.write('Tugevaimad korrelatsioonid:')
#st.write(corr_pairs[corr_pairs < 1.0].head(10))  # Top 10 pairs

# Kui mitu väljakutset iga inimene korraga valis?
#test = data.copy()
#kokku = test[valjakutsed_veerud].sum(axis=1)
#st.write(kokku.value_counts())

###################################################
# TEKSTIILIDE KOGUS                               #
###################################################
st.write('## Loobutud tekstiilide kogus ühes kalendriaastas')

st.write('Uuringust selgub, et enamus vastajaid loobub aastas kuni 5 kg (44%) või kuni 10 kg (23%) tekstiilidest. Väike osa (16%) loobub alla 1 kg aastas. 8% valis, et nad loobuvad kuni 15 kg ja 3% loobub üle 15 kg tekstiilidest aastas.')

st.write('Küsimuse vabatekstilisest väljast ilmneb, et vastanutel on olnud keeruline määrata tekstiilide kogust kilogrammides. Selgub, et vastanud (ja laiem tarbijaskond) ei oska sageli rõivaste hulka seostada kaalunumbri väärtusega. ' \
'Tihti inimesed ka unustavad võrdlemisi ruttu, millest ja millal nad on loobunud. Seega tuleb nende tulemuste puhul arvestada suhteliselt suure oletuslikkusega. ' \
'Arvestades, et keskmine loobutud tekstiilide kogus keskmise eestlase kohta on 17kg, siis võib oletada, et uuringule vastajad pigem alahindasid oma loobutud tekstiilide koguseid.')

st.write('**Vastajate jaotus loobutud tekstiilide koguse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])
# Leia vastajate arv teadlikkuse alusel
loobutud_tekstiilid = sagedustabel(
    df_data=data_puhastatud,
    df_koodid=koodid,
    tunnus='K14_tekstiilide_kogus'
)

# Kuva tulpdiagramm
fig, ax = loo_tulpdiagramm(
    df=loobutud_tekstiilid,
    title='',
    style_config=style
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
plt.close(fig)

###################################################
# MITTEVAJALIKUD TEKSTIILID                       #
###################################################
st.write('## Toimimine mittevajalike rõivaste ja tekstiilidega')

st.write('Mõistmaks, kuidas tarbija käitub kasutuskõlbulike rõivaste ja kodutekstiilidega, mida ta enam ei vaja, küsiti uuringus osalejatelt valikvastuste ja vabas vormis vastuse esitamise võimalusega mida vastajad selliste tekstiilidega ette võtavad. ' \
'Kõige sagedamini valiti korraga 3-4 põhjust, mis näitab, et korraga esineb mitu moodust kasutuskõlbulikest tekstiilidest loobumisel ja inimesed ei eelista ühte konkreetset viisi.')

st.write('Enamus vastanutest (82%) viib kasutuskõlblikud tekstiilid avalikesse kogumiskastidesse ja 72% annab need edasi perele või tuttavatele. ' \
'Veebis teisel ringil müümine (51%) ja ise tuunimine ning ümber tegemine (32%) on samuti levinud, mis näitab mitmekesiseid loobumisviise ja keskkonnateadlikku lähenemist. ' \
'Viimasele viitab ka see, et kõige sagedamini valiti koos vastusevariante: “müün veebis”, “annan perele/tuttavatele” ja “teen ise ümber”.')

st.write('Samas on 36% vastajatest toonud välja, et nad viskavad kasutuskõlbulikud tekstiilid segaolmejäätmetesse. ' \
'Vabatekstilistest vastustest tuleb välja, et sageli on tegemist katkiste ning määrdunud asjadega ehk tegelikult kasutuskõlbmatute rõivaste ja tekstiilidega. ' \
'Nenditi, et kuigi linnapildis on nähtud ja teatakse kantavate ja korralike riiete ning tekstiilide kogumispunkte, siis ei teata kuhu viia kasutuskõlbmatuid asju. ' \
'Ära visatavate esemetena toodi kõige enam välja just sokke ning aluspesu. Ehk vastustest tuleb välja, et olmeprügisse visatakse esemeid parema lahenduse või info puudumise tõttu. ' \
'Tuntakse muret ning huvi, mida teha just mainitud aluspesu ning sokkidega, mis liigituvad tekstiilijäätmeks, aga ei saa liikuda edasi teisele ringile oma esialgsel kujul. ' \
'See annab tugeva indikatsiooni parandada riigi ja KOV-ide kommunikatsiooni seoses tekstiilijäätmete sorteerimisega.')

st.write('**Käitumine mittevajalikest tekstiilidest loobumisel**')
tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

mittevajalikud_tekstiilid = mitmikvastuse_sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K15_mittevajalikud_tekstiilid'
).sort_values(by='protsent', ascending=False)

fig, ax = loo_hor_tulpdiagramm(
    df=mittevajalikud_tekstiilid,
    title='',
    style_config=style,
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

#plt.savefig('Documentation/kasutuskolblikud_tekstiilid.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

#abitabel = data[data['K15_mittevajalikud_tekstiilid_5'] == 1]

# Probleemi tõsidus x loobumisel oluline
#valjakutsed_loobumine = loo_mitmikvastuse_risttabel(
#    df_data=abitabel,
#    df_koodid=koodid,
#    tunnus_single='K15_mittevajalikud_tekstiilid_5', 
#    tunnus_multiselect='K22_peamised_valjakutsed', 
#    normalize=True
#)

#test = loo_risttabel(
#    df_data=abitabel,
#    df_koodid=koodid,
#    tunnus_rida='K15_mittevajalikud_tekstiilid_5', 
#    tunnus_veerg='K9_probleemi_tosidus' 
#    #normalize=True
#)
#test

###################################################
# LOOBUMISE PÕHJUSED                              #
###################################################
st.write('## Loobumise põhjused')

st.write('Rõivastest ja kodutekstiilidest loobumiseks on oluliselt rohkem põhjuseid kui lihtsalt “läks katki”. Uuringus oli vastajatele antud võimalus valida mitu erinevat vastust ning soovi korral lisada vabatekstiline täiendus muu põhjendusega. ' \
'Kõige sagedamini valiti korraga 2-3 põhjust, ehk ka see näitab, et loobumise põhjuseid on alati mitmeid.')

st.write('Peamised loobumise põhjused on selged: 70% loobub põhjusel, et ese on katki/määrdunud, 60% kuna ese on kulunud/ilme kaotanud ja 54% kuna ajas on kehadimensioonid muutunud. ' \
'Need kolm kategooriat domineerivad ning viitavad, et tarbijad loobuvad rõivastest pigem praktilistel põhjustel, mitte moe ega tarbimisharjumuste tõttu. Kõige sagedamini koos valitud variandid olid ese on katki/määrdunud ja ese on kulunud/ilme kaotanud. ' \
'See on positiivne signaal jätkusuutlikkuse seisukohalt. Samas võivad tulemused varjata ka materjalide kvaliteedi muret - rõivaid kantakse kuni kulumiseni, kuid halva kvaliteediga ese kulub kiiremini kui kandjal sellest väsimus tekib.')

st.write('Täiendavate vabatekstiliste vastuste seas toodi kõige enam välja just lasteriietega seonduvat ehk lapsed kasvavad riietest ruttu välja. Kindel on see, et laps ei jõua päriselt läbi kanda kõiki riideid, ' \
'kuid neile tekib tõenäoliselt kandmise jooksul plekke või pisidefekte. Need aga ei segaks rõiva kandmist järgmisel lapsel. Tasuks populariseerida mõtet, et lasterõivastel pisiplekkide esinemine on normaalne ja ' \
'soodustada lasteriiete ringlust plekkidest-pisiparandustest hoolimata.')

st.write('**Vastajate jaotus tekstiilidest loobumise põhjuste alusel**')
tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

loobumise_pohjused = mitmikvastuse_sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K19_loobumise_pohjused'
).sort_values(by='protsent', ascending=False)

fig, ax = loo_hor_tulpdiagramm(
    df=loobumise_pohjused,
    title='',
    style_config=style,
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
plt.close(fig)

###################################################
# KASUTUSKÕLBMATUD TEKSTIILID                     #
###################################################
st.write('## Kasutuskõlbmatutest tekstiilidest loobumise viisid')

st.write('Selleks, et mõista kuidas tarbijad hetkel kasutuskõlbmatute tekstiilidega toimivad, küsiti kuhu peamiselt viiakse kasutuskõlbmatud rõivad ja tekstiilid. ' \
'Vastajal oli võimalik valida mitu vastusevarianti ning oma vastuseid vabatekstiväljal täpsustada. Kõige enam valiti korraga vaid 1 sobiv variant.')

st.write('Vastustes joonistub välja, et inimestel ei ole ühte selget viisi, mil moel kasutuskõlbmatute tekstiilidega kõige targemini toimetada. ' \
'Ülekaalukalt kõige sagedamini valiti segaolmejäätmete konteineritesse viimist (57%), mis ei ole nõuetekohane ega ka keskkonnasõbralik lahendus, kuid mis oli lubatud praktika enne 2025. aasta jaanuari. ' \
'Rõivakonteineritesse viimine (36%) on samuti levinud, kuigi neisse konteineritesse oodatakse vaid kasutuskõlbulikke rõivaid ja tekstiile. ' \
'Jäätmejaama viib ainult 14%, mis on õige viis, kuid selgelt alakasutatud. See näitab vajadust parema info järele kasutuskõlbmatute tekstiilide käitlemise kohta.')

st.write('**Vastajate jaotus kasutuskõlbmatutest tekstiilidest loobumise viiside alusel**')
tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

kolbmatud = mitmikvastuse_sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K23_kasutuskolbmatud_tekstiilid'
).sort_values(by='protsent', ascending=False)

fig, ax = loo_hor_tulpdiagramm(
    df=kolbmatud,
    title='',
    style_config=style,
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

#plt.savefig('Documentation/kasutuskolbmatud_tekstiilid.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)

st.write('### Maakondlikud erinevused kasutuskõlbmatutest tekstiilidest loobumisel')

st.write('Regionaalsed erinevused on märkimisväärsed. Pärnumaa (42%), Harjumaa (27%) ja Tartumaa (27%) elanikud kasutavad rohkem rõivakonteinereid. Samas Viljandimaal (60%) on suur hulk neid vastajaid, kes eelistavad segaolmejäätmete konteinereid. ' \
'Järva eristub jällegi nende vastajate poolest, kes kas põletavad (15%) või matavad (9%) kasutuskõlbmatuid tekstiile. Need erinevused võivad peegeldada infrastruktuuri kättesaadavust ja kohalikke harjumusi.')

st.write('**Loobumisviisid maakondade lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Kogumisviisid vanuse alusel
elukoht_kasutuskolbmatu = loo_mitmikvastuse_risttabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus_single='K5_elukoht', 
    tunnus_multiselect='K23_kasutuskolbmatud_tekstiilid', 
    normalize=True
)

# Kuva tulpdiagramm
fig, ax = loo_hor_stacked_tulpdiagramm(
    df=elukoht_kasutuskolbmatu,
    title='',
    style_config=style,
    sort=False
)
tab1.pyplot(fig)
tab2.dataframe(
    elukoht_kasutuskolbmatu,
    column_config={'K5_elukoht': ''}
)
plt.close(fig)

st.write('### Riikliku juhise selguse mõju tekstiilidest loobumisele')

st.write('Paradoksaalselt, isegi need, kelle jaoks on riiklikud kogumisjuhised täiesti selged, viivad kasutuskõlbmatuid tekstiile segaolmejäätmete konteineritesse (46%) või rõivakonteinerisse (24%), mis ei ole nõuetekohane praktika. ' \
'See näitab, et ka pelgalt juhistest arusaamine ei pruugi tagada korrektset käitumist. Samas grupp, kus juhised on arusaadavad, kasutab teistest oluliselt rohkem jäätmejaama (32%).')

st.write('**Riikliku juhise selgus vs loobumise viisid**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Probleemi tõsidus x loobumisel oluline
juhis_kasutuskolbmatu = loo_mitmikvastuse_risttabel(
    df_data=data_puhastatud,
    df_koodid=koodid,
    tunnus_single='K28_riikliku_juhise_selgus', 
    tunnus_multiselect='K23_kasutuskolbmatud_tekstiilid', 
    normalize=True
)

# Loo heatmap
fig, ax = loo_heatmap(
    df=juhis_kasutuskolbmatu,
    title=''
)
tab1.pyplot(fig)
tab2.dataframe(
    juhis_kasutuskolbmatu.reindex(juhis_kasutuskolbmatu.index[::-1]),
    column_config={'K28_riikliku_juhise_selgus': ''}
)
plt.close(fig)

###################################################
# SOBIMATUD TEKSTIILID                            #
###################################################
st.write('## Korduskasutuseks sobimatud tekstiilid')

st.write('Rõivastest loobumise harjumused on tihedalt seotud ka kogumissüsteemide toimimise ja nende selgusega. Seetõttu küsiti, kas vastajad on teadlikult viinud tekstiilikonteineritesse rõivaid, mis korduskasutuseks ei sobi. ' \
'Vastustest selgub, et 66% vastanutest ei ole seda kunagi teadlikult teinud, mis on positiivne. Siiski 27% on eseme seisukorras kahelnud ja 7% viinud selliseid tekstiile teadlikult rõivakonteinerisse. ' \
'See näitab, et tarbijatel esineb ebakindlust selles, milliseid tekstiile konteinerisse tohib panna. Mitmed vastajad märkisid, et neil puudub selge arusaam konteinerite eesmärgist või korduskasutuse kriteeriumidest.')

st.write('**Vastajate jaotus teadliku käitumise lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])
# Leia vastajate arv teadlikkuse alusel
sobimatu_kaitumine = sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K26_korduskasutuseks_sobimatud_tekstiilid'
)

# Kuva tulpdiagramm
fig, ax = loo_tulpdiagramm(
    df=sobimatu_kaitumine,
    title='',
    style_config=style
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
plt.close(fig)

###################################################
# ULTRAKIIRMOE OSTMINE                            #
###################################################
st.write('## Ultrakiirmoe ostmise harjumused')

vastuste_arv = data_puhastatud['K41_ultrakiirmoe_ostmine'].count()

st.write('Viimastel aastatel levima hakanud ultrakiirmoodi (nt Shein ja PrettyLittleThing) peetakse kiireks ja odavaks võimaluseks enda garderoobi värskust lisada. ' \
f'Valikulise lisaküsimusena oli vastajatel võimalik täpsustada kas ja kui sageli nad ostavad ultrakiirmoodi. Vastanuid oli kokku {vastuste_arv}.')

st.write('Enamik vastanutest (62%) ei osta kunagi ultrakiirmoodi, mis on positiivne signaal, kuid mis ei välista, et oste ei ole tehtud näiteks teise ringi kauplustest. ' \
'Siiski 24% ostab kiirmoodi harva ja 8% mõnikord. 4% on tunnistanud ultrakiirmoe sagedast ja 2% väga sagedast ostmist. See näitab, et kuigi ultrakiirmood ei ole domineeriv ostuharjumus, ' \
'puutub siiski märgatav osa vastajatest sellega kokku, luues potentsiaalse sihtrühma teadlikkuse tõstmiseks.')

st.write('Küsimuse vabatekstilistes täpsustuses on välja toodud, et ultrakiirmoe peamiseks ostupõhjuseks on odav hind. Seda soetatakse eelkõige lastele, kiirelt kuluvate esemete või piiratud eelarve puhul.')

st.write('**Vastajate jaotus loobutud ultrakiirmoe soetamise lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])
# Leia vastajate arv ultrakiirmoe ostmise sageduse alusel
kiirmood = sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K41_ultrakiirmoe_ostmine'
)

# Kuva tulpdiagramm
fig, ax = loo_tulpdiagramm(
    df=kiirmood,
    title='',
    style_config=style
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
plt.close(fig)

st.write('### Vanuselised erinevused ultrakiirmoe ostmises')

st.write('Kui vaadelda ultrakiirmoe ostmise harjumusi vanusegruppide alusel, siis selgub ootuspärane muster: nooremad ostavad ultrakiirmoodi sagedamini. ' \
'Alla 18-aastaste ja 18-29-aastaste hulgas ostab ultrakiirmoodi vastavalt 55% ja 44% vastajatest, samas kui vanemaealiste (üle 64) puhul on see osakaal 25% ja nende hulgas on ainult harvad ostjad. ' \
'See kinnitab, et ultrakiirmoe tarbimine on peamiselt noorte nähtus, mis vajab sihitud teavitust.')

st.write('**Ultrakiirmoe ostmise sagedus vanusegruppide lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Ultrakiirmoe ostmine vanuse alusel
kiirmood_vanus = loo_risttabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus_rida='K3_vanus', 
    tunnus_veerg='K41_ultrakiirmoe_ostmine', 
    normalize=True
)

# Kuva tulpdiagramm
fig, ax = loo_hor_stacked_tulpdiagramm(
    df=kiirmood_vanus,
    title='',
    style_config=style
)
tab1.pyplot(fig)
tab2.dataframe(kiirmood_vanus,
    column_config={'K3_vanus': ''}
)
plt.close(fig)

###################################################
# RÕIVASTE OSTMISSAGEDUS                          #
###################################################
st.write('## Uute rõivaste ostmissagedus')

vastuste_arv = data_puhastatud['K40_ostmissagedus'].count()

st.write(f'Valikulise lisaküsimusena oli vastajatel võimalik täpsustada kas ja kui sageli nad ostavad ultrakiirmoodi. Vastanuid oli kokku {vastuste_arv}. ' \
'Valdav enamik (57%) ostab uusi rõivaid kord kvartalis, mis näitab mõõdukat tarbimist. 20% ostab kord aastas ja 6% veelgi harvem. ' \
'Sagedasemateks ostjateks (kord kuus või sagedamini) klassifitseerub 17% vastanutest, mis on suhteliselt madal näitaja.')

st.write('**Vastajate jaotus loobutud rõivaste soetamise sageduse lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel'])
# Leia vastajate arv ostmissageduse alusel
ostmissagedus = sagedustabel(
    df_data=data_puhastatud, 
    df_koodid=koodid, 
    tunnus='K40_ostmissagedus')

# Kuva tulpdiagramm
fig, ax = loo_tulpdiagramm(
    df=ostmissagedus,
    title='',
    style_config=style
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
plt.close(fig)

st.write('### Vanuselised erinevused rõivaste ostmissageduses')

st.write('Rõivaste ostmissagedus erineb vanusegruppide lõikes. Nooremad (alla 18) ostavad uusi rõivad kord kuus (45%) või ka sagedamini (3%). Mida vanemaks vastajad muutuvad, seda harvem uusi rõivaid ostetakse. ' \
'Näiteks kord kvartalis uusi rõivaid ostjate osakaal 18-29-aastaste hulgas on 69%, kuid vanemate kui 64 seas 25. ' \
'Viimaste seas on suurim osa (75%) neid, kes ostavad kord kvartalis või harvem, mis võib peegeldada nii sissetulekut kui ka elustiili erinevusi.')

st.write('**Uute rõivaste ostmise sagedus vanusegruppide lõikes**')

tab1, tab2 = st.tabs(['Graafik', 'Tabel (% vastanutest)'])

# Eemalda sorteerimiskäitumine, kus valikuks Null-kulu eluviis, muu
# sorteerimine_puhas = data_puhastatud[data_puhastatud['K7_sorteerimiskaitumine'].isin([1, 2, 3, 4])]

# sorteerimiskaitumine_grupeeritud = sagedustabel(sorteerimine_puhas, sort_koodid, 'K7_sorteerimiskaitumine', use_full_codebook=False)
#print(f'Vastanutest {sorteerimiskaitumine_grupeeritud.loc[sorteerimiskaitumine_grupeeritud['kood']==3, 'protsent_str'].to_string(index=False)} sorteerib 3-s või enamas kategoorias')

# Käitumine vanuse alusel
sagedus_vanus = loo_risttabel(data_puhastatud, koodid, 'K3_vanus', 'K40_ostmissagedus', normalize=True)

# Kuva tulpdiagramm
fig, ax = loo_hor_stacked_tulpdiagramm(
    sagedus_vanus,
    '',
    style
)
tab1.pyplot(fig)
tab2.dataframe(sagedus_vanus,
    column_config={'K3_vanus': ''}
)
plt.close(fig)