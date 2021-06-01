import streamlit as st

import charts
import processing


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
force_mean = force_columns.mean()
force_std = force_columns.std()


if what_to_plot == "All force curves":
    fig = charts.plot_all(force_columns, normalize=normalize)
else:
    fig = charts.plot_average(force_columns, normalize=normalize)

st.pyplot(fig=fig)
