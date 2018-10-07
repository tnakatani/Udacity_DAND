# A/B Testing

A/B tests are used to test changes on a web page by running an experiment where a **control group** sees the old version, while the **experiment group** sees the new version. A metric is then chosen to measure the level of engagement from users in each group. These results are then used to judge whether one version is more effective than the other. A/B testing is very much like hypothesis testing with the following hypotheses:

- **Null Hypothesis: The new version is no better, or even worse, than the old version**
- **Alternative Hypothesis: The new version is better than the old version**

If we fail to reject the null hypothesis, the results would suggest keeping the old version. If we reject the null hypothesis, the results would suggest launching the change. These tests can be used for a wide variety of changes, from large feature additions to small adjustments in color, to see what change maximizes your metric the most.

A/B testing also has its drawbacks. It can help you compare two options, but it can't tell you about an option you haven’t considered. It can also produce bias results when tested on existing users, due to factors like change aversion and novelty effect.

- **Change Aversion**: Existing users may give an unfair advantage to the old version, simply because they are unhappy with change, even if it’s ultimately for the better.
- **Novelty Effect**: Existing users may give an unfair advantage to the new version, because they’re excited or drawn to the change, even if it isn’t any better in the long run.

## Case Study - Website Click Through Rate
The first change Audacity wants to try is on their homepage. They hope that this new, more engaging design will increase the number of users that explore their courses, that is, move on to the second stage of the funnel.

The metric we will use is the click through rate for the Explore Courses button on the home page. Click through rate (CTR) is often defined as the the number of clicks divided by the number of views. Since Audacity uses cookies, we can identify unique users and make sure we don't count the same one multiple times. For this experiment, we'll define our click through rate as:

**CTR: # clicks by unique users / # views by unique users**

Now that we have our metric, let's set up our null and alternative hypotheses:

**H<sub>0</sub>: CTR<sub>new</sub> ​ ≤ CTR<sub>old</sub>**

**H<sub>1</sub>: CTR<sub>new</sub>​ > CTR<sub>old</sub>**
​	 

Our alternative hypothesis is what we want to prove to be true, in this case, that the new homepage design has a higher click through rate than the old homepage design. And the null hypothesis is what we assume to be true before analyzing data, which is that the new homepage design has a click through rate that is less than or equal to that of the old homepage design. As you’ve seen before, we can rearrange our hypotheses to look like this:

**H<sub>0</sub>: CTR<sub>new</sub> - CTR<sub>old</sub> ​ ≤ 0**

**H<sub>1</sub>: CTR<sub>new</sub> -​ CTR<sub>old</sub> > 0**

## Recap
Again, let's recap the steps we took to analyze the results of this A/B test.

- We computed the **observed difference** between the metric, average reading duration, for the control and experiment group.
- We simulated the **sampling distribution** for the difference in means (or average reading durations).
We used this sampling distribution to simulate the **distribution under the null hypothesis**, by creating a random normal distribution centered at 0 with the same spread and size.
- We computed the **p-value** by finding the proportion of values in the null distribution that were greater than our observed difference.
- We used this p-value to determine the **statistical significance** of our observed difference.

## Drawing Conclusions
Since the Bonferroni method is too conservative when we expect correlation among metrics, we can better approach this problem with more sophisticated methods, such as the [closed testing procedure](http://en.wikipedia.org/wiki/Closed_testing_procedure), [Boole-Bonferroni bound](http://en.wikipedia.org/wiki/Bonferroni_bound), and the [Holm-Bonferroni method](http://en.wikipedia.org/wiki/Holm%E2%80%93Bonferroni_method). These are less conservative and take this correlation into account.

If you do choose to use a less conservative method, just make sure the assumptions of that method are truly met in your situation, and that you're not just trying to [cheat on a p-value](http://freakonometrics.hypotheses.org/19817). Choosing a poorly suited test just to get significant results will only lead to misguided decisions that harm your company's performance in the long run.

## Difficulties in A/B Testing
As you saw in the scenarios above, there are many factors to consider when designing an A/B test and drawing conclusions based on its results. To conclude, here are some common ones to consider.

- Novelty effect and change aversion when existing users first experience a change
- Sufficient traffic and conversions to have significant and repeatable results
Best metric choice for making the ultimate decision (eg. measuring revenue vs. clicks)
- Long enough run time for the experiment to account for changes in behavior based on time of day/week or seasonal events.
- Practical significance of a conversion rate (the cost of launching a new feature vs. the gain from the increase in conversion)
- Consistency among test subjects in the control and experiment group (imbalance in the population represented in each group can lead to situations like [Simpson's Paradox](https://en.wikipedia.org/wiki/Simpson%27s_paradox))

---

## How To's

### Bootstrapping
```python
# Create a sampling distribution of the difference in proportions
# with bootstrapping
diffs = []
size = df.shape[0]
for _ in range(10000):
    b_samp = df.sample(size, replace=True)
    control_df = b_samp.query('group == "control"')
    experiment_df = b_samp.query('group == "experiment"')
    control_ctr = control_df.query('action == "enroll"').count()[0] / control_df.query('action == "view"').count()[0]
    experiment_ctr = experiment_df.query('action == "enroll"').count()[0] / experiment_df.query('action == "view"').count()[0]
    diffs.append(experiment_ctr - control_ctr)  

# Convert to numpy array
diffs = np.asarray(diffs)

# Plot sampling distribution
plt.hist(diffs);     
```

### Calculate p-value
```python
# Simulate distribution under the null hypothesis
null_vals = np.random.normal(0, diffs.std(), diffs.size)

# Plot the null distribution
plt.hist(null_vals);

# Plot observed statistic with the null distibution
plt.hist(null_vals)
plt.axvline(obs_diff, c='red')

# Compute p-value
(null_vals > obs_diff).mean()
```
