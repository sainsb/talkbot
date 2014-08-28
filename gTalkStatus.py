

#import xmpp

#login = 'redtrails'
#pwd   = 'tortugas12'

#cnx = xmpp.Client('gmail.com', debug=[])
#cnx.connect(server=('talk.google.com',5223))
#cnx.auth(login,pwd, 'botty')
#cnx.send(xmpp.Message( "ben.sainsbury@oregonmetro.gov" ,"Hello World form Python" ) )

#cnx.sendInitPresence()
#import time
#print('sleeping for a few')
#time.sleep(10)
#roster=cnx.getRoster()
#jids = roster.getItems()
#for i in jids:
#        print i
#        print "Name = %s" % roster.getName(i)
#        print "Show = %s" % roster.getShow(i)
#        print "Status = %s" % roster.getStatus(i)

#!/usr/bin/python
import sys, xmpp, os, datetime, serial

class bcolors:
    HEADER = '\033[95m'
    ORANGE = '\033[40m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class serial_colors:
    DO_NOT_DISTURB='10 0 0\n'
    AWAY='10 3 0\n'
    LOGGED_OFF='0 0 0\n'
    AVAILABLE='0 10 0\n'

class status:
    DO_NOT_DISTURB='Do not disturb'
    AWAY='Away'
    LOGGED_OFF='Logged off'
    AVAILABLE='Available'
    UNKNOWN='Unknown'

class person():
    def __init__(self, name, status, id):
      self.name = name
      self.id = id
      self.status = status
      self.last_change = ''
      self.options = []

    def addOption(option):
      if option not in self.options:
          self.options.append(option)

    def __str__(self):
      return self.last_change+", "+self.name+", "+self.status+", "+str(self.id)+", "+str(self.options)

people = []

DRC=[
     ['max.woodbury',0],
     ['ben.sainsbury',1],
     ['justin.houk',2],
     ['clinton.chiavarini',3],
     ['molly.vogt',4],
     ['kellie.hauger',5],
     ['linda.martin',6],
     ['jeremy.murray',7],
     ['karen.scott-lowthian',8],
     ['steve.erickson',9],
     ['zac.christensen',10],
     ['minott.kerr',11]
     ]

def presenceCB(conn,msg):
    #print str(msg)
    #if msg.getBody() is None:
    #    return
    #try:
    person=str(msg.getFrom().getStripped())
    #person = str(msg.getFrom())
    #print person
    print person
    for p in people:
        if person.split('@')[0].upper() == p.name.replace(' ','.').upper():

            if person not in p.options:
                p.options.append(person)
                ser.write(str(p.id)+' '+serial_colors.LOGGED_OFF)

            mytime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            p.last_change=mytime
            _status = msg.getStatus()
            message = msg.getShow()
            priority = msg.getPriority()

            print 'DEBUG:', person, message, priority, _status

            if message is None and priority is None and _status is None:
                p.status=status.LOGGED_OFF
                ser.write(str(p.id)+' '+serial_colors.LOGGED_OFF)
                print bcolors.HEADER + str(p) + bcolors.ENDC +' '
            if message is None and priority==0:
                p.status=status.LOGGED_OFF
                ser.write(str(p.id)+' '+serial_colors.LOGGED_OFF)
                print bcolors.HEADER + str(p) + bcolors.ENDC +' '
            elif message is None and priority=='1':
                p.status=status.AVAILABLE
                ser.write(str(p.id)+' '+serial_colors.AVAILABLE)
                print bcolors.HEADER + str(p) + bcolors.ENDC +' '
            elif _status is not None:
                if message=="dnd":
                    p.status=status.DO_NOT_DISTURB
                    ser.write(str(p.id)+' ' + serial_colors.DO_NOT_DISTURB)
                    print bcolors.FAIL+ str(p) + bcolors.ENDC +' '
                if message in ("away","xa"):
                    p.status=status.AWAY
                    ser.write(str(p.id)+' '+serial_colors.AWAY)
                    print bcolors.WARNING + str(p) + bcolors.ENDC + ' '
                if message is None or message=='available':
                    p.status=status.AVAILABLE
                    ser.write(str(p.id)+' '+serial_colors.AVAILABLE)
                    print bcolors.OKGREEN + str(p) + bcolors.ENDC+' '

    #except Exception as e:
    #    print str(e)

        #if 'ben.sainsbury@oregonmetro.gov/Talk' in str(msg.getFrom()):

        #if m == None and p==0:
        #    print "signed out"
        #elif m == "dnd":
        #    print "do not disturb"
        #elif m == "away" or m =="xa":
        #    print "away"
        #elif m is None and p==24:
        #    print "available"
        #else:
        #    print "wtf"
        #print "status: ",s,"show: ",m, "pri: ", p
            
        #print msg.getFrom(), "show", msg.getShow(), "status", msg.getStatus(), "priority", msg.getPriority()

def StepOn(conn):
    try:
        conn.Process(1)
    except KeyboardInterrupt:
        return 0
    return 1

def GoOn(conn):
    while StepOn(conn):
        pass

def main():
   
    jid="gisdeveloper@oregonmetro.gov"
    pwd = "G1SDevelope8"
        
    jid="ben.sainsbury@oregonmetro.gov"
    pwd = "myCaldera10"

    jid=xmpp.protocol.JID(jid)

    #cl = xmpp.Client(jid.getDomain())
    cl = xmpp.Client(jid.getDomain(), debug=[])

    if cl.connect(server=('talk.google.com', 5222)) == "":
        print "not connected"
        sys.exit(0)

    if cl.auth(jid.getNode(),pwd) == None:
        print "authentication failed"
        sys.exit(0)

    cl.RegisterHandler('presence', presenceCB)
    cl.sendInitPresence()

    GoOn(cl)

#mark everyone out.
ser = serial.Serial(2, 9600)

for emp in DRC:
    people.append(person(emp[0].replace(".", ' '), status.LOGGED_OFF, emp[1]))
    ser.write(str(emp[1])+' '+serial_colors.LOGGED_OFF)

main()