import threading
times = 0

def Partition(A, p, r):

    x = A[r]

    i = p - 1

    for j in range(p, r):

        if (A[j] <= x):

            i = i + 1

            A[i], A[j] = A[j], A[i]

    A[i+1], A[r] = A[r], A[i+1]

    return i + 1



def QuickSort(A, p, r):
    global times
    if times < 7:
	times = times+ 1

        q = Partition(A, p, r)
	QuickSort(A, q+ 1, r)
	l = threading.Thread(target = QuickSort, args= (A, p, q- 1))
	l.start()
	l.join()
	return 
    if p < r:
        q = Partition(A, p, r)

        QuickSort(A, p, q-1)

        QuickSort(A, q+1, r)



if __name__ == '__main__':

    LEN = 20000000
    L = range(LEN)
    num_list=[]
    with open("randomInt.txt") as f:

       for line in f:
         try :
           num_list.append(int(line))
         except:
           continue #or other stuffs

    QuickSort(num_list, 0, len(L)- 1)

    if L == range(LEN):  # Python3 list(range(LEN)) instead of range(LEN)

        print("successfully sorted")

    else:

        print("sort failed: %s" % L)
