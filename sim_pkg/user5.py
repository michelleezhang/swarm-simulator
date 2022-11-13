import math
from math import sqrt
from cmath import exp 
from math import atan2 
import cmath
import string
import numpy as np
import re
import zlib

def usr(robot):
    # check if using legendre or pseudo zernike for moment calc
    # 1: use legendre polynomial for moments
    # 0: use pseudo zernike
    lpoly = 1

    # max number of robots is 100
    numrobots = 50

    # highest moment order
    maxorder = 8

    # from the image 
    A00 = 0.1442351221066887 #bunny 
    #A00 = 0.04846459003079923 #grey circles

    # how many decimal places to round sent message 
    rounddeci = 8

    # factor to speed or slow robots 
    adjspeed = 0.04

    # tolerance for the number of consecutive missed messages before a robot is forgotten
    misstol = 1.5*numrobots

    # used for simulation to print to file
    log = open("experiment_log"+str(robot.id), 'wb')

    # where the Jphi file is on the robot
    path = "./Jphi.txt"

    # parse the data to get Jphi that will be used in gradient descent
    tmpJphi = np.loadtxt(path, dtype=str, delimiter="|")

    # upload the desired moments
    path = "./DesMom.txt"

    filetype = float 
    if lpoly == 0: 
        filetype = complex 
    tmpDesMom = np.loadtxt(path, dtype=filetype)

    # Parameters and set up ------------------------------------------------------------------------------------------------------------------
    robot.set_led(0,0,100)

    # used to normalize the robot positions to be between -1 and 1
    # dimensions of the field
    minfieldx = -1.5
    maxfieldx = 1.5

    minfieldy = -1.5
    maxfieldy = 1.5

    # robot dimensions (of actual coachbot, wheel diameter=3cm, distance between wheels=12cm)
    base = 0.077 #/maxfieldx
    wheelradius = 0.031/2.0 #/maxfieldx
    
    # for collision avoidance
    # distance where robots are too close (proximity radius)
    coliR1 = 1.0*base
    # distance where robots can ignore neighbors (ignore radius)
    coliR2 = 3.5*base

    # normalize to be between -1,1 
    coliR1 = coliR1/maxfieldx
    coliR2 = coliR2/maxfieldx

    # used for point offset from the actual (x,y) used to recover point robot model
    h = base/2   


    # maximum saturation velocity robots can move
    maxvel = 0.4*(6.0*math.pi) #rad/s
    maxpwm = 40

    # number of coefficients
    numcoef = (((maxorder+1)*(maxorder+2))/2)-1

    # number of elements to be distributely averaged
    nelem = int(numcoef)
    comelem = 2

    # the desired moments
    desmom = np.zeros((nelem,1), dtype= filetype)
  
    for i in range(nelem):
        desmom[i,0] = tmpDesMom[i]


    # nelem x nelem matrix to be tuned, should be symmetric positive-definite gain matrix
    CG = np.zeros((nelem,nelem))
    #np.fill_diagonal(CG,1)

    for d in range(1,maxorder+1):
        tmpcoeff = (((d+1)*(d+2))/2)-1
        prevcoeff = ((d*(d+1))/2)-1

        tmpcoeff = tmpcoeff-prevcoeff
        
        #gain = (1.0/pow(d,0.5))
        gain = (1.0/pow(d,1.7))#+5.0
        #gain = (1.0/pow(10.0,d)) #+0.2

        for i in range(tmpcoeff):
            CG[i+prevcoeff,i+prevcoeff] = gain

    # for distributed average consensus
    aij = 1.0
    di_out = 0

    # track which robots are in the memory state and would be the value for di_out 
    # increments based on when robots are added to memory state 
    # decrements based on when robots are forgotten 
    dival = 0

    # max possible number, di_out and gamma will change based on messages from neighbors
    for i in range(numrobots-1):
        di_out +=  aij
    

    # gamma*di_out < 1
    gamma = 1.0/numrobots
    comgamma = 1.0/numrobots  

    # initialize x[0] to be all zeros
    xi = np.zeros((nelem+1,1), dtype=filetype)
    yi = np.zeros((nelem+1,1), dtype=filetype)

    comxi = np.zeros((comelem+1,1))
    comyi = np.zeros((comelem+1,1))


    # keep track of every neighbor's message for memory state
    # top row is neighbor index, 2nd is COMx, 3rd is COMy, and everything below in that column is the data
    # don't keep track of own measurement
    # fill with value of -1 which will never be a robot ID
    nmem_nr = numrobots-1
    nmem = np.zeros((nelem+6,nmem_nr), dtype=filetype)
    nmem.fill(-1)

    # index of next neighbor to be added to nmem
    next_nmem_idx = 0

    # flag to see if all neighbors have been added to nmem, 0 for false, 1 for true
    addAllN = 0

    # flag to see if at least one neighbor has been added to nmem
    # 0 for no neighbor, 1 for at least 1
    addN = 0

    # flag if there is a missede message - used to graph
    # 0: no missed, 1: missed
    missed = 0

    # keep a running tracker on how many messages are missed
    totmissed = 0

    # track the nearest neighbor
    nearestX = 0
    nearestY = 0
    nearestDist = 100000

    comavgx = 0
    comavgy = 0

    #````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
    while True:
        # delay is 20ms
        robot.delay()

        weights = np.zeros((nelem,1),dtype=filetype)

        # get position data from sensors
        rx, ry, rtheta = getPose(robot)

        # offset the point
        rx = rx + h*math.cos(rtheta)
        ry = ry + h*math.sin(rtheta)

        # normalize the x,y position to be between -1,1
        rx = rx/maxfieldx 
        ry = ry/maxfieldy 

        pose = np.zeros((2,1))
        pose[0,0] = rx
        pose[1,0] = ry

        # make moments with respect to swarm's COM instead of global COM--------------------------
        # calculate estimates of the moment coefficients

        # shift moments that are second order and higher
        tmpv = np.zeros((2,1))
        tmpv[0,0] = comavgx
        tmpv[1,0] = comavgy

        tmpweights1 = calcMoments(lpoly, 1, pose, A00, numrobots)
        tmpweights2 = calcMoments(lpoly, maxorder, (pose-tmpv), A00, numrobots)

        weights[0,0] = tmpweights1[0,0]
        weights[1,0] = tmpweights1[1,0]
        weights[2:,0] = tmpweights2[2:,0]

        # update ui
        ui = np.ones((nelem+1,1),dtype=filetype)
        ui[0:nelem,[0]] = weights

        comui = np.ones((comelem+1,1))
        comui[0,0] = rx
        comui[1,0] = ry


        # check messages from neighbors ----------------------------------------------------------
        msgs = robot.recv_msg()

        # keep track of neighbors
        nID = []
        nx = []

        # keep track of neighbor estimates of swarm COM
        ncom = []

        # if there are received messages
        if len(msgs) > 0:
            # track the nearest neighbor
            nearestX = rx
            nearestY = ry
            nearestDist = 100000

            for i in range(len(msgs)):
                msg = msgs[i]

                # decompress the message 
                msg = zlib.decompress(msg).decode()

                # convert from string to float array
                # remove everything from message except the numbers, letters, . + |
                msg = re.sub('[^a-zA-z.+-|0-9]','',msg)

                data = np.array(msg.split('|')).astype(filetype)

                #if len(data) == nelem+7: 
                # reshape to be vertical array
                data = np.reshape(data, (nelem+7,1))

                # neighbor's id
                obotID = data[0,0]

                # neighbor's x,y position
                obotx = data[1,0]
                oboty = data[2,0]

                # neighbor's estimate of the swarm com x, y
                ncomx = data[3,0]
                ncomy = data[4,0]
                ncombot = data[5,0]

                if lpoly == 0: 
                    # neighbor's id
                    obotID = obotID.real

                    # neighbor's x,y position
                    obotx = obotx.real
                    oboty = oboty.real

                    # neighbor's estimate of the swarm com x, y
                    ncomx = ncomx.real
                    ncomy = ncomy.real
                    ncombot = ncombot.real


                # extract out the data without the robot id, x, y position, comx, comy
                for dd in range(6):
                    data = np.delete(data,0)

                # make sure the array is vertical
                obotData = np.reshape(data, (nelem+1,1))

                # check if already added it as a neighbor
                if obotID not in nID:
                    nID.append(obotID)
                    nx.append(obotData)

                    tmpcom = np.zeros((comelem+1,1))
                    tmpcom[0,0] = ncomx
                    tmpcom[1,0] = ncomy
                    tmpcom[2,0] = ncombot
                    ncom.append(tmpcom)

                    # this neighbor is closer
                    distaway = calcdist(rx,ry,obotx,oboty)
                    if  distaway < nearestDist:
                        nearestX = obotx
                        nearestY = oboty
                        nearestDist = distaway

                    # check if all possible neighbors have been added
                    # next_nmem_idx increments after adding a neighbor
                    if next_nmem_idx == (numrobots-1):
                        # all neighbors have been added
                        addAllN = 1

                    # check to make sure message isn't from an already recorded neighbor
                    # flag, 0: id not recorded, 1: id is recorded
                    recID = 1
                    checkID = np.where(nmem[0,:] == obotID)
                    if checkID[0].size == 0:
                        # this id doesn't exist yet
                        recID = 0

                    # add new neighbor to nmem; not all neighbors added yet and ID not already recorded
                    if addAllN == 0 and recID == 0:
                        # add it to the neighbor memory array
                        nmem[0, [next_nmem_idx]] = obotID

                        # start the counter for how many missed messages 
                        nmem[1, [next_nmem_idx]] = 0

                        # add COM x,y to neighbor memory array
                        nmem[2:5, [next_nmem_idx]] = tmpcom

                        # fill up rest of column with the data
                        nmem[5:nelem+6,[next_nmem_idx]] = obotData

                        # increase the index
                        next_nmem_idx+=1
                        # increment counter for number of neighbors 
                        dival += 1

                    else:
                        # this neighbor is already in nmem; just update where it is
                        nmem[2:5, checkID[0]] = tmpcom
                        nmem[5:nelem+6,checkID[0]] = obotData

                        # restart the counter for how many missed messages 
                        nmem[1, checkID[0]] = 0


                    # neighbor added
                    addN = 1

            # went through all msgs
        # end if


        # implement the memory state ---------------------------------------------------------------
        # go through every message received by looking through nID
        # robot's whose ID is not in nID need to use memory state
        # find robot IDs missing from the most recent messages
        notRecID = 0
        if lpoly == 1: 
            notRecID = np.setdiff1d(nmem[0,:],nID)
        else: 
            notRecID = np.setdiff1d(nmem[0,:].real,nID)

        # find the neighbor estimates now
        nest = np.zeros((nelem+1,1),dtype=filetype)
        ncomest = np.zeros((comelem+1,1))

        ri = np.zeros((nelem+1,1),dtype=filetype)
        comri = np.zeros((comelem+1,1))


        # loop through all neighbors in nmem
        # make sure there are first neighbors added to nmem
        if addN == 1:
            missed = 0
            for i in range(nmem[0].size):
                # memory state

                # go through each column and check if the ID was flagged as not having a recent msg
                currID = nmem[0,i]
                if lpoly == 0: 
                    currID = currID.real

                # only do this if the ID is not -1
                if currID != -1:
                    # we didn't hear from this robot this time
                    if currID in notRecID:
                        # no new message was received - use memory
                        # find previous data stored in nmem
                        curridx = 0 
                        if lpoly == 1: 
                            curridx = np.where(nmem[0,:]==currID)
                        else: 
                            curridx = np.where(nmem[0,:].real ==currID)

                        # increment the missed message counter 
                        nmem[1, curridx[0]] += 1

                        missedidx = 0 
                        if lpoly == 1: 
                            missedidx = nmem[1, curridx[0]]
                        else: 
                            missedidx = nmem[1, curridx[0]].real
                            
                        # only use if there have been less than the allowed consecutive missed number of msgs 
                        if  missedidx < misstol:        
                            ri = nmem[5:nelem+6, curridx[0]]
                            if lpoly == 1: 
                                comri = nmem[2:5, curridx[0]]
                            else:
                                comri = nmem[2:5, curridx[0]].real

                            # comment out prediction term (instead of memory state + prediction, use just memory state)
                            # yi hasn't updated yet so it's still yi[t-1]
                            #ri += gamma*yi
                            #comri += comgamma*comyi

                        # this robot needs to be forgotten 
                        else: 
                            # delete the column 
                            tmpnmem = np.delete(nmem, curridx[0], 1)

                            # new column of -1 fillers 
                            newcol = np.ones((nelem+6,1))
                            newcol.fill(-1)

                            # add the new column to the end 
                            nmem = np.concatenate((tmpnmem,newcol),1)
                            
                            # not all possible robots have been added, decrease counter 
                            next_nmem_idx -= 1 
                            addAllN = 0

                            dival -= 1 
                        
                        missed += 1
                        totmissed += 1
                    else:
                        # we heard from this robot, use the current message data
                        # find the index in nID
                        nIDidx = nID.index(currID)

                        ri = nx[nIDidx]
                        comri = ncom[nIDidx]

                    # multiply ri by aij and add to the neighbor estimates
                    nest += aij*ri
                    ncomest += aij*comri
            # looped through all neighbors


        # update di_out based on neighbors 
        if dival > 0: 
            di_out = dival


        yi = ui - di_out*xi + nest
        comyi = comui - di_out*comxi + ncomest


        # update estimate
        xi += gamma*yi
        comxi += comgamma*comyi

        # swarm COM x, y
        comavgx = comyi[0,0]/comyi[comelem,0]
        comavgy = comyi[1,0]/comyi[comelem,0]


        # processing data to be sent out to other robots ------------------------------------------------------------------------------------
        if rounddeci > 0: 
            # round the decimal places so data sent is smaller 
            for i in range(nelem+1):
                if lpoly == 1: 
                    xi[i,0] = round(xi[i,0],rounddeci)
                else: 
                    tempreal = round(xi[i,0].real,rounddeci)
                    tempimag = round(xi[i,0].imag,rounddeci)
                    xi[i,0] = complex(tempreal,tempimag)

            rx = round(rx,rounddeci)
            ry = round(ry,rounddeci)
            for i in range(3):
                comxi[i,0] = round(comxi[i,0],rounddeci)
        
        # add the robot id to the first index
        tmpxi = np.insert(xi,0,robot.id)

        # now insert the robot x, y to the 2nd and 3rd index positions
        tmpxi = np.insert(tmpxi,1,rx)
        tmpxi = np.insert(tmpxi,2,ry)

        # insert the estimated swarm com x,y to the 4th and 5th index positions
        tmpxi = np.insert(tmpxi,3,comxi[0,0])
        tmpxi = np.insert(tmpxi,4,comxi[1,0])
        tmpxi = np.insert(tmpxi,5,comxi[2,0])

        tmpxi = np.reshape(tmpxi, (nelem+7,1))

        # flatten it for transport
        flatxi = np.ravel(tmpxi)

        # change to string
        stringxi = np.array2string(flatxi, separator = "|")

        # remove [] characters from string
        stringxi = stringxi.replace("[","")
        stringxi = stringxi.replace("]","")

        # compress message to be sent 
        compxi = zlib.compress(stringxi.encode())

        # send aij*xi to neighbors, aij = 1
        robot.send_msg(compxi)


        # logging ----------------------------------------------------------------------------------------------------------------------------------------
        swrite = "{},".format(rx)
        log.write(swrite)
        log.flush()

        swrite = "{},".format(ry)
        log.write(swrite)
        log.flush()

        swrite = "{},".format(totmissed)
        log.write(swrite)
        log.flush()

        swrite = "{},".format(comavgx)
        log.write(swrite)
        log.flush()

        swrite = "{},".format(comavgy)
        log.write(swrite)
        log.flush()

        # log all the moment coefficients
        for i in range(nelem-1):
            stmp = yi[i,0]/yi[nelem,0]
            swrite = "{},".format(stmp)
            log.write(swrite)
            log.flush()

        # last coefficient doesn't need a comma following it and needs a new line\
        stmp = yi[nelem-1,0]/yi[nelem,0]
        swrite = "{},".format(stmp)
        log.write(swrite)
        log.flush()


        swrite = "{} \n".format(missed)
        log.write(swrite)
        log.flush()


        # moving ---------------------------------------------------------------------------------------------------------------------------------------
        # calculate the control law
        ci = np.zeros((2,1))
        
        # estimated moments 
        vi = np.zeros((nelem,1),dtype=filetype)

        for ii in range(nelem):
            vi[ii,0] = yi[ii,0]/yi[nelem,0]

        if lpoly==1: 
            # ci' = -[Jphi].T*CG*[vi - fs],
            #    vi = actual local moment estimate
            #    fs = desired moments (nelem,1)           
            vf = vi - desmom
            #print(vi)

            # calculate Jphi (nelem,2) Jacobian matrix of moment vector
            Jphishape = tmpJphi.shape

            jx = rx
            jy = ry 

            Jphi = np.zeros((Jphishape[0],Jphishape[1]), dtype=filetype)
            for i in range(Jphishape[0]):
                for j in range(Jphishape[1]):
                    Jphi[i,j] = eval(tmpJphi[i,j])
            # got Jphi now

            # calculate ci' (commanded velocity)
            JphiT = np.transpose(Jphi)

            JphiT = -JphiT

            ci = np.dot(JphiT,CG)
            ci = np.dot(ci,vf)

        if lpoly == 0: 
            # take the derivative of the cost with respect to x and y 
            # use these as velocity commands 
            dJx = 0 
            dJy = 0 

            # go through every moment coefficient 
            # counter to keep track of the moment coefficient 
            cc = 0          
            for p in range(1,maxorder+1):
                dAdx = 0 
                dAdy = 0 
                for q in range(p+1):
                    r = math.sqrt(pow(rx,2) + pow(ry,2))
                    # calculate dA/dr and dA/dtheta
                    dSr = calcdSr(p,q,r)
                    dAdr = dSr * cmath.exp(-1j*q*rtheta) * A00 *(p+1)/numrobots 

                    # find radial functions Spq
                    Spq = 0
                    for k in range(q,p+1):
                        Spq += calcPZM(p,q,k)*pow(r,k)
                    dAdtheta = Spq * cmath.exp(-1j*q*rtheta) * (-1j)*q *A00*(p+1)/numrobots

                    # calculate dA/dx and dA/dy where r = sqrt(x^2 + y^2) and theta = atan(y/x)
                    # finding dA/dx [p,q] and dA/dtheta [p,q] - associated with each coefficient 
                    dAdx = dAdr*math.cos(rtheta) - dAdtheta*math.sin(rtheta)*(1/r)
                    dAdy = dAdr*math.sin(rtheta) + dAdtheta*math.cos(rtheta)*(1/r)

                    # real part of the gradient 
                    a = CG[cc,cc]*(vi[cc,0].real - desmom[cc,0].real)

                    # imaginary part of the gradient
                    b = CG[cc,cc]*(vi[cc,0].imag - desmom[cc,0].imag)

                    dJx += a*dAdx.real
                    dJx += b*dAdx.imag

                    dJy += a*dAdy.real
                    dJy += b*dAdy.imag 

                    cc += 1 
            # went through all the moment coefficients 

            # velocity command 
            ci[0,0] = -dJx
            ci[1,0] = -dJy 

        #if robot.id == 0:
        #    print(ci)

        # desired velocity after collision avoidance
        desvel = np.zeros((2,1))

        # find vector from the robot to its nearest neighbor
        nearestvec = np.zeros((2,1))
        nearestvec[0,0] = nearestX - rx
        nearestvec[1,0] = nearestY - ry

        # calculate collision avoidance vector in direction of -nearestvec with magnitude ci
        magnearvec = calcdist(0,0,nearestvec[0,0],nearestvec[1,0])
        coliavec = -(calcdist(0,0,ci[0,0],ci[1,0])*nearestvec)/magnearvec


        alpha = (magnearvec - coliR1)/(coliR2-coliR1)

        if magnearvec > coliR2:
            desvel = ci
            #robot.set_led(0,0,100)
        elif magnearvec <= coliR1:
            desvel = coliavec
            #robot.set_led(100,0,0)
        else:
            desvel = alpha*ci + (1-alpha)*coliavec
            #robot.set_led(0,100,0)

        # adjust the robot velocity 
        desvel = adjspeed*desvel

        # get wheel velocities from commanded velocity
        uL, uR = getWheelVel(robot,desvel[0,0],desvel[1,0],rtheta,base/maxfieldx, wheelradius/maxfieldx)

        # velocity motor pwm to send out to robot
        compwmL = 0
        compwmR = 0

        Lwheelvels = 0
        Lwheelpwm = 0

        Rwheelvels = 0
        Rwheelpwm = 0

        numspace = 2*maxpwm

        minvel = 0

        if uL < 0:
            if uL < -maxvel:
                uR = (maxvel*uR)/abs(uL)
                uL = -maxvel
            # map velocities to pwm signal
            Lwheelvels = np.linspace(-maxvel,minvel,num=numspace)
            Lwheelpwm = np.linspace(-maxpwm,minvel,num=numspace)
        else:
            if uL > maxvel:
                uR = (maxvel*uR)/abs(uL)
                uL = maxvel
            # map velocities to pwm signal
            Lwheelvels = np.linspace(minvel,maxvel,num=numspace)
            Lwheelpwm = np.linspace(minvel,maxpwm,num=numspace)

        if uR < 0:
            if uR < -maxvel:
                uL = (maxvel*uL)/abs(uR)
                uR = -maxvel
            # map velocities to pwm signal
            Rwheelvels = np.linspace(-maxvel,minvel,num=numspace)
            Rwheelpwm = np.linspace(-maxpwm,minvel,num=numspace)
        else:
            if uR > maxvel:
                uL = (maxvel*uL)/abs(uR)
                uR = maxvel
            # map velocities to pwm signal
            Rwheelvels = np.linspace(minvel,maxvel,num=numspace)
            Rwheelpwm = np.linspace(minvel,maxpwm,num=numspace)


        # find closest wheel pwm that most closely matches
        # find index of this value using absolute difference function
        adfuL = lambda i : abs(Lwheelvels[i] - uL)
        uLidx = min(range(len(Lwheelvels)), key=adfuL)

        adfuR = lambda i : abs(Rwheelvels[i] - uR)
        uRidx = min(range(len(Rwheelvels)), key=adfuR)

        # commanded pwm signals to send to the robot
        compwmL = Lwheelpwm[uLidx]
        compwmR = Rwheelpwm[uRidx]

        if robot.id == 0:
            print(compwmL,compwmR)

        if abs(compwmL) < 7.0 and abs(compwmR) < 7.0: 
            robot.set_led(100,0,0)
        else:
            robot.set_led(0,100,0)

        robot.set_vel(compwmL,compwmR)


# functions --------------------------------------------------------------------


# generate legendre polynomial recursively
# Inputs:
#   n (int): order of legendre polynomial
#   x (int): value to be evaluated
# Outputs:
#   fx (double): evaluated legendre polynomial
def calcLegendre(n,x):
    if n==0:
        return 1.0
    elif n==1:
        return x
    else:
        return ((2*n-1)/float(n))*x*calcLegendre(n-1,x) - ((n-1)/float(n))*calcLegendre(n-2,x)

# generate pseudo zernike moments coefficients recursively
# Inputs:
#   p (int): order of pseudo zernike moment
#   q (int): repetition
#   k (int): summation of radial function counter
# Outputs:
#   x (double): coefficient of radial function
def calcPZM(p,q,k):
    if k < p:
        return -calcPZM(p,q,k+1)*(k+q+2)*(k-q+1)/((p+k+2)*(p-k))
    elif q < p:
        return calcPZM(p,q+1,p)*(k+q+2)/(k-q)
    else:
        return 1

# generate moments
# Inputs:
#   momtype (int): 1 if using legendre polynomials, 0 if pseudo zernike moments
#   momorder (int): highest order moment to calculate
#   pos  (2 x 1 matrix): (x,y) position of robot
#   A00 is actually A00/numrobots
# Outputs:
#   avgweights (np array): averaged weights of the function
def calcMoments(momtype, momorder, pos, A00, numrobots):
    # use legendre moments
    if momtype == 1:
        # preallocate array
        # sum of natural numbers formula (n(n+1))/2
        numelements = int((((momorder+1)*(momorder+2))/2)-1)

        #avgweights = np.zeros((numelements,1))

        weights = np.zeros((numelements,1))

        # keep track of array element
        counter = 0

        x = pos[0,0]
        y = pos[1,0]

        for i in range(1,momorder+1):
            # keep track of the degrees changing
            step = i

            while step >= 0:
                p = step
                q = i - step

                Ppx = calcLegendre(p,x)
                Pqy = calcLegendre(q,y)

                tmpL = ((2*p+1)*(2*q+1)/4.0)*Ppx*Pqy

                weights[counter,0] = tmpL

                step = step -1
                counter = counter +1
                #print("-------------------------")
            # end while
        # end for loop

        #avgweights = weights

        return weights

    else: # using pseudo zernike moments
        # preallocate array
        # sum of natural numbers formula (n(n+1))/2
        numelements = int((((momorder+1)*(momorder+2))/2)-1)

        weights = np.zeros((numelements,1), dtype = complex)

        # keep track of array element
        counter = 0

        x = pos[0,0]
        y = pos[1,0]

        # convert to polar coordinates
        r = math.sqrt(pow(x,2) + pow(y,2))
        theta = math.atan2(y,x)

        # theta should be between 0 and 2pi but atan2 is [-pi,pi]
        if theta < 0:
            theta += 2*math.pi

        # only calculate those inside unit circle
        if abs(r) <= 1:
            for p in range(1,momorder+1):
                for q in range(p+1):
                    # find radial functions Spq
                    Spq = 0
                    for k in range(q,p+1):
                        Spq = Spq + calcPZM(p,q,k,)*pow(r,k)

                    # find pseudo zernike polynomials Wpq
                    Wpq = Spq * cmath.exp(-1j*q*theta)

                    weights[counter,0] = ((p+1))*Wpq*A00
                    counter = counter +1
                # end while loop
            # end for loop

        return weights


# For pzm: calculate dS/dr where S = calcPZM*r^k
# Inputs:
#   p (int): order of pseudo zernike moment
#   q (int): repetition
#   r (double): radial component given robot x, y
# Outputs: 
#   dSr (double): dS/dr at the specific moment order and robot position 
def calcdSr(p,q,r):
    dSr = 0.0
    for k in range(q,p+1):
        if k>0: 
            dSr += calcPZM(p,q,k)*k*pow(r,k-1)
    return dSr 


# helper function to calculate distance from (x2,y2) and (x1,y1)
def calcdist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


# returns robot x, y, theta
def getPose(robot):
    # get robot's pose (x,y,theta)
    pose_t=robot.get_pose()

    while not pose_t:
        pose_t=robot.get_pose()
    # check robot's position
    x = pose_t[0]
    y = pose_t[1]
    theta = pose_t[2] #between 0 and pi and -pi and 0
    return x, y, theta


# returns robot left and right wheel velocities (ul,ur) from a commanded velocity (ux,uy).T
# Inputs:
#   ux: commanded x velocity of the reference point
#   uy: commanded y velocity of the reference point
#   theta: robot theta value
#   L: distance between robot wheels
#   R: wheel radius
def getWheelVel(robot,ux,uy, theta, L, R):
    comU = np.zeros((2,1))
    comU[0,0] = ux
    comU[1,0] = uy

    h = L/2

    tmp = np.zeros((2,2))
    tmp[0,0] = 2*h*math.cos(theta) + L*math.sin(theta)
    tmp[0,1] = 2*h*math.sin(theta) - L*math.cos(theta)
    tmp[1,0] = 2*h*math.cos(theta) - L*math.sin(theta)
    tmp[1,1] = 2*h*math.sin(theta) + L*math.cos(theta)

    u = np.zeros((2,1))
    u = (1/(2*h*R))*np.dot(tmp,comU)

    ul = u[0,0]
    ur = u[1,0]

    return ul, ur