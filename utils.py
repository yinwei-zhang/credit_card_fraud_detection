import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn import pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

def read_data(PATH):
    df = pd.read_csv(PATH)
    X, y = df.drop('Class', axis=1), df['Class']
    # use y as the label for stratify and keep the proportion of the class in the train and test dataset
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=2023, stratify=y)
    return Xtrain, Xtest, ytrain, ytest

def get_preprocessor():
    attributes = ['Amount', 'Time']
    num_processor = pipeline.Pipeline(steps=([('imputer', SimpleImputer(strategy='median')),
                                              ('robust_scaler', RobustScaler())]))
    preprocessor = ColumnTransformer([('num', num_processor, attributes)], remainder='passthrough')
    return preprocessor


def get_model(MODEL_NAME, CV_STRATEGY):
    if MODEL_NAME == 'logistic_regression':
        PARAMS = {'penalty': ['l2', 'l1'],
                  'C': [0.01, 1, 100, 10000]}
        MODEL =GridSearchCV(estimator=LogisticRegression(solver='liblinear'), param_grid=PARAMS, cv= CV_STRATEGY)

    elif MODEL_NAME == 'random_forest':
        PARAMS = {'max_depth': [3, 7, 11],
                  'n_estimators': [10, 30, 70]}

        MODEL = GridSearchCV(estimator=RandomForestClassifier(), param_grid=PARAMS, cv= CV_STRATEGY)

    elif MODEL_NAME == 'gradient_boost':
        PARAMS = {'max_depth': [3, 7, 11],
                  'n_estimators': [10, 30, 70]}
        MODEL = GridSearchCV(estimator=GradientBoostingClassifier(subsample = 0.3), param_grid=PARAMS, cv= CV_STRATEGY)
        #MODEL = RandomizedSearchCV(GradientBoostingClassifier(), PARAMS, n_iter=n_iter)

    else:
        raise Exception('Sorry, there is no such model in the database')

    return MODEL


def draw_plot(ax, precision, recall):
    # Draw the precision-recall curve
    ax.step(recall, precision, color='r', alpha=0.2,
             where='post')
    ax.fill_between(recall, precision, step='post', alpha=0.2,
                     color='#F59B00')
    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    ax.set_ylim([0.0, 1.05])
    ax.set_xlim([0.0, 1.0])
    return
