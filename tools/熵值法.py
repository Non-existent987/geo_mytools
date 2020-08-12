import pandas as pd

class EmtropyMethod:
    def __init__(self, index, positive, negative, row_name):
        if len(index) != len(row_name):
            raise Exception('数据指标行数与行名称数不符')
        if sorted(index.columns) != sorted(positive+negative):
            raise Exception('正项指标加负向指标不等于数据指标的条目数')

        self.index = index.copy().astype('float64')
        self.positive = positive
        self.negative = negative
        self.row_name = row_name
        
    def uniform(self):
        uniform_mat = self.index.copy()
        min_index = {column:min(uniform_mat[column]) for column in uniform_mat.columns}
        max_index = {column:max(uniform_mat[column]) for column in uniform_mat.columns}
        for i in range(len(uniform_mat)):
            for column in uniform_mat.columns:
                if column in self.negative:
                    uniform_mat[column][i] = (uniform_mat[column][i] - min_index[column]) / (max_index[column] - min_index[column])
                else:
                    uniform_mat[column][i] = (max_index[column] - uniform_mat[column][i]) / (max_index[column] - min_index[column])

        self.uniform_mat = uniform_mat
        return self.uniform_mat
        
    def calc_probability(self):
        try:
            p_mat = self.uniform_mat.copy()
        except AttributeError:
            raise Exception('你还没进行归一化处理，请先调用uniform方法')
        for column in p_mat.columns:
            sigma_x_1_n_j = sum(p_mat[column])
            p_mat[column] = p_mat[column].apply(lambda x_i_j: x_i_j / sigma_x_1_n_j if x_i_j / sigma_x_1_n_j != 0 else 1e-6)

        self.p_mat = p_mat
        return p_mat
                 
    def calc_emtropy(self):
        try:
            self.p_mat.head(0)
        except AttributeError:
            raise Exception('你还没计算比重，请先调用calc_probability方法')

        import numpy as np
        e_j  = -(1 / np.log(len(self.p_mat)+1)) * np.array([sum([pij*np.log(pij) for pij in self.p_mat[column]]) for column in self.p_mat.columns])
        ejs = pd.Series(e_j, index=self.p_mat.columns, name='指标的熵值')

        self.emtropy_series = ejs
        return self.emtropy_series
        
    def calc_emtropy_redundancy(self):
        try:
            self.d_series = 1 - self.emtropy_series
            self.d_series.name = '信息熵冗余度'
        except AttributeError:
            raise Exception('你还没计算信息熵，请先调用calc_emtropy方法')

        return self.d_series
            
    def calc_Weight(self):
        self.uniform()
        self.calc_probability()
        self.calc_emtropy()
        self.calc_emtropy_redundancy()
        self.Weight = self.d_series / sum(self.d_series)
        self.Weight.name = '权值'
        return self.Weight
            
    def calc_score(self):
        self.calc_Weight()

        import numpy as np
        self.score = pd.Series(
            [np.dot(np.array(self.index[row:row+1])[0], np.array(self.Weight)) for row in range(len(self.index))],
            index=self.row_name, name='得分'
        ).sort_values(ascending=False)
        return self.score

if __name__ == '__main__':
	df= pd.read_csv('e.csv', encoding='gbk')
	df = df.dropna().reset_index(drop=True)
	#如果编辑解释器不是jupyter-notebook或命令行，用print函数包裹下面的代码
	# print(df.head())

	indexs = ["GDP总量增速", "人口总量", "人均GDP增速", "地方财政收入总额", "固定资产投资", "社会消费品零售总额增速", "进出口总额","城镇居民人均可支配收入", "农村居民人均可支配收入"]

	Positive = indexs
	Negative = []

	province = df['地区']
	index = df[indexs]

	em = EmtropyMethod(index, Negative, Positive, province)
	print(em.calc_score())