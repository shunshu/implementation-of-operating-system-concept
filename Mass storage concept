# disk scheduling algorithms


class DiskScheduler:
    _POLICIES = ['FCFS', 'SSTF', 'SCAN', 'LOOK', 'C-SCAN', 'C-LOOK']

    def __init__(self, nCylinders):
        self.nCylinders = nCylinders

    def schedule(self, initPos, requestQueue, policy, direction):
        '''
            request is the list of cylinders to access
            policy is one of the strings in _POLICIES.
            direction is 'up' or 'down'
            returns the list for the order of cylinders to access.
        '''
        if policy == 'FCFS':
            # return the disk schedule for FCFS
            return requestQueue

        if policy == 'SSTF':
            # shortest seek time first
            # compute and return the schedule for the shortest seek time first
            quene = []
            curpos = initPos
            dif = 500
            index = 0
            length = len(requestQueue)
            Queue = []
            for i in range(length):
                Queue.append(requestQueue[i])
            for i in range(length):
                for j in range(len(Queue)):
                    if abs(curpos - Queue[j]) < dif:
                        dif = abs(curpos - Queue[j])
                        index = j
                dif = 500
                quene.append(Queue[index])
                del Queue[index]
            return quene

        if policy in ['SCAN', 'C-SCAN', 'LOOK', 'C-LOOK']:
            # sequentially one direction to one end, 
            # then sequentially to the other `
            # decide on direction (up or down) based on initial request
            # compute and return the schedule accordingly
            quene = []
            index = 0
            Queue = []
            length = len(requestQueue)
            for i in range(length):
                Queue.append(requestQueue[i])
            for i in range(len(Queue)- 1):
                for j in range (len(Queue)- i- 1):
                    if Queue[j] > Queue[j+ 1]:
                        temp = Queue[j]
                        Queue[j] = Queue[j+ 1]
                        Queue[j+ 1] = temp
            if policy == 'SCAN':
                if direction == 'down':
                    for i in range(len(Queue)):
                        if Queue[i] > initPos:
                            index = i
                            break
                    for i in range(index):
                        quene.append(Queue[index- i- 1])
                        del Queue[index- i- 1]
                    if quene[-1] is not 0:
                        quene.append(0)
                    for i in range(len(Queue)):
                        quene.append(Queue[0])
                        del Queue[0]
                    return quene
                elif direction == 'up':
                    for i in range(len(Queue)):
                        if Queue[i] > initPos:
                            index = i
                            break
                    for i in range(len(Queue)- index):
                        quene.append(Queue[index])
                        del Queue[index]
                    if quene[-1] is not 199:
                        quene.append(199)
                    for i in range(len(Queue)):
                        quene.append(Queue[-1])
                        del Queue[-1]
                    return quene
            elif policy == 'C-SCAN':
                if direction == 'down':
                    for i in range(len(Queue)):
                        if Queue[i] > initPos:
                            index = i
                            break
                    for i in range(index):
                        quene.append(Queue[index- i- 1])
                        del Queue[index- i- 1]
                    if quene[-1] is not 0:
                        quene.append(0)
                    if Queue[-1] is not 199:
                        quene.append(199)
                    for i in range(len(Queue)):
                        quene.append(Queue[-1])
                        del Queue[-1]
                    return quene
                elif direction == 'up':
                    for i in range(len(Queue)):
                        if Queue[i] > initPos:
                            index = i
                            break
                    for i in range(len(Queue)- index):
                        quene.append(Queue[index])
                        del Queue[index]
                    if quene[-1] is not 199:
                        quene.append(199)
                    if Queue[0] is not 0:
                        quene.append(0)
                    for i in range(len(Queue)):
                        quene.append(Queue[0])
                        del Queue[0]
                    return quene
            elif policy == 'LOOK':
                if direction == 'down':
                    for i in range(len(Queue)):
                        if Queue[i] > initPos:
                            index = i
                            break
                    for i in range(index):
                        quene.append(Queue[index- i- 1])
                        del Queue[index- i- 1]
                    for i in range(len(Queue)):
                        quene.append(Queue[0])
                        del Queue[0]
                    return quene
                elif direction == 'up':
                    for i in range(len(Queue)):
                        if Queue[i] > initPos:
                            index = i
                            break
                    for i in range(len(Queue)- index):
                        quene.append(Queue[index])
                        del Queue[index]
                    for i in range(len(Queue)):
                        quene.append(Queue[-1])
                        del Queue[-1]
                    return quene
            elif policy == 'C-LOOK':
                if direction == 'down':
                    for i in range(len(Queue)):
                        if Queue[i] > initPos:
                            index = i
                            break
                    for i in range(index):
                        quene.append(Queue[index- i- 1])
                        del Queue[index- i- 1]
                    for i in range(len(Queue)):
                        quene.append(Queue[-1])
                        del Queue[-1]
                    return quene
                elif direction == 'up':
                    for i in range(len(Queue)):
                        if Queue[i] > initPos:
                            index = i
                            break
                    for i in range(len(Queue)- index):
                        quene.append(Queue[index])
                        del Queue[index]
                    for i in range(len(Queue)):
                        quene.append(Queue[0])
                        del Queue[0]
                    return quene

def totalSeeks(initPos, queue):
    lastPos = initPos
    totalMoves = 0
    for p in queue:
        totalMoves += abs(p - lastPos)
        lastPos = p
    return totalMoves



if __name__  == '__main__':
    def TestPolicy(scheduler, initHeadPos, requestQueue, policy, direction):
        s = scheduler.schedule(initHeadPos, requestQueue, policy, direction)
        t = totalSeeks(initHeadPos, s)
        print('policy %s %s (%d): %s' % (policy, direction, t, s))

    scheduler = DiskScheduler(200)
    requestQueue = [98, 183, 37, 122, 14, 124, 65, 67]
    initHeadPos = 53
    for policy in DiskScheduler._POLICIES:
        if policy[:2] == 'C-' or policy[-4:] in ['SCAN', 'LOOK']:
            TestPolicy(scheduler, initHeadPos, requestQueue, policy, 'up')
            TestPolicy(scheduler, initHeadPos, requestQueue, policy, 'down')
        else:
            TestPolicy(scheduler, initHeadPos, requestQueue, policy, '')

    print('more tests on SCAN and C-SCAN')
    rQs = [[98, 37, 0, 122, 14], [98, 37, 199, 122, 14], [98, 0, 37, 199, 14]]
    for q in rQs:
        print('Q=%s' % q)
        for policy in ['SCAN', 'C-SCAN']:
            for direction in ['up', 'down']:
                TestPolicy(scheduler, initHeadPos, q, policy, direction)
