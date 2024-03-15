import pandas as pd
import math as math
from sklearn.linear_model import LinearRegression, LogisticRegression #, SGDRegressor, Lasso, LassoCV, Ridge, RidgeCV, ElasticNet, ElasticNetCV
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import ConfusionMatrixDisplay
from yellowbrick.classifier import ClassPredictionError
import matplotlib.pyplot as plt

class Models:

    def __init__(self) -> None:
        pass
    

    def logistic_regression(self, x_train : pd.DataFrame, x_test : pd.DataFrame, y_train : pd.Series, y_test : pd.Series):

        self.__shape_validation(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

        print("Logistic Regression : ", end="\n\n")
        logistic_reg = LogisticRegression()
        logistic_reg.fit(x_train, y_train)

        train_pred = logistic_reg.predict(x_train)
        test_pred = logistic_reg.predict(x_test)

        train_acc = accuracy_score(y_train, train_pred)
        test_acc = accuracy_score(y_test, test_pred)

        logistic_reg_model = logistic_reg
        y_pred_proba_logistic = logistic_reg_model.predict_proba(x_test)[:, 1]
        return logistic_reg, train_acc, test_acc, y_pred_proba_logistic

    def xgbclassifier(self, reg_lambda: float, reg_alpha: float, learning_rate: float, max_depth: int, x_train : pd.DataFrame, x_test : pd.DataFrame, y_train : pd.Series, y_test : pd.Series):

        self.__shape_validation(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

        model_name = "XGB Classifier"
        print("xgbclassifier : ", end="\n\n")
        xgbclassifier = XGBClassifier(
                            reg_lambda = reg_lambda,
                            reg_alpha = reg_alpha,
                            learning_rate = learning_rate,
                            max_depth = max_depth
                        )
        xgbclassifier.fit(x_train, y_train)

        train_pred_xgb = xgbclassifier.predict(x_train)
        test_pred_xgb = xgbclassifier.predict(x_test)

        train_acc_xgb = accuracy_score(y_train, train_pred_xgb)
        test_acc_xgb = accuracy_score(y_test, test_pred_xgb)

        xgbclassifier_model = xgbclassifier
        y_pred_proba_xgb = xgbclassifier_model.predict_proba(x_test)[:, 1]

        self.display_classificiation_metrics(xgbclassifier, x_test, y_test, model_name)

        self.class_prediction_error(x_train, x_test, x_test, y_test, xgbclassifier, 'XGBClassifier')
        return train_acc_xgb, test_acc_xgb, y_pred_proba_xgb

    
    def linear_regression_ols(self, x_train : pd.DataFrame, x_test : pd.DataFrame, y_train : pd.Series, y_test : pd.Series):

        self.__shape_validation(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

        print("Linear Regression OLS Model : ", end="\n\n")
        ols = LinearRegression()
        ols.fit(x_train,y_train)
        print('RMSE in Train: '+str(round(math.sqrt(mean_squared_error(y_train,ols.predict(x_train))),2)))
        print('R2 in Train: '+str(round(r2_score(y_train,ols.predict(x_train)),2)))

        print('RMSE in Test: '+ str(round(math.sqrt(mean_squared_error(y_test,ols.predict(x_test))),2)))
        print('R2 in Test: '+ str(round(r2_score(y_test,ols.predict(x_test)),2)))
    

    def __shape_validation(self, x_train_shape : tuple, x_test_shape : tuple, y_train_shape : tuple, y_test_shape : tuple):
        if(x_train_shape[0] != y_train_shape[0]):
            raise Exception("Train Dataset Size Mismatch")
        if(x_test_shape[0] != y_test_shape[0]):
            raise Exception("Test Dataset Size Mismatch")

    def display_classificiation_metrics(self, trained_classifier, X_test, y_test, model_name=""):
        y_test_predicted = trained_classifier.predict(X_test)
        #display confusion matrix
        ConfusionMatrixDisplay.from_predictions(y_test, y_test_predicted)
        plt.title(f'confusion matrix for {model_name} test data')
        plt.show()
        #print precision, recall, f1_score with respect to class with label 1 and accuracy
        print("classification report for test data:\n")
        print(classification_report(y_test, y_test_predicted))

    def class_prediction_error(self, x_train: pd.DataFrame, y_train: pd.DataFrame, x_test: pd.DataFrame, y_test: pd.DataFrame, model, model_name: str):
        visualizer = ClassPredictionError(model,  classes=['low', 'high'])

        # Fit the training data to the visualizer
        visualizer.fit(x_train, y_train)

        # Evaluate the model on the test data
        visualizer.score(x_test, y_test)

        # Draw visualization
        visualizer.show()
