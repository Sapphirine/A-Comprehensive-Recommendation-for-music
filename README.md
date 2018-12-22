# A-Comprehensive-Recommendation-for-music
### A description and introduction about final project of EECS 6893 Big Data Analysis
- For this project, it has been finished by Zheyao Gao (uni:zg2308) and Jinyang Li (uni:jl5173).
- We created a recommendation system for music with Collaborative Filtering, Cosine Similarity and Pricinple Components Analysis.
- Also we visualize our songs with colors (RGB features) in our applications.

Our Youtube Link is (public):https://youtu.be/NgmXX_LrvjA 


Our Github Link is (github):https://github.com/Sapphirine/A-Comprehensive-Recommendation-for-music

**Note:**
For the ratings.csv in the data:
  Because it's two large, you can fetch them in this website: http://labrosa.ee.columbia.edu/millionsong/. Or you can download them more directly through this github link:https://github.com/sastafford/million-song-dataset

## Abstract
- With the rapid development of the era of big data, information is gradually showing an overload state. As one of the most effective methods to implement the balance of interests between information producers and consumers in recent years, the recommendation system (also known as personalized content distribution) play more and more important roles in recent years. According to estimates by Wall Street analysts, the purchase Conversion Rate[1] of Amazon can be as high as 60%. Therefore, exploring how to implement and improve a personalized and comprehensive recommendation is more meaningful.

## Introduction about Package
- code (folder): The main source code of our project
  - webserver (folder)
  - als.ipynb
  - als.py
  - similarity.ipynb
- data (folder): The dataset that we used in the project and it also includes result file (csv)
  - raw dataset:
    - features.csv
    - ratings.csv (too large to upload here, this is the website where we fetch them http://labrosa.ee.columbia.edu/millionsong/
    - song_info.csv
  - result csv file:
    - Top 10.csv
    - CF_Recommendation.csv
    - similarity.csv
