# Album of the Year Project

[Album of the Year](https://www.albumoftheyear.org) (AOTY) is an online album rating and discussion forum created in 2008. AOTY allows users to individually write reviews and score albums; these scores are compiled for users to show to friends and for general record-keeping. AOTY also allows these scores to be downloaded as a CSV file so the data can be processed. Albums are rated on a scale of 0–100.

In this project users are able to upload their own CSV files to a Streamlit application. A series of statistical tests described in detail below will be conducted. If a user does not have an AOTY account the application will default to my data. As of writing I have rating 194 albums.

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

## Troubleshooting & Permanent Setup

If your virtual environment becomes unusable (shebangs in `./.venv/bin/` point to a missing Python), it's usually because the venv was created at one absolute path and the project was moved or synced (e.g., via iCloud). For a durable setup, follow these recommendations:

- **Create the venv locally and don't move it.** Run from the project root:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- **If you move the project, recreate the venv** (don't try to reuse the old `.venv`).

- **Avoid placing the project in cloud-synced folders** (iCloud/Dropbox) when the venv is inside the project; syncing can change paths and break the venv. If you must use cloud storage, keep the venv outside the synced folder or recreate it after moving.

- **Alternative: use `pipx` for CLI tools** like Streamlit so you can run them globally without relying on a local venv:
```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install streamlit
streamlit run app.py
```

- **Use a Python version manager** (e.g., `pyenv`) if you work across multiple projects with different Python versions — that reduces environment friction.

- **Add `.venv` to `.gitignore`** so the venv isn't checked into Git accidentally.

With these practices you'll avoid the "No such file or directory" errors from broken shebangs in `./.venv/bin/*`.

## Statistical Approach

I'm running statistical tests (linear regression significance, Shapiro-Wilk, one-way ANOVA) to determine whether any of the trends I find in my rating habits are statistically significant, or if I'm just making things up.
