#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int *A; // array
int times = 0;

void swap(int *a, int *b){
    int temp = *a;
    *a = *b;
    *b = temp;
}

int Partition(int p, int r) {
    int pivot = A[r];
    int i = p -1;
    int j;
    for (j = p; j < r; j++) {
        if (A[j] < pivot) {
            i++;
            swap(&A[i], &A[j]);
        }
    }
    i++;
    swap(&A[i], &A[r]);
    return i;
}

void* QuickSort(void *arg) {
    // your code
    if (times < 7)
    {
        times++;
        pthread_t lthread,rthread;
        int *input=(int*)arg;
        int a[2];
        int b[2];
        int c[2];
        a[0]=input[0];
        a[1]=input[1];
        int q=Partition(a[0],a[1]);
        b[0]=a[0];
        b[1]=q-1;
        c[0]=q+1;
        c[1]=a[1];
        pthread_create(&lthread,NULL,QuickSort,(void*)b);
        pthread_create(&rthread,NULL,QuickSort,(void*)c);  
	      pthread_join(lthread,NULL);
        pthread_join(rthread,NULL);
        return 0;
    }
    int *input=(int*)arg;
    int a[2];
    int b[2];
    int c[2];
    a[0]=input[0];
    a[1]=input[1];
    if(a[0]<a[1])
    {
        int q=Partition(a[0],a[1]);
        b[0]=a[0];
        b[1]=q-1;
        c[0]=q+1;
        c[1]=a[1];
        QuickSort(b);
        QuickSort(c);
    }
}
int main(int argc, char *argv[]) {
        // read randomInt.txt into array A
        // same as Sec 2.1.
        int i;
        FILE* fh = fopen("randomInt.txt", "r");
        int len;
        fscanf(fh, "%d", &len);
        A = calloc(len, sizeof(int));
        for (i = 0; i < len; i++) {
                fscanf(fh, "%d", A+i);
        }
        fclose(fh);
        int args[2] = { 0, len-1 };
        QuickSort(args);

        // check if they are sorted. This part is same as Sec 2.1

        for (i = 0; i < len; i++) {
              if (A[i] != i) {
                        fprintf(stderr, "error A[%d]=%d\n", i, A[i]);
                }
        }
	return 0;
}
