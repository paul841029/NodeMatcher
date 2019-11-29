class Train(object):
    def fit(self, train_trees):
        raise NotImplemented

    def predict(self, test_trees):
        raise NotImplemented


class Naive(Train):
    def __init__(self):
        self.trained_model = None

    def fit(self, train_trees):
        pass

    def predict(self, test_trees):
        return 1, 1, 1
