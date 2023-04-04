import csv
import queue
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar(start, end):
    # Begin your code (Part 4)
    """
    I first use csv.reader to read the files, and convert it to list of rows of data.
    For each data I store it into two dimension dictionary.(including edges and heuristic)
    
    I use a priority_queue to implement A star algorithm, 
    and store every node's parent into "From"
    When A star algorithm detect the end node, finish the algorithm.
    
    Using the informaion from node's parent,
    I can get the path from strat to end, and the distance of the road.
    
    *A star algorithm:
    First put the (float(heur[start][end]),start,-1,0) into the priority_queue.
    structure in priority_queue: (heuristic value, nodeID,ID of node's parent, true distance)
    Heuristic function = straight distance to destination + true distance from start point.
    
    For every time, I get the most priority (the least Heuristic value) element out, 
    and push it's neighbor (Heuristic value and distance) which haven't detect into the priority queue
    until the priority queue is empty or detect the end node.
    In addition, I add "dis" (dictionary) to record the Heuristic value of node which is in the priority queue
    If the Heuristic value of new explore is larger than previous explore, not add it into priority queue.
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
            edges[row[0]][row[1]]=([row[2],row[3]])
    heur = dict()
    with open(heuristicFile,newline = '') as csvfile:
        rows = csv.reader(csvfile)
        rows = list(rows)
        title = rows[0]
        rows.remove(rows[0])
        for row in rows:
            heur[row[0]] = dict()
            for i in range(1,4):
                heur[row[0]][title[i]] = row[i]
    pq = queue.PriorityQueue()
    pq.put((float(heur[start][end]),start,-1,0))
    From = dict()
    dis = dict()
    path,dist,num_visited = [],0,0
    while pq.not_empty:
        now = pq.get()
        #print(now)
        if From.get(now[1])!=None:
            continue
        dis[now[1]] = now[0]
        From[now[1]] = now[2]
        num_visited+=1
        
        if now[1]==end :
            break
        #print(now)
        for i in edges[now[1]]:
            temp =now[3]+float(edges[now[1]][i][0])+float(heur[i][end])
            if dis.get(i) ==None: #unexplored
                pq.put((temp,i,now[1],now[3]+float(edges[now[1]][i][0])))
                dis[i] = temp
            if temp<dis[i]:
                pq.put((temp,i,now[1],now[3]+float(edges[now[1]][i][0])))
                dis[i] = temp
    now = now[1]
    while From[now]!=-1:
        dist += float(edges[From[now]][now][0])
        path.append(int(now))
        now = From[now]
    path.append(int(now))
    path.reverse()
    return path,dist,num_visited
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(426882161, 1737223506)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
