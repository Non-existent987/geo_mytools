#!/usr/bin/env python
# coding: utf-8

import pandas as pd

# from sklearn import neighbors
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import cross_val_score

class MySklearn(object):

    def classification_function(self,
                                data_good, 
                                data_bad, 
                                good_x = ['RRU经度','RRU纬度'], 
                                good_y = '地市',
                                bad_x = ['RRU经度','RRU纬度'],
                                bad_y = 'city',
                                n_neighbors = 50,
                                cv = 20):
        '''
            机器学习分类方法：
            最初用在根据经纬度判断属于那一个地市
            接收两个表格，一个所有经纬度都有对应的地市
            一个经纬度没有对应的地市
            输出没有对应地市的结果
            res = classification_function(data_good, 
                                data_bad, 
                                good_x = ['RRU经度','RRU纬度'], 
                                good_y = '地市',
                                bad_x = ['RRU经度','RRU纬度'])
        '''
        from sklearn import neighbors
        from sklearn.preprocessing import LabelEncoder
        from sklearn.model_selection import cross_val_score
        knn=neighbors.KNeighborsClassifier(n_neighbors=n_neighbors,weights='distance')#根据距离 50代表的是周边选取50个进行比较，少数服从多数
        #knn=neighbors.KNeighborsClassifier(n_neighbors=50,weights='uniform')#根据权重0代表的是周边选取50个进行比较，少数服从多数

        le=LabelEncoder() # 初始化label
        le.fit(data_good[good_y])#使用，有确定方案的数据 唯一列
        le.fit(data_good[good_y]) #使用，有确定方案的数据 唯一列
        y=le.transform(data_good[good_y])##用离散值转化标签值
        x=data_good[good_x] # 使用，有确定方案的数据 可多列
        #logistic中的scoring参数指定为accuracy
        
        
        scores=cross_val_score(knn,x,y,cv=cv,scoring='accuracy')#
        knn.fit(x,y)
        score = knn.score(x,y)
        print('训练集准确度：',score)
        data_bad[bad_y]=le.inverse_transform(knn.predict(data_bad[bad_x]))
        return data_bad
    def classification_function_data_one(self,
                                        data, 
                                        col_x = ['RRU经度','RRU纬度'], 
                                        col_y = '地市',
                                        n_neighbors = 50,
                                        cv = 20):
        '''
            机器学习分类方法，根据经纬度判断归属的地市
            输入一个表格有经纬度和地市，经纬度不能缺失
            根据经纬度判断地市为空的那些数据，并填充

            res = classification_function_data_one(data, 
                                        col_x = ['RRU经度','RRU纬度'], 
                                        col_y = '地市')
        '''
        from sklearn import neighbors
        from sklearn.preprocessing import LabelEncoder
        from sklearn.model_selection import cross_val_score
        knn=neighbors.KNeighborsClassifier(n_neighbors=n_neighbors,weights='distance')#根据距离 50代表的是周边选取50个进行比较，少数服从多数
        #knn=neighbors.KNeighborsClassifier(n_neighbors=50,weights='uniform')#根据权重0代表的是周边选取50个进行比较，少数服从多数
        data_x = data.loc[data[col_y].notna()].reset_index(drop=True)
        data_y = data.loc[data[col_y].isna()].reset_index(drop=True)
        le=LabelEncoder() # 初始化label
        le.fit(data_x[col_y])#使用，有确定方案的数据 唯一列
        y=le.transform(data_x[col_y])##用离散值转化标签值
        x=data_x[col_x] # 使用，有确定方案的数据 可多列
        #logistic中的scoring参数指定为accuracy
        scores=cross_val_score(knn,x,y,cv=cv,scoring='accuracy')#
        knn.fit(x,y)

        data_y[col_y]=le.inverse_transform(knn.predict(data_y[col_x]))
        data = data_x.append(data_y)
        return data