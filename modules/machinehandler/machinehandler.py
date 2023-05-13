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

    def run(self):
        # Setup
        self.conn.send(MachineStatus.SETUP)

        # Initialize all motors and encoders
        self.init_motors()

        self.home_axes()
        while(True):
            #print("loop")
            if self.conn.poll():
                #print("READ")
                stat = self.conn.recv()
                #print(stat)
                if(stat == MachineStatus.RUNNING):
                    if self.mc.get_actives()==1:
                        self.move =self.conn.recv()
                        self.moveMagnet(self.findVelocity())
                        #self.mc.run(self.controls)
                    else:
                        #send home message
                        self.conn.send(MachineStatus.ERROR)
                        self.conn.send("Please Home First")
                        pass
                if(stat == MachineStatus.HOME):
                    print("HOMING")
                    self.home_axes()
                if(stat == MachineStatus.GOPOS):
                    if self.mc.get_actives()==1:
                        print("GOING TO POSITION")
                        move = self.conn.recv()
                        #print(move.points[0].x())
                        #print(move.points[0].y())
                        self.goToPt(move.getPoints()[0].x(), move.getPoints()[0].y(),move.getRot()[0])
                        #print("back to loop")
                    else:
                        #send home message
                        self.conn.send(MachineStatus.ERROR)
                        self.conn.send("Please Home First")
                        pass
                if(stat ==MachineStatus.TOGGLEROT):
                    self.mc.r_mot.write_enable()
                if(stat == MachineStatus.DEBUG):
                    speeds=[60000]
                    for i in speeds:
                        self.testSpeed(i)
                if(stat ==MachineStatus.KILL):
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
        new_step = 8
        old_step = 8
        delay_convert = 1#old_step/new_step
        # self.mc.h_mot_h.write_modes(new_step)
        # self.mc.h_mot_l.write_modes(new_step)
        # self.mc.v_mot.write_modes(new_step)
        start = time.time_ns()
        # set a signal type
        self.mc.h_mot_l.set_limit_action(sig_type=GPIO.FALLING)
        self.mc.h_mot_h.set_limit_action(sig_type=GPIO.FALLING)
        #self.mc.h_mot_h.set_limit_action(fxn=lambda x:HACKFXN(self.mc.h_mot_l, self.mc.h_mot_h), sig_type=GPIO.RISING)
        self.mc.v_mot.set_limit_action(sig_type=GPIO.FALLING)
        self.mc.r_mot.set_limit_action(sig_type=GPIO.FALLING)
        self.mc.set_actives(1)  
        self.mc.h_mot_h.write_dir(0)
        self.mc.h_mot_l.write_dir(0)
        self.mc.v_mot.write_dir(0)
        self.mc.r_mot.write_dir(1)
        def HACKFXN(m1, m2):
            print("SUCCESS")
            m1.active=0
            m2.active=0
        self.mc.error_msg=False
        self.mc.set_en_sb(1, 1)
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
        self.mc.h_mot_h.write_dir(1)
        self.mc.h_mot_l.write_dir(1)
        self.mc.v_mot.write_dir(1)
        self.mc.r_mot.write_dir(0)
        self.mc.h_mot_l.set_limit_action(0)
        self.mc.h_mot_h.set_limit_action(0)
        self.mc.v_mot.set_limit_action(0)
        self.mc.r_mot.set_limit_action(0)
        self.mc.run([("Move",1500000, 1500000, 500000, 1500000, 1500000*200*2)])
        self.mc.run([("Move",1500000*(400*2*20/12), 1500000*(400*2*20/12), 1500000*(400*2*20/12), 1500000, 1500000*((400*2*20/12)-135))])
        if time.time_ns()-start>26000000000 or self.mc.error_msg:
            print("Failed to Home")
            self.mc.set_actives(0)
            self.conn.send(MachineStatus.ERROR)
            self.conn.send("System failed to home. \n Please try again.")
        else:
            self.conn.send(MachineStatus.ERROR)
            self.conn.send("System is now home.")
        self.mc.set_en_sb(0, 1)
        self.mc.set_home()
        self.mc.print_current_positions()   # print the positions after the move


        self.mc.h_mot_h.write_modes(old_step)
        self.mc.h_mot_l.write_modes(old_step)
        self.mc.v_mot.write_modes(old_step)

        print("Finished Homing")

    def goToPt(self, x, y,rot):
        degPerRad = 57.2957
        degPerPulse = 1.8/8
        mmPerPulse = 6 / degPerRad  * degPerPulse
        print(mmPerPulse)

        yPulsesToMove = 2*(y-self.mc.y) / mmPerPulse    # since y has to move faster
        xPulsesToMove = 2*(x-self.mc.x) / mmPerPulse +yPulsesToMove
        print(x-self.mc.x)
        print(y-self.mc.y)
        rotPulesToMove = 2*(rot-self.mc.rot)*(20/12)/(degPerPulse)
        print(rot-self.mc.rot)
        print(rotPulesToMove)
        speed= 60
        speed_pulse=speed/mmPerPulse
        if yPulsesToMove >= xPulsesToMove and abs(yPulsesToMove)> 50:
            timeToComp = abs(yPulsesToMove/speed_pulse)
        elif yPulsesToMove < xPulsesToMove and abs(xPulsesToMove)>50:
            timeToComp = abs(xPulsesToMove/speed_pulse)
        else:
            timeToComp = 5

        timeToComp *=1000000000
        #timeToComp = 7000000000
        
        


        yVel = yPulsesToMove / timeToComp
        xVel = xPulsesToMove / timeToComp #+yVel
        rotVel = math.copysign(1,rotPulesToMove)*speed_pulse /1000000000
        timeToRot= abs(rotPulesToMove/speed_pulse)
        timeToRot *=1000000000

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
        self.controls = [("Move",abs(yDel), abs(yDel), abs(xDel), timeToComp*1.5, timeToComp/100)]*100

        self.mc.h_mot_h.write_dir(math.copysign(1,yDel))
        self.mc.h_mot_l.write_dir(math.copysign(1,yDel))
        self.mc.v_mot.write_dir(math.copysign(1,xDel))
        self.mc.r_mot.write_dir(-1*math.copysign(1,rotDel))
        self.mc.set_en_sb(1, 1)
        self.mc.h_mot_l.set_limit_action(fxn =self.limit_error, sig_type=GPIO.FALLING)
        self.mc.h_mot_h.set_limit_action(fxn =self.limit_error,sig_type=GPIO.FALLING)
        #self.mc.h_mot_h.set_limit_action(fxn=lambda x:HACKFXN(self.mc.h_mot_l, self.mc.h_mot_h), sig_type=GPIO.RISING)
        self.mc.v_mot.set_limit_action(fxn =self.limit_error,sig_type=GPIO.FALLING)
        self.mc.r_mot.set_limit_action(fxn =self.limit_error,sig_type=GPIO.FALLING)
        self.set_error_action(fxn=self.limit_error, sig_type=GPIO.FALLING)
        self.mc.run(self.controls)
        self.controls=[("Move",timeToRot*1.1,timeToRot*1.1,timeToRot*1.1,abs(rotDel),timeToRot/100)]*100
        self.mc.run(self.controls)
        self.mc.set_en_sb(0, 1)
        self.mc.h_mot_l.set_limit_action(0)
        self.mc.h_mot_h.set_limit_action(0)
        self.mc.v_mot.set_limit_action(0)
        self.mc.r_mot.set_limit_action(0)
        self.set_error_action(0)
        self.mc.y = self.mc.h_mot_h.dist_travel()
        self.mc.x = self.mc.v_mot.dist_travel()-self.mc.y
        self.mc.rot = self.mc.r_mot.rot_travel()
        print(self.mc.x,x)
        print(self.mc.y,y)
        print(self.mc.rot,rot)
        if abs(self.mc.x-x)>10 or abs(self.mc.y-y)>10 or abs(self.mc.rot-rot)>5:
            self.conn.send(MachineStatus.ERROR)
            self.conn.send("System start position is not exact.\n Please try again.")
        print("At Position")
        while self.in_interrupt:
            #print(self.in_interrupt)
            pass
        print("Passed")

    def moveMagnet(self,delay:list):
        self.goToPt(self.move.getPoints()[0].x(),self.move.getPoints()[0].y(),self.move.getRot()[0])
        #Assuming no acceleration/decleration
        self.mc.h_mot_l.set_limit_action(fxn =self.limit_error, sig_type=GPIO.FALLING)
        self.mc.h_mot_h.set_limit_action(fxn =self.limit_error,sig_type=GPIO.FALLING)
        #self.mc.h_mot_h.set_limit_action(fxn=lambda x:HACKFXN(self.mc.h_mot_l, self.mc.h_mot_h), sig_type=GPIO.RISING)
        self.mc.v_mot.set_limit_action(fxn =self.limit_error,sig_type=GPIO.FALLING)
        self.mc.r_mot.set_limit_action(fxn =self.limit_error,sig_type=GPIO.FALLING)
        self.set_error_action(fxn=self.limit_error, sig_type=GPIO.FALLING)
        self.controls=[]
        acc_time = delay[4]*.1
        delay[4]*=.8
        time_delay= delay[4]
        #set propper direction
        set_dir = ("Dir",math.copysign(1,delay[0]),math.copysign(1,delay[1]),math.copysign(1,delay[2]),math.copysign(1,delay[3]))
        self.controls.append(set_dir)
        y_acc=self.create_accel_delays(0,abs(delay[5]))
        x_acc=self.create_accel_delays(0,abs(delay[6]))
        y_dec=self.create_accel_delays(abs(delay[5]),0)
        x_dec=self.create_accel_delays(abs(delay[6]),0)
        acc_delay =[tuple(("Move",y_acc[i],y_acc[i],x_acc[i],abs(delay[3]),acc_time*.1))for i in range(len(y_acc))]
        dec_delay =[tuple(("Move",y_dec[i],y_dec[i],x_dec[i],abs(delay[3]),acc_time*.1))for i in range(len(y_dec))]
        self.controls.extend(acc_delay)
        while time_delay>100000000:
            self.controls.append(("Move",abs(delay[0]),abs(delay[1]),abs(delay[2]),abs(delay[3]),100000000))
            time_delay-=100000000
        self.controls.append(("Move",abs(delay[0]),abs(delay[1]),abs(delay[2]),abs(delay[3]),time_delay))
        self.controls.extend(dec_delay)
        #switch directions
        switch_dir = (set_dir[0],-1*set_dir[1],-1*set_dir[2],-1*set_dir[3],-1*set_dir[4])
        self.controls.append(switch_dir)
        #might be slightly different based on the math for x direction
        self.controls.extend(acc_delay)
        while delay[4]>100000000:
            self.controls.append(("Move",abs(delay[0]),abs(delay[1]),abs(delay[2]),abs(delay[3]),100000000))
            delay[4]-=100000000
        self.controls.append(("Move",abs(delay[0]),abs(delay[1]),abs(delay[2]),abs(delay[3]),delay[4]))
        self.controls.extend(dec_delay)
        self.controls*=self.move.getOsc()
        self.mc.set_en_sb(1, 1)
        #print(self.controls)
        if self.move.getSpeed()>125:
            self.mc.encoder_count(b'2')
        else:
            self.mc.encoder_count(b'1')
        self.mc.run(self.controls)
        self.mc.set_en_sb(0, 1)
        self.mc.h_mot_l.set_limit_action(0)
        self.mc.h_mot_h.set_limit_action(0)
        self.mc.v_mot.set_limit_action(0)
        self.mc.r_mot.set_limit_action(0)
        self.set_error_action(0)
        self.mc.set_actives(0)
        while self.in_interrupt:
            pass

    def findVelocity(self):
        delta_x = self.move.getPoints()[1].x()-self.move.getPoints()[0].x()
        delta_y = self.move.getPoints()[1].y()-self.move.getPoints()[0].y()
        delta_angle = self.move.getRot()[1]-self.move.getRot()[0]
        total_dist= ((delta_x**2)+(delta_y**2))**.5
        if total_dist==0:
            self.conn.send(MachineStatus.ERROR)
            self.conn.send("There is no distance to move.")
            return [10,10,10,10,0,0,0]
        x_speed = self.move.getSpeed()*delta_x/total_dist
        y_speed = self.move.getSpeed()*delta_y/total_dist
        rot_speed = self.move.getSpeed()*delta_angle/total_dist
        x_speed_act=y_speed+x_speed
        y_delay = self.vel_to_delay(y_speed)
        x_delay = self.vel_to_delay(x_speed_act)
        if self.move.getSpeed()==0:
            self.conn.send(MachineStatus.ERROR)
            self.conn.send("There is no speed given.")
            return [10,10,10,10,0,0,0]
        path_time = total_dist/self.move.getSpeed()*1000000000
        if rot_speed ==0:
            rot_delay=2*path_time
        else:
            rot_delay = (1000000000/(rot_speed*(20/12)))*(1.8/(8*2))
        return [y_delay,y_delay,x_delay,rot_delay,path_time,y_speed,x_speed_act]

    def vel_to_delay(self,velocity):
        if velocity == 0: 
            return 1000000000
        return (1000000000/(velocity*(360/(12*math.pi))))*(1.8/(8*2))


    def create_accel_delays(self, start_v, end_v):
        delays = []
        for i in range(10):
            delays.append(self.vel_to_delay((.1*(end_v-start_v)+start_v)))
        return delays
        #for xvel, yvel from max velocity to 0 in increments of 1ms# decelleration
        #    x: vel_to_del(vxel)
        #    y = vel_to_del(yvel + yvel)

    def limit_error(self,num):
        print("WHY")
        self.in_interrupt=True
        self.mc.set_actives(0)
        self.mc.error_msg=True     
        #send message to front end
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
        self.conn.send(MachineStatus.ERROR)
        self.conn.send("System hit the edge. \nPosition is incorrect, please home before continuing. ")#+ str(num))
        #switch directions
        #move back so there is no home issue
        #time.sleep(.01)
        print("test")
        self.in_interrupt =False
         
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



