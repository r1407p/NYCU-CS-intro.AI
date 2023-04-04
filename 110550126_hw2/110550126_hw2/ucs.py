import csv
import queue
edgeFile = 'edges.csv'


def ucs(start, end):
    # Begin your code (Part 3)
    """ 
    I first use csv.reader to read the file, and convert it to list of rows of data.
    For each data I store it into two dimension dictionary.
    I use a priority_queue to implement uniform cost search algorithm, 
    and store every node's parent into "From"
    When uniform cost search algorithm detect the end node, finish the algorithm.
    
    Using the informaion from node's parent,
    I can get the path from strat to end, and the distance of the road.
    
    *uniform cost search algorithm:
    First put the (0,start node) into the priority_queue.
    structure in priority_queue: (distance from start point,nodeID, ID of node's parent)
    For every time, I get the most priority (the closest) element out, 
    and push it's neighbor (and distance) which haven't detect into the priority queue
    until the priority queue is empty or detect the end node.
    In addition, I add "dis" (dictionary) to record the distance of node which is in the priority queue
    If the distance of new explore is larger than previous explore, not add it into priority queue.
    """
    start = str(start)
    end = str(end)
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
            edges[row[0]][row[1]]=([row[2],row[3],False])
    From = dict()
    dis = dict()
    pq = queue.PriorityQueue()
    path,dist,num_visited = [],0,0
    pq.put((0,start,-1))
    n =0 
    while pq.not_empty:
        now = pq.get()
        
        if From.get(now[1])!=None:
            continue
        dis[now[1]] = now[0]
        From[now[1]] = now[2]
        num_visited+=1
        if end ==now[1]:
            break
        for i in edges[now[1]]:
            temp = now[0]+float(edges[now[1]][i][0])
            if dis.get(i) ==None: #unexplored
                pq.put((temp,i,now[1]))
                dis[i] = temp
            if temp<dis[i]:
                pq.put((temp,i,now[1]))
                dis[i] = temp
    now = end
    while From[now]!=-1:
        dist += float(edges[From[now]][now][0])
        path.append(int(now))
        now = From[now]
    path.append(int(now))
    path.reverse()
    return path,dist,num_visited
        
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(426882161, 4413398107)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
