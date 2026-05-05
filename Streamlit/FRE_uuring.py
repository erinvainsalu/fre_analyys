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

st.write('Aastal 2025 jõustunud seadus näeb ette tekstiilijäätmete liigiti kogumise olmeprügist eraldi, ' \
'ehk tarbijal ei ole enam seaduse järgi lubatud visata tekstiilijäätmeid, näiteks kulunud ja katkiseid rõivaid, olmeprügi hulka. ')