def solution(dimensions, your_position, trainer_position, distance):
    
    def sq_dist(p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    
    def cal_slope(p1, p2):
        return (p2[1]-p1[1])/(p2[0]-p1[0]) if p1[0] != p2[0] else None
        
    def gen_pts(dims, yp, tp, dist):
        # generate points along x-axis
        yps_q1 = []
        tps_q1 = []
        
        yps_temp = [yp]
        tps_temp = [tp]
        
        i = 1
        while (2 * dims[0] * i - yp[0] <= yp[0] + dist):
            yps_temp.append([2 * dims[0] * i - yp[0], yp[1]])
            yps_temp.append([2 * dims[0] * i + yp[0], yp[1]])
            i += 1
        
        i = 1
        while (2 * dims[0] * i - tp[0] <= yp[0] + dist):
            tps_temp.append([2 * dims[0] * i - tp[0], tp[1]])
            tps_temp.append([2 * dims[0] * i + tp[0], tp[1]])
            i += 1
        
        yps_q1 += yps_temp
        tps_q1 += tps_temp

        j = 1
        while (2 * dims[1] * j - yp[1] <= yp[1] + dist):
            yps_q1 += list(map(lambda x: [x[0], 2 * dims[1] * j - yp[1]], yps_temp))
            yps_q1 += list(map(lambda x: [x[0], 2 * dims[1] * j + yp[1]], yps_temp))
            j += 1
        
        j = 1
        while (2 * dims[1] * j - tp[1] <= yp[1] + dist):
            tps_q1 += list(map(lambda x: [x[0], 2 * dims[1] * j - yp[1]], tps_temp))
            tps_q1 += list(map(lambda x: [x[0], 2 * dims[1] * j + yp[1]], tps_temp))
            j += 1
            
        yps_q2 = list(map(lambda x: [-1 * x[0], x[1]], yps_q1))
        yps_q3 = list(map(lambda x: [-1 * x[0], -1 * x[1]], yps_q1))
        yps_q4 = list(map(lambda x: [x[0], -1 * x[1]], yps_q1))

        tps_q2 = list(map(lambda x: [-1 * x[0], x[1]], tps_q1))
        tps_q3 = list(map(lambda x: [-1 * x[0], -1 * x[1]], tps_q1))
        tps_q4 = list(map(lambda x: [x[0], -1 * x[1]], tps_q1))
        
        yps = yps_q1 + yps_q2 + yps_q3 + yps_q4
        tps = tps_q1 + tps_q2 + tps_q3 + tps_q4
        
        return (yps, tps)
    
    

    yps, tps = gen_pts(dimensions, your_position, trainer_position, distance)
    # yps = yps[1:]
    yps_dist = list(map(lambda x: sq_dist(x, your_position), yps))

    yps = list(filter(lambda x: True if sq_dist(your_position, x) <= distance * distance else False, yps))
    tps = list(filter(lambda x: True if sq_dist(your_position, x) <= distance * distance else False, tps))


    slope_dist = dict()
    count = 0
    
    for p in tps:
        slope = cal_slope(p, your_position)
        key = (slope, p[0] > your_position[0])
        if key not in slope_dist:
            slope_dist[key] = sq_dist(p, your_position)
            count += 1
        elif key in slope_dist and sq_dist(p, your_position) < slope_dist[key]:
            slope_dist[key] = sq_dist(p, your_position)
            
    for p in yps:
        slope = cal_slope(p, your_position)
        key = (slope, p[0] > your_position[0])
        if key in slope_dist and slope_dist[key] is not None and sq_dist(p, your_position) <= slope_dist[key]:
            slope_dist[key] = None
            count -= 1
            
    return count

# assert solution([3, 2], [1, 1], [2, 1], 4) == 7
# assert solution([300, 275], [150, 150], [180, 100], 500) == 9
assert solution([2, 5], [1, 2], [1, 4], 11) == 27
# assert solution([23, 10], [6, 4], [3, 2], 23) == 8
# assert solution([1250, 1250], [1000, 1000], [500, 400], 10000) == 196
# assert solution([10, 10], [4, 4], [3, 3], 5000) == 739323
# assert solution([3, 2], [1, 1], [2, 1], 7) == 19
# assert solution([2, 3], [1, 1], [1, 2], 4) == 7
# assert solution([3, 4], [1, 2], [2, 1], 7) == 10
# assert solution([4, 4], [2, 2], [3, 1], 6) == 7
# assert solution([3, 4], [1, 1], [2, 2], 500) == 54243