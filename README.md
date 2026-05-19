# Job Search Email Automation

An automated job search pipeline that scrapes company contact information from PitchBook and sends personalized cold outreach emails to companies in target industries and locations. Built to solve a personal problem during post-graduation job search.

## Background

After graduating with a CS and Data Science degree, traditional job applications were yielding low response rates. Built this tool to programmatically identify companies in target industries (financial services, real estate, fintech) within target geographic areas, extract decision-maker contact information, and send personalized cold emails asking about data analyst and data science opportunities. The approach successfully landed a full-time Data Analyst role.

## Features

- Automated UW-Madison institutional login flow via Selenium WebDriver
- PitchBook search results scraping across paginated company listings
- Email extraction from company profiles
- Pagination handling to scrape across multiple result pages
- Welcome popup auto-dismissal
- Duplicate email filtering
- CSV export with formatted spacing for downstream email campaigns

## Tech Stack

- Python
- Selenium WebDriver (browser automation)
- webdriver-manager (automated ChromeDriver setup)
- Pandas (data export)

## How It Works

1. Authenticates through UW-Madison's NetID Single Sign-On
2. Logs into PitchBook through the institutional EzProxy
3. Navigates to pre-filtered search results (filtered by industry, location, company size)
4. Iterates through all result pages
5. Extracts mailto: links from each page
6. Deduplicates and exports to CSV
7. CSV is then used as input for a separate personalized email outreach script

## Results

The automation enabled outreach to hundreds of companies that wouldn't have been feasible to research manually. The targeted approach resulted in significantly higher response rates than mass-applying through job boards, and ultimately led to landing a Data Analyst position at a Milwaukee-based real estate finance firm.

## Note

This project was built for personal job search purposes using credentials I had legitimate access to as a UW-Madison student. The repository excludes the email sending portion which contained personal SMTP credentials and outreach templates.
