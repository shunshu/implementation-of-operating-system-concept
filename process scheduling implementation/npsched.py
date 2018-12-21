from fifo import FIFO
from minheap import MinHeap
from task import Task
class NPScheduler: # nonpreemptive scheduler
   def __init__(self, N, policy='SJF'):
      self.N = N  # number of timesteps to schedule
      self.running = None
      self.clock = 0    # the current timestep being scheduled
      self.policy = policy
      # instantiate the readyQueue, which may be a FIFO or MinHeap
      self.readyQuene = MinHeap()
      # you may need additional queues for 
      # - tasks that have been added but not released yet
      # - tasks that have been completed
      # - the Gantt chart
      self.notReadyQuene = MinHeap()
      self.completed_quene = MinHeap()
      self.ganttChart = MinHeap()

   def addTask(self, task):
      # if the release time of the new task is not in the future, then
      # put it in ready queue; otherwise, put into not-ready queue.
      # you may need to copy the scheduler policy into the task

          if task.release > self.clock:
             self.notReadyQuene.put(task)
             task.setPriorityScheme(self.policy)
       
          else: 
             self.readyQuene.put(task)
             task.setPriorityScheme(self.policy)

   def dispatch(self, task):
      # dispatch here means assign the chosen task as the one to run
      # in the current time step.
      # the task should be removed from ready-queue by caller;
      # The task may be empty (None).
      # This method will make an entry into the Gantt chart and perform
      # bookkeeping, including
      # - recording the last dispatched time of this task,
      # - increment the wait times of those tasks not scheduled
      #   but in the ready queue
      self.running = task
      self.ganttChart.put(task)
      if (self.running == None):
         self.ganttChart.put('None')
      else:
         pass
      for i in self.readyQuene:
         i.incrWaitTime()

      

   def releaseTasks(self):
     
      # this is called at the beginning of scheduling each time step to see
      # if new tasks became ready to be released to ready queue, when their
      #  release time is no later than the current clock.
     while True:
        r = self.notReadyQuene.head()
        # assuming the not-Ready Queue outputs by release time
        if r is None or r.releaseTime() > self.clock:
           break
        r = self.notReadyQuene.get()
        r.setPriorityScheme(self.policy)
        self.readyQuene.put(r)

   def checkTaskCompletion(self):
      # if there is a current running task, check if it has just finished.
      # (i.e., decrement remaining time and see if it has more work to do.
      # If so, perform bookkeeping for completing the task, 
      # - move task to done-queue, set its completion time and lastrun time
      # set the scheduler running task to None, and return True
      # (so that a new task may be picked.)
      # but if not completed, return False.
      # If there is no current running task, also return True.
      if (self.running != None):
         self.running.decrRemaining()
      if self.running is None:
         return True
      if(self.running.remaining_time<=0):
             self.completed_quene.put(self.running)
             self.running.setCompletionTime(self.clock)
             self.running=None
             return True
      else:
         return False
   def schedule(self):
     # scheduler that handles nonpreemptive scheduling.
     # the policy such as RR, SJF, or FCFS is handled by the task as it 
     # defines the attribute to compare (in its __iter__() method)
     # first, check if added but unreleased tasks may now be released
     # (i.e., added to ready queue)
     self.releaseTasks()
     if self.checkTaskCompletion() == False:
	self.dispatch(self.running)
        # There is a current running task and it is not done yet!
        # the same task will continue running to its completion.
        # simply redispatch the current running task.
     else:
        # task completed or no running task.
        # get the next task from priority queue and dispatch it.
	#self.dispatch()
        r=self.readyQuene.head()
        if(r!=None):
           self.running=self.readyQuene.get()
           self.dispatch(self.running)
        else:
           self.dispatch(None)
   def clockGen(self):
      # this method runs the scheduler one time step at a time.
      for self.clock in range(self.N):
         # now run scheduler here
         self.schedule()
         yield self.clock

   def getSchedule(self):
      return '-'.join(map(str, self.ganttChart))

   def getThroughput(self):
      # calculate and return throughput as a tuple

      return (self.completed_quene._len_(),self.clock)

   def getWaitTime(self):
      # calculate and return
      return # (numerator, denominator)

   def getTurnaroundTime(self):
      # calculate the turnaround time in terms of a tuple with
      #  separate turnaround times, #processes
      return # (numerator, denominator)

def testNPScheduler(tasks, policy):
   nClocks = 20
   scheduler = NPScheduler(nClocks, policy)
   for t in tasks:
      t.setPriorityScheme(policy)

   for t in tasks:
      scheduler.addTask(t)

   for clock in scheduler.clockGen():
      pass

   print('nonpreemptive %s: %s' % (scheduler.policy, scheduler.getSchedule()))

if __name__ == '__main__':
   tasks = [Task(*i) for i in [('A', 0, 7), ('B', 2, 4), ('C', 4, 1), ('D', 5, 4)]]
   print('tasks = %s' % tasks)
   for policy in ['SJF', 'FCFS', 'RR']:
      tasks = [Task(*i) for i in [('A', 0, 7), ('B', 2, 4), ('C', 4, 1), ('D', 5, 4)]]
      testNPScheduler(tasks, policy)
