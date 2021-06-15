"""Code for loading trained models in the web app. The TrainedModel class
provides a unified prediction interface for models from different libraries."""

import pandas as pd
import xgboost as xgb
from typing import Optional


class TrainedModel:
    def __init__(
        self,
        model,
        year: int,
        library: str,
        X_test: Optional[pd.DataFrame] = None,
        y_test: Optional[pd.Series] = None,
    ) -> None:
        self.model = model
        self.year = year
        self.library = library
        self._X_test = X_test
        self._y_test = y_test

    def get_predictions(self):
        if self.X_test is None or self.y_test is None:
            raise Exception("Test data not supplied.")
        if self.library == "xgboost":
            dtest = xgb.DMatrix(self.X_test, label=self.y_test)
            y_pred = self.model.predict(dtest)
            y_pred = pd.DataFrame(y_pred, index=self.y_test.index)
            y_pred.columns = ["churn_pred"]
            return y_pred
        if self.library == "sklearn":
            results = pd.DataFrame(self.model.predict_proba(self.X_test), index=self.y_test.index)
            y_pred = results.iloc[:, 1]
            y_pred.columns = ["churn_pred"]
            return y_pred
        else:
            raise Exception(f"Library {self.library} is not yet implemented.")

    @property
    def X_test(self):
        return self._X_test

    @X_test.setter
    def X_test(self, X_test):
        self._X_test = X_test

    @property
    def y_test(self):
        return self._y_test

    @y_test.setter
    def y_test(self, y_test):
        self._y_test = y_test


def load_xgboost_model(filename):
    bst = xgb.Booster()
    bst.load_model(filename)
    return bst
