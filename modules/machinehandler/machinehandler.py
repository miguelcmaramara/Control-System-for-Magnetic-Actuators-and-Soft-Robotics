import typing
from multiprocessing.connection import Connection
from ..shared.machinestatus import MachineStatus
from ..hardwarectrl.multiMotorTest import Motor_controller, Stepper_motor
from ..gui.MotorMovement import MotorMovement
import time
import math
import RPi.GPIO as GPIO

class MachineHandler:
    def __init__(self, config, conn: Connection):
        self.config = config
        self.conn = conn
        self.move = MotorMovement()
        self.error_pin=int(self.config['pi4.Misc.pins']['error_pin'])
        self.in_interrupt=False
        pass
    #Runs the continuous loop for the backend
    def run(self):
        # Setup
        self.conn.send(MachineStatus.SETUP)

        # Initialize all motors and encoders
        self.init_motors()

        self.home_axes()
        while(True):
            #print("loop")
            #Checks if something is being sent
            if self.conn.poll():
                #print("READ")
                #Reads what is being sent
                stat = self.conn.recv()
                #print(stat)
                if(stat == MachineStatus.RUNNING):
                    #If the motors are active meaning there is no error forcing it to rehome
                    if self.mc.get_actives()==1:
                        #Gets the next thing being sent which would be the motor movement object
                        self.move =self.conn.recv()
                        #Move the magnet based on the delays found from velocity. 
                        self.moveMagnet(self.findVelocity())
                        #self.mc.run(self.controls)
                    else:
                        #send home message
                        self.conn.send(MachineStatus.ERROR)
                        self.conn.send("Please Home First")
                        pass
                if(stat == MachineStatus.HOME):
                    print("HOMING")
                    #Home all the motors
                    self.home_axes()
                if(stat == MachineStatus.GOPOS):
                    #If the motors are active meaning there is no error forcing it to rehome
                    if self.mc.get_actives()==1:
                        print("GOING TO POSITION")
                        move = self.conn.recv()
                        #The next thing sent would be the motor movement object
                        #print(move.points[0].x())
                        #print(move.points[0].y())
                        #It would go to the first point from the motor movement object
                        self.goToPt(move.getPoints()[0].x(), move.getPoints()[0].y(),move.getRot()[0])
                        #print("back to loop")
                    else:
                        #send home message
                        self.conn.send(MachineStatus.ERROR)
                        self.conn.send("Please Home First")
                        pass
                if(stat ==MachineStatus.TOGGLEROT):
                    #It would toggle the enable pin for the rotation motor 
                    #this would toggle if the rotation motor is locked or not
                    self.mc.r_mot.write_enable()
                if(stat == MachineStatus.DEBUG):
                    #Used as a debuging and testing system
                    speeds=[60000]
                    for i in speeds:
                        self.testSpeed(i)
                if(stat ==MachineStatus.KILL):
                    #it would close the program
                    print("Exit")
                    exit()
        print("WHY you break")
                #self.home_axes

    # initializes the motors and puts them into the motor control object
    def init_motors(self):
        # self.config ['pi4.pins.horizontal.light']['mot_step_pin']
        h_mot_l = Stepper_motor(
                 step_pin=int(self.config['pi4.pins.horizontal.light']['mot_step']),
                 dir_pin=int(self.config['pi4.pins.horizontal.light']['mot_dir']),
                 #sb_pin=int(self.config['pi4.pins.horizontal.light']['mot_sb']),
                 en_pin=int(self.config['pi4.pins.horizontal.light']['mot_sb']),
                 mode_0_pin=int(self.config['pi4.pins.horizontal.light']['mot_mode_0']),
                 mode_1_pin=int(self.config['pi4.pins.horizontal.light']['mot_mode_1']),
                 #mode_2_pin=int(self.config['pi4.pins.horizontal.light']['mot_mode_2']),
                 limit_switch=int(self.config['pi4.pins.horizontal.light']['limit_switch'])
                 )
        h_mot_h = Stepper_motor(
                 step_pin=int(self.config['pi4.pins.horizontal.heavy']['mot_step']),
                 dir_pin=int(self.config['pi4.pins.horizontal.heavy']['mot_dir']),
                #  sb_pin=int(self.config['pi4.pins.horizontal.heavy']['mot_sb']),
                 en_pin=int(self.config['pi4.pins.horizontal.light']['mot_sb']),
                 mode_0_pin=int(self.config['pi4.pins.horizontal.heavy']['mot_mode_0']),
                 mode_1_pin=int(self.config['pi4.pins.horizontal.heavy']['mot_mode_1']),
                 #mode_2_pin=int(self.config['pi4.pins.horizontal.heavy']['mot_mode_2']),
                 limit_switch=int(self.config['pi4.pins.horizontal.heavy']['limit_switch'])
                 )
        v_mot = Stepper_motor(
                 step_pin=int(self.config['pi4.pins.vertical']['mot_step']),
                 dir_pin=int(self.config['pi4.pins.vertical']['mot_dir']),
                #  sb_pin=int(self.config['pi4.pins.vertical']['mot_sb']),
                en_pin=int(self.config['pi4.pins.horizontal.light']['mot_sb']),
                 mode_0_pin=int(self.config['pi4.pins.vertical']['mot_mode_0']),
                 mode_1_pin=int(self.config['pi4.pins.vertical']['mot_mode_1']),
                 #mode_2_pin=int(self.config['pi4.pins.vertical']['mot_mode_2']),
                 limit_switch=int(self.config['pi4.pins.vertical']['limit_switch'])
                 )
        r_mot = Stepper_motor(
                 step_pin=int(self.config['pi4.pins.rotational']['mot_step']),
                 dir_pin=int(self.config['pi4.pins.rotational']['mot_dir']),
                 en_pin=int(self.config['pi4.pins.rotational']['mot_en']),
                 mode_0_pin=int(self.config['pi4.pins.rotational']['mot_mode_0']),
                 mode_1_pin=int(self.config['pi4.pins.rotational']['mot_mode_1']),
                 limit_switch=int(self.config['pi4.pins.rotational']['limit_switch'])
                 )

        self.mc = Motor_controller(h_mot_l, h_mot_h, v_mot, r_mot,self.conn,self.config)
        self.controls=[]
        #self.controls = [
        #        (5000000, 250000, 5000000, 250000, 3000000000),
        #        (250000, 5000000, 250000, 5000000, 3000000000),
        #        (5000000, 250000, 5000000, 250000, 3000000000),
        #        (250000, 5000000, 250000, 5000000, 3000000000),
        #        (5000000, 250000, 5000000, 250000, 3000000000),
        #        (250000, 5000000, 250000, 5000000, 3000000000)
        #        ]

        # self.mc.run(self.controls)


    # home axes function
    def home_axes(self):
        #new_step = 8
        #old_step = 8
        #delay_convert = 1#old_step/new_step
        # self.mc.h_mot_h.write_modes(new_step)
        # self.mc.h_mot_l.write_modes(new_step)
        # self.mc.v_mot.write_modes(new_step)
        start = time.time_ns()
        # sets up the limit switches to stop the motor when it is hit
        self.mc.h_mot_l.set_limit_action(sig_type=GPIO.FALLING)
        self.mc.h_mot_h.set_limit_action(sig_type=GPIO.FALLING)
        #self.mc.h_mot_h.set_limit_action(fxn=lambda x:HACKFXN(self.mc.h_mot_l, self.mc.h_mot_h), sig_type=GPIO.RISING)
        self.mc.v_mot.set_limit_action(sig_type=GPIO.FALLING)
        self.mc.r_mot.set_limit_action(sig_type=GPIO.FALLING)
        #set the motors to active
        self.mc.set_actives(1)
        #Set the directions of the motor  
        self.mc.h_mot_h.write_dir(0)
        self.mc.h_mot_l.write_dir(0)
        self.mc.v_mot.write_dir(0)
        #Rotation motor always turns the right way
        self.mc.r_mot.write_dir(1)
        #def HACKFXN(m1, m2):
        #    print("SUCCESS")
        #    m1.active=0
        #    m2.active=0
        #Since it is homeing remove the error
        self.mc.error_msg=False
        #Sets the motors to be enabled
        self.mc.set_en_sb(1, 1)
        #While at least one of the motors was still active or total time is less than 25 seconds
        while (self.mc.h_mot_h.get_active()==1 or self.mc.h_mot_l.get_active()==1 or self.mc.v_mot.get_active()==1 or self.mc.r_mot.get_active()==1) and (time.time_ns()-start)<25000000000 and not self.mc.error_msg:
            self.controls = [
                ("Move",400000, 400000, 400000, 1500000, 5000000)
                #(5000000, 5000000, 5000000, 5000000, 10000000000),
                #(5000000, 5000000, 5000000, 250000, 3000000000),
                #(5000000, 5000000, 5000000, 5000000, 3000000000),
                #(5000000, 5000000, 5000000, 250000, 3000000000),
                #(5000000, 5000000, 5000000, 5000000, 3000000000)
                ]
            #self.mc.print_current_positions()   # print before the move

            self.mc.run(self.controls)          # run the controls program
        self.mc.set_actives(1)               # reactivate all of the motors
        #Sets the motor to the proper directions
        self.mc.h_mot_h.write_dir(1)
        self.mc.h_mot_l.write_dir(1)
        self.mc.v_mot.write_dir(1)
        self.mc.r_mot.write_dir(0)
        #Remove the actions for the limit switches
        self.mc.h_mot_l.set_limit_action(0)
        self.mc.h_mot_h.set_limit_action(0)
        self.mc.v_mot.set_limit_action(0)
        self.mc.r_mot.set_limit_action(0)
        #Move the motors away from the limit switches, so it is safetly away before it starts moving again
        self.mc.run([("Move",1500000, 1500000, 500000, 1500000, 1500000*200*2)])
        self.mc.run([("Move",1500000*(400*2*20/12), 1500000*(400*2*20/12), 1500000*(400*2*20/12), 1500000, 1500000*((400*2*20/12)-135))])
        #if time it took is over 26 seconds (to account for extra time to move away from home) or if there was any error
        if time.time_ns()-start>26000000000 or self.mc.error_msg:
            #inform the using that the system failed to home and disactivate the motors
            print("Failed to Home")
            self.mc.set_actives(0)
            self.conn.send(MachineStatus.ERROR)
            self.conn.send("System failed to home. \n Please try again.")
        else:
            #Otherwise inform the user the the system is home
            self.conn.send(MachineStatus.ERROR)
            self.conn.send("System is now home.")
        #Disable the linear motors so they are not locked, but rotation is locked
        self.mc.set_en_sb(0, 1)
        #They the system it is now home and reset anything that is needed
        self.mc.set_home()
        self.mc.print_current_positions()   # print the positions after the move


        #self.mc.h_mot_h.write_modes(old_step)
        #self.mc.h_mot_l.write_modes(old_step)
        #self.mc.v_mot.write_modes(old_step)

        print("Finished Homing")

    #goes to a given position where the input is the final points where x and y are in mm and rot is in deg
    def goToPt(self, x, y,rot):
        degPerRad = 57.2957
        degPerPulse = 1.8/8
        mmPerPulse = 6 / degPerRad  * degPerPulse
        print(mmPerPulse)
        #find the number of pulses to move from its given location 
        #times 2 because it takes 2 pulses per step, 1 on, 1 off
        yPulsesToMove = 2*(y-self.mc.y) / mmPerPulse    
        xPulsesToMove = 2*(x-self.mc.x) / mmPerPulse +yPulsesToMove# since x has to move faster
        #print(x-self.mc.x)
        #print(y-self.mc.y)
        rotPulesToMove = 2*(rot-self.mc.rot)*(20/12)/(degPerPulse)
        #print(rot-self.mc.rot)
        #print(rotPulesToMove)
        speed= 60 #mm/s
        speed_pulse=speed/mmPerPulse #pulses/s
        #uses the larger number so the fastest speed is always 60 to find the time to complete the motion in s
        #values have to be larger than 50 to ensure that there are some steps the motion
        if yPulsesToMove >= xPulsesToMove and abs(yPulsesToMove)> 50:
            timeToComp = abs(yPulsesToMove/speed_pulse)
        elif yPulsesToMove < xPulsesToMove and abs(xPulsesToMove)>50:
            timeToComp = abs(xPulsesToMove/speed_pulse)
        else:
            timeToComp = 5

        timeToComp *=1000000000 #sets time in ns
        #timeToComp = 7000000000
        
        

        #finds the velocity of the motion in pulses/ns
        yVel = yPulsesToMove / timeToComp
        xVel = xPulsesToMove / timeToComp #+yVel
        #roation moves seperatly, find the velocity and proper sign 
        rotVel = math.copysign(1,rotPulesToMove)*speed_pulse /1000000000
        #find the time it takes to rotat
        timeToRot= abs(rotPulesToMove/speed_pulse)
        timeToRot *=1000000000

        #finds the delay time for each direction, if the delay is zero just set the delay time to larger than the total time. 
        if xVel == 0:
            xDel = timeToComp*1.1
        else:
            xDel = 1/xVel
        if yVel ==0:
            yDel = timeToComp*1.1
        else:
            yDel = 1/yVel
        if rotVel ==0:
            rotDel = timeToRot*1.1
        else:
            rotDel = 1/rotVel
        print(rotDel,timeToRot)
        #controls for the linear motioj
        self.controls = [("Move",abs(yDel), abs(yDel), abs(xDel), timeToComp*1.5, timeToComp/100)]*100
        #write the direction of the motors, as sign of the delay time still relates to direction of motion
        self.mc.h_mot_h.write_dir(math.copysign(1,yDel))
        self.mc.h_mot_l.write_dir(math.copysign(1,yDel))
        self.mc.v_mot.write_dir(math.copysign(1,xDel))
        self.mc.r_mot.write_dir(-1*math.copysign(1,rotDel))
        #turns on the motors
        self.mc.set_en_sb(1, 1)
        #turns on the limit switches so that if they are it it would stop the motion and cause an error
        self.mc.h_mot_l.set_limit_action(fxn =self.limit_error, sig_type=GPIO.FALLING)
        self.mc.h_mot_h.set_limit_action(fxn =self.limit_error,sig_type=GPIO.FALLING)
        #self.mc.h_mot_h.set_limit_action(fxn=lambda x:HACKFXN(self.mc.h_mot_l, self.mc.h_mot_h), sig_type=GPIO.RISING)
        self.mc.v_mot.set_limit_action(fxn =self.limit_error,sig_type=GPIO.FALLING)
        self.mc.r_mot.set_limit_action(fxn =self.limit_error,sig_type=GPIO.FALLING)
        self.set_error_action(fxn=self.limit_error, sig_type=GPIO.FALLING)
        #run the linear motion
        self.mc.run(self.controls)
        #set up and run the rotational motion
        self.controls=[("Move",timeToRot*1.1,timeToRot*1.1,timeToRot*1.1,abs(rotDel),timeToRot/100)]*100
        self.mc.run(self.controls)
        #disable the linear motions
        self.mc.set_en_sb(0, 1)
        #disable the limit switch actions
        self.mc.h_mot_l.set_limit_action(0)
        self.mc.h_mot_h.set_limit_action(0)
        self.mc.v_mot.set_limit_action(0)
        self.mc.r_mot.set_limit_action(0)
        self.set_error_action(0)
        #set the location of the system based on how many steps the motor rotated
        self.mc.y = self.mc.h_mot_h.dist_travel()
        self.mc.x = self.mc.v_mot.dist_travel()-self.mc.y
        self.mc.rot = self.mc.r_mot.rot_travel()
        #print(self.mc.x,x)
        #print(self.mc.y,y)
        #print(self.mc.rot,rot)
        #if the location is not where it was supposed to be inform the user
        if abs(self.mc.x-x)>10 or abs(self.mc.y-y)>10 or abs(self.mc.rot-rot)>5:
            self.conn.send(MachineStatus.ERROR)
            self.conn.send("System start position is not exact.\n Please try again.")
        print("At Position")
        while self.in_interrupt:
            #print(self.in_interrupt)
            pass
        print("Passed")

    #moves the magnet a given oscillations path
    #list is [h_mot_l_delay, h_mot_h_delay, v_mot_delay, r_mot_delay, total_time, max_y_speed,max_x_speed]
    #all delay and times are in ns, speed is in mm/s
    #speeds are need to properly find acceleration and deceleration
    def moveMagnet(self,delay:list):
        #go to start point
        self.goToPt(self.move.getPoints()[0].x(),self.move.getPoints()[0].y(),self.move.getRot()[0])
        #turn on the limit switches to catch error (switches turned on and off during go to start position)
        self.mc.h_mot_l.set_limit_action(fxn =self.limit_error, sig_type=GPIO.FALLING)
        self.mc.h_mot_h.set_limit_action(fxn =self.limit_error,sig_type=GPIO.FALLING)
        #self.mc.h_mot_h.set_limit_action(fxn=lambda x:HACKFXN(self.mc.h_mot_l, self.mc.h_mot_h), sig_type=GPIO.RISING)
        self.mc.v_mot.set_limit_action(fxn =self.limit_error,sig_type=GPIO.FALLING)
        self.mc.r_mot.set_limit_action(fxn =self.limit_error,sig_type=GPIO.FALLING)
        self.set_error_action(fxn=self.limit_error, sig_type=GPIO.FALLING)
        #initialize commands
        self.controls=[]
        #time to accelerate/decleration is 10% of total time
        acc_time = delay[4]*.1
        #time for rest of the path is 80% of total time
        delay[4]*=.8
        time_delay= delay[4]
        #set propper direction
        set_dir = ("Dir",math.copysign(1,delay[0]),math.copysign(1,delay[1]),math.copysign(1,delay[2]),math.copysign(1,delay[3]))
        #append directions to list
        self.controls.append(set_dir)
        #get list of acceleration and decleration delays based on max speeds
        y_acc=self.create_accel_delays(0,abs(delay[5]))
        x_acc=self.create_accel_delays(0,abs(delay[6]))
        y_dec=self.create_accel_delays(abs(delay[5]),0)
        x_dec=self.create_accel_delays(abs(delay[6]),0)
        #get acceleration and decleration delays into proper tuple format
        acc_delay =[tuple(("Move",y_acc[i],y_acc[i],x_acc[i],abs(delay[3]),acc_time*.1))for i in range(len(y_acc))]
        dec_delay =[tuple(("Move",y_dec[i],y_dec[i],x_dec[i],abs(delay[3]),acc_time*.1))for i in range(len(y_dec))]
        #add accelerations into the list
        self.controls.extend(acc_delay)
        #based on remaining delay time add cmd of crusing speeds into list of commands each cmd lasts .1 s
        while time_delay>100000000:
            self.controls.append(("Move",abs(delay[0]),abs(delay[1]),abs(delay[2]),abs(delay[3]),100000000))
            time_delay-=100000000
        #appends any additional time left in the delay
        self.controls.append(("Move",abs(delay[0]),abs(delay[1]),abs(delay[2]),abs(delay[3]),time_delay))
        #append declerations into the list
        self.controls.extend(dec_delay)
        #switch directions
        switch_dir = (set_dir[0],-1*set_dir[1],-1*set_dir[2],-1*set_dir[3],-1*set_dir[4])
        self.controls.append(switch_dir)
        #add accelerations for the opposite directions, delay times are the same, just opposite motor direction, which already switched
        self.controls.extend(acc_delay)
        #preform have list appends as before, where each cmd lasts .1s
        while delay[4]>100000000:
            self.controls.append(("Move",abs(delay[0]),abs(delay[1]),abs(delay[2]),abs(delay[3]),100000000))
            delay[4]-=100000000
        self.controls.append(("Move",abs(delay[0]),abs(delay[1]),abs(delay[2]),abs(delay[3]),delay[4]))
        self.controls.extend(dec_delay)
        #that is for 1 oscillation, multiply the list for total number of oscillations
        self.controls*=self.move.getOsc()
        #turn on the motors
        self.mc.set_en_sb(1, 1)
        #print(self.controls)
        #if speed is above 1/2 of max speed, have pico send data every 2 triggers of the encoder
        if self.move.getSpeed()>125:
            self.mc.encoder_count(b'2')
        else:
            #otherwise have the pico send data for every trigger
            self.mc.encoder_count(b'1')
        #run the commands
        self.mc.run(self.controls)
        #turn off the linear motors
        self.mc.set_en_sb(0, 1)
        #reset the limit switch actions
        self.mc.h_mot_l.set_limit_action(0)
        self.mc.h_mot_h.set_limit_action(0)
        self.mc.v_mot.set_limit_action(0)
        self.mc.r_mot.set_limit_action(0)
        self.set_error_action(0)
        #set the motors to inactive to ensure that the user homes it after every oscillation motion
        self.mc.set_actives(0)
        while self.in_interrupt:
            pass
    
    #returns the delays based on the speeds in the motor movement objevt
    #returned list is [h_mot_l_delay, h_mot_h_delay, v_mot_delay, r_mot_delay, total_time, max_y_speed,max_x_speed]
    #all delay and times are in ns, speed is in mm/s
    #speeds are need to properly find acceleration and deceleration
    def findVelocity(self):
        #finds the distance between the 2 points
        delta_x = self.move.getPoints()[1].x()-self.move.getPoints()[0].x()
        delta_y = self.move.getPoints()[1].y()-self.move.getPoints()[0].y()
        delta_angle = self.move.getRot()[1]-self.move.getRot()[0]
        #finds total distance
        total_dist= ((delta_x**2)+(delta_y**2))**.5
        #if there is no distance there is no where to move, send message to user and return values that would not cause motion cmds
        if total_dist==0:
            self.conn.send(MachineStatus.ERROR)
            self.conn.send("There is no distance to move.")
            return [10,10,10,10,0,0,0]
        #find the percentage of total speed for each direction
        x_speed = self.move.getSpeed()*delta_x/total_dist
        y_speed = self.move.getSpeed()*delta_y/total_dist
        rot_speed = self.move.getSpeed()*delta_angle/total_dist
        #since x motor needs to move with y the proper speed of x that the motor needs is the speeds added together
        x_speed_act=y_speed+x_speed
        #get delay based on given speeds
        y_delay = self.vel_to_delay(y_speed)
        x_delay = self.vel_to_delay(x_speed_act)
        #if there is no speed it can not move, send message to user and return values that would not cause motion cmds
        if self.move.getSpeed()==0:
            self.conn.send(MachineStatus.ERROR)
            self.conn.send("There is no speed given.")
            return [10,10,10,10,0,0,0]
        #find total time it takes to move the path in ns
        path_time = total_dist/self.move.getSpeed()*1000000000
        #finds rotation delay
        if rot_speed ==0:
            rot_delay=2*path_time
        else:
            rot_delay = (1000000000/(rot_speed*(20/12)))*(1.8/(8*2))
        return [y_delay,y_delay,x_delay,rot_delay,path_time,y_speed,x_speed_act]

    #function to take an input velocity for linear directions and return the delay it needs
    #input is in mm/s
    def vel_to_delay(self,velocity):
        #if no velocity return arbitrary large value
        if velocity == 0: 
            return 1000000000
        #otheriwse return delay in ns based on 12mm diameter and 1/8 microstep
        return (1000000000/(velocity*(360/(12*math.pi))))*(1.8/(8*2))

    #creates a list of delays from a start velocity to an end velocity
    #velocities must be in mm/s
    def create_accel_delays(self, start_v, end_v):
        delays = []
        #divide the acceleration into 10 sections and find the delay time for that given velocity
        for i in range(10):
            delays.append(self.vel_to_delay((.1*(end_v-start_v)+start_v)))
        return delays
        #for xvel, yvel from max velocity to 0 in increments of 1ms# decelleration
        #    x: vel_to_del(vxel)
        #    y = vel_to_del(yvel + yvel)

    #function for when a limit switch is hit during regular motion
    def limit_error(self,num):
        print("WHY")
        self.in_interrupt=True
        #turn off the motors
        self.mc.set_actives(0)
        self.mc.error_msg=True     
        #intened to make the motors back up a little after hitting a home switch, so the system could saftely rehome itself,
        #does not work as it causes other issues with unknown causes and solutions
        #time.sleep(.001)
        #self.mc.error_msg=False
        #self.mc.h_mot_h.write_dir(1)
        #self.mc.h_mot_l.write_dir(1)
        #self.mc.v_mot.write_dir(1)
        #self.mc.r_mot.write_dir(0)
        #if num ==int(self.config['pi4.pins.vertical']['limit_switch']):
        #    self.mc.v_mot.set_active(1)
        #    self.mc.run([("Move",1500000, 1500000, 500000, 1500000, 1500000*200*2)])
        #    self.mc.v_mot.set_active(0)
        #if num == int(self.config['pi4.pins.horizontal.light']['limit_switch']) or num == int(self.config['pi4.pins.horizontal.heavy']['limit_switch']) :
        #    self.mc.h_mot_h.set_active(1)
        #    self.mc.h_mot_l.set_active(1)
        #    self.mc.run([("Move",1500000, 1500000, 500000, 1500000, 1500000*200*2)])
        #    self.mc.h_mot_h.set_active(0)
        #    self.mc.h_mot_l.set_active(0)
        #if num == int(self.config['pi4.pins.rotational']['limit_switch']):
        #    print("test")
        #    self.mc.r_mot.set_active(1)
        #    self.mc.run([("Move",1500000, 1500000, 500000, 1500000, 1500000*200*2)])
        #    self.mc.r_mot.set_active(0)
        #self.mc.error_msg=True 
        #send message to front end
        self.conn.send(MachineStatus.ERROR)
        self.conn.send("System hit the edge. \nPosition is incorrect, please home before continuing. ")#+ str(num))
        #switch directions
        #move back so there is no home issue
        #time.sleep(.01)
        print("test")
        self.in_interrupt =False
         
    #sets the limit action for the error_pin, the pin for the 3 switches at the end of the stage bounds
    def set_error_action(self, set=1, fxn=None, sig_type=GPIO.RISING):
        #callback=self.limit_error()
        callback=None
        if fxn is not None:
            callback = fxn
        if(set):
            GPIO.setup(self.error_pin, GPIO.IN)
            GPIO.add_event_detect(self.error_pin, sig_type, callback=callback)
            #print("Set Up Error",self.error_pin)
            #print(GPIO.input(self.error_pin))
        else:   # if not set, then unset
            GPIO.remove_event_detect(self.error_pin)
        
  
    #test function for testing different speeds based on the different methods
    #insures speeds are proper and reachable
    #used to test limit on pico sending encoder data.
    def testSpeed(self,delay):
        step =8
        #self.mc.h_mot_h.write_modes(step)
        self.mc.r_mot.set_active(1)
        self.mc.v_mot.set_active(1) 
        start_time = time.time()
        #for i in range(200*step*2*4):
        #    self.mc.run([(delay/5, delay/3, delay/7, delay, delay-1)])
        print(start_time-time.time())
        self.mc.run([(delay,delay,delay,delay,1000000000)])
        print(self.mc.r_mot.num_steps)
        print(self.mc.v_mot.num_steps) 



