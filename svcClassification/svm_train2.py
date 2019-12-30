# coding:utf-8
import warnings
from time import time
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import make_scorer
import pickle


import sys
import os
last_path = os.path.dirname(os.getcwd())
sys.path.append(os.path.join(last_path,'data'))
from get_data import *

warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn", lineno=193)

warnings.filterwarnings("ignore", module="sklearn", lineno=241)

model_path = os.path.join(last_path,r'model')

def ml_svc(X, y):
    """
    svc 算法
    :param X: 训练集
    :param y: 标签
    :param model_name: 模型名
    :return: 1.model
    """
    # 定义模型名
    model_name = '2.model'

    log_name = 'history.log'


    # 取出部分样例划分 训练集（寻参用） 和 测试集（评估用），进行 网格寻参 以及 评估模型

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

    # 网格寻参范围
    param_grid = {
        'C': [2 ** i for i in range(-3, 15, 2)],
        # 'degree':[j for j in range(3,6)],
        # 'C': [2 ** i for i in range(-5, 15, 2)],
        'gamma': [2 ** i for i in range(3, -15, -2)],
    }
    #  param_grid = {
    #     'C': [1e3, 5e3, 1e4, 5e4, 1e5],
    #     'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1],
    # }

    # 定义模型
    svc = SVC(kernel='rbf',class_weight='balanced',probability=True) #,max_iter=50000000

    # 定义用于网格寻参的对象，每次锁定一组参数，进行5折交叉验证，评定标准为 f1 score
    clf = GridSearchCV(svc, param_grid, scoring='f1', n_jobs=4, cv=3) #10 4
    # --------------------
    # 开始在数据集 X_train, y_train 上进行网格寻参
    clf.fit(X_train, y_train)
    #
    # # 打印最优的参数
    # print(clf.best_estimator_)
    #
    # # 评估模型，这里的原理是利用最优参数对应的模型进行预测
    y_pred = clf.predict(X_test)
    a = classification_report(y_test, y_pred)
    b = confusion_matrix(y_test, y_pred)

    #
    #-------------------
    # model.fit(X_train,y_train)
    # y_pred=model.predict(X_test)
    # print(classification_report(y_test, y_pred))
    # print(confusion_matrix(y_test, y_pred))




    # # 重新定义 svc 模型
    svc = SVC(kernel='rbf',
        C=clf.best_params_['C'],gamma=clf.best_params_['gamma'], class_weight='balanced',probability=True) #, gamma=clf.best_params_['gamma'] ,max_iter=5000000

    # # 训练模型
    model = svc.fit(X, y)
    #
    # # # 打印模型信息
    # # print(model)
    #
    # # 打印最优的参数
    print('best_estimator_:',clf.best_estimator_)
    #
    # # 评估模型，这里的原理是利用最优参数对应的模型进行预测
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    with open(log_name,'w') as f:
        f.write('11111:\n%s\n%s\n22222\n%s\n%s\n%s'%(str(a),str(b),str(classification_report(y_test, y_pred)),str(confusion_matrix(
            y_test,y_pred)),str(clf.best_estimator_)))

    #
    # # 保存模型
    with open( os.path.join(model_path,r'1226_2.model'), 'wb') as f:
        pickle.dump(model, f)
    return model

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    data, label = get_labeldata()
    ml_svc(data,label)