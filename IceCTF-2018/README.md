## Forensics 300: Lost in the Forest

**Challenge**
You've rooted a notable hacker's system and you're sure that he has hidden something juicy on there. Can you find his secret?

**Solution**
We receive a zip file named 'fs.zip' which contains a partial root file system of our hacker's machine. After unzipping we need to get an idea of what we are looking at. This is a perfect time to use `Tree` and just for fun lets use the `a` and `H` flags, a to see hidden files, and H to create an html page so we can easily view the files in a browser, for qucikly checking on things:
From just outsize of the unzipped directory run this:
```tree -aH . > web.html```

From there we can see everything in the directory the first thing that sticks out to me is the clue.png but that turned out to be a ![red herring](clue.png)

Next I notice the `hzpxbsklqvboyou` file which contains:
```8NHY25mYthGfs5ndwx2Zk1lcaFGc4pWdVZFQoJmT8NHY25mYthGfs5ndwx2Zk1lcaFGc4pWdVZFQoJmT8NHY25mYthGfs5ndwx2Zk1lcaFGc4pWdVZFQoJmT8NHY25mYthGfs5ndwx2Zk1lcaFGc4pWdVZFQoJmT8NHY25mYthGfs5ndwx2Zk1lcaFGc4pWdVZFQoJmT```

That looks like a base 64 encoded string, but decoding it spits out a lot of garbage.

Next we see there is a .bash_history file so we can get an idea of what the user was doing.
There were some commands of interest:

```
wget https://gist.githubusercontent.com/Glitch-is/bc49ee73e5413f3081e5bcf5c1537e78/raw/c1f735f7eb36a20cb46b9841916d73017b5e46a3/eRkjLlksZp
mv eRkjLlksZp tool.py
./tool.py ../secret > ../hzpxbsklqvboyou
```

So that script generated the base64 stuff on the desktop. 
lets examine that encode function:
```
def encode(filename):
    with open(filename, "r") as f:
        s = f.readline().strip()
        return base64.b64encode((''.join([chr(ord(s[x])+([5,-1,3,-3,2,15,-6,3,9,1,-3,-5,3,-15] * 3)[x]) for x in range(len(s))])).encode('utf-8')).decode('utf-8')[::-1]*5

```

The function takes in a file and reads just the first line of it.
Then it perfroms a pretty messy encrption function on it, lets see if we can break it down.
the `*5` at the end takes our encoded string and multipplies it by itself 5 times, simple
The `[::-1]` is a handy lilttle trick in python to reverse a string.
The decodes and encodes are pretty self explanatary, just like the b64encode is.
The inside of the base64 encoding gets a little complicated though
It looks like each character in the string is converted to its ascii value gets an int from the list added to it, and then converted back to a character. The `[5, -1...]*3` is used to make sure the list of arrays matches the input string length...probably. 

so now that we know how that `hzpxbsklqvboyou` file was encrypted we can write a little decoder function:

```
def decode(filename):
    with open(filename, "rw") as f:
        s = f.readline().strip()
        #note that i manually divided the orignal string by 5 before reading it in
        s = s[::-1]  #this reverse the string
        s = base64.b64decode(s) #this decodes the string
        print s #sanity check
        newString = (''.join([chr(ord(s[x]) - ([5,-1,3,-3,2,15,-6,3,9,1,-3,-5,3,-15] *3)[x]) for in range(len(s))])).decode('utf-8').encode('utf-8') #we just had to change the order of decode and encode, and then rather then add those int values, we subtract them
        print newString
```

running that decode prints out: `IceCTF{good_ol_history_lesson}`
