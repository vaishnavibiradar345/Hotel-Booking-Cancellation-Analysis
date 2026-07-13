# 🏨 Hotel Booking Demand — Exploratory Data Analysis

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-1.5+-150458?style=flat&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat&logo=jupyter&logoColor=white)

> Exploratory data analysis of 119,000+ hotel booking records to uncover what drives cancellations and how guest behaviour varies across City and Resort Hotels.

---

## 🔴 Live Dashboard

**[▶ Open Interactive Dashboard →](https://your-app.streamlit.app)**
*(Replace this link after deploying to Streamlit Cloud — see deployment steps below)*

---

## 📊 Project Overview

This project performs end-to-end EDA on the [Hotel Booking Demand dataset](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand), covering:

- **Data cleaning** — handling missing values, PII removal, outlier treatment, invalid row removal
- **Feature engineering** — total stay nights, total guests, family flag, lead time buckets
- **Univariate analysis** — distributions of lead time, stay length, guest count, and country
- **Bivariate analysis** — relationships between booking attributes and cancellation rates
- **Hotel comparison** — City Hotel vs Resort Hotel across ADR, stay length, lead time, and cancellation
- **Customer behaviour** — market segment, customer type, deposit type, repeat guests, distribution channel
- **Booking behaviour** — family bookings, booking changes, special requests

---

## 🔍 Key Findings

- **Lead time is the strongest predictor of cancellation.** Bookings made 300+ days in advance cancel at 75% (City Hotel) vs 43% (Resort Hotel). Short lead times cancel at under 15%.
- **City Hotel has a structurally higher cancellation rate (42%) than Resort Hotel (28%)** across all months and segments — this is not a seasonal pattern.
- **Guest engagement reduces cancellation.** Each additional special request is associated with a lower cancellation rate. The same holds for booking modifications.
- **Direct bookings cancel at 17% vs 41% for TA/TO channel bookings.** Shifting guests toward direct channels is the highest-leverage operational change.
- **Repeat guests cancel at 15% vs 38% for new guests** — a 2.5× difference that makes loyalty investment worthwhile.
- **Portugal dominates the source market**, followed by UK, France, Spain, and Germany. Top 5 countries account for the majority of all bookings.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Pandas | Data manipulation and cleaning |
| NumPy | Numerical operations |
| Matplotlib + Seaborn | EDA notebook visualisations |
| Plotly | Interactive dashboard charts |
| Streamlit | Dashboard framework |
| Jupyter Notebook | Analysis and storytelling |

---

## 📁 Project Structure

```
hotel-booking-eda/
│
├── HotelBookingDA_Enhanced.ipynb   # Full EDA notebook with analysis and insights
├── app.py                          # Streamlit interactive dashboard
├── hotel_booking.csv               # Dataset (119,390 records, 32 features)
├── requirements.txt                # Python dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/hotel-booking-eda.git
cd hotel-booking-eda

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Streamlit dashboard
streamlit run app.py

# 4. Or open the EDA notebook
jupyter notebook HotelBookingDA_Enhanced.ipynb
```

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub (public)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select this repo → set **Main file path** to `app.py`
4. Click **Deploy** — live in ~2 minutes
5. Replace the demo link at the top of this README with your deployed URL

---

## 📈 Skills Demonstrated

`Exploratory Data Analysis` · `Data Cleaning` · `Feature Engineering` · `Data Visualisation`
`Business Insight Communication` · `Python` · `Pandas` · `Seaborn` · `Plotly` · `Streamlit`

---

## 📂 Dataset

- **Source:** [Hotel Booking Demand — Kaggle](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand)
- **Original paper:** Antonio, Almeida & Nunes (2019), *Data in Brief*
- **Records:** 119,390 bookings across City and Resort Hotels (2015–2017)
- **Features:** 36 columns covering booking details, guest profile, and reservation status

---

*This project was completed as part of a personal data analyst portfolio.*
