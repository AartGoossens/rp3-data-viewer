import pandas as pd
import streamlit as st

import charts
import processing
import state

st.set_page_config(
    page_title="RP3 data viewer",
    page_icon=":computer:",
)

st.markdown(
    """
    # :computer: RP3 data viewer
    """
)

uploaded_file = st.file_uploader("Select an RP3 .json file")
if uploaded_file is None:
    st.stop()

df = processing.load_rp3_json(uploaded_file)
state = state.get_state(snapshots=pd.DataFrame())

df = processing.filter_data(df)

what_to_plot = st.radio(
    label="What to plot",
    options=["Average force curve", "All force curves"],
    index=0,
)

if what_to_plot == "All force curves":
    normalize = False
else:
    normalize = st.checkbox("Normalize forces")

force_columns = processing.get_force_columns(df, normalize=normalize)


if what_to_plot == "All force curves":
    charts.plot_all(force_columns, normalize=normalize)
else:
    charts.plot_average(force_columns, normalize=normalize)

with st.form("Save snapshot"):
    st.markdown(
        """
        # Comparison
        - Filter the data with the sliders at the top
        - Give the snapshot a name
        - Save the snapshot
        - Compare the average force curves in the chart below
        """
    )
    snapshot_name = st.text_input("Snapshot name")
    submitted = st.form_submit_button(label="Save snapshot")
    if submitted:
        state.snapshots[snapshot_name] = force_columns.mean()

if not state.snapshots.empty:
    charts.plot_multiple(state.snapshots)
