import matplotlib.pyplot as plt

plt.rcParams.update(
    {
        "figure.facecolor": (1.0, 0.0, 0.0, 0.0),  # red   with alpha = 30%
        "axes.facecolor": (0.0, 1.0, 0.0, 0.0),  # green with alpha = 50%
        "savefig.facecolor": (0.0, 0.0, 1.0, 0.0),  # blue  with alpha = 20%
    }
)


def sentiment_piechart(sentiment_scores):
    print(sentiment_scores)
    labels, frequencies = ["positive", "neutral", "negative"], []
    for label in labels:
        frequencies.append(sentiment_scores[label])
    colors = ["#A0EE2A", "#FFE000", "#F85634"]
    f, ax = plt.subplots()
    ax.pie(frequencies, labels=labels, colors=colors)

    return f
