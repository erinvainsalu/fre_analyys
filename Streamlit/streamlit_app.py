import streamlit as st

# Defineeri alamlehed
main_page = st.Page('FRE_uuring.py', title='Uuring')
page_2 = st.Page('Demograafilised_andmed.py', title='Vastajate demograafilised andmed')
page_3 = st.Page('Tarbijate_teadlikkus.py', title='Tarbijate teadlikkus')
page_4 = st.Page('Tarbijakaitumine.py', title='Tänane tarbijakäitumine')
page_5 = st.Page('Kokkuvote.py', title='Kokkuvõte')

# Seadista navigatsioon
pg = st.navigation([main_page, page_2, page_3, page_4, page_5])

# Run the selected page
pg.run()