# Album of the Year Project

[Album of the Year](https://www.albumoftheyear.org) (AOTY) is an online album rating and discussion forum created in 2008. AOTY allows users to individually write reviews and score albums; these scores are compiled for users to show to friends and for general record-keeping. AOTY also allows these scores to be downloaded as a CSV file so the data can be processed. Albums are rated on a scale of 0–100.

If you want to check out my profile and follow me:
https://www.albumoftheyear.org/user/-raven/
(I would recommend an adblocker)

In this project, I took my own CSV file of scores after a year and a half of rating albums and processed the data to discover trends about my listening and rating habits using a variety of statistical tests.

**Note:** As I listen to and review more albums (which is frequently), I will try to update the CSV file in the project to reflect the changes. As of writing, I have rated 174 albums.

## Graphs & Tests Included

This project includes an interactive dashboard with the following views:

1. **Distribution of Scores**
   Plots the frequency of the scores I give as a histogram, with a normal distribution curve overlaid for comparison, plus a table showing exact album counts per rating range. Also includes a **Shapiro-Wilk Normality Test**, which checks whether my ratings are statistically consistent with a normal distribution, rather than just assuming so from the histogram shape. This view is shown by default on my AOTY profile; however, I recreated it so I could determine additional stats, such as the standard deviation, skewness, and kurtosis.

2. **Album Rating Based on the Date I Rated Them**
   Plots the score of an album against the date I rated it, with a least-squares line of best fit, to see whether I've reviewed albums more negatively or positively on average over time.

3. **Album Rating Based on Year of Release**
   Plots my rating of albums against the year an album came out, with a line of best fit, to help answer the age-old question: is new music truly worse than older music?

4. **Average Rating of Albums Released Each Year**
   Shows which years of music I liked the most (and least) on average, with a trend line across years.

5. **Ratings by Album Type (Box Plot)**
   Compares the spread of ratings across EPs, LPs, Live albums, and Unreleased albums. Also includes a **one-way ANOVA test**, which checks whether the average rating actually differs significantly between album types, or whether any differences are just chance.

Every section includes a plain-English "How this works" explanation of the statistics involved.

## Data

The dashboard reads from `AOTY_Ratings.csv`, which contains the following columns:

| Column | Description |
|---|---|
| Album Name | Title of the album |
| Type | EP, LP, Live, or Unreleased |
| Artist | Artist name |
| Rating | My score, 0–100 |
| Date Rated | The date I rated the album |
| Year | Year the album was released |

**Note:** the "Ratings by Album Type" view and its ANOVA test depend on the `Type` column being populated. If you're adapting this project with your own export and that column comes through empty or missing, that section won't work correctly until it's filled in.

## Project Structure

```text
your-repo/
├── app.py
├── requirements.txt
├── AOTY_Ratings.csv
└── README.md
```

## How to Run

1. **Clone the repository** and make sure `app.py`, `requirements.txt`, and `AOTY_Ratings.csv` are all in the same folder:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install the required packages:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. **Launch the dashboard:**
   ```bash
   streamlit run app.py
   ```
5. Your browser should open automatically to a local address (usually `http://localhost:8501`). Use the sidebar to switch between graphs and statistical tests.

## Statistical Approach

I'm running statistical tests (linear regression significance, Shapiro-Wilk, one-way ANOVA) to determine whether any of the trends I find in my rating habits are statistically significant, or if I'm just making things up.
