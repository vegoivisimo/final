import pandas as pd
import numpy as np
  # Set backend for Spyder
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix


def plot_confusion_matrix(y, y_predict, model_name):
    cm = confusion_matrix(y, y_predict)
    plt.figure()
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax)
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title(f'Confusion Matrix - {model_name}')
    ax.xaxis.set_ticklabels(['did not land', 'land'])
    ax.yaxis.set_ticklabels(['did not land', 'landed'])
    plt.tight_layout()
    plt.savefig(f'confusion_matrix_{model_name.lower().replace(" ", "_")}.png')
    plt.close()


url1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
url2 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv"
try:
    data = pd.read_csv(url1)
    X = pd.read_csv(url2)
except Exception as e:
    print(f"Error loading datasets: {e}")
    exit(1)


Y = data['Class'].to_numpy()


transform = preprocessing.StandardScaler()
X = transform.fit_transform(X)


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
print(f"Test set size: {Y_test.shape[0]} samples")


parameters_lr = {'C': [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}
lr = LogisticRegression()
logreg_cv = GridSearchCV(lr, parameters_lr, cv=10)
logreg_cv.fit(X_train, Y_train)
print("Logistic Regression - Best parameters:", logreg_cv.best_params_)
print("Logistic Regression - CV Accuracy:", logreg_cv.best_score_)


logreg_accuracy = logreg_cv.score(X_test, Y_test)
print("Logistic Regression - Test Accuracy:", logreg_accuracy)

yhat_lr = logreg_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat_lr, "Logistic Regression")


parameters_svm = {
    'kernel': ('linear', 'rbf', 'poly', 'sigmoid'),
    'C': np.logspace(-3, 3, 5),
    'gamma': np.logspace(-3, 3, 5)
}
svm = SVC()
svm_cv = GridSearchCV(svm, parameters_svm, cv=10)
svm_cv.fit(X_train, Y_train)
print("SVM - Best parameters:", svm_cv.best_params_)
print("SVM - CV Accuracy:", svm_cv.best_score_)


svm_accuracy = svm_cv.score(X_test, Y_test)
print("SVM - Test Accuracy:", svm_accuracy)


yhat_svm = svm_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat_svm, "SVM")


parameters_tree = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_depth': [2*n for n in range(1, 10)],
    'max_features': ['sqrt', None],  # 'auto' is deprecated
    'min_samples_leaf': [1, 2, 4],
    'min_samples_split': [2, 5, 10]
}
tree = DecisionTreeClassifier()
tree_cv = GridSearchCV(tree, parameters_tree, cv=10)
tree_cv.fit(X_train, Y_train)
print("Decision Tree - Best parameters:", tree_cv.best_params_)
print("Decision Tree - CV Accuracy:", tree_cv.best_score_)


tree_accuracy = tree_cv.score(X_test, Y_test)
print("Decision Tree - Test Accuracy:", tree_accuracy)


yhat_tree = tree_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat_tree, "Decision Tree")


parameters_knn = {
    'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
    'p': [1, 2]
}
knn = KNeighborsClassifier()
knn_cv = GridSearchCV(knn, parameters_knn, cv=10)
knn_cv.fit(X_train, Y_train)
print("KNN - Best parameters:", knn_cv.best_params_)
print("KNN - CV Accuracy:", knn_cv.best_score_)


knn_accuracy = knn_cv.score(X_test, Y_test)
print("KNN - Test Accuracy:", knn_accuracy)

yhat_knn = knn_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat_knn, "KNN")


accuracies = {
    'Logistic Regression': logreg_accuracy,
    'SVM': svm_accuracy,
    'Decision Tree': tree_accuracy,
    'KNN': knn_accuracy
}
best_model = max(accuracies, key=accuracies.get)
print("\nModel Comparison:")
for model, acc in accuracies.items():
    print(f"{model}: {acc:.4f}")
print(f"\nBest performing model: {best_model} with test accuracy {accuracies[best_model]:.4f}")

print("\nConfusion matrices saved as PNG files in the working directory.")