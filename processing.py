import json

import pandas as pd
import streamlit as st


RP3_FORCE_MEASUREMENT_INTERVAL = 2.2225  # In centimeters.


def filter_data(data):
    min_stroke_rate = 0
    max_stroke_rate = 100
    min_power = 0
    max_power = 1500
    min_heart_rate = 0
    max_heart_rate = 250
    with st.beta_expander("Filter data"):
        min_stroke_rate, max_stroke_rate = st.slider(
            label="Select a stroke rate range",
            min_value=0,
            max_value=100,
            value=(0, 100),
            format="%s/min",
        )

        min_power, max_power = st.slider(
            label="Select a power range",
            min_value=0,
            max_value=1500,
            value=(0, 1500),
            format="%iW",
        )

        min_heart_rate, max_heart_rate = st.slider(
            label="Select an heart rate range",
            min_value=0,
            max_value=250,
            value=(0, 250),
            format="%i bpm",
        )

    filtered_data = data.loc[
        data["stroke_rate"].between(min_stroke_rate, max_stroke_rate) & \
        data["power"].between(min_power, max_power) & \
        data["pulse"].between(min_heart_rate, max_heart_rate)
    ]
    return filtered_data


def extract_force_curves(df):
    curve_df = pd.DataFrame()
    for _, curve in df.iterrows():
        curve_values = pd.Series([int(i) for i in curve["curve_data"].split(",")])
        curve_values = curve_values.reindex(range(250))
        curve_df[curve["stroke_number"]] = curve_values
        
    curve_transposed = curve_df.T.rename(columns=lambda x: f"force_{x}")
    
    return curve_transposed


def num_of_elements(curve_data):
    return len([int(i) for i in curve_data.split(",")])


def load_rp3_json(uploaded_file):
    data = json.load(uploaded_file)

    strokes = []
    for interval in data["workout_intervals"]:
        strokes += interval["strokes"]
    df = pd.DataFrame(strokes)

    df["curve_data_n"] = df["curve_data"].apply(num_of_elements)

    df = df.join(extract_force_curves(df))

    return df


def get_force_columns(data, normalize=False):
    force_columns = data.loc[:, data.columns.str.startswith("force_")]
    force_columns = force_columns.rename(columns=lambda x: int(x[6:]))
    force_columns.index = force_columns.index * RP3_FORCE_MEASUREMENT_INTERVAL
    if normalize:
        force_columns = force_columns.apply(func=lambda x: x / x.max(), axis="columns")

    return force_columns
