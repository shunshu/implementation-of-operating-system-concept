# Deadlock Detection, similar to Banker's

from banker import Banker, sumColumn, IncrVec, DecrVec, GtVec, LeVec

class DeadlockDetector(Banker):
   def __init__(self, alloc, totalRsrc):
      Banker.__init__(self, alloc, None, totalRsrc)
      self.Finish = []
      self.Sequence = []
   def detect(self, Request):
      '''detect deadlock with the request matrix'''
      # 1(a) initialize Work = a copy of Available
      # 1(b) Finish[i] = (Allocation[i] == [0, ...0])
      self.Work = self.Available
      self.traceSafety = True
      done = 0 
      flag = False
      for i in range(len(self.Allocation)):
          self.Finish.append((self.Allocation[i] == [0,0,0]))
      print(self.Finish)
      # optionally, you can keep a Sequence list
      for _ in range(2):
          for i in range(self.n):
              if self.traceSafety: print('i=%d, ' % i, end="")
              if LeVec(Request[i], self.Work):
                  if self.Finish[i] == False:
                      print('(Request[%d]=%s) <= (Work=%s) True, append P%d' %(i, Request[i], self.Work, i))
                      for j in range(len(self.Work)):
                         self.Work[j] += self.Allocation[i][j]
                      self.Finish[i] = True
                      self.Sequence.append(i)
                      done += 1
                      print('   (+Allocation[%d]=%s) => (Work=%s), Finish=%s' %(i, self.Allocation[i], self.Work, self.Finish))
                      if (done == 5):
                          flag = True
                          break
                  elif self.Finish[i]:
                      print('Finish[%d] is True, skipping' % (i))
              else:
                  print('(Request[%d]=%s) <= (Work=%s) False, P%d must wait' %(i, Request[i], self.Work, i))
          if flag == True:
              break
              # Step 2: similar to safety algorithm
              #   if there is an i such that (Finish[i] == False)
              #   and Request_i <= Work, (hint: LeVec() or GtVec()) then
              #   Step 3: 
              #     Work += Allocation[i] # hint IncrVec()
              #     Finish[i] = True
              #        continue Step 2
      for i in range(5):
          if (self.Finish[i] == False):
              return None
      return self.Sequence
      # Step 4: either done iterating or (no such i exists)
      #    Finish vector indicates deadlocked processes.
      #    if all True then no deadlock.

 
if __name__ == '__main__':
   Allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 3], [2, 1, 1], [0, 0, 2]]
   Request    = [[0, 0, 0], [2, 0, 2], [0, 0, 0], [1, 0, 0], [0, 0, 2]]
   Available  = [0, 0, 0]
   TotalResources = [7, 2, 6]
   d_1 = DeadlockDetector(Allocation, TotalResources)
   s_1 = d_1.detect(Request)
   if s_1 is not None:
      print('sequence = %s' % s_1)
   else:
      print('deadlock')
   Allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 3], [2, 1, 1], [0, 0, 2]]
   Request    = [[0, 0, 0], [2, 0, 2], [0, 0, 1], [1, 0, 0], [0, 0, 2]]
   Available  = [0, 0, 0]
   TotalResources = [7, 2, 6]
   d_2 = DeadlockDetector(Allocation, TotalResources)
   s_2 = d_2.detect(Request)
   if s_2 is not None:
      print('sequence = %s' % s_2)
   else:
      print('deadlock')
