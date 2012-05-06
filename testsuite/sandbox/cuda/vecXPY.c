void VecXPY(int n, double *x, double *y) {

    /*@ begin PerfTuning (
          def performance_params {
            param TC[] = range(16,33,16);
            param CB[] = [True, False];
            param SC[] = range(1,3);
            param CFLAGS[] = map(join, product(['', '-use_fast_math'], ['', '-Xptxas -dlcm=cg']));
          }
          def build {
            arg build_command = 'nvcc -arch=sm_20 @CFLAGS';
          }
          def input_params {
            param N[] = [1000];
          }
          def input_vars {
            decl static double y[N] = random;
            decl static double x[N] = random;
          }
          def performance_counter {
            arg method = 'basic timer';
            arg repetitions = 10;
          }
    ) @*/

    register int i;
    int n=N;

    /*@ begin Loop(transform CUDA(threadCount=TC, cacheBlocks=CB, streamCount=SC)
        for (i=0; i<=n-1; i++)
          y[i]+=x[i];
    ) @*/

    for (i=0; i<=n-1; i++)
        y[i]+=x[i];

    /*@ end @*/
    /*@ end @*/
}
