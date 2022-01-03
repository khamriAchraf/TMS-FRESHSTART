import numpy as np
import math


class BranchAndBound:

    def __init__(self,M):
        for i in range(len(M)):
            M[i][i]=0
        self.adj = M
        self.N = len(M)
        self.final_path = [None] * (self.N + 1)
        self.visited = [False] * self.N
        self.final_res = np.inf


    def TSP(self):
        # Calculate initial lower bound for the root node
        # using the formula 1/2 * (sum of first min +
        # second min) for all edges. Also initialize the
        # curr_path and visited array
        self.curr_bound = 0
        self.curr_path = [-1] * (self.N + 1)
        self.visited = [False] * self.N

        # Compute initial bound
        for i in range(self.N):
            self.curr_bound += (self.firstMin(i) + self.secondMin(i))

        # Rounding off the lower bound to an integer
        self.curr_bound = math.ceil(self.curr_bound / 2)

        # We start at vertex 1 so the first vertex
        # in curr_path[] is 0
        self.visited[0] = True
        self.curr_path[0] = 0

        # Call to TSPRec for curr_weight
        # equal to 0 and level 1
        self.TSPRec(0, 1)

    def TSPRec(self, curr_weight,level):

        # base case is when we have reached level N
        # which means we have covered all the nodes once
        if level == self.N:

            # check if there is an edge from
            # last vertex in path back to the first vertex
            if self.adj[self.curr_path[level - 1]][self.curr_path[0]] != 0:

                # curr_res has the total weight
                # of the solution we got
                curr_res = curr_weight + self.adj[self.curr_path[level - 1]] \
                    [self.curr_path[0]]
                if curr_res < self.final_res:
                    self.copyToFinal()
                    self.final_res = curr_res
            return

        # for any other level iterate for all vertices
        # to build the search space tree recursively
        for i in range(self.N):

            # Consider next vertex if it is not same
            # (diagonal entry in adjacency matrix and
            # not visited already)
            if (self.adj[self.curr_path[level - 1]][i] != 0 and
                    self.visited[i] == False):
                temp = self.curr_bound
                curr_weight += self.adj[self.curr_path[level - 1]][i]

                # different computation of curr_bound
                # for level 2 from the other levels
                if level == 1:
                    self.curr_bound -= ((self.firstMin(self.curr_path[level - 1]) + self.firstMin(i)) / 2)
                else:
                    self.curr_bound -= ((self.secondMin(self.curr_path[level - 1]) + self.firstMin(i)) / 2)

                # curr_bound + curr_weight is the actual lower bound
                # for the node that we have arrived on.
                # If current lower bound < final_res,
                # we need to explore the node further
                if self.curr_bound + curr_weight < self.final_res:
                    self.curr_path[level] = i
                    self.visited[i] = True

                    # call TSPRec for the next level
                    self.TSPRec(curr_weight, level + 1)

                # Else we have to prune the node by resetting
                # all changes to curr_weight and curr_bound
                curr_weight -= self.adj[self.curr_path[level - 1]][i]
                curr_bound = temp

                # Also reset the visited array
                visited = [False] * len(self.visited)
                for j in range(level):
                    if self.curr_path[j] != -1:
                        visited[self.curr_path[j]] = True

    # Function to copy temporary solution
    # to the final solution
    def copyToFinal(self):
        self.final_path[:self.N + 1] = self.curr_path[:]
        self.final_path[self.N] = self.curr_path[0]

    # Function to find the minimum edge cost
    # having an end at the vertex i
    def firstMin(self,i):
        min = np.inf
        for k in range(self.N):
            if self.adj[i][k] < min and i != k:
                min = self.adj[i][k]

        return min

    # function to find the second minimum edge
    # cost having an end at the vertex i
    def secondMin(self,i):
        first, second = np.inf, np.inf
        for j in range(self.N):
            if i == j:
                continue
            if self.adj[i][j] <= first:
                second = first
                first = self.adj[i][j]

            elif (self.adj[i][j] <= second and
                  self.adj[i][j] != first):
                second = self.adj[i][j]
        return second

