import zmq
import sys
import threading
import time
import csv
import datetime
from time import gmtime, strftime 
from random import randint, random
from optparse import OptionParser
startSendData = 0
context = zmq.Context()
fp = open('log_client.csv', 'w', newline='')
file_csv = csv.writer(fp, delimiter=',')
def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()
def init():
    a = csv.writer(fp, delimiter=',')
    data = [['id','start','end', 'r_sent','r_recv','err']]
    a.writerows(data)   
class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, identity, id, host, port):
        self.identity = identity
        self.id = id
        self.host = host
        self.port = port
        threading.Thread.__init__ (self)

    def run(self):
        #context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        identity = self.identity+'-%d' % self.id
        socket.identity = identity.encode('ascii')
        socket.connect('tcp://{0}:{1}'.format(self.host, self.port))
        print('Client %s started' % (identity))
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        reqs = 0
        t_end = time.time() + 60 * 2
        s_count = 100
        r_count = 0
        t_start = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')        
        #print('Start time: {}'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
        #for i in range(s_count):
        socket.send_multipart([b'20', b'ping'])
        #while time.time() < t_end:        
        while True: 
            socks = dict(poller.poll(10))
        
            # Handle socket activity on backend
            if socks.get(socket) == zmq.POLLIN:
                frames = socket.recv_multipart()
                if not frames:
                    break # Interrupted                
                #print('Data recv: {0}, {1}'.format(frames[0], frames[1]))
                if frames[0]== b'21' and  frames[1]==b'ping':
                    r_count += 1
            if startSendData == 1:
                start_t = datetime.datetime.fromtimestamp(time.time()).strftime('%S')
                if int(start_t) % 10 == 0:
                    if flag == True:
                        socket.send_multipart([b'20', b'ping'])
                        flag = False
                else:
                    flag = True                
                #if r_count== s_count:
                 #   break
        #while reqs <60:
            #reqs = reqs + 1
            #print('Req #%d sent..' % (reqs))
            #socket.send_multipart([b'20', b'ping'])
            #event, msg = socket.recv_multipart()
            #tprint('Client %s received(%s): %s' % (identity, event, msg))
            #socket.send_string(u'request #%d' % (reqs))
            #for i in range(5):
                #sockets = dict(poll.poll(1000))
                #if socket in sockets:
                    #event, msg = socket.recv_multipart()
                    #tprint('Client %s received(%s): %s' % (identity, event, msg))
        socket.close()
        t_end = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') 
        file_csv.writerows( [[identity,t_start,t_end, s_count,r_count,s_count-r_count]])         
        #print('end time: {}'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
        #print('Client {} : Req Sent: {}, Rep recvd:{}, err: {}'.format(identity, s_count, r_count, s_count-r_count))
        #socket.close()
        #context.term()
def command_parser():
    parser = OptionParser(usage="usage: %prog [options] ",
                      version="%prog 1.0")
    parser.add_option("-s", "--host",
                      action="store",
                      dest="host",
                      default="192.168.232.129",
                      help="Enter the Zeromq Server Host for connection.")
    parser.add_option("-p", "--port",
                      action="store",
                      dest="port",
                      default=5000,
                      help="Enter Zeromq Server Port for  connection")
    parser.add_option("-b", "--buffer",
                      action="store",
                      dest="buffer",
                      default=20,
                      help="Enter buffer data size")
    parser.add_option("-c", "--count",
                      action="store",
                      dest="maxclient",
                      default=1000,
                      help="Enter max client count")
    parser.add_option("-r", "--reqcount",
                      action="store",
                      dest="reqcount",
                      default=10,
                      help="how many request will be send by client in one second")
    parser.add_option("-t", "--timeout",
                      action="store",
                      dest="timeout",
                      default=60,
                      help="Enter timeout value.")
    parser.add_option("-l", "--logfile",
                      action="store", # optional because action defaults to "store"
                      dest="logfile",
                      default="result.log",
                      help="Output log written in file",)
    parser.add_option("-z", "--zidfile",
                      action="store", # optional because action defaults to "store"
                      dest="zidfile",
                      default="zid.txt",
                      help="file containg the zing ids",)
    (options, args) = parser.parse_args()

    #if len(args) != 1:
        #parser.error("wrong number of arguments")

    print (options)
    print (args)
    #print("{0} {1} {2}".format(options.environment, options.cssfile, options.xhtml_flag))
    #arg1 = sys.argv[1]
    #arg2 = sys.argv[2]
    #print(arg1)
    #print(arg2)
    #print(size(sys.argv))
    return (options, args)

#def launch_client(options):
    #context  = zmq.Context()
    #print("Connecting to hello world server...")
    #socket = context.socket(zmq.REQ)
    #socket.connect("tcp://{0}:{1}".format(options.host, options.port))
    
    #for req in range(options.reqcount):
        #print("Sending request %s ..." % req)
        #socket.send(b"Hello")
        
        #message = socket.recv()
        #print("Received reply %s  [ %s ]" % (req, message))  
    #print('Exiting the launch_client')
def connect(options, args):
    print (options)
    print (args)
    init()
    x = datetime.datetime.fromtimestamp(time.time()).strftime('%H%M')
    identity = "worker"+x    
    for count in range(int(options.maxclient)):
        client = ClientTask(identity, count, options.host, options.port)
        client.start()
        #time.sleep(0.05)
        #client.join()
    #fp.close()
    #context.term()
    print('task done...')
    startSendData = 1
   
    
def main():
    (options, args) = command_parser()
    connect(options, args)

if __name__ == '__main__':
    
    main()
