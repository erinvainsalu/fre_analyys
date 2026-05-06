import sys
import os

import streamlit as st
import pandas as pd

# Leie peakaust
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Impordi tabelite ja graafikute joonistamiseks vajalikud funktsioonid
from Python.visuaalide_abilised import leia_sildi_mapping
from Python.visuaalide_abilised import sagedustabel

st.title('Tarbijate hoiakud tekstiilide liigiti kogumisel rõivastest ja kodutekstiilidest loobumisel')

st.write('Uuring "Tarbijate hoiakud tekstiilide liigiti kogumisel rõivastest ja kodutekstiilidest loobumisel" kutsuti ellu Jääk OÜ eestvedaja Auli Uiboupini algatusel. ' \
'Uuringu peamiseks läbiviijaks oli Fashion Revolution Estonia MTÜ, nõuandvas rollis osales Kerli Kant Hvass.')

st.write('Fashion Revolution Estonia on osa ülemaailmselt liikumisest Fashion Revolution. ' \
'[Fashion Revolution](https://www.fashionrevolution.org/) on rahvusvaheline moeaktivismile suunatud organisatsioon, mis ühendab inimesi, kes panevad moetööstuse toimima. ' \
'Oeganisatsioon sündis pärast 2013. aastal Bangladeshis aset leidnud tootmishoone Rana Plaza varingut, ' \
'mille käigus hukkus tuhandeid inimesi. ' \
'Tol hetkel sai selgeks, et moetööstus peab hakkama kasumi kõrvalt rohkem väärtustama inimesi ja planeeti.')

st.write('[Fashion Revolution Estonia MTÜ](https://www.fashionrevolution.org/europe/estonia/) seisab tugevalt puhtama, turvalisema, eetilisema, läbipaistvama ja jätkusuutlikuma moetööstuse eest. ' \
'Fashion Revolution Estonia põhiline eesmärk on tuua tarbijateni suuremat teadlikkust jätkusuutliku moe tarbimisest, mis aitab teha läbimõeldud otsuseid igapäevaelus.')

st.write('Tekstiilijäätmete olmeprügist eraldi kogumine on Eestis kohustuslik alates 1. jaanuarist 2025. ' \
'See tähendab, et inimestel on kohustus koguda tekstiilijäätmed eraldi muudest jäätmetest ning kohalik omavalitsus peab tagama võimaluse need omavalitsuse piires ära anda.')

st.write('Uuringu eesmärk oli mõista, millised on tarbijate vajadused ja väljakutsed kasutatud tekstiilidest loobumisel ning nende valmisolek tekstiile sorteerida enne nende äraandmist. ' \
'Soov oli kasutada kogutud tagasisidet üldisemalt tekstiilide kogumise ja ringlusse saatmise paremaks korraldamiseks Eestis. ' \
'Uuringu käigus koguti andmeid Google Forms vahendusel 2025. aastal perioodil 10. märts kuni 30. aprill. ' \
'Infot uuringu kohta levitati sotsiaalmeedias ning paberkandjal.')

st.write('Uuring analüüsib Eesti tarbijate käitumismustreid ja motivatsiooni tekstiiltoodete liigiti kogumisel ning nende tagastamisel pärast kasutusest loobumist. Uuringu eesmärk on koguda andmeid tarbijate käitumise, vajaduste ja takistuste kohta, et toetada kasutatud tekstiilidele tõhusate kogumismudelite loomist. Selle uuringu loomise põhjuseks on EL tekstiili strateegiast tulenev regulatsioon, mis näeb muuhulgas ette tekstiilijäätmete olmeprügist eraldi kogumise kohustuse alates 2025. a. jaanuarist. Samas ka tekstiilijäätmete suurenev keskkonnamõju ning vajadus arendada ringmajanduse põhimõtteid Eestis (seda nii üleriigiliselt kui väiksemate piirkondade pilootprojektide eesmärgil). Eestis ei ole varasemalt läbi viidud sarnast ulatuslikku uuringut, mis ühendaks tarbijate valmisoleku, kogumissüsteemide sobivuse ja keskkonnateadlikkuse. Uuring annab ülevaate tarbijate hoiakutest, kogemustest ja ootustest, pakkudes esmaseid andmeid poliitika- ja äriplaanide kujundamiseks. Samuti aitab see tuvastada peamised barjäärid, mis mõjutavad tarbijate osalust tekstiili sorteerimises ja tagastamises.')