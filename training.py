import pandas as pd
import error_analysis_
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, GridSearchCV
from sklearn.preprocessing import StandardScaler

X = pd.read_csv('features_train.csv')
X_test = pd.read_csv('features_test.csv')
y = pd.read_csv('target_train.csv').values.ravel()
y_test = pd.read_csv('target_test.csv').values.ravel()

scaler = StandardScaler()
X = scaler.fit_transform(X)
X_test = scaler.fit_transform(X_test)

print('LOGREG')

params_grid = {'C': [.1, 1, 10], 'solver': ['lbfgs', 'liblinear']}
model = LogisticRegression(max_iter=500)
grid = GridSearchCV(param_grid=params_grid, estimator=model, scoring='f1', cv=5)
grid.fit(X, y)
print(grid.best_estimator_, grid.best_score_)


model = grid.best_estimator_
"""scores = cross_val_score(model, X, y, cv=5, scoring='precision')
print(np.mean(scores), scores)"""
model.fit(X, y)
"""y_pred = model.predict(X)
error_analysis_.metrics(y, y_pred)
error_analysis_.plot_confusion_matrix(y, y_pred)
y_pred_df = cross_val_predict(model, X, y, cv=5, method="decision_function")
error_analysis_.plot_precision_recall(y, y_pred_df, versus=True)
error_analysis_.plot_roc_curve(y, y_pred_df)"""

y_pred = model.predict(X_test)
error_analysis_.metrics(y_test, y_pred)
error_analysis_.plot_confusion_matrix(y_test, y_pred)
y_pred_df = cross_val_predict(model, X_test, y_test, cv=5, method="decision_function")
error_analysis_.plot_precision_recall(y_test, y_pred_df, versus=True)
error_analysis_.plot_roc_curve(y_test, y_pred_df)





