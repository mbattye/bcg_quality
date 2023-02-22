import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import pathlib

st.title("BCG Quality Improvement Project")
st.header("A project to improve BCG vaccine rates for neonates.")

filepath = pathlib.Path(__file__).parent/"BCG QIP.xlsx"
df_vaccines = pd.read_excel(filepath, "BCG_vaccine_data")
df_clinic = pd.read_excel(filepath, "clinic_lists")
# Remove anomolies
df_vaccines = df_vaccines[df_vaccines['details'] != 'Referred by GP']
# Change P and H to Patient and Hospital
df_vaccines['patient_hospital_cancelled'] = df_vaccines['patient_hospital_cancelled'].replace(['P','H'], ['Patient','Hospital'])

col_names = ["# of Days before Vaccine", "# of Days before First Appoinment Offered", "# of Days for Screening Scanned"]

with st.expander("View Summary Table"):
    vaccine_stats = df_vaccines.describe()
    vaccine_stats.pop('year')
    vaccine_stats.pop('id')
    vaccine_stats.columns = col_names
    st.dataframe(vaccine_stats)

max_days = int(df_vaccines.vaccine_days.max())
days = st.slider("Select days after birth:", 0, max_days, 28)

limit_percentile_vd = stats.percentileofscore(df_vaccines.vaccine_days,days)
limit_percentile_fad = stats.percentileofscore(df_vaccines.first_appointment_days,days)

st.write(f"At {days} days after birth:")
st.write(f"{round(limit_percentile_vd,1)}% of babies received the vaccine.")
st.write(f"{round(limit_percentile_fad,1)}% were offered a first appointment.")

check = st.checkbox("Seperate by Patient vs. Hospital Cancelled?")

if check:
    set_hue = "patient_hospital_cancelled"
else:
    set_hue = None

sns.set_style("whitegrid")
figure = sns.jointplot(data=df_vaccines, x="first_appointment_days", y="vaccine_days", hue=set_hue)
figure.fig.suptitle("Number of Days Before Vaccine vs First Appointment Offered")
figure.fig.tight_layout()
plt.xlabel("First Appointment for Vaccine Offered")
plt.ylabel("Number of Days Taken to Receive the BCG Vaccine")
plt.axhline(y = days, color = 'r', linestyle = '--')
plt.axvline(x = days, color = 'r', linestyle = '--')
if check:
    figure.ax_joint.legend(title="Cancellations")

st.pyplot(figure)

st.write(f"**patients referred by GP were removed from dataset.")
