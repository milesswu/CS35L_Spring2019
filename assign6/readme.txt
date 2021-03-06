Miles Wu

Implementation Choices:
Saw the opportunity to use parallelism on the nested for loop in the
main function of the main.c file. In order to have this process be
split among and executed by threads, I moved the loop into its own
function. This required the new function to have access to the
variables 'nthreads' and 'scene'. I decided to enable this by changing
them both to be global variables (this was decided after a failed
implementation using a struct *See Problem 3)

The way I split tasks among threads was by passing into the function
the thread number being executed and using that as a starting point for
the loop instead. Additionally I incremented the loop iterator by
nthreads instead of by 1. This ensured that every thread would operate
on a different set of pixels (since they start on a different pixel)
and that all pixels would still be processed (all pixels not processed
by one thread will be processed by another thread).

Needed to aggregate results instead of executing the print statement
at the end of the loop now placed in the thread function. Necessary so
that the output was in the correct order (one thread executing faster
than another would not affect results). Handled this using a global
array that would store the scaled_color values for each pixel. Would
then sequentially print all of the values after joining all threads
together.

Problems:
1. Tried to access struct's data members before casting it to the
struct data type. This caused  a problem because I was then
essentially attempting to dereference a void pointer.

2. Also had a problem with creating a pointer to struct to contain the
arguments, setting the arguments, and then passing it into the thread
function. Did not realize that a pointer to a struct needed to be
created using malloc. Tried to use a non pointer instance of the
struct but then could not pass it into the thread function. Eventually
just used malloc to solve the problem.

3. Originally tried to use a struct to old nthreads and scene as
arguments for the thread function. This created a problem where
threads would end up having the same threadNum argument (since I only
created one pointer to a struct and then updated the threadNum field
for every creation). This was due to a memory aliasing problem. My
initial thought to solve this problem was to create an array of
structs and pass them in accordingly. However, I realized how wasteful
this approach would be since the only field changing in every struct
would be the threadNum field. Thus I instead opted to make 'nthreads'
and 'scene' global variables while using an array of thread numbers to
specify which thread was performing the thread function.

Conclusions:
Running make clean check produces the following results

time ./srt 1-test.ppm >1-test.ppm.tmp

real    0m44.368s
user    0m44.352s
sys     0m0.007s
mv 1-test.ppm.tmp 1-test.ppm
time ./srt 2-test.ppm >2-test.ppm.tmp

real    0m22.522s
user    0m44.900s
sys     0m0.000s
mv 2-test.ppm.tmp 2-test.ppm
time ./srt 4-test.ppm >4-test.ppm.tmp

real    0m11.329s
user    0m44.468s
sys     0m0.000s
mv 4-test.ppm.tmp 4-test.ppm
time ./srt 8-test.ppm >8-test.ppm.tmp

real    0m5.729s
user    0m44.358s
sys     0m0.003s
mv 8-test.ppm.tmp 8-test.ppm
time ./srt 1-test.ppm >1-test.ppm.tmp

real    0m43.144s
user    0m43.137s
sys     0m0.002s
mv 1-test.ppm.tmp 1-test.ppm
time ./srt 2-test.ppm >2-test.ppm.tmp

real    0m22.314s
user    0m44.517s
sys     0m0.002s
mv 2-test.ppm.tmp 2-test.ppm
time ./srt 4-test.ppm >4-test.ppm.tmp

real    0m11.319s
user    0m44.545s
sys     0m0.003s
mv 4-test.ppm.tmp 4-test.ppm
time ./srt 8-test.ppm >8-test.ppm.tmp

real    0m5.789s
user    0m44.364s
sys     0m0.001s
mv 8-test.ppm.tmp 8-test.ppm

As we can see, the threaded implementation of SRT significantly
improves performance when using a larger number of threads. 
For each increase in threads by a power of two, the real time of the
program decreased by about half as much time and the real time of the
program using 8 threads is around 1/7 of the time the program runs
using 1 thread. The user time of the multi-threaded runs are all
slightly above the user time of the single-threaded run, which likely
has to do with the thread creation and thread joining processes. Even
so, the overall performance of the multi-threaded runs are far better
than the single-threaded run.
