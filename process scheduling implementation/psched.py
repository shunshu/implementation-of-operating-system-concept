from npsched import NPScheduler
from task import Task
from minheap import MinHeap
class PScheduler(NPScheduler): # subclass from nonpreemptive scheduler
   # this means it can inherit 
   # __init__(), addTask(), dispatch(), releaseTasks()
   # clockGen(), getSchedule()

   def preempt(self):
      # this is the new method to add to put the running task
      # back into ready queue, plus any bookkeeping if necessary.
      self.readyQuene.put(self.running)
         
   def schedule(self):
 
      self.releaseTasks() # same as before
      if self.checkTaskCompletion() == False:
         # still have operation to do.
         # see if running task or next ready task has higher priorityi
         # hint: compare by first typecasting the tasks to tuple() first
         #   and compare them as tuples.  The tuples are defined in
         #   the __iter__() method of the Task class based on policy.
         # if next ready is not higher priority, redispatch current task.
         # otherwise,
         # - swap out current running (by calling preempt method)
         print(1)
         if(self.readyQuene. __len__()==0 or tuple(self.running)<=tuple(self.readyQuene.head())):
             self.dispatch(self.running)
         elif(self.readyQuene. __len__() != 0 and tuple(self.running)>tuple(self.readyQuene.head())):
             r=self.readyQuene.get()
             self.preempt()
             self.running=r
             self.dispatch(self.running)
      else:
        # task completed or no running task.
        # get the next task from priority queue and dispatch it.
        #self.dispatch()
        print(2)
        r = self.readyQuene.head()
        if(r!=None):
           self.running=self.readyQuene.get()
           self.dispatch(self.running)
        else:
           self.dispatch(None)
def testPScheduler(tasks, policy):
   # this is same as before, but instantiate the preemptive scheduler.
   nClocks = 20
   scheduler = PScheduler(nClocks, policy)
   # the rest is the same as before
   for t in tasks:
      t.setPriorityScheme(policy)

   for t in tasks:
      scheduler.addTask(t)
   for clock in scheduler.clockGen():
      pass
   print('preemptive %s: %s' % (scheduler.policy, scheduler.getSchedule()))
   t_1=scheduler.getThroughput()
   t_2=scheduler.getWaitTime()
   t_3=scheduler.getTurnaroundTime()

if __name__ == '__main__':
   tasks = [Task(*i) for i in [('A', 0, 7), ('B', 2, 4), ('C', 4, 1), ('D', 5, 4)]]
   print('tasks = %s' % tasks)
   for policy in ['SJF', 'FCFS', 'RR']:
         tasks = [Task(*i) for i in [('A', 0, 7), ('B', 2, 4), ('C', 4, 1), ('D', 5, 4)]]
         testPScheduler(tasks, policy)
