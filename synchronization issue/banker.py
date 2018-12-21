# Bankers Algorithms is a resource allocation and deadlock
# avoidance algorithm developed by Edsger Dijkstra
# that tests for safety by simulating the allocation of
# predetermined maximum possible amounts of all resources
 
# utility functions 

def sumColumn(M, col):
   '''
       M is a row major matrix, and col is the column index.
       returns the scalar sum of the values in the column.
   '''
   return sum(list(map(lambda x: x[col], M)))
#  it is the same as
#   tot = 0
#   for row in M:
#     tot += row[col]
#   return tot

def IncrVec(A, B):
   '''
     vector A += B, assuming len(A) == len(B)
   '''
   # your code here

   for i in range(len(B)):
     A[i] += B[i]
 
     

def DecrVec(A, B):
   '''
     vector A -= B, assuming len(A) == len(B)
   '''
   # your code here
   for i in range(len(B)):
     A[i] -= B[i]
 
def GtVec(A, B):
   '''
      vector greater-than.
      if one or more of A[i]>B[i], the whole thing is true
   '''
   # your code here
   for i in range(len(A)):
   	if A[i] > B[i]:
   		return True
def LeVec(A, B):
   '''
     vector A[i] <= B[i] (less-than-or-equal-to).
     True if ALL pairs are true.
   '''
   # your code here
   for i in range(len(A)):
   	if A[i] > B[i]:
   		return False
   return True
class Banker:
   def __init__(self, alloc, max, totalRsrc):
      self.Allocation = alloc
      self.n = len(alloc) # number of processes
      self.TotalResources = totalRsrc
      self.m = len(totalRsrc)  # number of resources
      # the following line allows the deadlock detection algorithm
      # to be able to subclass without max (since it doesn't need it)
      if max is not None:
         self.Max = max
         self.Need = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]# your code here to initialize the Need matrix.
         for i in range(self.n):
           for j in range(self.m):
             self.Need[i][j] = self.Max[i][j] - self.Allocation[i][j]
              # Need[i][j] = Max[i][j] - Allocation[i][j] \
      self.Available = [0,0,0] # your code here to compute Available vector.
      self.Available = self.TotalResources
      for i in range(self.m):
        for j in range(self.n):
          self.Available[i] -= self.Allocation[j][i]
              # hint: involves TotalResources and sumColumn() function,
      # a boolean flag to indicate whether in Safety() function you want to
      # print the traced output. by default False, but can be set to True.
      self.traceSafety = False

   def Safety(self):
      if self.traceSafety: print('Need=%s, Available=%s' % (self.Need, self.Available))
      # step 1
      Sequence = []  # use this list to save the safe sequence 
      Finish = [False for i in range(self.n)]
      Work =  [] # your code to initialize Work vector
      Work = self.Available[:]
      done = 0 # indicate how many processes are done
      flag = False # for breaking nested loop
      # step 2
      for _ in range(self.n):
          for i in range(self.n):
              if self.traceSafety: 
              	 print('i=%d, ' % i, end="")
              # follow the pseudocode on slide 37
              # may need to print
              # compare Need[i] with Work.
              # - hint: you may use LecVec(A, B) for A <= B:
              if self.Need[i] <= Work:
              # step 3
              # - update bookkeeping including Work, Finish, and add to sequence
              # - Hint: you may want to use IncrVec() for Work += Allocation
                 if Finish[i] == False:
                    print('(Need[%d]=%s) <= (Work=%s) True, append P%d' %(i, self.Need[i], Work, i))
                    Finish[i] = True
                    Sequence.append(i)
                    done +=1
                    for j in range(len(Work)):
                       Work[j] += self.Allocation[i][j]
                    if (done == 5):
                    	flag = True
                    	break
                 elif Finish[i]:
                 	print('Finish[%d] True, skipping' % (i))
              else:
              	 print('(Need[%d]=%s) <= (Work=%s) False, P%d must wait' %(i, self.Need[i], Work, i))
          if flag == True:
          	break
      # step 4. return the sequence if there is one, or None if not.
      for i in Finish:
        if Finish[i] == False:
          return None
      return Sequence
   def Request(self, i, rqst):  # slide 47
      '''
         called with the requesting process i and the resource vector
         for how many instances of each resource to request.
         the rqst is a vector of m length.
      '''
      # step 1
      # hint: use GtVec of LeVec to compare request vector rqst with Need[i]
      # raise an exception if over
      if rqst > self.Need[i]:
      	 print('raise error condition: process has exceeded its maximum claim')
      	 return
      # step 2
      # in case of wait, simply return None
      if LeVec(rqst, self.Available):
      # step 3
      # pretend to allocate requested resource:
      # save snapshot of Available, Allocation, and Need
      # update Available, Allocation, and Need
      # call Safety()
      # if a safe sequence exists, return it.
      # otherwise, restore saved snapshot and return None
         self.snapshot_Available = self.Available
         self.snapshot_Allocation = self.Allocation[i]
         self.snapshot_Need = self.Need[i]
         string = [0,0,0]
         for j in range(len(self.Available)):
             self.snapshot_Available[j] -= rqst[j]
             self.snapshot_Allocation[j] += rqst[j]
             self.snapshot_Need[j] -= rqst[j]
         if LeVec(string, self.snapshot_Available):
         	return 1
         else:
         	return None
   def Release(self, i):
      '''
         need this function to release the resources allocated to process P_i
         after it has finished execution.
      '''
      # hint: update Available, Allocation, and Need.
      # hint: you may want to call utility functions IncrVec
      # hint: but in which order? who goes first, last, or don't care?
      str = [0,0,0]
      if LeVec(str, self.snapshot_Available):
      	for j in range(len(str)):
      	   self.Available[j] += self.snapshot_Allocation[j]
      	   self.Allocation[i][j] = self.snapshot_Allocation[j]
      	   self.Need[i][j] = self.snapshot_Need[j]
 
######################## 
def TestUtility():
   print('Testing Utility Functions:')
   # test vector. A, B, C, compare.  Here A + B = C, and A > B.
   L = [[[1, 2, 1], [1, 0, 2], [2, 2, 3], True],
        [[1, 2, 3], [2, 2, 4], [3, 4, 7], False],
        [[2, 3, 3], [2, 3, 3], [4, 6, 6], False]]

   for T in L:
      # make a copy
      A, B, C, compare = T[0][:], T[1][:], T[2][:], T[3]
      print('A = %s, B = %s, ' % (A, B))
      IncrVec(A, B)
      print('A += B is %s, expect %s' % (A, C))
      DecrVec(A, B)
      print('A -= B is %s, expect %s' % (A, T[0]))
      print('A > B is %s, expect %s; A <= B is %s, expect %s' % (GtVec(A, B), compare, LeVec(A, B), not compare))

def TestConstructor():
   Allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
   Max        = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
   Available=[3, 3, 2],
   Need=[[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]]
   TotalResources = [10, 5, 7]
   b = Banker(Allocation, Max, TotalResources)
   # check Available and Need are computed properly
   print("b.Available=%s, expect %s" % (b.Available, Available))
   print("b.Need=%s, expect %s" % (b.Need, Need))

def TestSafety():
   Allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
   Max        = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
   TotalResources = [10, 5, 7]
   b = Banker(Allocation, Max, TotalResources)
   b.traceSafety = True
   s = b.Safety()
   b.traceSafety = False
   print('s is %s' % s)
   return b, s

def TestRequests(banker, sequence):
   n = 5
   m = 3
   requestVector = [[0, 2, 0], [1, 0, 2], [3, 0, 0], [0, 1, 1], [3, 3, 0]]
   if sequence is None:
      print('impossible to safely satisfy request vector')
   else:
      print('Found safe sequence %s' % sequence)
      # follow the sequence
      for j in range(n):
         i = sequence[j]
         print('P%d allocated %s, requesting %s, ' % (i, banker.Allocation[i], requestVector[i]))
         if banker.Request(i, requestVector[i]) is None:
            print('err: following sequence %s but cannot fulfil P%d request %s' % (sequence, i, requestVector[i]))
         banker.Release(i)
         print(" P%d releasing, available=%s" % (i, banker.Available))


if __name__ == '__main__':
   TestUtility()
   TestConstructor()
   banker, sequence = TestSafety()
   TestRequests(banker, sequence)
