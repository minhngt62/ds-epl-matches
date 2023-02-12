# English Premier Leagues Matches and Starting Lineups

The English Premier League, commonly referred to as the EPL, is the top tier of professional football in England and one of the most popular and widely followed football leagues in the world. It was founded in 1992 and consists of 20 clubs playing 38 matches each, for a total of 380 matches in a season. The league operates on a promotion and relegation system, with the bottom three clubs being relegated to the second tier of English football and being replaced by the top three clubs from that division. Over the years, the Premier League has become known for its high levels of competitiveness, world-class players, and intense rivalries between clubs. The league attracts a huge following both domestically and internationally, and its matches are broadcast to millions of viewers in over 200 countries.

Currently, there are many differernt prediction schemas for match results but a strategy that aims to forecast a match result from the beginning is rarely seen. Therefore, we focus on the starting lineups of both teams (home and away) in a match, exploiting the player statistics to gain insights into how the lineup tactics (e.g., positions, formation,...) affect the final match result and, perform prediction (win/lose/draw).

**For more details, please read the report provided in folder `reports`.**

<p align="center">
  <img src="https://user-images.githubusercontent.com/86721208/218306170-72ec837d-917e-4b1b-ae14-a31a989f38e1.jpg" />
</p>

## Introduction to Data Science - DSAI K65: Group 17
1. Nguyễn Tống Minh (Email: minh.nt204885@sis.hust.edu.vn)
2. Nguyễn Công Đạt (Email: dat.nc200137@sis.hust.edu.vn)
3. Hoàng Long Vũ (Email: vu.hl204897@sis.hust.edu.vn)
4. Lý Nhật Nam (Email: nam.ln204886@sis.hust.edu.vn)

## Project Structure

```
data/                       # where to store the data
-- ./scraping/              # raw data collected from the website
-- ./tabular/               # saved processed data by each step
notebook                    # jupyter notebooks for the pipeline
-- ./images/                # figures from the notebooks
-- ./models/                # all trained models from modelling
reports                     # project report
README.md           
```
---

# Setup

To rerun the notebooks, you will need to install the specific setup below. We suggest you use [`Anaconda`](https://www.anaconda.com/) for this project. One to note is that hyperparameter tunning of the notebook for modelling takes a lot of time to run completely.

1. Install [`Python 3`](https://www.python.org/downloads/) (above $3.6$).
2. Change the working directory to the project root, then install required packages and libraries:
    ```
    pip install -r requirements.txt
    ```
