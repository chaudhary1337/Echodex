import matplotlib.pyplot as plt


def sentiment_piechart(sentiment_scores):
    print(sentiment_scores)
    labels, frequencies = ['positive', 'neutral', 'negative'], []
    for label in labels:
        frequencies.append(sentiment_scores[label])
    colors = ['green', 'yellow', 'red']
    f, ax = plt.subplots()
    ax.pie(frequencies, labels=labels, colors=colors)

    return f
