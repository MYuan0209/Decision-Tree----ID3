import pandas
import numpy


def read(path):
    data = pandas.read_csv(path, engine='python')
    label = data.columns[:-1]
    attribute = data.values[:, -1]
    data = data.values[:, :-1]
    return data, attribute, label


def probability(x):
    """
    求当前样本集合D中每一类样本所占的比例
    :param x:
    :return:
    """
    return [x[val == x].size / x.size for val in numpy.unique(x)]


def information_entropy(attribute):
    """
    求样本集合x的信息熵
    :param attribute: 结果 -> array
    :return: 结果的信息熵 -> float
    """
    p = probability(attribute)
    return -numpy.sum(p * numpy.log2(p))


def conditional_information_entropy(data, attribute):
    """
    求条件信息熵
    :param data: 输入 -> array
    :param attribute: 结果 -> array
    :return: 条件信息熵 -> array
    """
    return [numpy.sum([data[val == data].size / data.size * information_entropy(attribute[val == data])
                       for val in numpy.unique(data)]) for data in data.T]


def information_gain(data, attribute):
    """
    求信息增益
    :param data: 输入 -> array
    :param attribute: 结果 -> array
    :return: 每一列的信息增益 -> array
    """
    ent = information_entropy(attribute)
    ce = numpy.array(conditional_information_entropy(data, attribute))
    return ent - ce


def tree_generate(data, attribute, label):
    """
    产生决策树
    :param data: 输入 -> array
    :param attribute: 结果 -> array
    :param label: 列标签 -> Index
    :return: 决策树 -> dict
    """
    # 如果输入全属于同一类别或所有输入的结果取值相同，直接返回结果
    p = probability(attribute)
    if data.shape[1] == 1 or p[0] == 1:
        return attribute[numpy.argmax(p)]
    # 获得最大信息增益所对应的序号
    nodes = information_gain(data, attribute)
    max_index = nodes.argmax()
    # 建立树的根节点
    node = label[max_index]
    edge = {}
    tree = {node: edge}
    # 递归建立树的有向边
    cross_flag = numpy.ones(label.size, dtype=bool)
    cross_flag[max_index] = False
    for value in numpy.unique(data.T[max_index]):
        row_flag = value == data.T[max_index]
        edge[value] = tree_generate(data[row_flag][:, cross_flag], attribute[row_flag], label[cross_flag])
    return tree


def predict(tree, character, label):
    """
    预测函数
    :param tree: 决策树 -> dict
    :param character: 特征向量 -> array
    :param label: 列标签 -> Index
    :return: 预测结果
    """
    root = tree
    # 从根节点搜索到叶子节点
    while isinstance(root, dict):
        # 获得节点值对应的列标签序号
        node = [k for k in root.keys()][0]
        index = numpy.where(label == node)[0][0]
        # 将根节点改为对应序号的子节点
        edge = root[node]
        root = edge[character[index]]
    return root


def main():
    data_path = "data.csv"
    data, attribute, label = read(data_path)
    tree = tree_generate(data, attribute, label)
    print(tree)
    ans = [predict(tree, t, label) for t in data]
    print(ans)


if __name__ == '__main__':
    main()
