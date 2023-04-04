import csv
import queue
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
    """
    I first use csv.reader to read the file, and convert it to list of rows of data.
    For each data I store it into two dimension dictionary.
    I use a stack(LifoQueue) to implement dfs algorithm, 
    and store every node's parent into "From". 
    When dfs algorithm detect the end node, finish the algorithm.
    Using the informaion from node's parent,
    I can get the path from strat to end, and the distance of the road.
    
    *dfs algorithm:
    First put the start node into the stack.
    For every time, I get the top element out, 
    and push it's neighbor which haven't detect into the top of stack
    until the stack is empty or detect the end node.
    """
    edges = dict()
    with open(edgeFile, newline='') as csvfile:
        rows = csv.reader(csvfile)
        rows = list(rows)
        title = rows[0]
        rows.remove(rows[0])
        for row in rows:
            if edges.get(row[0])==None:
                edges[row[0]] = dict()
            if edges.get(row[1])==None:
                edges[row[1]] = dict()
            edges[row[0]][row[1]]=([row[2],row[3]]) 
    
    stack = queue.LifoQueue()
    start = str(start)
    stack.put(start)
    From = dict()
    From[start] = -1
    path,dist,num_visited = [],0,0
    while stack.not_empty:
        now = stack.get()
        flag= False
        for i in edges[now]:
            if From.get(i)==None:
                num_visited+=1
                From[i] = now
                stack.put(i)
                if i == str(end):
                    flag = True
                    break
        if(flag):
            break
    now = str(end)
    while From[now]!=-1:
        dist += float(edges[From[now]][now][0])
        path.append(int(now))
        now = From[now]
    path.append(int(now))
    path.reverse()
    return path,dist,num_visited
    # End your code (Part 2)

if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
