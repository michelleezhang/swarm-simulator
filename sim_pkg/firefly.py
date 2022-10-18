import time
import random 

def usr(robot):

    T = random.randint(500,600)
    start_time = time.time()*1000
    print(T)
    while True:        
        id = robot.id

        if id == 3:
            robot.set_led(0,100,0)
            robot.delay(100)
            curr_time = time.time()*1000 - start_time
            curr_time = round(curr_time, 2)
            msg = "time:"+ str(curr_time)+';'
            robot.send_msg("led:(0,100,0);delay:1000;"+msg)
            robot.set_led(0,0,0)
            robot.delay(1000)

        else:
            val = robot.recv_msg(clear=True)
            if len(val[0]) > 1:
                txt = val[0]
                sub_str = 'delay'
                res = [i for i in range(len(txt)) if txt.startswith(sub_str, i)]

                # print(txt)
                # Get the delay
                ind = res[-1]
                # print(ind)
                
                txt = txt[ind:]
                # print(txt)
                ind_delim = txt.index(";")
                # print(ind_delim)
                delay_val = txt[6:ind_delim]
                print("Delay_val:",delay_val)
                delay_val = float(delay_val)
                
                # Get the time 
                ind = txt.index("time")
                ind_delim = ind +1 + txt[ind+1:].index(";")
                time_val = txt[ind+5:ind_delim]
                time_val = float(time_val)
                curr_time = time.time()*1000 - start_time
                print("Curr time:",curr_time)
                
                next_time = time_val + delay_val
                print("Next time:",next_time)
                T = delay_val
                del_Sleep = next_time - curr_time - 10
                print("Del Sleep:",del_Sleep)
                if del_Sleep> 0:
                    time.sleep((del_Sleep)/1000)
                continue
                
                
            r, g, b = (0, 100, 0)
            robot.set_led(r,g,b)
            robot.delay(100)
            T = int(T)
            curr_time = time.time()*1000 - start_time
            curr_time = round(curr_time, 2)
            msg_time = "time:"+ str(curr_time)+';'
            msg = "led:("+ str(r)+","+str(g)+","+str(b)+");" + "delay:"+ str(T)+";" + msg_time
            robot.send_msg(msg)
            robot.set_led(0,0,0)
            robot.delay(T)
        