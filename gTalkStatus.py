import sys, xmpp, os, datetime, telnetlib

MOBILE_KEYWORDS = ['ANDROID']

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
    MOBILE='0 0 10\n'

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
      self.options = {}
      self.clients = []

    def addOption(option):
      if option not in self.options:
          self.options.append(option)

    def __str__(self):
      return self.last_change+", "+self.name+", "+self.status+", "+str(self.id)+", "+str(self.options)

people = []

DRC=[
     ['bsbury',0],
     ['ccni',1],
     ['dee',2],
     ['jurray',3],
     ['j',4],
     ['jouk',5],
     ['kothian',6],
     ['kauger',7],
     ['lrtin',8],
     ['mbury',9],
     ['merr',10],
     ['mgt',11],
     ['pey',12],
     ['snder',13],
     ['sickson',14]
     ]

def presenceCB(conn,msg):

    person=str(msg.getFrom().getStripped())

    for p in people:
        if person.split('@')[0].upper() == p.name.replace(' ','.').upper():

            if str(msg.getFrom()) not in p.options.iterkeys():
                p.options[str(msg.getFrom())] = status.UNKNOWN
                #ser.write(str(p.id)+' '+serial_colors.LOGGED_OFF)

            mytime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            p.last_change=mytime
            _status = msg.getStatus()
            message = msg.getShow()
            priority = msg.getPriority()

            print 'DEBUG:', msg.getFrom(), message, priority, _status, p.options

            if message is None and ((priority is None and _status is None) or priority==0):
                p.options[str(msg.getFrom())]=status.LOGGED_OFF
                
            elif message is None and priority=='1':
                p.options[str(msg.getFrom())]=status.AVAILABLE
            elif _status is not None:
                if message=="dnd":
                    p.options[str(msg.getFrom())]=status.DO_NOT_DISTURB
                if message in ("away","xa"):
                    p.options[str(msg.getFrom())]=status.AWAY
                if message is None or message=='available':
                    p.options[str(msg.getFrom())]=status.AVAILABLE
                    
            if status.DO_NOT_DISTURB in p.options.itervalues():
                ser.write(str(p.id)+' ' + serial_colors.DO_NOT_DISTURB)
                print bcolors.FAIL+ str(p) + bcolors.ENDC +' '
                return
            if status.AVAILABLE in p.options.itervalues():
                for k,v in p.options.iteritems():
                    if any(word in k.upper() for word in MOBILE_KEYWORDS):
                        ser.write(str(p.id)+' '+serial_colors.MOBILE)
                        print bcolors.OKBLUE + str(p) + bcolors.ENDC+' '
                        return
                
                ser.write(str(p.id)+' '+serial_colors.AVAILABLE)
                print bcolors.OKGREEN + str(p) + bcolors.ENDC+' '
            elif status.AWAY in p.options.itervalues():
                ser.write(str(p.id)+' '+serial_colors.AWAY)
                print bcolors.WARNING + str(p) + bcolors.ENDC + ' '
            else: #logged off
                ser.write(str(p.id)+' '+serial_colors.LOGGED_OFF)
                print bcolors.HEADER + str(p) + bcolors.ENDC +' '

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
   
        
    jid= {useremail}
    pwd = {password}

    jid=xmpp.protocol.JID(jid)

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
#open an IP socket to wifly.
ser = telnetlib.Telnet('192.168.0.12',2000)

for emp in DRC:
    people.append(person(emp[0].replace(".", ' '), status.LOGGED_OFF, emp[1]))
    ser.write(str(emp[1])+' '+serial_colors.LOGGED_OFF)

main()