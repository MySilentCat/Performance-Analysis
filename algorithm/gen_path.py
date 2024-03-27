from graphviz import Digraph


class ActivityGraph:
    def __init__(self):
        self.adj_list = {}
        self.branch_merge = {}

    def add_edge(self, start, end):
        if start not in self.adj_list:
            self.adj_list[start] = []
        self.adj_list[start].append(end)

    # 删除边
    def remove_edge(self, start, end):
        if start in self.adj_list:
            self.adj_list[start].remove(end)

    # 绘制图形
    def draw(self, name):
        dot = Digraph(comment='The Round Table')
        dot.node('Begin', 'Begin')
        dot.node('Final', 'Final')

        for start, end_list in self.adj_list.items():
            for end in end_list:
                dot.node(start, start)
                dot.node(end, end)
                dot.edge(start, end)

        # 画图
        dot.render(name, view=True)

        # def add_branch_merge(self, branch, merge):

    #     self.branch_merge[branch] = merge # 分叉节点和合并节点

    def find_paths(self, start, end, current_path=None):
        if current_path is None:
            current_path = []

        current_path.append(start)

        if start == end:
            yield list(current_path)
        elif start in self.adj_list:
            for neighbor in self.adj_list[start]:
                yield from self.find_paths(neighbor, end, current_path)

        current_path.pop()

    def find_execution_paths(self, start):
        if start not in self.adj_list:
            return []
        paths = []
        for neighbor in self.adj_list[start]:
            paths.extend(list(self.find_paths(neighbor, "Final")))
        return paths

    # 找到 start 到 end 之间的所有对应的 第一个节点到最后一个节点的路径
    def find_paths_nodes(self, start, end, current_path=None):
        pairs = set()  # 保存路径起始位置和结束位置对的列表
        # 遍历从 start 到 end 之间的所有路径
        for path in self.find_paths(start, end, current_path):
            pairs.add((path[1], path[-2]))
        return pairs


# 将活动图保存在ActivityGraph类中
def edge2graph(f):
    graph = ActivityGraph()

    f_nodes = set()  # F 节点set
    for edge in f:
        # 记录有哪些F节点
        if "Fork" in edge[0] and '.' not in edge[0]:
            f_nodes.add(edge[0])
        graph.add_edge(edge[0], edge[1])

    return graph, f_nodes


# 合并F节点
def merge_f_nodes(graph, f_nodes):
    # 遍历图结构，如果遇到 F 节点，则记录每条子路径的开始节点和对应的J之前的最后一个节点
    for f_node in f_nodes:
        # f_node 是 F1 ，转换成对应的J1
        j_node = f_node.replace("Fork", "Join")
        pairs = graph.find_paths_nodes(f_node, j_node)
        # 根据pairs，改变图结构，将 F 的不同路径串联 例如 F1 pairs {('D1', 'M1'), ('A5', 'A5')} 串联成 增加 M1 -> A5,,,, 删除 F1 -> A5, M1 -> J1
        # 保留第一个pair 的 末尾节点，删除其他的pair的开始节点，中间加上 | 分隔
        pre = ""
        for pair in pairs:
            if pre == "":
                pre = pair[1]
            else:
                graph.add_edge(pre, pair[0])
                # 在不同的路径之间添加分隔符
                # graph.add_edge(pre, pair[0] + "|")
                # graph.add_edge(pair[0] + "|", pair[0])

                graph.remove_edge(f_node, pair[0])

                pre = pair[1]
            graph.remove_edge(pre, j_node)
        graph.add_edge(pre, j_node)

    return graph


def print_execution_paths(paths):
    rst = []
    for path in paths:
        path.insert(0, "Begin")
        if path not in rst:
            rst.append(path)
    return rst


def run(edges):
    graph, f_nodes = edge2graph(edges)  # f_nodes = {'F1', 'F2'}, 即图中需要合并的F节点
    # graph.draw("graph1")
    # 将F节点合并
    graph = merge_f_nodes(graph, f_nodes)
    # 绘制合并后的图结构
    # graph.draw("graph2")
    # 获取所有路径
    paths = graph.find_execution_paths("Begin")
    # print(paths)
    # 打印所有路径
    return print_execution_paths(paths)


if __name__ == "__main__":
    a = [('DataBase.query(String)', 'Final'), ('BookMapper.detail(String)', 'DataBase.query(String)'), ('BookService.detail(String)',
                                                                                                        'BookMapper.detail(String)'), ('BookController.detail(String)', 'BookService.detail(String)'), ('Begin', 'BookController.detail(String)')]
    b = [('BookService.readFile(String)', 'Merge1'), ('DataBase.query(String)', 'Decision1'), ('BookMapper.query(Book)', 'DataBase.query(String)'), ('BookService.query(Book)', 'BookMapper.query(Book)'),
         ('Merge1', 'Final'), ('Begin', 'BookController.download(String)'), ('BookController.download(String)', 'BookService.query(Book)'), ('Decision1', 'BookService.readFile(String)'), ('Decision1', 'Merge1')]
    c = [('Decision1', 'DataBase.query(String)'), ('Decision1', 'DataBase.update(String)'), ('Merge1', 'Join1'), ('Begin', 'BookController.detail(String)'), ('BookController.detail(String)', 'Fork1'), ('BookService.query(Book)', 'BookMapper.query(Book)'), ('BookService.detail(String)', 'BookMapper.detail(String)'), ('BookService.printAll(Book)', 'Final'), ('BookMapper.query(Book)', 'Join1'), ('BookMapper.detail(String)', 'Decision1'),
         ('DataBase.query(String)', 'Merge1'), ('DataBase.update(String)', 'Merge1'), ('Fork1', 'BookService.detail(String)'), ('Fork1', 'BookService.query(Book)'), ('Join1', 'BookService.printAll(Book)')]
    d = [('DataBase.add(String)', 'Merge1'), ('BookMapper.create(Book)', 'DataBase.add(String)'), ('BookService.create(Book)', 'BookMapper.create(Book)'), ('DataBase.query(String)', 'Decision1'), ('BookMapper.query(Book)', 'DataBase.query(String)'),
         ('BookService.query(Book)', 'BookMapper.query(Book)'), ('BookController.create(Book)', 'BookService.query(Book)'), ('Merge1', 'Final'), ('Begin', 'BookController.create(Book)'), ('Decision1', 'Merge1'), ('Decision1', 'BookService.create(Book)')]
    graph, f_nodes = edge2graph(d)  # f_nodes = {'F1', 'F2'}, 即图中需要合并的F节点
    graph.draw("graph1")
    # 将F节点合并
    graph = merge_f_nodes(graph, f_nodes)
    # 绘制合并后的图结构
    graph.draw("graph2")
    # 获取所有路径
    paths = graph.find_execution_paths("Begin")
    print(paths)
    # 打印所有路径
    print_execution_paths(paths)
