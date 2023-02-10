#include <stdio.h>
//#include <unistd.h>
#include <pigpio.h>
#include <time.h>
#include <sys/timeb.h>


void runMotor(int numStep, long timeDelay, int clockwise, int stepPin, int dirPin){
    struct timespec tim, tim2;
    tim.tv_sec = 0;
    tim.tv_nsec = timeDelay;
    printf("moving\n");
        gpioWrite(dirPin, clockwise);
        for(int i = 0; i < numStep; i++){
            gpioWrite(stepPin, 1);
            nanosleep(&tim, &tim2);
            gpioWrite(stepPin, 0);
            nanosleep(&tim, &tim2);
        }
        gpioWrite(dirPin, 0);
    printf("finished\n");
}

void getInput(){
    int getInput;
    printf("Starting\n");
    scanf("%d", &getInput);
    printf("Got input, moving motor\n");

}

int main(){
    if(gpioInitialise() < 0){
        printf("Pigpio failed to initailise\n");
    } else {
        // Setup
        gpioSetMode(20, PI_INPUT);//dir
        gpioSetMode(21, PI_INPUT); // step

        // loop
        struct timeb start, end;

   
        getInput();
        ftime(&start);
        runMotor(1600, 1600000L, 0, 21, 20);
        ftime(&end);
        printf("Time: %u\n", (int)(1000 * (end.time - start.time) + (end.millitm - start.millitm)));

        getInput();
        ftime(&start);
        runMotor(1600, 800000L, 0, 21, 20);
        ftime(&end);
        printf("Time: %u\n", (int)(1000 * (end.time - start.time) + (end.millitm - start.millitm)));

        getInput();
        ftime(&start);
        runMotor(1600, 400000L, 0, 21, 20);
        ftime(&end);
        printf("Time: %u\n", (int)(1000 * (end.time - start.time) + (end.millitm - start.millitm)));

        getInput();
        ftime(&start);
        runMotor(1600, 200000L, 0, 21, 20);
        ftime(&end);
        printf("Time: %u\n", (int)(1000 * (end.time - start.time) + (end.millitm - start.millitm)));

        getInput();
        ftime(&start);
        runMotor(1600, 100000L, 0, 21, 20);
        ftime(&end);
        printf("Time: %u\n", (int)(1000 * (end.time - start.time) + (end.millitm - start.millitm)));

        getInput();
        ftime(&start);
        runMotor(1600, 50000L, 0, 21, 20);
        ftime(&end);
        printf("Time: %u\n", (int)(1000 * (end.time - start.time) + (end.millitm - start.millitm)));

                getInput();
        ftime(&start);
        runMotor(1600, 10000L, 0, 21, 20);
        ftime(&end);
        printf("Time: %u\n", (int)(1000 * (end.time - start.time) + (end.millitm - start.millitm)));

        getInput();
                ftime(&start);
        runMotor(1600, 5000L, 0, 21, 20);
        ftime(&end);
        printf("Time: %u\n", (int)(1000 * (end.time - start.time) + (end.millitm - start.millitm)));

        getInput();
                        ftime(&start);
        runMotor(1600, 1000L, 0, 21, 20);
        ftime(&end);
        printf("Time: %u\n", (int)(1000 * (end.time - start.time) + (end.millitm - start.millitm)));

        getInput();
                                ftime(&start);
        runMotor(1600, 500L, 0, 21, 20);
        ftime(&end);
        printf("Time: %u\n", (int)(1000 * (end.time - start.time) + (end.millitm - start.millitm)));

        
    }

    gpioTerminate();
    return 0;
}
