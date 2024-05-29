# TMDB_analysis_assesment
# Movie Data Analysis

This repository contains an analysis of movie data extracted from two APIs, processed using ETL techniques, and analyzed with pandas in Jupyter Notebook.

## Overview

We extracted data from movie and genre APIs, cleaned and transformed it using an ETL pipeline, and loaded it into a SQLite database. The analysis focused on various aspects of movie data over the past 10 years.

## Data Extraction and Cleaning

- **APIs Used:** Movie list API and Genre API
- **ETL Process:**
  - Extracted data from APIs
  - Transformed data: handled missing values, normalized formats
  - Loaded data into SQLite database using pandas

## Analysis

Using pandas, we analyzed the data to answer several key questions:

1. **Most Votes by Year:** Identified the year with the highest vote count for movies.
2. **Common Genres:** Determined the most common genres in the past 10 years.
3. **Most Popular Movie:** Found the most popular movie in the past 10 years.
4. **Language Distribution:** Analyzed the distribution of movie languages.
5. **Average Voting per Year:** Calculated the average voting for movies each year.
6. **Movie Release Months:** Identified the months with the highest number of movie releases.

## Key Findings

- **Year with Most Votes:** [specific year]
- **Most Common Genre:** [genre]
- **Most Popular Movie:** [movie title]
- **Language Distribution:** [languages and their proportions]
- **Average Voting:** [average votes per year]
- **Peak Release Months:** [months]

## How to Use

1. **Run ETL Pipeline:** Execute `TMDB_assesment_project_pipeline.py` in Jupyter to extract, transform, and load the data.
2. **Analyze Data:** Open `TMDB_project_analysis.ipynb` to perform and visualize the analysis.

## Files

- `TMDB_assesment_project_pipeline.py`: Jupyter Notebook for ETL pipeline
- `TMDB_project_analysis.ipynb`: Jupyter Notebook for data analysis
- `movies.db`: SQLite database with the cleaned data
- `README.md`: This file

## Conclusion

This project provides insights into movie trends over the past decade, helping to understand voting patterns, genre popularity, and release schedules.

## License

Licensed under the MIT License.

