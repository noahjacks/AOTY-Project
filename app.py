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

    with st.expander("ℹ️ How this works"):
        st.markdown(
            """
This histogram groups every rating into a 10-point bucket (0–9, 10–19, ... 100)
and counts how many albums fall into each one.

The **black curve** is a normal distribution (bell curve) fitted to the data's
own mean (μ) and standard deviation (σ), then scaled up so its height matches
the histogram's raw counts instead of a 0–1 probability density. It's a visual
reference for "what a perfectly normal version of this data would look like" —
it does not prove the data actually is normal (see the Shapiro-Wilk test for that).

- **Mean:** the average rating.
- **Standard deviation:** how spread out the ratings are around the mean —
  a small value means most ratings cluster close together; a large value means
  they're spread across a wide range.
- **Skewness:** measures asymmetry. 0 is perfectly symmetric; positive means a
  longer tail of high outlier scores, negative means a longer tail of low ones.
- **Kurtosis:** measures how "peaked" or "flat" the distribution is compared to
  a normal curve. Positive means more values clustered near the mean with a
  sharper peak; negative means a flatter, more spread-out shape.
"""
        )

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

    with st.expander("ℹ️ How this works"):
        st.markdown(
            """
This is a **least squares linear regression**. It finds the straight line
`y = slope · x + intercept` that minimizes the sum of squared vertical
distances between every actual point and the line. Squaring the errors keeps
them all positive (so they don't cancel out) and penalizes big misses more
than small ones. There's a direct formula for the best slope and intercept —
no guessing or trial-and-error involved.

- **Slope:** how much the average rating changes per year of release. A
  slope near 0 means release year barely matters to your ratings.
- **R² (R-squared):** the percentage of variation in Rating explained by
  Year. A low R² (e.g. 0.05) means year explains very little — most of the
  scatter in your ratings comes from something other than release year.
- **p-value:** tests whether the true slope could plausibly be zero (i.e.,
  no real relationship) and what you're seeing is just random scatter.
  A p-value under 0.05 means that's unlikely, so the trend is probably real;
  above 0.05 means the "trend" could easily be coincidence.
"""
        )

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

    with st.expander("ℹ️ How this works"):
        st.markdown(
            """
Same **least squares linear regression** as the Year Released plot, but here
the x-axis is the date you rated each album (converted to a plain number of
days via `toordinal()`, since regression math needs numbers, not calendar
dates) and the fitted line is converted back to real dates for display.

- **Slope:** the average change in rating per **day** that passes — a tiny
  number is expected here since ratings rarely swing much day to day, so it's
  more useful to think of it scaled up (e.g., slope × 365 ≈ change per year).
- **R² and p-value:** interpreted the same way as before — R² is how much of
  the rating variation this date trend explains, and the p-value tells you
  whether the slope is likely a real drift in your habits or just noise.
"""
        )

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

    with st.expander("ℹ️ How this works"):
        st.markdown(
            """
This groups every album by its release year and takes the **mean rating**
within each year — so each point is an average of however many albums you
rated from that year, not an individual album.

The green best-fit line is the same least squares regression as before, just
fit across these yearly averages instead of every individual rating. Because
it's fit to fewer points (one per year, rather than one per album), it
answers a slightly different question: "is there a trend in how I rate
entire years on average," rather than "is there a trend across every single
album I've rated."
"""
        )

# ----------------------------------------------------------------------------
# 5. Box Plot by Album Type
# ----------------------------------------------------------------------------
elif view == "Ratings by Album Type (Box Plot)":
    st.header("Ratings by Album Type")

    types = df["Type"].unique()
    data_by_type = [df[df["Type"] == t]["Rating"] for t in types]

    fig, ax = plt.subplots()
    ax.boxplot(data_by_type, tick_labels=types)
    ax.axhline(average_score, color="red", linestyle="--", linewidth=2,
               label=f"Overall Average: {average_score:.2f}")
    ax.set_title("Ratings by Album Type")
    ax.set_xlabel("Type")
    ax.set_ylabel("Rating")
    ax.legend()
    st.pyplot(fig)

    st.write("**Counts by type:**")
    st.dataframe(df["Type"].value_counts().rename("Count"))

    with st.expander("ℹ️ How this works"):
        st.markdown(
            """
A box plot summarizes each album type's ratings using five numbers:

- **Median** (the line inside the box): the middle rating when all values for
  that type are sorted — less affected by outliers than the mean.
- **Box edges (Q1 and Q3):** the 25th and 75th percentiles — the middle 50%
  of ratings for that type fall inside the box.
- **Whiskers:** extend to the typical range of the data beyond the box.
- **Points beyond the whiskers:** individual outlier ratings.

This is more informative than just comparing averages, since two types can
have the same average rating but very different spreads — one consistent,
one all over the place. Check the counts table too: a type with very few
ratings can look dramatically different just from having less data to average.
"""
        )

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

    with st.expander("ℹ️ How this works"):
        st.markdown(
            """
The **Shapiro-Wilk test** checks whether a dataset plausibly came from a
normal (bell curve) distribution. It works by sorting your ratings and
comparing them against the values you'd expect to see, in that same sorted
order, if the data had been drawn from a perfect normal distribution with
your data's mean and standard deviation. The result is a statistic **W**
(between 0 and 1, where closer to 1 means a better match to normal).

The **p-value** attached to W tests the hypothesis "this data came from a
normal distribution":
- **p < 0.05:** reject that hypothesis — the data is *not* well described as
  normal (common for bounded, real-world scores like ratings, which often
  cluster around certain numbers or skew toward one end).
- **p ≥ 0.05:** not enough evidence to say it isn't normal.

This is a check on whether the smooth curve drawn over the histogram is a
statistically meaningful model of your ratings, or just a nice-looking
reference shape.
"""
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

    with st.expander("ℹ️ How this works"):
        st.markdown(
            """
**One-way ANOVA** (Analysis of Variance) tests whether the average ratings
of two or more groups (here: EP, LP, Live, Unreleased) are genuinely
different, or whether the differences you see could just be random chance.

It works by comparing two kinds of variance:
- **Between-group variance:** how spread out the group *averages* are from
  the overall average (e.g., is the EP average far from the LP average?).
- **Within-group variance:** how spread out individual ratings are *within*
  each type (e.g., how scattered are individual LP ratings around the LP
  average?).

```
F = (variance between group averages) / (variance within groups)
```

A large **F-statistic** means the gaps between group averages are big
relative to the natural scatter already present within each group — a
meaningful difference. A small F means the group averages could easily
differ just from ordinary noise, even if album type made no real difference.

The **p-value** converts F into a probability: it's the chance of seeing an
F this large (or larger) if album type had *no* real effect on rating at all.
- **p < 0.05:** at least one type's average rating is genuinely different.
- **p ≥ 0.05:** no solid evidence any type is rated differently.

Note that ANOVA only tells you *that* a difference exists somewhere among
the groups — not *which* specific pair of types differs. A follow-up
**Tukey's HSD test** would answer that, if you want that extra detail.
"""
        )