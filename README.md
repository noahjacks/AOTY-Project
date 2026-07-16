Album of the Year Project

If you want to check out my profile and follow me:
https://www.albumoftheyear.org/user/-raven/
(I would recommend an adblocker)

Album of the Year (AOTY) is an online album rating and discussion forum created in 2008. AOTY allows users to individually write reviews and score albums; these scores are compiled for users to show to friends and for general record-keeping. AOTY also allows these scores to be downloaded as a CSV file so the data can be processed. Albums are rated on a scale of 0–100.

In this project, I've taken my own CSV file of scores after a year and a half of rating albums and processed the data to discover trends about my listening and rating habits, using a variety of statistical tests.

Graphs & Tests Included

This project includes an interactive dashboard with the following views:


Distribution of Scores
Plots the frequency of the scores I give as a histogram, with a normal distribution curve overlaid for comparison. This is shown by default on my AOTY profile; however, I recreated it so I could determine additional stats, such as the standard deviation, skewness, and kurtosis.
Album Rating Based on the Date I Rated Them
Plots the score of an album against the date I rated it, with a least-squares line of best fit, to see whether I've reviewed albums more negatively or positively on average over time.
Album Rating Based on Year of Release
Plots my rating of albums against the year an album came out, with a line of best fit, to help answer the age-old question: is new music truly worse than older music?
Average Rating of Albums Released Each Year
Shows which years of music I liked the most (and least) on average, with a trend line across years.
Ratings by Album Type (Box Plot)
Compares the spread of ratings across EPs, LPs, Live albums, and Unreleased albums.
Normality Test (Shapiro-Wilk)
Tests whether my ratings are statistically consistent with a normal distribution, rather than just assuming so from the histogram shape.
ANOVA: Rating by Type
Tests whether the average rating actually differs significantly between album types, or whether any differences are just chance.


Data

The dashboard reads from AOTY_Ratings.csv, which contains the following columns:

ColumnDescriptionAlbum NameTitle of the albumTypeEP, LP, Live, or UnreleasedArtistArtist nameRatingMy score, 0–100Date RatedThe date I rated the albumYearYear the album was released

Project Structure

your-repo/
├── app.py
├── requirements.txt
├── AOTY_Ratings.csv
└── README.md

How to Run


Clone the repository and make sure app.py, requirements.txt, and AOTY_Ratings.csv are all in the same folder:


   git clone https://github.com/yourusername/your-repo.git
   cd your-repo


Install the required packages:


   pip install -r requirements.txt


Launch the dashboard:


   streamlit run app.py


Your browser should open automatically to a local address (usually http://localhost:8501). Use the sidebar to switch between graphs and statistical tests.


Statistical Approach

I'm running statistical tests (linear regression significance, Shapiro-Wilk, one-way ANOVA) to determine whether any of the trends I find in my rating habits are statistically significant, or if I'm just making things up.
