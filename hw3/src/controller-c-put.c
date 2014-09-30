/* -*-	indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
/*
Copyright (c) 2014, Daniel M. Lofaro <dan@danlofaro.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the author nor the names of its contributors may
      be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

/* Standard Stuff */
#include <string.h>
#include <stdio.h>

/* Required Headers */
#include "controller.h"
#include "getch.h"

/* For Ach IPC */
#include <errno.h>
#include <fcntl.h>
#include <assert.h>
#include <unistd.h>
#include <pthread.h>
#include <ctype.h>
#include <stdbool.h>
#include <math.h>
#include <inttypes.h>
#include <ach.h>





/* Ach Channel IDs */
ach_channel_t chan_controller_ref;      // Feed-Forward (Reference)

int main(int argc, char **argv) {

    /* Open Ach Channel */
    // this channel is used to communicate with the python process that drives the actuators
    int r = ach_open(&chan_controller_ref, CONTROLLER_REF_NAME , NULL);
    assert( ACH_OK == r );


    /* Create initial structures to read and write from */
    struct controller_ref c_ref;
    memset( &c_ref, 0, sizeof(c_ref));

    /* for size check */
    size_t fs;

    /* Get the current feed-forward (state) */
    r = ach_get( &chan_controller_ref, &c_ref, sizeof(c_ref), &fs, NULL, ACH_O_LAST );
    if(ACH_OK != r) {
        assert( sizeof(c_ref) == fs );
    }

    // last values in arrow key sequences for linux ubuntu
    //only tested on my computer
    int KEY_UP = 65;
    int KEY_DOWN = 66;
    int KEY_RIGHT = 67;
    int KEY_LEFT = 68;
    int USER_QUIT = 100;

    char myKey = getch();

    printf("USER, PLEASE ENTER ARROW KEY OR QUIT WITH 'q'\n");


    //do not stop unless user quits with 'q'
    while(myKey != 'q'){
        printf("ENTER ARROW KEY OR QUIT WITH 'q'\n");
        // first value in linux ubuntu arrow key sequence is 27
        if ((int)(myKey) == 27){
            myKey = getch();
            // second value in linux ubuntu arrow key sequence is 91
            if((int)(myKey) == 91){
                myKey = getch();
                printf("%c", myKey);
		printf("\n");
                printf("%d",(int)(myKey));
                // arrow key up makes velocity increment in python process that this c process talks to
                if((int)(myKey) == KEY_UP){
                    printf("increase wheel velocities\n");
                    r = ach_get( &chan_controller_ref, &c_ref, sizeof(c_ref), &fs, NULL, ACH_O_LAST );
                    if(ACH_OK != r) {
                        assert( sizeof(c_ref) == fs );
                    }
                    c_ref.key = (char)(KEY_UP);
                    ach_put( &chan_controller_ref, &c_ref, sizeof(c_ref));
                }
                // arrow key down makes velocity decrement in python process that this c process talks to
                else if((int)(myKey) == KEY_DOWN){
                    printf("decrease wheel velocities\n");
                    r = ach_get( &chan_controller_ref, &c_ref, sizeof(c_ref), &fs, NULL, ACH_O_LAST );
                    if(ACH_OK != r) {
                        assert( sizeof(c_ref) == fs );
                    }
                    c_ref.key = (char)(KEY_DOWN);
                    ach_put( &chan_controller_ref, &c_ref, sizeof(c_ref));
                }
                // arrow key left makes robot right wheel increase vel OR left wheel decrease vel to turn left without the
                // robot wobbling by easing into the turn                
                else if((int)(myKey) == KEY_LEFT){
                    printf("turn left\n");
                    r = ach_get( &chan_controller_ref, &c_ref, sizeof(c_ref), &fs, NULL, ACH_O_LAST );
                    if(ACH_OK != r) {
                        assert( sizeof(c_ref) == fs );
                    }
                    c_ref.key = (char)(KEY_LEFT);
                    ach_put( &chan_controller_ref, &c_ref, sizeof(c_ref));
                }
                // arrow key right makes robot left wheel increase vel OR right wheel decrease vel to turn right without the
                // robot wobbling by easing into the turn
                else if((int)(myKey) == KEY_RIGHT){
                    printf("turn right\n");
                    r = ach_get( &chan_controller_ref, &c_ref, sizeof(c_ref), &fs, NULL, ACH_O_LAST );
                    if(ACH_OK != r) {
                        assert( sizeof(c_ref) == fs );
                    }
                    c_ref.key = (char)(KEY_RIGHT);
                    ach_put( &chan_controller_ref, &c_ref, sizeof(c_ref));
                }
                else{
                    myKey = getch();
                }
            }
            else{
                myKey = getch();
            }
        }
        else{
            myKey = getch();
        }

    }

    // exited while loop, user input must want to quit
    if(myKey == 'q'){
        printf("user wishes to quit\n");			
        r = ach_get( &chan_controller_ref, &c_ref, sizeof(c_ref), &fs, NULL, ACH_O_LAST );
        if(ACH_OK != r) {
            assert( sizeof(c_ref) == fs );
        }
        // write quit value to channel
        c_ref.key = (char)(USER_QUIT);
        ach_put( &chan_controller_ref, &c_ref, sizeof(c_ref));
    }

/*
    ach_put( &chan_controller_ref, &c_ref, sizeof(c_ref));
*/
}

