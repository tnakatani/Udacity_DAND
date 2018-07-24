# Intro to Data Analysis Practice

## Jupyter

### Magic Keywords
Special commands you can run in cells that let you control the notebook itself.

1. [`%matplotlib`](https://matplotlib.org/users/index.html) - for visualization
  - On higher resolution screens such as Retina displays, the default images in notebooks can look blurry. Use `%config InlineBackend.figure_format = 'retina'` after `%matplotlib` inline to render higher resolution images.
2. [`%timeit`](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-timeit) - for code run time
3. [`%pdb`](https://docs.python.org/3/library/pdb.html) - for interactive debugging

### Converting Notebooks / Creating Slideshows
- To convert a notebook to an HTML file, use [nbconvert](https://nbconvert.readthedocs.io/en/latest/usage.html) command
  ```
  jupyter nbconvert --to html notebook.ipynb
  ```
- To create the slideshow from the notebook file, you'll need to use nbconvert:
  ```
  jupyter nbconvert notebook.ipynb --to slides
  ```
- To convert and immediately see the slideshow, use:
  ```
  jupyter nbconvert notebook.ipynb --to slides --post serve
  ```

## Data Analysis Process

1. **Question**: Either you're given data and ask questions based on it, or you ask questions first and gather data based on that later.
  -In both cases, great questions help you focus on relevant parts of your data and direct your analysis towards meaningful insights.
2. **Wrangle**: You get the data you need in a form you can work with in three steps: gather, assess, clean.
  - You gather the data you need to answer your questions, assess your data to identify any problems in your data’s quality or structure,.
  - Clean your data by modifying, replacing, or removing data to ensure that your dataset is of the highest quality and as well-structured as possible.
3. **Explore**: aka EDA (Exploratory Data Analysis), you explore and then augment your data to maximize the potential of your analyses, visualizations, and models.
  - Finding patterns in your data, visualizing relationships in your data, and building intuition about what you’re working with.
  - After exploring, you can do things like remove outliers and create better features from your data, also known as feature engineering.
4. **Draw Conclusions**: This step is typically approached with machine learning or inferential statistics, which will focus on drawing conclusions with descriptive statistics.
5. **Communicate**: You often need to justify and convey meaning in the insights you’ve found. Or, if your end goal is to build a system, you usually need to share what you’ve built, explain how you reached design decisions, and report how well it performs.
  - There are many ways to communicate your results: reports, slide decks, blog posts, emails, presentations, or even conversations. Data visualization will always be very valuable.
