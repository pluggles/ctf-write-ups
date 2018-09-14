#!/usr/bin/python3
import sys
import base64

def encode(filename):
    with open(filename, "r") as f:
        s = f.readline().strip()
        f.close
        return base64.b64encode((''.join([chr(ord(s[x])+([5,-1,3,-3,2,15,-6,3,9,1,-3,-5,3,-15] * 3)[x]) for x in range(len(s))])).encode('utf-8')).decode('utf-8')[::-1]

def decode(filename):
    with open(filename, "rw") as f:
        s = f.readline().strip()
        s = s[::-1]
        s = base64.b64decode(s)
        print s
        newString = (''.join([chr(ord(s[x]) - ([5,-1,3,-3,2,15,-6,3,9,1,-3,-5,3,-15] *3)[x]) for x in range(len(s))])).decode('utf-8').encode('utf-8')
        print newString

if __name__ == "__main__":
	print(decode(sys.argv[1]))
    #s = "test"
    #8NHY25mYthGfs5ndwx2Zk1lcaFGc4pWdVZFQoJmT
    #print ([5,-1, 3] *3)[7]
    #print "8NHY25mYthGfs5ndwx2Zk1lcaFGc4pWdVZFQoJmT"[::-1]