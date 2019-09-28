# PISA Data Exploration
## Taichi Nakatani


## Dataset

PISA is a survey of students' skills and knowledge as they approach the end of compulsory education. It is not a conventional school test. Rather than examining how well students have learned the school curriculum, it looks at how well prepared they are for life beyond school.

The dataset is quite massive with around 50,000 rows and approximately 600 columns. Trying to wrangle a dataset this large would be cumbersome, so I filtered down the dataset to specific data points I am interested in working with.

For this study, I'm interesting in exploring the following themes:
1. Cultural background of the student, and how that correlates with scores.
2. Family structure of the student, and how that correlates with scores.
2. Out-of-school study time, and how that correlates with scores.
3. Cross cultural comparisons of scores by country.


## Summary of Findings

### Correlation of Scores

In the exploration, I found that there was a strong correlation between any pair of test score averages. This is further evidenced by the correlation matrix, where all variable pairs have a correlation of around 0.9.  The relationship is
approximately linear between test score. This seems to imply that having a high test score on one test is strongly correlated with having a high score on another test.

While all of the correlation is high, there is a slightly lower correlation between reading and math scores. Judging by the data in the chart the order of correlation strength (from strongest to weakest) is as follows:
1. Math and Science
2. Reading and Science
3. Math and Reading

### Study Time versus Score

My first interest is to see if there is any interesting insights from exploring study time data and score data. Since there is a lot of data, I chose to go with a heatmap to display the data.

From the heatmap that I created, I observed that most students in both countries generally spend around 5 hours of outside study per week, and scores between the 400 and 600 mark.
There doesn't seem to be much of a correlation between study time and test scores as much as I'd expected. In general the chart reflects the general bell curve of scores and the rarity of study time spent over 10 hours.

### Cultural Background and Scores

As imagined, students who speak a different language at home than the language tested generally has a lower average score compared to those who speak the language of the test at home. Those who speak the language of the test at home generally peak around 500 and 550, while those who speak another language is slightly closer to 400. Surprisingly, the difference in scores was not as drastic as I expected it to be.

### Family Structure and Scores

The chart shows that the median distribution is higher for students where both parents are at home versus single parent or no parent for math and reading scores.  Additionally, there is a decidedly smaller difference between having both parents at home and a single parent at home than I expected. They both have a high concentration of students who have an average score in the high 500.  On the other hand, compare to the smaller difference between both parent and single parent family structure, having no parent at home significantly lowers the average scores of the student, where the mean is down to approximately 400.

### Distribution of Scores by Country

Comparing the distribution of scores between Japan and USA, Japan has a higher averages score for both Math and Reading compared to the United States. This difference is the most pronounced in Math, where Japan surpasses the United States by around 50 points.  On the other hand, United States has a higher average of Science scores which was somewhat surprising to see.  Judging by the plot, United States surpasses Japan by around 50 points in regards to Science scores.

## Key Insights for Presentation

For the presentation, I focus on just the factor of cultural background and family structure, and how that affects the overall score of the student.

I start by introductions of the dataset and notes on any adjustments I made to the dataset prior to creating the charts that follow.  I also state what sort of analysis I am interested in pursuing.

I initially show the violinplot that shows the relationship between the language spoken at home by the student and how that affects their reading score.  This is then followed by the violinplot that shows how a student's family structure could affect their score.  I think these two charts were the strong insights that I was able to find about how background affects the students score.  The final chart is a cross-analysis of test score averages between Japan and USA, to drive home how your upbringing (in a national sense) can also affect the outcome of the score.  I chose to use pairgrid plot using seaborn to put the USA and Japan scores side by side.  Each plot is shown with different colors to emphasize that they are different datapoints.

#### Resources Used:
- https://pandas.pydata.org/pandas-docs/stable/
- https://seaborn.pydata.org
- https://www.oecd.org/pisa/pisaproducts/PISA-2012-technical-report-final.pdf
- https://catherineh.github.io/programming/2016/05/24/seaborn-pairgrid-tips
