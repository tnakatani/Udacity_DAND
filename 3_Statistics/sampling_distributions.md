# Sampling Distributions

## Sampling Distributions
- Sampling Distributions are the distribution of a statistic (any statistic).
- There are two very important mathematical theorems that are related to sampling distributions: The Law of Large Numbers and The Central Limit Theorem.
- The Law of Large Numbers states that as a sample size increases, the sample mean will get closer to the population mean. In general, if our statistic is a "good" estimate of a parameter, it will approach our parameter with larger sample sizes.
- The Central Limit Theorem states that with large enough sample sizes our sample mean will follow a normal distribution, but it turns out this is true for more than just the sample mean.

## Bootstrapping
- Bootstrapping is a technique where we sample from a group with replacement.
- We can use bootstrapping to simulate the creation of sampling distribution.
- By bootstrapping and then calculating repeated values of our statistics, we can gain an understanding of the sampling distribution of our statistics.

## Confidence Intervals
In this video, you saw an example of how to build a confidence interval using the sampling distribution of the statistic that best estimates your parameter of interest. In this case, we used a sample mean height to estimate the population mean height.

You can interpret your confidence interval as *We are 95% confident, the population mean falls between the bounds that you find*. Notice that the percent and the parameter can both change depending on what you are building your confidence interval for, and what percentage you cutoff in each tail.

## Confidence Intervals in Difference
In this video, you built a confidence interval for the difference of the average heights for coffee drinkers and non-coffee drinkers. The interval was built at a 95% confidence level, and since the difference did not contain zero, this suggested there was truly a difference in the average heights in the population of coffee drinkers as compared to non-coffee drinkers.

Specifically, we can be 95% confident that the *difference in the average heights for coffee drinkers as compared to non-coffee drinkers was in the provided interval of 0.59 to 2.37 inches.*

Notice the similarity of the wording to the last confidence interval you built. The highlighted portions signify the two parts that can change in your conclusions:

- The confidence level.
- The parameter you are capturing with your interval.

## Confidence Intervals and Sample Size
It is important to understand the way that your sample size and confidence level relate to the confidence interval you achieve at the end of your analysis.

Assuming you control all other items of your analysis:

1) Increasing your sample size will decrease the width of your confidence interval.
2) Increasing your confidence level (say 95% to 99%) will increase the width of your confidence interval.

You saw that you can compute:

1) The confidence interval width as the difference between your upper and lower bounds of your confidence interval.
2) The margin of error is half the confidence interval width, and the value that you add and subtract from your sample estimate to achieve your confidence interval final results.

## Confidence Intervals (& Hypothesis Testing) vs. Machine Learning
Confidence intervals take an aggregate approach towards the conclusions made based on data, as these tests are aimed at understanding population parameters (which are aggregate population values).

Alternatively, machine learning techniques take an individual approach towards making conclusions, as they attempt to predict an outcome for each specific data point.

In the final lessons of this class, you will learn about two of the most fundamental machine learning approaches used in practice: linear and logistic regression.

## Recap
In this lesson, you learned:

1) How to use your knowledge of bootstrapping and sampling distributions to create a confidence interval for any population parameter.

2) You learned how to build confidence intervals for the population mean and difference in means, but really the same process can be done for any parameter you are interested in.

3) You also learned about how to use python built-in functions to build confidence intervals, but that these rely on assumptions like the Central Limit Theorem.

4) You learned about the difference between statistical significance and practical significance.

5) Finally, you learned about other language associated with confidence intervals like margin of error and confidence interval width, and how to correctly interpret your confidence intervals. Remember, confidence intervals are about parameters in a population, and not about individual observations.
