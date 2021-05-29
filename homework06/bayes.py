from collections import defaultdict, Counter
from math import log

import string

def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator).lower()

class NaiveBayesClassifier:

    def __init__(self, alpha):
        self.alpha = alpha
        self.words_counts = defaultdict(Counter)
        self.labels_counts = Counter()

        self.words = set()
        self.labels = set()

        self.probs = defaultdict(lambda: defaultdict(lambda: 0))
        self.labels_probs = dict()

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """

        for i in range(len(X)):
            self.labels.add(y[i])

            self.labels_counts[y[i]] += 1

            for word in clean(X[i]).split(" "):
                word = word.lower()

                self.words.add(word)

                self.words_counts[y[i]][word] += 1

        for label in self.labels:
            self.labels_probs[label] = self.labels_counts[label] / len(y) 
        
        for word in self.words:
            for label in self.labels:
                self.probs[label][word] =                                                               \
                    (self.words_counts[label][word] + self.alpha) /                                     \
                    (sum(self.words_counts[l][word] for l in self.labels) + self.alpha * len(self.words))

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        y = []

        for x in X:
            max_prob = float('-inf')
            max_label = None

            for label in self.labels:
                prob = log(self.labels_probs[label])
                for word in clean(x).split(" "):
                    if self.probs[label][word] != 0:
                        prob += log(self.probs[label][word])
                
                if prob >= max_prob:
                    max_prob = prob
                    max_label = label

            y.append(max_label)

        return y

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        y = self.predict(X_test)

        rights = 0

        for i in range(len(y)):
            if y[i] == y_test[i]:
                rights += 1
        
        return rights / len(y)

if __name__ == "__main__":
    import csv

    with open("data/SMSSpamCollection") as f:
        data = list(csv.reader(f, delimiter="\t"))

    X, y = [], []
    for target, msg in data:
        X.append(clean(msg))
        y.append(target)

    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

    model = NaiveBayesClassifier(alpha=0.05)
    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))
