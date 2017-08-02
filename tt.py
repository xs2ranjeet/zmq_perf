import subprocess
import re
import sys

#p = subprocess.Popen('sudo forever list', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#for line in p.stdout.readlines():
##    re.sub('[^a-zA-Z0-9-_*.]', '', line)
    #x = line.decode('utf-8')
x = 'data:    [1] elYB /bin/bash /home/ranjeet/ultronpush/demo_zmq_ultron_script_5000.sh 7709    23543    /home/ranjeet/logs/elYB.log 0:1:9:52.940'
if x.find('5000.sh') > 0:
    print(x)
    y = x.split(' ')
    for  z in y:
        if z.find('.log') > 0:
            print(z)
#retval = p.wait()

def get_log_file(zmq_script):
    p = subprocess.Popen('sudo forever list', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
    #    re.sub('[^a-zA-Z0-9-_*.]', '', line)
        x = line.decode('utf-8')    
        if x.find(zmq_script) > 0:
            print(x)
            y = x.split(' ')
            for  z in y:
                if z.find('.log') > 0:
                    print(z)   
                    return z

def search_in_log(zmq_script, date_filter, zid_filter):
    log = get_log_file(zmq_script)
    cmd = 'cat '+ log + ' | grep '+ date_filter+ ' | grep '+zid_filter
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
    #    re.sub('[^a-zA-Z0-9-_*.]', '', line)
        x = line.decode('utf-8')
        print(x)

if __name__== '__main__':
    for x in sys.argv:
        print(x)
    search_in_log(sys.argv[1],sys.argv[2],sys.argv[3])