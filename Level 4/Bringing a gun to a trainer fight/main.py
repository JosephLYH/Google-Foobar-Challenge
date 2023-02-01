import numpy as np
from collections import defaultdict

class Solution:
    def gen_quadrants(self):
        self.origs = np.concatenate([self.origs, -self.origs, [-1, 1]*self.origs, [1, -1]*self.origs], axis=0)
        self.dests = np.concatenate([self.dests, -self.dests, [-1, 1]*self.dests, [1, -1]*self.dests], axis=0)
    
    def expand_x(self):
        temp_origs = self.origs.copy()
        temp_dests = self.dests.copy()

        i = 1
        while (self.dims[0] * 2*i - self.orig[0] <= self.dist + self.orig[0]):
            self.origs = np.concatenate([
                self.origs, 
                np.array([[self.dims[0] * 2*i - self.orig[0], y] for _, y in temp_origs]), 
                np.array([[self.dims[0] * 2*i + self.orig[0], y] for _, y in temp_origs]),
            ])
            i += 1
        
        i = 1
        while (self.dims[0] * 2*i - self.dest[0] <= self.dist + self.orig[0]):
            self.dests = np.concatenate([
                self.dests, 
                np.array([[self.dims[0] * 2*i - self.dest[0], y] for _, y in temp_dests]), 
                np.array([[self.dims[0] * 2*i + self.dest[0], y] for _, y in temp_dests]),
            ])
            i += 1

    def expand_y(self):
        temp_origs = self.origs.copy()
        temp_dests = self.dests.copy()

        i = 1
        while (self.dims[1] * 2*i - self.orig[1] <= self.dist + self.orig[1]):
            self.origs = np.concatenate([
                self.origs, 
                np.array([[x, self.dims[1] * 2*i - self.orig[1]] for x, _ in temp_origs]), 
                np.array([[x, self.dims[1] * 2*i + self.orig[1]] for x, _ in temp_origs]), 
            ])
            i += 1

        i = 1
        while (self.dims[1] * 2*i - self.dest[1] <= self.dist + self.orig[1]):
            self.dests = np.concatenate([
                self.dests,
                np.array([[x, self.dims[1] * 2*i - self.dest[1]] for x, _ in temp_dests]), 
                np.array([[x, self.dims[1] * 2*i + self.dest[1]] for x, _ in temp_dests]), 
            ])
            i += 1

    def calculate_slope(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        if x1 == x2:
            return np.inf

        return (y2 - y1)/(x2 - x1)

    def solution(self, dims, orig, dest, dist):
        self.origs = np.array([orig])
        self.dests = np.array([dest])
        self.orig = orig
        self.dest = dest
        self.dims = dims
        self.dist = dist
        self.count = 0
        self.slopes_dist = defaultdict(lambda: None)

        self.expand_x()
        self.expand_y()
        self.gen_quadrants()

        self.origs = self.origs[1:]
        self.origs = self.origs[np.array([np.linalg.norm(x - self.orig) for x in self.origs]) <= self.dist]
        self.dests = self.dests[np.array([np.linalg.norm(x - self.orig) for x in self.dests]) <= self.dist]

        for p in self.dests:
            slope = self.calculate_slope(self.orig, p)
            key = (slope, p[0] > self.orig[0])
            if not self.slopes_dist[key]:
                self.slopes_dist[key] = np.linalg.norm(self.orig - p)
                self.count += 1
            elif np.linalg.norm(self.orig - p) < self.slopes_dist[key]:
                self.slopes_dist[key] = np.linalg.norm(self.orig - p)

        for p in self.origs:
            slope = self.calculate_slope(self.orig, p)
            key = (slope, p[0] > self.orig[0])
            if self.slopes_dist[key] and np.linalg.norm(self.orig - p) < self.slopes_dist[key]:
                self.slopes_dist[key] = None
                self.count -= 1

        return self.count

if __name__ == '__main__':
    solution = Solution()
    # assert solution.solution([3, 2], [1, 1], [2, 1], 4) == 7
    # assert solution.solution([300, 275], [150, 150], [180, 100], 500) == 9
    assert solution.solution([2, 5], [1, 2], [1, 4], 11) == 27
    # assert solution.solution([23, 10], [6, 4], [3, 2], 23) == 8
    # assert solution.solution([1250, 1250], [1000, 1000], [500, 400], 10000) == 196
    # assert solution.solution([10, 10], [4, 4], [3, 3], 5000) == 739323
    # assert solution.solution([3, 2], [1, 1], [2, 1], 7) == 19
    # assert solution.solution([2, 3], [1, 1], [1, 2], 4) == 7
    # assert solution.solution([3, 4], [1, 2], [2, 1], 7) == 10
    # assert solution.solution([4, 4], [2, 2], [3, 1], 6) == 7
    # assert solution.solution([3, 4], [1, 1], [2, 2], 500) == 54243