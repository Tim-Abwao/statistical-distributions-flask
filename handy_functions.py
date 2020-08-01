import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
from datetime import datetime
from statistics import mean, median, stdev, mode
from scipy.stats import (
    norm,
    poisson,
    bernoulli,
    uniform,
    geom,
    alpha,
    t,
    beta,
    chi2,
    expon,
    f,
    gamma,
    pareto,
    binom,
    nbinom,
)

distributions = {
    "Normal": norm,
    "Poisson": poisson,
    "Bernoulli": bernoulli,
    "Uniform": uniform,
    "Geometric": geom,
    "Alpha": alpha,
    "Beta": beta,
    "Chi-squared": chi2,
    "Exponential": expon,
    "F": f,
    "Gamma": gamma,
    "Pareto": pareto,
    "Student t": t,
    "Binomial": binom,
    "Negative Binomial":  nbinom
}


def validate_probability(p):
    """
    Ensures probabilities stick to the range 0<=p<=1 by assigning a default
    value of p=0.5 for entries greater than 1
    """
    return p if 0 <= p <= 1 else 0.5


def get_random_sample(distribution, size, *parameters):
    """
    Returns a random sample of size {size} with the given {parameters},
    for the specified {distribution}.
    """
    try:
        return distributions[distribution].rvs(*parameters, size=size)
    except KeyError:
        return 1


def clear_old_files(extension):
    old_files = glob.glob("static/files/*." + extension, recursive=True)
    for file in old_files:
        os.remove(file)


def get_graphs(data):
    """
    Plots  distribution graph of the random sample and saves it to a png file
    """
    # clear old graphs
    clear_old_files("png")
    # create time-stamped names for the graph image
    graph_names = [
        "files/" + str(datetime.now()) + f"_{kind}.png"
        for kind in ["distplot", "violinplot", "boxplot"]
    ]
    graph_loc = ["static/" + name for name in graph_names]
    sns.set()
    # Distribution plot
    plt.figure(figsize=(10, 6))
    sns.distplot(data, color="teal")
    plt.xticks(rotation=90)
    plt.title("Distribution plot", fontsize=25, fontweight=550, pad=20)
    plt.savefig(graph_loc[0], transparent=True)
    # Violin plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(data, color="#3FBFBF")
    plt.xticks(rotation=90)
    plt.title("Violin plot", fontsize=25, fontweight=550, pad=20)
    plt.savefig(graph_loc[1], transparent=True)
    # Box plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(data, color="#3FBFBF")
    plt.xticks(rotation=90)
    plt.title("Box plot", fontsize=25, fontweight=550, pad=20)
    plt.savefig(graph_loc[2], transparent=True)

    return graph_names


def floatInt_to_int(x):
    """
    Converts float values with zero fractional parts into integers
    """
    return int(x) if x % 1 == 0 else x


def descriptive_stats(random_sample):
    """
    Returns basic descriptive statistics for the random sample
    """
    try:
        _mean = floatInt_to_int(round(mean(random_sample), 4))
        _median = floatInt_to_int(round(median(random_sample), 4))
    except ValueError:
        _median = _mean = "No data to process."

    try:
        std = floatInt_to_int(round(stdev(random_sample), 4))
        _min = floatInt_to_int(round(min(random_sample), 4))
        _max = floatInt_to_int(round(max(random_sample), 4))
    except ValueError:
        std = _min = _max = "Not available. At least 2 data points required."

    try:
        _mode = floatInt_to_int(round(mode(random_sample), 4))
    except ValueError:
        _mode = "No unique mode."

    return [
        ("Mean: ", _mean),
        ("Median: ", _median),
        ("Mode: ", _mode),
        ("Standard Deviation: ", std),
        ("Minimum: ", _min),
        ("Maximum: ", _max),
    ]


if __name__ == '__main__':
    print(get_random_sample('F', 100, *[1, 2]))
