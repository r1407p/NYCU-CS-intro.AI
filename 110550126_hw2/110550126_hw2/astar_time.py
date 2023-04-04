import csv
import queue
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Begin your code (Part 6)
    """
    I first use csv.reader to read the files, and convert it to list of rows of data.
    For each data I store it into two dimension dictionary.
    (including edges (convert the speed from km/h -> m/sec ) and heuristic)
    I use a priority_queue to implement A star_time algorithm, 
    and store every node's parent into "From"
    When A star_time algorithm detect the end node, finish the algorithm.
    
    Using the informaion from node's parent,
    I can get the path from strat to end, and the distance of the road.
    
    *A star_time algorithm:
    First put the (float(heur[start][end])/(60/3.6),start,-1,0) into the priority_queue.
    structure in priority_queue: (heuristic value, nodeID,ID of node's parent, true distance)
    Heuristic function = straight distance to destination/(60/3.6) + true time from start point.
    (we assume the average speed is 60km/hr)
    
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
            edges[row[0]][row[1]]=([row[2],float(row[3])/3.6])
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
    pq.put((float(heur[start][end])/(60/3.6),start,-1,0))
    From = dict()
    dis = dict()
    path, time, num_visited = [],0,0
    while pq.not_empty:
        now = pq.get()
        if From.get(now[1])!=None:
            continue
        dis[now[1]] = now[0]
        From[now[1]] = now[2]
        num_visited+=1
        if now[1]==end :
            break
        for i in edges[now[1]]:
            temp = now[3]+float(edges[now[1]][i][0])/float(edges[now[1]][i][1])+ float(heur[i][end])/(60/3.6)
            if dis.get(i) ==None: #unexplored
                pq.put((temp,i,now[1],now[3]+float(edges[now[1]][i][0])/float(edges[now[1]][i][1])))
                dis[i] = temp
            if temp<dis[i]:
                pq.put((temp,i,now[1],now[3]+float(edges[now[1]][i][0])/float(edges[now[1]][i][1])))
                dis[i] = temp
    now = now[1]
    while From[now]!=-1:
        time += float(edges[From[now]][now][0])/float(edges[From[now]][now][1])
        path.append(int(now))
        now = From[now]
    path.append(int(now))
    path.reverse()
    return path,time,num_visited
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time( 1718165260,  8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
