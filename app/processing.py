import json

import pandas as pd
import streamlit as st


RP3_FORCE_MEASUREMENT_INTERVAL = 2.2225  # In centimeters.

DEFAULT_MIN_STROKE_RATE = 0
DEFAULT_MAX_STROKE_RATE = 100
DEFAULT_MIN_POWER = 0
DEFAULT_MAX_POWER = 1500
DEFAULT_MIN_HEART_RATE = 0
DEFAULT_MAX_HEART_RATE = 250


def filter_data(data):
    min_stroke_rate = DEFAULT_MIN_STROKE_RATE
    max_stroke_rate = DEFAULT_MAX_STROKE_RATE
    min_power = DEFAULT_MIN_POWER
    max_power = DEFAULT_MAX_POWER
    min_heart_rate = DEFAULT_MIN_HEART_RATE
    max_heart_rate = DEFAULT_MAX_HEART_RATE
    with st.beta_expander("Filter data", expanded=True):
        min_stroke_rate, max_stroke_rate = st.slider(
            label="Select a stroke rate range",
            min_value=0,
            max_value=100,
            value=(DEFAULT_MIN_STROKE_RATE, DEFAULT_MAX_STROKE_RATE),
            format="%s/min",
        )

        min_power, max_power = st.slider(
            label="Select a power range",
            min_value=0,
            max_value=1500,
            value=(DEFAULT_MIN_POWER, DEFAULT_MAX_POWER),
            format="%iW",
        )

        min_heart_rate, max_heart_rate = st.slider(
            label="Select an heart rate range",
            min_value=0,
            max_value=250,
            value=(DEFAULT_MIN_HEART_RATE, DEFAULT_MAX_HEART_RATE),
            format="%i bpm",
        )

    filtered_data = data.loc[
        data["stroke_rate"].between(min_stroke_rate, max_stroke_rate) & \
        data["power"].between(min_power, max_power) & \
        data["pulse"].between(min_heart_rate, max_heart_rate)
    ]
    filter_config = {
        "min_stroke_rate": min_stroke_rate,
        "max_stroke_rate": max_stroke_rate,
        "min_power": min_power,
        "max_power": max_power,
        "min_heart_rate": min_heart_rate,
        "max_heart_rate": max_heart_rate,
    }
    return filtered_data, filter_config


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

def _create_single_snapshot_name(filter_config, name):
    title = name.replace("_", " ")
    min_value = filter_config[f"min_{name}"]
    max_value = filter_config[f"max_{name}"]
    if min_value != globals()[f"DEFAULT_MIN_{name.upper()}"]:
        if max_value != globals()[f"DEFAULT_MAX_{name.upper()}"]:
            filter_name = f"{min_value}<={title}<={max_value}"
        else:
            filter_name = f"{title}>={min_value}"
    elif max_value != globals()[f"DEFAULT_MAX_{name.upper()}"]:
        filter_name = f"{title}<={max_value}"
    else:
        filter_name = None
    return filter_name


def create_snapshot_name(filter_config):
    bits = []
    names = {i[4:] for i in filter_config.keys()}

    for name in names:
        single_snapshot_name = _create_single_snapshot_name(filter_config, name)
        if single_snapshot_name is not None:
            bits.append(single_snapshot_name)

    if bits:
        snapshot_name = ", ".join(bits)
    else:
        snapshot_name = "all data"

    return snapshot_name
