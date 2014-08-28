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
     ['user a',0],
     ['user b',1],
     ['user c',2],
     ['user d',3],
     ['user e',4],
     ['user f',5],
     ['user g',6],
     ['user h',7],
     ['user i',8],
     ]

def presenceCB(conn,msg):
 
    person=str(msg.getFrom().getStripped())

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
        
    jid=''#sainsb
    pwd = ''#sainsb's password

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
ser = serial.Serial(2, 9600)

for emp in DRC:
    people.append(person(emp[0].replace(".", ' '), status.LOGGED_OFF, emp[1]))
    ser.write(str(emp[1])+' '+serial_colors.LOGGED_OFF)

main()