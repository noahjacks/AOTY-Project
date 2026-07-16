import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, linregress, shapiro, f_oneway

# ----------------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------------
st.set_page_config(page_title="Album of the Year Ratings Dashboard", layout="wide")
st.title("🎵 Album of the Year — Ratings Dashboard")

# ----------------------------------------------------------------------------
# Load data
# ----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("AOTY_Ratings.csv")
    df["Date Rated"] = pd.to_datetime(df["Date Rated"])
    return df

df = load_data()
average_score = df["Rating"].mean()

# ----------------------------------------------------------------------------
# Sidebar menu
# ----------------------------------------------------------------------------
view = st.sidebar.radio(
    "Choose a graph or test:",
    [
        "Distribution of Ratings",
        "Rating vs. Year Released",
        "Rating vs. Date Rated",
        "Average Rating by Year",
        "Ratings by Album Type (Box Plot)",
        "Normality Test (Shapiro-Wilk)",
        "ANOVA: Rating by Type",
    ],
)

st.sidebar.markdown("---")
st.sidebar.write(f"**Total albums rated:** {len(df)}")
st.sidebar.write(f"**Overall average rating:** {average_score:.2f}")

# ----------------------------------------------------------------------------
# 1. Distribution of Ratings
# ----------------------------------------------------------------------------
if view == "Distribution of Ratings":
    st.header("Distribution of Ratings")

    bin_edges = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
    fig, ax = plt.subplots()
    counts, edges, patches = ax.hist(
        df["Rating"], bins=bin_edges, color="royalblue", edgecolor="black"
    )

    mu, std = df["Rating"].mean(), df["Rating"].std()
    x = np.linspace(0, 110, 300)
    p = norm.pdf(x, mu, std)
    bin_width_avg = np.mean(np.diff(edges))
    p_scaled = p * len(df["Rating"]) * bin_width_avg
    ax.plot(x, p_scaled, color="black", linewidth=2,
            label=f"Normal Dist (μ={mu:.1f}, σ={std:.1f})")

    ax.axvline(average_score, color="red", linestyle="--", linewidth=2,
               label=f"Average: {average_score:.2f}")
    ax.set_title("Distribution of Ratings")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Frequency")
    ax.legend()
    st.pyplot(fig)

    st.write(f"**Mean:** {mu:.2f} &nbsp;&nbsp; **Std Dev:** {std:.2f} &nbsp;&nbsp; "
             f"**Skewness:** {df['Rating'].skew():.2f} &nbsp;&nbsp; "
             f"**Kurtosis:** {df['Rating'].kurt():.2f}")

# ----------------------------------------------------------------------------
# 2. Rating vs. Year Released
# ----------------------------------------------------------------------------
elif view == "Rating vs. Year Released":
    st.header("Album Ratings Based on Year Released")

    fig, ax = plt.subplots()
    ax.scatter(df["Year"], df["Rating"], alpha=0.5)

    slope, intercept, r_value, p_value, std_err = linregress(df["Year"], df["Rating"])
    best_fit = slope * df["Year"] + intercept
    ax.plot(df["Year"], best_fit, color="black", linewidth=3,
            label=f"Best Fit (slope={slope:.3f})")
    ax.axhline(average_score, color="red", linestyle="--", linewidth=2,
               label=f"Average: {average_score:.2f}")
    ax.set_title("Album Ratings Based on Year Released")
    ax.set_xlabel("Year Released")
    ax.set_ylabel("Rating")
    ax.legend()
    st.pyplot(fig)

    st.write(f"**Slope:** {slope:.4f} &nbsp;&nbsp; **R²:** {r_value**2:.4f} &nbsp;&nbsp; "
             f"**p-value:** {p_value:.4g}")
    if p_value < 0.05:
        st.success("This trend is statistically significant (p < 0.05).")
    else:
        st.info("This trend is NOT statistically significant (p ≥ 0.05) — could be noise.")

# ----------------------------------------------------------------------------
# 3. Rating vs. Date Rated
# ----------------------------------------------------------------------------
elif view == "Rating vs. Date Rated":
    st.header("Album Ratings Based on Date Rated")

    fig, ax = plt.subplots()
    ax.scatter(df["Date Rated"], df["Rating"], alpha=0.5)

    date_nums = df["Date Rated"].map(pd.Timestamp.toordinal)
    slope, intercept, r_value, p_value, std_err = linregress(date_nums, df["Rating"])
    best_fit = slope * date_nums + intercept
    ax.plot(df["Date Rated"], best_fit, color="black", linewidth=3,
            label=f"Best Fit (slope={slope:.5f})")
    ax.axhline(average_score, color="red", linestyle="--", linewidth=2,
               label=f"Average: {average_score:.2f}")
    ax.set_title("Album Ratings Based on Date Rated")
    ax.set_xlabel("Date Rated")
    ax.set_ylabel("Rating")
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

    st.write(f"**Slope:** {slope:.5f} (rating change per day) &nbsp;&nbsp; "
             f"**R²:** {r_value**2:.4f} &nbsp;&nbsp; **p-value:** {p_value:.4g}")
    if p_value < 0.05:
        st.success("Your rating habits have shifted significantly over time (p < 0.05).")
    else:
        st.info("No significant drift in your rating habits over time (p ≥ 0.05).")

# ----------------------------------------------------------------------------
# 4. Average Rating by Year
# ----------------------------------------------------------------------------
elif view == "Average Rating by Year":
    st.header("Average Rating of Albums Every Year")

    avg_by_year = df.groupby("Year")["Rating"].mean().reset_index()

    fig, ax = plt.subplots()
    ax.plot(avg_by_year["Year"], avg_by_year["Rating"], marker="o", color="royalblue")

    slope, intercept, r_value, p_value, std_err = linregress(
        avg_by_year["Year"], avg_by_year["Rating"]
    )
    best_fit = slope * avg_by_year["Year"] + intercept
    ax.plot(avg_by_year["Year"], best_fit, color="green", linewidth=2,
            label=f"Best Fit (slope={slope:.3f})")
    ax.axhline(average_score, color="red", linestyle="--", linewidth=2,
               label=f"Overall Average: {average_score:.2f}")
    ax.set_title("Average Rating of Albums Every Year")
    ax.set_xlabel("Year Released")
    ax.set_ylabel("Average Rating")
    ax.legend()
    st.pyplot(fig)

    st.dataframe(avg_by_year.rename(columns={"Rating": "Average Rating"}))

# ----------------------------------------------------------------------------
# 5. Box Plot by Album Type
# ----------------------------------------------------------------------------
elif view == "Ratings by Album Type (Box Plot)":
    st.header("Ratings by Album Type")

    types = df["Type"].unique()
    data_by_type = [df[df["Type"] == t]["Rating"] for t in types]

    fig, ax = plt.subplots()
    ax.boxplot(data_by_type, labels=types)
    ax.axhline(average_score, color="red", linestyle="--", linewidth=2,
               label=f"Overall Average: {average_score:.2f}")
    ax.set_title("Ratings by Album Type")
    ax.set_xlabel("Type")
    ax.set_ylabel("Rating")
    ax.legend()
    st.pyplot(fig)

    st.write("**Counts by type:**")
    st.dataframe(df["Type"].value_counts().rename("Count"))

# ----------------------------------------------------------------------------
# 6. Shapiro-Wilk Normality Test
# ----------------------------------------------------------------------------
elif view == "Normality Test (Shapiro-Wilk)":
    st.header("Is My Rating Distribution Normal?")

    stat, p_value = shapiro(df["Rating"])
    st.write(f"**Shapiro-Wilk statistic:** {stat:.4f}")
    st.write(f"**p-value:** {p_value:.4g}")

    if p_value < 0.05:
        st.warning(
            "The p-value is below 0.05, so we reject the idea that ratings are "
            "normally distributed. The normal curve on the histogram is a useful "
            "visual reference, but not a statistically accurate model of your data."
        )
    else:
        st.success(
            "The p-value is above 0.05, so we fail to reject normality — your "
            "ratings are plausibly consistent with a normal distribution."
        )

# ----------------------------------------------------------------------------
# 7. ANOVA across Album Types
# ----------------------------------------------------------------------------
elif view == "ANOVA: Rating by Type":
    st.header("Do Ratings Differ Significantly by Album Type?")

    types = df["Type"].unique()
    groups = [df[df["Type"] == t]["Rating"] for t in types]

    stat, p_value = f_oneway(*groups)
    st.write(f"**F-statistic:** {stat:.4f}")
    st.write(f"**p-value:** {p_value:.4g}")

    if p_value < 0.05:
        st.success(
            "There IS a statistically significant difference in average rating "
            "between at least some album types (p < 0.05)."
        )
    else:
        st.info(
            "No statistically significant difference in average rating between "
            "album types (p ≥ 0.05) — any differences you see could be chance."
        )

    st.write("**Average rating by type:**")
    st.dataframe(df.groupby("Type")["Rating"].mean().rename("Average Rating"))
