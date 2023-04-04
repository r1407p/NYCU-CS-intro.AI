import csv
import queue
edgeFile = 'edges.csv'


def bfs(start, end):
    # Begin your code (Part 1)
    """
    I first use csv.reader to read the file, and convert it to list of rows of data.
    For each data I store it into two dimension dictionary.
    I use a queue to implement bfs algorithm,
    and store every node's parent into "From".
    When bfs algorithm detect the end node, finish the algorithm.
    Using the informaion from node's parent,
    I can get the path from strat to end, and the distance of the road.
    
    *bfs algorithm:
    First put the start node into the queue.
    For every time, I get the front element out, 
    and push it's neighbor which haven't detect into the back of queue
    until the queue is empty or detect the end node.
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
    qu = queue.Queue()
    start = str(start)
    qu.put(start)
    From = dict()
    From[start] = -1
    path,dist,num_visited = [],0,0
    while qu.not_empty:
        now = qu.get()
        flag= False
        for i in edges[now]:
            if From.get(i)==None:
                num_visited+=1
                From[i] = now
                qu.put(i)
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
    # End your code (Part 1)


if __name__ == '__main__':
    
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
