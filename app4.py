# Cols without NHANES: Potassium, Telomeres, Troponin

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mpld3
import streamlit.components.v1 as components
from io import BytesIO
import json

#create your figure and get the figure object returned

st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    
st.sidebar.header('Biomarker Explorer 0.78')

st.sidebar.subheader('Your Info')

with st.sidebar.form(key='users'):
    age = st.number_input('Age')
    gender = st.selectbox('Gender', np.array(['Not Working Yet', 'Not Working Yet']))
    ethnicity = st.selectbox('Ethnicity', np.array(['Not Working Yet', 'Not Working Yet']))
    submitted = st.form_submit_button(label = 'Go')

properties = json.load(open('NHANES_properties.json'))

NHANES_cols = list(properties.keys())



NHANES_files = [
        '1999albumin.csv',
        '1999alkalinephosphatase.csv',
        '1999alt.csv',
        '1999ast.csv',
        '1999bilirubin.csv',
        '1999bloodalbumin.csv',
        '1999bloodcreatinine.csv',
        '1999bloodpressure60secpulse.csv',
        '1999bloodpressuresystolic.csv',
        '1999bloodpressurediastolic.csv',
        '1999bloodpressuremaxinflation.csv',
        '1999calcium.csv',
        '1999cardiovo2.csv',
        '1999cholesterolhdl.csv',
        '1999cholesterolldl.csv',
        '1999cholesteroltotal.csv',
        '1999crp.csv',
        '2017crphs.csv',
        '1999cystatin.csv',
        '2017fastingglucose.csv',
        '1999fastinginsulin.csv',
        '1999glycohemoglobin.csv',
        '1999hematocrit.csv',
        '1999homocysteine.csv',
        '2017triglyceride.csv',
        '1999meanplatelet.csv',
        '1999profilebloodureanitrogen.csv',
        '1999profileFSH.csv',
        '1999redcellwidth.csv',
        '1999selenium.csv',
        '1999sexsteroidadlg.csv',
        '2015femaleestradiol.csv',
        '2015maleshbg.csv',
        '2015maletest.csv',
        '1999iron.csv',
        '1999uricacid.csv',  
        '2001fibrinogen.csv',
        '2015apob.csv',
        '2015klotho.csv',
        '2007ferritin.csv',
        '2013gripstrength.csv',
    ]

keys = range(len(NHANES_cols))

# Button for filtering plots

with st.form(key='filters'):
    plot = st.multiselect(label='Search biomarker', options=np.hstack(('SELECT ALL', NHANES_cols)), default='SELECT ALL')
    submitted = st.form_submit_button(label = 'Go')
    
    
#Looping scatterplots - with dynamic user input

if 'SELECT ALL' in plot:
    plot = NHANES_cols

for biomarker in plot:
    
    index = NHANES_cols.index(biomarker)
    val = keys[index]
    file = NHANES_files[index]
    
    with st.container():
        col1_2, col2_2 = st.columns(2)
        
    with col1_2:
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        with st.form(key=f'Form{val}'):
            score = st.number_input(f'{biomarker}', key=val)
            submitted = st.form_submit_button(label='Go')
    
    with col2_2:
    
        NHANES2 = pd.read_csv(f"NHANES r format/r{file[:4]}/{file}")

        fig2, nex = plt.subplots()
        ylimit2 = properties[biomarker]['ylim']

        nex.scatter(NHANES2['Age'], NHANES2['biomarker'], color='gray', alpha=0.2)
        nex.scatter(age, score, color='lime', s=60, edgecolors='black')

        floatingmedian2 = NHANES2.groupby(['Age']).median()['biomarker']
        floatingmean2 = NHANES2.groupby(['Age']).mean()['biomarker']

        nex.scatter(floatingmedian2.index, floatingmedian2.values, color='black', s=10, label='Median')
        nex.scatter(floatingmean2.index, floatingmean2.values, color='red', s=10, label='Mean')

        nex.set_xlabel('Age (yrs)')
        nex.set_ylabel(biomarker.lower())
        nex.set_ylim(0, ylimit2)
        nex.set_xlim(0, 90)
        nex.legend()
        
        colors = properties[biomarker]['ranges'].keys()
        ranges = properties[biomarker]['ranges']
        y_ranges = [ranges[color] for color in colors]

        for (ymin, ymax), color in zip(y_ranges, colors):
            nex.axhspan(ymin, ymax, facecolor=color, alpha=0.3)


        fig_html2 = mpld3.fig_to_html(fig2)
    
        buf = BytesIO()
        fig2.savefig(buf, format="png")
        st.image(buf)
        plt.close(fig2)
