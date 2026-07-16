#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 13:42:00 2026

@author: noahjackson
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

def label_and_show(title, xlabel, ylabel):
    if title == "Distribution of Ratings":
        plt.axvline(average_score, color='red', linestyle='--', linewidth=2, label=f'Average: {average_score:.2f}')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
    else:
        plt.axhline(average_score, color='red', linestyle='--', linewidth=2, label=f'Average: {average_score:.2f}')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()


df = pd.read_csv('AOTY_Ratings.csv')

average_score = df['Rating'].mean()

df['Date Rated'] = pd.to_datetime(df['Date Rated'])

bin_edges = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
df['Rating'].hist(bins=bin_edges, color='royalblue', edgecolor='black')



# Plot histogram, capture bin info to help scale the curve
counts, edges, patches = plt.hist(df['Rating'], bins=bin_edges, color='royalblue', edgecolor='black')

# Fit a normal distribution to your data
mu, std = df['Rating'].mean(), df['Rating'].std()

# Generate smooth x values across the rating range, then the normal curve's y values
x = np.linspace(0, 110, 300)
p = norm.pdf(x, mu, std)

# Scale the curve to match histogram counts (not density)
bin_width_avg = np.mean(np.diff(edges))
p_scaled = p * len(df['Rating']) * bin_width_avg

plt.plot(x, p_scaled, color='black', linewidth=2, label=f'Normal Dist (μ={mu:.1f}, σ={std:.1f})')

plt.axvline(average_score, color='red', linestyle='--', linewidth=2, label=f'Average: {average_score:.2f}')
plt.legend()
label_and_show('Distribution of Ratings', 'Rating', 'Frequency')

plt.scatter(df['Year'], df['Rating'], alpha=0.5)
slope, intercept = np.polyfit(df['Year'], df['Rating'], 1)
best_fit_line = slope * df['Year'] + intercept
plt.plot(df['Year'], best_fit_line, color='black', linewidth=3, label=f'Best Fit (slope={slope:.3f})')
label_and_show('Album Ratings Based on Year Released', 'Year', 'Rating')

plt.scatter(df['Date Rated'], df['Rating'], alpha=0.5)
plt.xticks(rotation=45)
label_and_show('Album Ratings Based on Date Rated', 'Date Rated', 'Rating')

avg_by_year = df.groupby('Year')['Rating'].mean().reset_index()
avg_by_year.plot(kind='line', x='Year', y='Rating', marker='o', color='royalblue')
label_and_show('Average Rating of Albums Every Year', 'Year', 'Average Rating')
