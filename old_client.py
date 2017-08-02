import zmq
import sys
import threading
import time
from random import randint, random
from optparse import OptionParser

def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()
class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, id, host, port):
        self.id = id
        self.host = host
        self.port = port
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        identity = u'worker-%d' % self.id
        socket.identity = identity.encode('ascii')
        socket.connect('tcp://{0}:{1}'.format(self.host, self.port))
        print('Client %s started' % (identity))
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        reqs = 0
        while reqs <60:
            reqs = reqs + 1
            print('Req #%d sent..' % (reqs))
            socket.send_multipart([b'20', b'ping'])
            #socket.send_string(u'request #%d' % (reqs))
            for i in range(5):
                sockets = dict(poll.poll(1000))
                if socket in sockets:
                    event, msg = socket.recv_multipart()
                    tprint('Client %s received(%s): %s' % (identity, event, msg))
        print('Client %s exiting'.format(identity))
        socket.close()
        context.term()
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
                      default=5,
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

    #print (options)
    #print (args)
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
    for count in range(options.maxclient):
        client = ClientTask(count, options.host, options.port)
        client.start()   
   
    
def main():
    (options, args) = command_parser()
    connect(options, args)

if __name__ == '__main__':
    
    main()
