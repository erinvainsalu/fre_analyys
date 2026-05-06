import streamlit as st

# Defineeri alamlehed
main_page = st.Page('uuring.py', title='Uuringust')
page_2 = st.Page('demograafilised_andmed.py', title='Vastajate demograafilised andmed')
page_3 = st.Page('tarbijate_teadlikkus.py', title='Tarbijate teadlikkus')
page_4 = st.Page('tarbijakaitumine.py', title='Tänane tarbijakäitumine')
page_5 = st.Page('takistused_eelistused.py', title='Takistused ja eelistused')
page_6 = st.Page('kokkuvote.py', title='Kokkuvõte')

# Seadista navigatsioon
pg = st.navigation([main_page, page_2, page_3, page_4, page_5, page_6])

# Run the selected page
pg.run()