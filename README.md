# Hotel Booking Cancellation Analysis

## Overview

This project presents an exploratory data analysis (EDA) of the Hotel Booking Demand dataset containing over 119,000 booking records. The objective was to identify the key factors influencing booking cancellations and understand customer behaviour across City Hotels and Resort Hotels.

The analysis includes data cleaning, feature engineering, visualization, and business-focused insights, along with an interactive dashboard built using Streamlit.

## Objectives

* Clean and preprocess the dataset
* Perform exploratory data analysis
* Engineer meaningful features
* Compare booking patterns across hotel types
* Identify the primary drivers of booking cancellations
* Present findings through an interactive dashboard

## Key Insights

* Lead time is the strongest indicator of booking cancellation. Reservations made several months in advance show significantly higher cancellation rates.
* City Hotels consistently experience higher cancellation rates than Resort Hotels.
* Guests who make special requests or modify bookings are less likely to cancel.
* Direct bookings have substantially lower cancellation rates than bookings made through travel agents.
* Repeat guests are considerably less likely to cancel than first-time guests.
* Portugal, the United Kingdom, France, Spain, and Germany account for the majority of bookings.

## Technology Stack

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Plotly
* Streamlit
* Jupyter Notebook

## Project Structure

```text
hotel-booking-analysis/
│
├── HotelBookingDA_Enhanced.ipynb
├── app.py
├── hotel_booking.csv
├── requirements.txt
├── README.md
└── .gitignore
```

## Running the Project

Clone the repository.

```bash
git clone https://github.com/<your-username>/hotel-booking-analysis.git
cd hotel-booking-analysis
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard.

```bash
streamlit run app.py
```

Alternatively, open the notebook.

```bash
jupyter notebook HotelBookingDA_Enhanced.ipynb
```

## Skills Demonstrated

* Exploratory Data Analysis
* Data Cleaning and Preprocessing
* Feature Engineering
* Statistical Analysis
* Data Visualization
* Business Insight Generation
* Dashboard Development
* Python
* Pandas
* Plotly
* Streamlit

## Dataset

* **Source:** Hotel Booking Demand dataset (Kaggle)
* **Records:** 119,390 hotel bookings
* **Period:** 2015–2017
* **Hotels:** City Hotel and Resort Hotel

## Future Improvements

* Predictive modelling for cancellation prediction
* Interactive filtering and drill-down analysis
* Time-series forecasting of booking demand
* Automated reporting dashboard

## License

This project is intended for educational and portfolio purposes.
