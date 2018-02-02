import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import pydotplus

iris_feature_E='sepal length', 'sepal width', 'petal length', 'petal width'
iris_feature=u'花萼长度', u'花萼宽度', u'花瓣长度', u'花瓣宽度'
iris_class='Iris-setosa', 'Iris-versicolor', 'Iris-virginica'

if __name__=="__main__":
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    
    path=r'C:\Users\mashiji\Desktop\iris.data'
    data=pd.read_csv(path,header=None)
    x,y=np.split(data,(4,),axis=1)
    y=pd.Categorical(data[4]).codes
    # 为了可视化，仅使用前两列特征
    x=x.iloc[:,:2]
    x_train,x_test,y_train,y_test=train_test_split(x,y,train_size=0.7,random_state=1)
    print(y_test.shape)
    
    # 决策树参数估计
    # min_samples_split = 10：如果该结点包含的样本数目大于10，则(有可能)对其分支
    # min_samples_leaf = 10：若将某结点分支后，得到的每个子结点样本数目都大于10，则完成分支；否则，不进行分支
    model=DecisionTreeClassifier(criterion='entropy')
    model.fit(x_train,y_train)
    y_test_hat=model.predict(x_test)
    
    with open('iris.dot', 'w') as f:
        tree.export_graphviz(model, out_file=f)
    N,M=50,50
    x1_min,x2_min=x.min()
    x1_max,x2_max=x.max()
    t1=np.linspace(x1_min,x1_max,N)
    t2 = np.linspace(x2_min, x2_max, M)
    x1,x2=np.meshgrid(t1,t2)
    x_show=np.stack((x1.flat,x2.flat),axis=1)
    print(x_show.shape)
    
    cm_light = mpl.colors.ListedColormap(['#A0FFA0', '#FFA0A0', '#A0A0FF'])
    cm_dark = mpl.colors.ListedColormap(['g', 'r', 'b'])
    y_show_hat=model.predict(x_show)
    print(y_show_hat.shape)
    print(y_show_hat)
    y_show_hat=y_show_hat.reshape(x1.shape)
    print(y_show_hat)
    
    plt.figure(facecolor='w')
    plt.pcolormesh(x1,x2,y_show_hat,cmap=cm_light)
    plt.scatter(x_test[0],x_test[1],c=y_test.ravel(),edgecolors='k',s=150,zorder=10,cmap=cm_dark, marker='*')
    plt.scatter(x[0],x[1],c=y.ravel(),edgecolors='k',s=40,cmap=cm_dark)
    plt.xlabel(iris_feature[0],fontsize=15)
    plt.ylabel(iris_feature[1],fontsize=15)
    plt.xlim(x1_min,x1_max)
    plt.ylim(x2_min,x2_max)
    plt.grid(True)
    plt.title(u'鸢尾花数据的决策树分类', fontsize=17)
    plt.show()
    
    # 训练集上的预测结果
    y_test=y_test.reshape(-1)
    print(y_test)
    print(y_test_hat)
    
    result=(y_test==y_test_hat)
    acc=np.mean(result)
    print('准确度:%.2f%%' % (100*acc))
    
    #过拟合：错误率
    depth=np.arange(1,15)
    err_list=[]
    for d in depth:
        clf=DecisionTreeClassifier(criterion='entropy',max_depth=d)
        clf.fit(x_train,y_train)
        y_test_hat=clf.predict(x_test)
        result=(y_test_hat==y_test)
        if d==1:
            print(result)
        err=1-np.mean(result)
        err_list.append(err)
        print(d,'错误率:%.2f%%' % (100*err))
    plt.figure(facecolor='w')
    plt.plot(depth,err_list,'r-',lw=2)
    plt.xlabel(u'决策树深度', fontsize=15)
    plt.ylabel(u'错误率', fontsize=15)
    plt.title(u'决策树深度与过拟合', fontsize=17)
    plt.show()