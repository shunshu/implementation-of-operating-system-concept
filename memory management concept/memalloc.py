import bisect

class MemAlloc:

   _POLICIES = ('FirstFit', 'BestFit', 'WorstFit')

   def __init__(self, totalMemSize, policy = 'BestFit'):
      if not policy in MemAlloc._POLICIES:
         raise ValueError('policy must be in %s' % MemAlloc._POLICIES)
      self.allocation = { } # map pointer to (size)
      self.holes = [(0, totalMemSize)] # sorting by pointer
      self.policy = policy
      # your code here

   # insert your own utility methods as needed

   def malloc(self, reqSize):
      '''return the starting address of the block of memory, or None'''
      # your code here
      if self.policy == 'FirstFit':
          pointer = 0
          flag = False
          for i in range(len(self.holes)):
             if (reqSize <= self.holes[i][1]):
                flag = True
                self.allocation[self.holes[i][0]] = reqSize
                pointer = self.holes[i][0]
                address = self.holes[i][0]+ reqSize
                space = self.holes[i][1]- reqSize
                del (self.holes[i])
                self.holes.append((address, space))
                if (space == 0):
                    pop()
                self.holes.sort()
                break
          if flag:
              return pointer
          else:
              return None
      elif self.policy == 'BestFit':
          smallest = 100
          index = 0
          pointer = 0
          flag = False
          for i in range(len(self.holes)):
              if (self.holes[i][1] >= reqSize and self.holes[i][1] < smallest):
                  flag = True
                  smallest = self.holes[i][1]
                  index = i
          if flag:
              self.allocation[self.holes[index][0]] = reqSize
              pointer = self.holes[index][0]
              address = self.holes[index][0]+ reqSize
              space = self.holes[index][1]- reqSize
              del(self.holes[index])
              self.holes.append((address, space))
              if (space == 0):
                  self.holes.pop()
              self.holes.sort()
              return pointer
          else:
              return None
      elif self.policy == 'WorstFit':
          largest = 0
          pointer = 0
          index = 0
          flag = False
          for i in range(len(self.holes)):
              if (self.holes[i][1] >= reqSize and self.holes[i][1] > largest):
                  flag = True
                  largest = self.holes[i][1]
                  index = i
          if flag:
              self.allocation[self.holes[index][0]] = reqSize
              pointer = self.holes[index][0]
              address = self.holes[index][0]+ reqSize
              space = self.holes[index][1]- reqSize
              del(self.holes[index])
              self.holes.append((address, space))
              if (space == 0):
                  self.holes.pop()
              self.holes.sort()
              return pointer
          else:
              return None

   def free(self, pointer):
      '''free the previously allocated memory starting at pointer'''
      # your code here
      if self.allocation. __contains__(pointer):
          length = len(self.holes)
          if (length > 1):
              for i in range(length):
                  if ((pointer+ self.allocation[pointer]) <= self.holes[i+ 1][0] and pointer >= (self.holes[i][0]+ self.holes[i][1])):
                      if ((pointer+ self.allocation[pointer]) < self.holes[i+ 1][0] and pointer > (self.holes[i][0]+ self.holes[i][1])):
                          self.holes.append((pointer, (self.allocation[pointer])))
                          self.holes.sort()
                          del(self.allocation[pointer])
                          break
                      elif((pointer+ self.allocation[pointer]) == self.holes[i+ 1][0] and pointer > (self.holes[i][0]+ self.holes[i][1])):
                          self.holes.append((pointer, (self.holes[i+ 1][1]+ self.allocation[pointer])))
                          del (self.holes[i+ 1])
                          self.holes.sort()
                          del(self.allocation[pointer])
                          break
                      elif((pointer+ self.allocation[pointer]) < self.holes[i+ 1][0] and pointer == (self.holes[i][0]+ self.holes[i][1])):
                          self.holes.append((self.holes[i][0], (self.holes[i][1]+ self.allocation[pointer])))
                          del (self.holes[i])
                          self.holes.sort()
                          del(self.allocation[pointer])
                          break
                      elif((pointer+ self.allocation[pointer]) == self.holes[i+ 1][0] and pointer == (self.holes[i][0]+ self.holes[i][1])):
                          self.holes.append((self.holes[i][0], (self.holes[i][1]+ self.holes[i+ 1][1]+ self.allocation[pointer])))
                          del (self.holes[i], self.holes[i])
                          self.holes.sort()
                          del(self.allocation[pointer])
                          break
          elif (length == 1):
              if (pointer >= (self.holes[0][0]+ self.holes[0][1])):
                  if (pointer == (self.holes[0][0]+ self.holes[0][1])):
                      self.holes.append((self.holes[0][0], (self.holes[0][1]+ self.allocation[pointer])))
                      del(self.holes[0])
                      del(self.allocation[pointer])
                  elif (pointer > (self.holes[0][0]+ self.holes[0][1])):
                      self.holes.append((pointer, (pointer+ self.allocation[pointer])))
                      self.holes.sort()
                      del(self.allocation[pointer])
              elif ((pointer+self.allocation[pointer]) <= self.holes[0][0]):
                  if ((pointer+self.allocation[pointer]) == self.holes[0][0]):
                      self.holes.append((pointer, (self.holes[0][1]+ self.allocation[pointer])))
                      del(self.holes[0])
                      del(self.allocation[pointer])
                  elif ((pointer+self.allocation[pointer]) < self.holes[0][0]):
                      self.holes.append((pointer, (pointer+self.allocation[pointer])))
                      self.holes.sort()
                      del(self.allocation[pointer])
          elif (length == 0):
              self.holes.append((pointer, (pointer+ self.allocation[pointer])))
              del(self.allocation[pointer])
          
   def __str__(self):
      return repr(self.allocation)


def runTestScript(requests):
   ff = MemAlloc(20, 'FirstFit')
   bf = MemAlloc(20, 'BestFit')
   wf = MemAlloc(20, 'WorstFit')
   ffSym = {}
   bfSym = {}
   wfSym = {}
   for name, size in requests:
      if size is None:
         # do a free() call
         ff.free(ffSym[name]); del(ffSym[name])
         bf.free(bfSym[name]); del(bfSym[name])
         wf.free(wfSym[name]); del(wfSym[name])
         print('free(%s)' % name)
      else: 
         # do an malloc() call
         ffSym[name] = ff.malloc(size)
         bfSym[name] = bf.malloc(size)
         wfSym[name] = wf.malloc(size)
         print('%s=malloc(%d):' % (name, size))
      print(' FirstFit symbols=%s holes=%s allocation=%s' % (ffSym, ff.holes, ff.allocation))
      print(' BestFit symbols=%s holes=%s allocation=%s' % (bfSym, bf.holes, bf.allocation))
      print(' WorstFit symbols=%s holes=%s allocation=%s' % (wfSym, wf.holes, wf.allocation))

if __name__ == '__main__':

   requests = [('a', 10), ('b', 1), ('c', 4), ('c', None), ('a', None),
               ('d', 9),  # worst fit and first fit would use (0, 10), but best fit would use (11, 9)
               ('e', 10), # worst fit and first fit wold fail, but best fit would succeed with (0, 10)
    ]
   runTestScript(requests)

   print('------------------------')

   requests = [('a', 3), ('b', 6), ('c', 2), ('d', 5), # malloc
               ('a', None), ('c', None), # free
               ('e', 2),  # best fit (9, 2), first fit (0, 2), worst fit (16, 2)
               ('b', None), # free: best fit merges (0,3) and (3,6) => (0,9)
                   # first fit merges (3,6), (9,2) => (3, 8)
                   # worst fit merges (0,3), (3,6), (9,2) => (0,11)
               ('f', 11)   # both best fit and first fit fail, but worst fit succeeds
    ]
   runTestScript(requests)
