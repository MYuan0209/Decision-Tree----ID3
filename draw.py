import matplotlib.pyplot as plt
from pylab import mpl

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def retrieveTree(i):
    listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                   {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                   ]
    return listOfTrees[i]


def get_num_leafs(tree):
    """
    获取叶节点的数目和树的层数
    :param tree:
    :return:
    """
    num_leafs = 0
    first_side = list(tree.keys())
    first_str = first_side[0]
    second_dict = tree[first_str]
    for key in second_dict:
        if type(second_dict[key]).__name__ == 'dict':
            num_leafs += get_num_leafs(second_dict[key])
        else:
            num_leafs += 1
    return num_leafs


def get_tree_depth(tree):
    max_depth = 0
    first_side = list(tree.keys())
    first_str = first_side[0]
    second_dict = tree[first_str]
    for key in second_dict:
        if type(second_dict[key]).__name__ == 'dict':
            this_depth = 1 + get_tree_depth(second_dict[key])
        else:
            this_depth = 1
        if this_depth > max_depth:
            max_depth = this_depth
    return max_depth


def draw_node(node_txt, centerPt, parentPt, nodeType):
    draw_tree.ax1.annotate(node_txt, xy=parentPt, xycoords='axes fraction', xytext=centerPt, textcoords='axes fraction',
                           va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)


def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    draw_tree.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)


def plot_tree(myTree, parentPt, nodeTxt):
    num_leafs = get_num_leafs(myTree)
    depth = get_tree_depth(myTree)
    firstSide = list(myTree.keys())
    firstStr = firstSide[0]
    cntrPt = (plot_tree.xOff + (1.0 + float(num_leafs)) / 2.0 / plot_tree.totalW, plot_tree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    draw_node(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plot_tree.yOff = plot_tree.yOff - 1.0 / plot_tree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plot_tree(secondDict[key], cntrPt, str(key))
        else:
            plot_tree.xOff = plot_tree.xOff + 1.0 / plot_tree.totalW
            draw_node(secondDict[key], (plot_tree.xOff, plot_tree.yOff), cntrPt, leafNode)
            plotMidText((plot_tree.xOff, plot_tree.yOff), cntrPt, str(key))
    plot_tree.yOff = plot_tree.yOff + 1.0 / plot_tree.totalD


def draw_tree(tree):
    fig = plt.figure(facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    draw_tree.ax1 = plt.subplot(111, frameon=False, **axprops)
    plot_tree.totalW = float(get_num_leafs(tree))
    plot_tree.totalD = float(get_tree_depth(tree))
    plot_tree.xOff = -0.5 / plot_tree.totalW
    plot_tree.yOff = 1.0
    plot_tree(tree, (0.5, 1.0), '')
    mpl.rcParams["font.sans-serif"] = ["SimHei"]
    plt.show()


if __name__ == "__main__":
    mytree = retrieveTree(0)
    print(mytree)
    draw_tree(mytree)
