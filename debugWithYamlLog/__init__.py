import os, time

DEBUG = True

start = time.process_time()
def log(action):
    global start
    print("*** ", action, round(time.process_time()-start,3))
    start = time.process_time()


nl = "\n"
indented = "\n  "

LOG_FILE = None
def Log_file(path):
    global LOG_FILE
    if 'roof' in path or 'andbox' in path:
        path, filename = os.path.split(path)
        LOG_FILE = newpath = os.path.join(path, filename.replace('.idp', '_log.txt'))
        indent = 0
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
    else:
        LOG_FILE = None

def Log(string, indent=0):
    global LOG_FILE
    if LOG_FILE:
        f = open(LOG_FILE, "a")
        out = string.replace(nl, nl+(' '*indent))
        f.write(out)
        f.close()