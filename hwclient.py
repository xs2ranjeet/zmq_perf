import zmq
context  = zmq.Context()

print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.232.129:5555")

for req in range(10):
    print("Sending request %s ..." % req)
    socket.send(b"Hello")
    
    message = socket.recv()
    print("Received reply %s  [ %s ]" % (req, message))