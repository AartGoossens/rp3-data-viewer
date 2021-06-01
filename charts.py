import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.cm import get_cmap


def plot_average(data, normalize=False):
    force_mean = data.mean()
    force_std = data.std()

    fig = plt.figure()
    ax = plt.axes()
    ax.fill_between(
        x=force_mean.index,
        y1=force_mean - (1*force_std),
        y2=force_mean + (1*force_std),
        color="lightgray",
    )
    ax.plot(force_mean.index, force_mean, color="black")
    if normalize:
        ax.set_ylim(bottom=0, top=1)
    else:
        ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)

    ax.set_title(f"RP3 force curve with 1 standard deviation\n(n={len(data)})")
    ax.set_xlabel("Drive length [cm]")
    if normalize:
        ax.set_ylabel("normalized force [-]")
    else:
        ax.set_ylabel("force [AU]")
    ax2 = ax.twinx()
    ax2.set_yticks([])
    ylabel = ax2.set_ylabel("this chart is powered by gssns.io", color="gray")
    ylabel.set_rotation(270)
    ax2.yaxis.set_label_coords(0.99, 0.5)

    st.pyplot(fig=fig)


def plot_all(data, normalize=False):
    data = data.T
    fig = plt.figure()
    ax = plt.axes()
    for c in data.columns:
        ax.plot(data.index, data[c], color="lightgray")

    if normalize:
        ax.set_ylim(bottom=0, top=1)
    else:
        ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)

    ax.set_title(f"RP3 force curves\n(n={len(data)})")
    ax.set_xlabel("Drive length [cm]")

    if normalize:
        ax.set_ylabel("normalized force [-]")
    else:
        ax.set_ylabel("force [AU]")

    ax2 = ax.twinx()
    ax2.set_yticks([])
    ylabel = ax2.set_ylabel("this chart is powered by gssns.io", color="gray")
    ylabel.set_rotation(270)
    ax2.yaxis.set_label_coords(0.99, 0.5)

    st.pyplot(fig=fig)


def plot_multiple(data, normalize=False):
    fig = plt.figure()
    ax = plt.axes()
    ax.set_prop_cycle(color=get_cmap("Accent").colors)
    for c in data.columns:
        ax.plot(data.index, data[c], label=c)

    if normalize:
        ax.set_ylim(bottom=0, top=1)
    else:
        ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)

    ax.set_title(f"RP3 force curve with 1 standard deviation\n(n={len(data)})")
    ax.set_xlabel("Drive length [cm]")
    if normalize:
        ax.set_ylabel("normalized force [-]")
    else:
        ax.set_ylabel("force [AU]")

    ax.legend()

    ax2 = ax.twinx()
    ax2.set_yticks([])
    ylabel = ax2.set_ylabel("this chart is powered by gssns.io", color="gray")
    ylabel.set_rotation(270)
    ax2.yaxis.set_label_coords(0.99, 0.5)

    st.pyplot(fig=fig)
