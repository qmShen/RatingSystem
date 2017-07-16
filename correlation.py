from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Perceptron
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge

def calc_pearsonr(arr1 ,arr2):
    if len(arr1) != len(arr2):
        print('Unequal length')
        return False, False
    arr_no_none1 = []
    arr_no_none2 = []
    for index in range(len(arr1)):
        if arr1[index] == None or arr2[index] == None:
            continue
        arr_no_none1.append(arr1[index])
        arr_no_none2.append(arr2[index])

    if len(arr_no_none1) <= 1 or len(arr_no_none2) <= 1:
        return False, False
    # print(arr_no_none1, arr_no_none2)
    return pearsonr(arr_no_none1, arr_no_none2)

def linear_regression():
    with open('data/results_w_values.csv', 'r') as input:
        schema_line = input.readline()
        schemas = schema_line.split(',')
        schemas = [schema.strip() for schema in schemas]
        raw_X = []
        raw_Y = []
        item_line = input.readline()
        while item_line:
            items = item_line.split(',')
            items = [item.strip() for item in items]

            values = [float(item) for item in items[7:12]]
            raw_X.append(values)

            raw_Y.append(float(items[6]))
            item_line = input.readline()
        print(len(raw_X), len(raw_X[0]))

        fit_X = [[(x / 100) for x in x_arr]for x_arr in raw_X]
        max_y = max(raw_Y)
        min_y = min(raw_Y)
        fit_Y = [(y - min_y) / (max_y - min_y) for y in raw_Y]
        fit_X = raw_X
        fit_Y = raw_Y
        l_reg = linear_model.LinearRegression(fit_intercept=False)
        l_reg.fit(fit_X, fit_Y)

        print(schemas)
        print(l_reg.coef_)
        print("Mean squared error: %.2f" % np.mean((l_reg.predict(fit_X) - fit_Y) ** 2))

        # model = PolynomialFeatures(degree=2)
        # model.fit(fit_X, fit_Y)
        # print('powers', model.n_input_features_)
        # print('n_input_features_', model.powers_)
        # print('n_output_features_', model.n_output_features_)

        model = make_pipeline(PolynomialFeatures( degree=3), linear_model.LinearRegression(fit_intercept=False))
        model.fit(fit_X, fit_Y)

        print('c', model.steps[1][1].coef_)
        print("Mean squared error: %.2f" % np.mean((model.predict(fit_X) - fit_Y) ** 2))
        # print("Mean squared error: %.2f" % np.mean((model.predict(fit_X) - fit_Y) ** 2))
        # clf = Perceptron(fit_intercept=False, n_iter=10, shuffle=False).fit(X, fit_Y)
        # clf.predict(X)
        # clf.score(X, fit_Y)
def cal_correlation():
    with open('data/results_w_values.csv', 'r') as input:
        schema_line = input.readline()
        schemas = schema_line.split(',')
        schemas = [schema.strip() for schema in schemas]
        data_list = [[] for schema in schemas]
        item_line = input.readline()
        while item_line:
            items = item_line.split(',')
            items = [item.strip() for item in items]
            for index in range(len(schemas)):
                _value = float(items[index]) if index >= 1 else items[index]
                data_list[index].append(_value)
            item_line = input.readline()

        rank = [index for index in range(len(data_list[0]))]
        scores = data_list[6]
        features = data_list[7:]
        for feature in features:
            result = calc_pearsonr(scores, feature)
            print(result)
        result = calc_pearsonr(rank, feature)

        print(schemas)
        result = calc_pearsonr(features[0], features[1])

        plt.scatter(features[0], scores,  color='blue', s=1)
        plt.xticks(())
        plt.yticks(())

        plt.show()

if __name__ == "__main__":
    linear_regression()
    # X = [[1,2,3]]
    # poly = PolynomialFeatures(degree=2)
    # print(poly.fit_transform(X))