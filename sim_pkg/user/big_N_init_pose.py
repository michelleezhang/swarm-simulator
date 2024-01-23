'''
Firefly

Function to initialize agent's poses.
Input:
swarmsize --  swarmsize.
x -- An array to store  agents' x positions, the length of this array is the same as swarmsize
y -- An array to store agents' y positions, the length of this array is the same as swarmsize
theta -- An array to store agents' orientations, the length of this is the same as swarmsize

Usage:
Usr can configure an agent's initial x, y, theta by modifying the value of the corresponding element in array x, y, and theta.
For example, initialize agent 0's pose to x = 0, y = 1, theta = 2:
x[0] = 0
y[0] = 1
theta[0] = 2

Constraints to be considered:
x -- the value should range between -2.5 to 2.5.
y -- the value should range between -1.5 to 1.5.
theta -- the value should range between -pi to pi.

The minimal pairwise inter-agent distance should be greater than 0.12

def init(swarmsize, x, y, theta, a_ids):
import math
import random
for i in range(swarmsize):
x[i] = (i % 16 ) * 0.11-1
y[i] = (i / 16 ) * 0.11-1
a_ids[i] = 0
theta[i] = 0
if i==0:
a_ids[i]=1
elif i==15:
a_ids[i]=2
pass
'''
def init(swarmsize, x, y, theta, a_ids):
	from math import pi
	for i in range(0,swarmsize):
		if i == 0:
			x[i] = -2.8
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 1:
			x[i] = -2.6
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 2:
			x[i] = -2.4
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 3:
			x[i] = -2.2
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 4:
			x[i] = -2.0
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 5:
			x[i] = -1.8
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 6:
			x[i] = 0.8
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 7:
			x[i] = 1.0
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 8:
			x[i] = 1.2
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 9:
			x[i] = 1.4
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 10:
			x[i] = 1.6
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 11:
			x[i] = 1.8
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 12:
			x[i] = 2.0
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 13:
			x[i] = 2.2
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 14:
			x[i] = 2.4
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 15:
			x[i] = 2.6
			y[i] = 3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 16:
			x[i] = -2.8
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 17:
			x[i] = -2.6
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 18:
			x[i] = -2.4
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 19:
			x[i] = -2.2
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 20:
			x[i] = -2.0
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 21:
			x[i] = -1.8
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 22:
			x[i] = 0.8
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 23:
			x[i] = 1.0
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 24:
			x[i] = 1.2
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 25:
			x[i] = 1.4
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 26:
			x[i] = 1.6
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 27:
			x[i] = 1.8
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 28:
			x[i] = 2.0
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 29:
			x[i] = 2.2
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 30:
			x[i] = 2.4
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 31:
			x[i] = 2.6
			y[i] = 2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 32:
			x[i] = -2.8
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 33:
			x[i] = -2.6
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 34:
			x[i] = -2.4
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 35:
			x[i] = -2.2
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 36:
			x[i] = -2.0
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 37:
			x[i] = -1.8
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 38:
			x[i] = -1.6
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 39:
			x[i] = -1.4
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 40:
			x[i] = 0.8
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 41:
			x[i] = 1.0
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 42:
			x[i] = 1.2
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 43:
			x[i] = 1.4
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 44:
			x[i] = 1.6
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 45:
			x[i] = 1.8
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 46:
			x[i] = 2.0
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 47:
			x[i] = 2.2
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 48:
			x[i] = 2.4
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 49:
			x[i] = 2.6
			y[i] = 2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 50:
			x[i] = -2.8
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 51:
			x[i] = -2.6
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 52:
			x[i] = -2.4
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 53:
			x[i] = -2.2
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 54:
			x[i] = -2.0
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 55:
			x[i] = -1.8
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 56:
			x[i] = -1.6
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 57:
			x[i] = -1.4
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 58:
			x[i] = 0.8
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 59:
			x[i] = 1.0
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 60:
			x[i] = 1.2
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 61:
			x[i] = 1.4
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 62:
			x[i] = 1.6
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 63:
			x[i] = 1.8
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 64:
			x[i] = 2.0
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 65:
			x[i] = 2.2
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 66:
			x[i] = 2.4
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 67:
			x[i] = 2.6
			y[i] = 2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 68:
			x[i] = -2.8
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 69:
			x[i] = -2.6
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 70:
			x[i] = -2.4
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 71:
			x[i] = -2.2
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 72:
			x[i] = -2.0
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 73:
			x[i] = -1.8
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 74:
			x[i] = -1.6
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 75:
			x[i] = -1.4
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 76:
			x[i] = -1.2
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 77:
			x[i] = -1.0
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 78:
			x[i] = 0.8
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 79:
			x[i] = 1.0
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 80:
			x[i] = 1.2
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 81:
			x[i] = 1.4
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 82:
			x[i] = 1.6
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 83:
			x[i] = 1.8
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 84:
			x[i] = 2.0
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 85:
			x[i] = 2.2
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 86:
			x[i] = 2.4
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 87:
			x[i] = 2.6
			y[i] = 2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 88:
			x[i] = -2.8
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 89:
			x[i] = -2.6
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 90:
			x[i] = -2.4
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 91:
			x[i] = -2.2
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 92:
			x[i] = -2.0
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 93:
			x[i] = -1.8
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 94:
			x[i] = -1.6
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 95:
			x[i] = -1.4
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 96:
			x[i] = -1.2
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 97:
			x[i] = -1.0
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 98:
			x[i] = 0.8
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 99:
			x[i] = 1.0
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 100:
			x[i] = 1.2
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 101:
			x[i] = 1.4
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 102:
			x[i] = 1.6
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 103:
			x[i] = 1.8
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 104:
			x[i] = 2.0
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 105:
			x[i] = 2.2
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 106:
			x[i] = 2.4
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 107:
			x[i] = 2.6
			y[i] = 2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 108:
			x[i] = -2.8
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 109:
			x[i] = -2.6
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 110:
			x[i] = -2.4
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 111:
			x[i] = -2.2
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 112:
			x[i] = -2.0
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 113:
			x[i] = -1.8
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 114:
			x[i] = -1.6
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 115:
			x[i] = -1.4
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 116:
			x[i] = -1.2
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 117:
			x[i] = -1.0
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 118:
			x[i] = -0.8
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 119:
			x[i] = -0.6
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 120:
			x[i] = 1.2
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 121:
			x[i] = 1.4
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 122:
			x[i] = 1.6
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 123:
			x[i] = 1.8
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 124:
			x[i] = 2.0
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 125:
			x[i] = 2.2
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 126:
			x[i] = 2.4
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 127:
			x[i] = 2.6
			y[i] = 1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 128:
			x[i] = -2.8
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 129:
			x[i] = -2.6
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 130:
			x[i] = -2.4
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 131:
			x[i] = -2.2
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 132:
			x[i] = -2.0
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 133:
			x[i] = -1.8
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 134:
			x[i] = -1.6
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 135:
			x[i] = -1.4
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 136:
			x[i] = -1.2
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 137:
			x[i] = -1.0
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 138:
			x[i] = -0.8
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 139:
			x[i] = -0.6
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 140:
			x[i] = 1.2
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 141:
			x[i] = 1.4
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 142:
			x[i] = 1.6
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 143:
			x[i] = 1.8
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 144:
			x[i] = 2.0
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 145:
			x[i] = 2.2
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 146:
			x[i] = 2.4
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 147:
			x[i] = 2.6
			y[i] = 1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 148:
			x[i] = -2.8
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 149:
			x[i] = -2.6
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 150:
			x[i] = -2.4
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 151:
			x[i] = -2.2
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 152:
			x[i] = -2.0
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 153:
			x[i] = -1.8
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 154:
			x[i] = -1.6
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 155:
			x[i] = -1.4
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 156:
			x[i] = -1.2
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 157:
			x[i] = -1.0
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 158:
			x[i] = -0.8
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 159:
			x[i] = -0.6
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 160:
			x[i] = -0.4
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 161:
			x[i] = -0.2
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 162:
			x[i] = 1.6
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 163:
			x[i] = 1.8
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 164:
			x[i] = 2.0
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 165:
			x[i] = 2.2
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 166:
			x[i] = 2.4
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 167:
			x[i] = 2.6
			y[i] = 1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 168:
			x[i] = -2.8
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 169:
			x[i] = -2.6
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 170:
			x[i] = -2.4
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 171:
			x[i] = -2.2
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 172:
			x[i] = -2.0
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 173:
			x[i] = -1.8
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 174:
			x[i] = -1.6
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 175:
			x[i] = -1.4
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 176:
			x[i] = -1.2
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 177:
			x[i] = -1.0
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 178:
			x[i] = -0.8
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 179:
			x[i] = -0.6
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 180:
			x[i] = -0.4
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 181:
			x[i] = -0.2
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 182:
			x[i] = 1.6
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 183:
			x[i] = 1.8
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 184:
			x[i] = 2.0
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 185:
			x[i] = 2.2
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 186:
			x[i] = 2.4
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 187:
			x[i] = 2.6
			y[i] = 1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 188:
			x[i] = -2.8
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 189:
			x[i] = -2.6
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 190:
			x[i] = -2.4
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 191:
			x[i] = -2.2
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 192:
			x[i] = -2.0
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 193:
			x[i] = -1.8
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 194:
			x[i] = -1.6
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 195:
			x[i] = -1.4
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 196:
			x[i] = -1.2
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 197:
			x[i] = -1.0
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 198:
			x[i] = -0.8
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 199:
			x[i] = -0.6
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 200:
			x[i] = -0.4
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 201:
			x[i] = -0.2
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 202:
			x[i] = 0.0
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 203:
			x[i] = 0.2
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 204:
			x[i] = 2.0
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 205:
			x[i] = 2.2
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 206:
			x[i] = 2.4
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 207:
			x[i] = 2.6
			y[i] = 1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 208:
			x[i] = -2.8
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 209:
			x[i] = -2.6
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 210:
			x[i] = -2.4
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 211:
			x[i] = -2.2
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 212:
			x[i] = -2.0
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 213:
			x[i] = -1.8
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 214:
			x[i] = -1.6
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 215:
			x[i] = -1.4
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 216:
			x[i] = -1.2
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 217:
			x[i] = -1.0
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 218:
			x[i] = -0.8
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 219:
			x[i] = -0.6
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 220:
			x[i] = -0.4
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 221:
			x[i] = -0.2
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 222:
			x[i] = 0.0
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 223:
			x[i] = 0.2
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 224:
			x[i] = 2.0
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 225:
			x[i] = 2.2
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 226:
			x[i] = 2.4
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 227:
			x[i] = 2.6
			y[i] = 0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 228:
			x[i] = -2.8
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 229:
			x[i] = -2.6
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 230:
			x[i] = -2.4
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 231:
			x[i] = -2.2
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 232:
			x[i] = -2.0
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 233:
			x[i] = -1.8
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 234:
			x[i] = -1.6
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 235:
			x[i] = -1.4
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 236:
			x[i] = -1.2
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 237:
			x[i] = -1.0
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 238:
			x[i] = -0.8
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 239:
			x[i] = -0.6
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 240:
			x[i] = -0.4
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 241:
			x[i] = -0.2
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 242:
			x[i] = 0.0
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 243:
			x[i] = 0.2
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 244:
			x[i] = 0.4
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 245:
			x[i] = 0.6
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 246:
			x[i] = 2.0
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 247:
			x[i] = 2.2
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 248:
			x[i] = 2.4
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 249:
			x[i] = 2.6
			y[i] = 0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 250:
			x[i] = -2.8
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 251:
			x[i] = -2.6
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 252:
			x[i] = -2.4
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 253:
			x[i] = -2.2
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 254:
			x[i] = -2.0
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 255:
			x[i] = -1.8
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 256:
			x[i] = -1.6
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 257:
			x[i] = -1.4
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 258:
			x[i] = -1.2
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 259:
			x[i] = -1.0
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 260:
			x[i] = -0.8
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 261:
			x[i] = -0.6
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 262:
			x[i] = -0.4
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 263:
			x[i] = -0.2
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 264:
			x[i] = 0.0
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 265:
			x[i] = 0.2
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 266:
			x[i] = 0.4
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 267:
			x[i] = 0.6
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 268:
			x[i] = 2.0
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 269:
			x[i] = 2.2
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 270:
			x[i] = 2.4
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 271:
			x[i] = 2.6
			y[i] = 0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 272:
			x[i] = -2.8
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 273:
			x[i] = -2.6
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 274:
			x[i] = -2.4
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 275:
			x[i] = -2.2
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 276:
			x[i] = -1.6
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 277:
			x[i] = -1.4
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 278:
			x[i] = -1.2
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 279:
			x[i] = -1.0
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 280:
			x[i] = -0.8
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 281:
			x[i] = -0.6
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 282:
			x[i] = -0.4
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 283:
			x[i] = -0.2
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 284:
			x[i] = 0.0
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 285:
			x[i] = 0.2
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 286:
			x[i] = 0.4
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 287:
			x[i] = 0.6
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 288:
			x[i] = 0.8
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 289:
			x[i] = 1.0
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 290:
			x[i] = 2.0
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 291:
			x[i] = 2.2
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 292:
			x[i] = 2.4
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 293:
			x[i] = 2.6
			y[i] = 0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 294:
			x[i] = -2.8
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 295:
			x[i] = -2.6
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 296:
			x[i] = -2.4
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 297:
			x[i] = -2.2
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 298:
			x[i] = -1.6
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 299:
			x[i] = -1.4
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 300:
			x[i] = -1.2
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 301:
			x[i] = -1.0
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 302:
			x[i] = -0.8
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 303:
			x[i] = -0.6
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 304:
			x[i] = -0.4
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 305:
			x[i] = -0.2
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 306:
			x[i] = 0.0
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 307:
			x[i] = 0.2
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 308:
			x[i] = 0.4
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 309:
			x[i] = 0.6
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 310:
			x[i] = 0.8
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 311:
			x[i] = 1.0
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 312:
			x[i] = 2.0
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 313:
			x[i] = 2.2
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 314:
			x[i] = 2.4
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 315:
			x[i] = 2.6
			y[i] = -0.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 316:
			x[i] = -2.8
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 317:
			x[i] = -2.6
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 318:
			x[i] = -2.4
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 319:
			x[i] = -2.2
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 320:
			x[i] = -1.2
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 321:
			x[i] = -1.0
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 322:
			x[i] = -0.8
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 323:
			x[i] = -0.6
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 324:
			x[i] = -0.4
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 325:
			x[i] = -0.2
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 326:
			x[i] = 0.0
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 327:
			x[i] = 0.2
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 328:
			x[i] = 0.4
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 329:
			x[i] = 0.6
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 330:
			x[i] = 0.8
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 331:
			x[i] = 1.0
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 332:
			x[i] = 1.2
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 333:
			x[i] = 1.4
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 334:
			x[i] = 2.0
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 335:
			x[i] = 2.2
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 336:
			x[i] = 2.4
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 337:
			x[i] = 2.6
			y[i] = -0.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 338:
			x[i] = -2.8
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 339:
			x[i] = -2.6
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 340:
			x[i] = -2.4
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 341:
			x[i] = -2.2
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 342:
			x[i] = -1.2
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 343:
			x[i] = -1.0
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 344:
			x[i] = -0.8
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 345:
			x[i] = -0.6
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 346:
			x[i] = -0.4
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 347:
			x[i] = -0.2
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 348:
			x[i] = 0.0
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 349:
			x[i] = 0.2
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 350:
			x[i] = 0.4
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 351:
			x[i] = 0.6
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 352:
			x[i] = 0.8
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 353:
			x[i] = 1.0
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 354:
			x[i] = 1.2
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 355:
			x[i] = 1.4
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 356:
			x[i] = 2.0
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 357:
			x[i] = 2.2
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 358:
			x[i] = 2.4
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 359:
			x[i] = 2.6
			y[i] = -0.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 360:
			x[i] = -2.8
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 361:
			x[i] = -2.6
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 362:
			x[i] = -2.4
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 363:
			x[i] = -2.2
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 364:
			x[i] = -0.8
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 365:
			x[i] = -0.6
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 366:
			x[i] = -0.4
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 367:
			x[i] = -0.2
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 368:
			x[i] = 0.0
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 369:
			x[i] = 0.2
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 370:
			x[i] = 0.4
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 371:
			x[i] = 0.6
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 372:
			x[i] = 0.8
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 373:
			x[i] = 1.0
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 374:
			x[i] = 1.2
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 375:
			x[i] = 1.4
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 376:
			x[i] = 1.6
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 377:
			x[i] = 1.8
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 378:
			x[i] = 2.0
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 379:
			x[i] = 2.2
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 380:
			x[i] = 2.4
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 381:
			x[i] = 2.6
			y[i] = -0.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 382:
			x[i] = -2.8
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 383:
			x[i] = -2.6
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 384:
			x[i] = -2.4
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 385:
			x[i] = -2.2
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 386:
			x[i] = -0.8
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 387:
			x[i] = -0.6
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 388:
			x[i] = -0.4
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 389:
			x[i] = -0.2
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 390:
			x[i] = 0.0
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 391:
			x[i] = 0.2
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 392:
			x[i] = 0.4
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 393:
			x[i] = 0.6
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 394:
			x[i] = 0.8
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 395:
			x[i] = 1.0
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 396:
			x[i] = 1.2
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 397:
			x[i] = 1.4
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 398:
			x[i] = 1.6
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 399:
			x[i] = 1.8
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 400:
			x[i] = 2.0
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 401:
			x[i] = 2.2
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 402:
			x[i] = 2.4
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 403:
			x[i] = 2.6
			y[i] = -0.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 404:
			x[i] = -2.8
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 405:
			x[i] = -2.6
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 406:
			x[i] = -2.4
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 407:
			x[i] = -2.2
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 408:
			x[i] = -0.4
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 409:
			x[i] = -0.2
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 410:
			x[i] = 0.0
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 411:
			x[i] = 0.2
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 412:
			x[i] = 0.4
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 413:
			x[i] = 0.6
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 414:
			x[i] = 0.8
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 415:
			x[i] = 1.0
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 416:
			x[i] = 1.2
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 417:
			x[i] = 1.4
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 418:
			x[i] = 1.6
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 419:
			x[i] = 1.8
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 420:
			x[i] = 2.0
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 421:
			x[i] = 2.2
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 422:
			x[i] = 2.4
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 423:
			x[i] = 2.6
			y[i] = -1.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 424:
			x[i] = -2.8
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 425:
			x[i] = -2.6
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 426:
			x[i] = -2.4
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 427:
			x[i] = -2.2
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 428:
			x[i] = -0.4
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 429:
			x[i] = -0.2
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 430:
			x[i] = 0.0
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 431:
			x[i] = 0.2
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 432:
			x[i] = 0.4
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 433:
			x[i] = 0.6
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 434:
			x[i] = 0.8
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 435:
			x[i] = 1.0
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 436:
			x[i] = 1.2
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 437:
			x[i] = 1.4
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 438:
			x[i] = 1.6
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 439:
			x[i] = 1.8
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 440:
			x[i] = 2.0
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 441:
			x[i] = 2.2
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 442:
			x[i] = 2.4
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 443:
			x[i] = 2.6
			y[i] = -1.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 444:
			x[i] = -2.8
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 445:
			x[i] = -2.6
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 446:
			x[i] = -2.4
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 447:
			x[i] = -2.2
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 448:
			x[i] = -2.0
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 449:
			x[i] = -1.8
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 450:
			x[i] = 0.0
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 451:
			x[i] = 0.2
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 452:
			x[i] = 0.4
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 453:
			x[i] = 0.6
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 454:
			x[i] = 0.8
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 455:
			x[i] = 1.0
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 456:
			x[i] = 1.2
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 457:
			x[i] = 1.4
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 458:
			x[i] = 1.6
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 459:
			x[i] = 1.8
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 460:
			x[i] = 2.0
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 461:
			x[i] = 2.2
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 462:
			x[i] = 2.4
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 463:
			x[i] = 2.6
			y[i] = -1.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 464:
			x[i] = -2.8
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 465:
			x[i] = -2.6
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 466:
			x[i] = -2.4
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 467:
			x[i] = -2.2
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 468:
			x[i] = -2.0
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 469:
			x[i] = -1.8
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 470:
			x[i] = 0.0
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 471:
			x[i] = 0.2
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 472:
			x[i] = 0.4
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 473:
			x[i] = 0.6
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 474:
			x[i] = 0.8
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 475:
			x[i] = 1.0
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 476:
			x[i] = 1.2
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 477:
			x[i] = 1.4
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 478:
			x[i] = 1.6
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 479:
			x[i] = 1.8
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 480:
			x[i] = 2.0
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 481:
			x[i] = 2.2
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 482:
			x[i] = 2.4
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 483:
			x[i] = 2.6
			y[i] = -1.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 484:
			x[i] = -2.8
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 485:
			x[i] = -2.6
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 486:
			x[i] = -2.4
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 487:
			x[i] = -2.2
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 488:
			x[i] = -2.0
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 489:
			x[i] = -1.8
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 490:
			x[i] = -1.6
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 491:
			x[i] = -1.4
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 492:
			x[i] = 0.4
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 493:
			x[i] = 0.6
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 494:
			x[i] = 0.8
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 495:
			x[i] = 1.0
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 496:
			x[i] = 1.2
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 497:
			x[i] = 1.4
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 498:
			x[i] = 1.6
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 499:
			x[i] = 1.8
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 500:
			x[i] = 2.0
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 501:
			x[i] = 2.2
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 502:
			x[i] = 2.4
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 503:
			x[i] = 2.6
			y[i] = -1.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 504:
			x[i] = -2.8
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 505:
			x[i] = -2.6
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 506:
			x[i] = -2.4
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 507:
			x[i] = -2.2
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 508:
			x[i] = -2.0
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 509:
			x[i] = -1.8
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 510:
			x[i] = -1.6
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 511:
			x[i] = -1.4
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 512:
			x[i] = 0.4
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 513:
			x[i] = 0.6
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 514:
			x[i] = 0.8
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 515:
			x[i] = 1.0
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 516:
			x[i] = 1.2
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 517:
			x[i] = 1.4
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 518:
			x[i] = 1.6
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 519:
			x[i] = 1.8
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 520:
			x[i] = 2.0
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 521:
			x[i] = 2.2
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 522:
			x[i] = 2.4
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 523:
			x[i] = 2.6
			y[i] = -2.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 524:
			x[i] = -2.8
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 525:
			x[i] = -2.6
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 526:
			x[i] = -2.4
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 527:
			x[i] = -2.2
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 528:
			x[i] = -2.0
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 529:
			x[i] = -1.8
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 530:
			x[i] = -1.6
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 531:
			x[i] = -1.4
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 532:
			x[i] = -1.2
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 533:
			x[i] = -1.0
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 534:
			x[i] = 0.8
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 535:
			x[i] = 1.0
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 536:
			x[i] = 1.2
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 537:
			x[i] = 1.4
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 538:
			x[i] = 1.6
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 539:
			x[i] = 1.8
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 540:
			x[i] = 2.0
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 541:
			x[i] = 2.2
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 542:
			x[i] = 2.4
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 543:
			x[i] = 2.6
			y[i] = -2.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 544:
			x[i] = -2.8
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 545:
			x[i] = -2.6
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 546:
			x[i] = -2.4
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 547:
			x[i] = -2.2
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 548:
			x[i] = -2.0
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 549:
			x[i] = -1.8
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 550:
			x[i] = -1.6
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 551:
			x[i] = -1.4
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 552:
			x[i] = -1.2
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 553:
			x[i] = -1.0
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 554:
			x[i] = 0.8
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 555:
			x[i] = 1.0
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 556:
			x[i] = 1.2
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 557:
			x[i] = 1.4
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 558:
			x[i] = 1.6
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 559:
			x[i] = 1.8
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 560:
			x[i] = 2.0
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 561:
			x[i] = 2.2
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 562:
			x[i] = 2.4
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 563:
			x[i] = 2.6
			y[i] = -2.4
			a_ids[i] = i
			theta[i] = 0
		elif i == 564:
			x[i] = -2.8
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 565:
			x[i] = -2.6
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 566:
			x[i] = -2.4
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 567:
			x[i] = -2.2
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 568:
			x[i] = -2.0
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 569:
			x[i] = -1.8
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 570:
			x[i] = -1.6
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 571:
			x[i] = -1.4
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 572:
			x[i] = -1.2
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 573:
			x[i] = -1.0
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 574:
			x[i] = 1.2
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 575:
			x[i] = 1.4
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 576:
			x[i] = 1.6
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 577:
			x[i] = 1.8
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 578:
			x[i] = 2.0
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 579:
			x[i] = 2.2
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 580:
			x[i] = 2.4
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 581:
			x[i] = 2.6
			y[i] = -2.6
			a_ids[i] = i
			theta[i] = 0
		elif i == 582:
			x[i] = -2.8
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 583:
			x[i] = -2.6
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 584:
			x[i] = -2.4
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 585:
			x[i] = -2.2
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 586:
			x[i] = -2.0
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 587:
			x[i] = -1.8
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 588:
			x[i] = -1.6
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 589:
			x[i] = -1.4
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 590:
			x[i] = -1.2
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 591:
			x[i] = -1.0
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 592:
			x[i] = 1.2
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 593:
			x[i] = 1.4
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 594:
			x[i] = 1.6
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 595:
			x[i] = 1.8
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 596:
			x[i] = 2.0
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 597:
			x[i] = 2.2
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 598:
			x[i] = 2.4
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 599:
			x[i] = 2.6
			y[i] = -2.8
			a_ids[i] = i
			theta[i] = 0
		elif i == 600:
			x[i] = -2.8
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 601:
			x[i] = -2.6
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 602:
			x[i] = -2.4
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 603:
			x[i] = -2.2
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 604:
			x[i] = -2.0
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 605:
			x[i] = -1.8
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 606:
			x[i] = -1.6
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 607:
			x[i] = -1.4
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 608:
			x[i] = -1.2
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 609:
			x[i] = -1.0
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 610:
			x[i] = 1.6
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 611:
			x[i] = 1.8
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 612:
			x[i] = 2.0
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 613:
			x[i] = 2.2
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 614:
			x[i] = 2.4
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 615:
			x[i] = 2.6
			y[i] = -3.0
			a_ids[i] = i
			theta[i] = 0
		elif i == 616:
			x[i] = -2.8
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 617:
			x[i] = -2.6
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 618:
			x[i] = -2.4
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 619:
			x[i] = -2.2
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 620:
			x[i] = -2.0
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 621:
			x[i] = -1.8
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 622:
			x[i] = -1.6
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 623:
			x[i] = -1.4
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 624:
			x[i] = -1.2
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 625:
			x[i] = -1.0
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 626:
			x[i] = 1.6
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 627:
			x[i] = 1.8
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 628:
			x[i] = 2.0
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 629:
			x[i] = 2.2
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 630:
			x[i] = 2.4
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
		elif i == 631:
			x[i] = 2.6
			y[i] = -3.2
			a_ids[i] = i
			theta[i] = 0
	return x, y, theta, a_ids