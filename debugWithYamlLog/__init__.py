import inspect, os, time
from yaml import dump


NEWL = "\n"
indented = "\n  "

_indent = 0

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

def prepare(self):
    try:
        out = self.__log__()
    except:
        out = self
    if isinstance(out, dict):
        return {k:prepare(v) for k,v in out.items() if v is not None}
    else:
        return str(out)


def Log(something):
    global LOG_FILE, _indent
    if LOG_FILE:
        f = open(LOG_FILE, "a")
        out = f"{NEWL}{dump([prepare(something)], allow_unicode=True, sort_keys=False)}"[:-1] # drop last \n
        out = out.replace(NEWL, NEWL+(' '*_indent))
        f.write(out)
        f.close()


def log_calls(function):
    def _wrapper(*args, **kwds):
        global LOG_FILE, _indent
        if LOG_FILE:
            args_name = inspect.getargspec(function).args
            Log(f"calling {function.__name__}({','.join(str(v) for v in args if v is not None)})")

            _indent += 2

        out = function(*args, *kwds)

        if LOG_FILE:
            _indent -= 2
            Log(f"returning from {function.__name__}: {str(out)}")
        return out    
    return _wrapper

