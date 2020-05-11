–-
title: debugWithYamlLog
tags: 
   ID: 20200510155836
–-
logger vs debugger : [reference](https://web.archive.org/web/20130527013805/http://andrevanderschyff.za.net/?p=143)
logger:
* can compare 2 runs
* can show relevant data, and ignore irrelevant data
* can go back in history

Painpoints when using a log to debug an application:
* need indentation → debug.indent, debug.dedent
* include data structure → use .__log__() instead of __str__(), [JSON](https://www.json.org/json-en.html) ? [YAML](https://lzone.de/cheat-sheet/YAML) ?
* size of log file → use [messagepack](https://msgpack.org/) ?
* tools to analyze ?  text editor ?? specialized tool ? [JSON viewer](https://code.visualstudio.com/docs/languages/json) ? query , filter ?

API:
* log decorator for function: [here](https://dev.to/mandrewcito/a-tiny-python-log-decorator-1o5m)
    * indent : adds indentation + '- ': at begin of a method
    * dedent: reduces indentation
    * auto-indent by looking at [stack size](https://stackoverflow.com/questions/34115298/how-do-i-get-the-current-depth-of-the-python-interpreter-stack) ? No
* log 1-line string → yaml([string]) + indent
* log variable →  yaml([object]) with [yamlable](https://smarie.github.io/python-yamlable/) (or as explained [here](https://yaml.readthedocs.io/en/latest/dumpcls.html)), then indent it
    * but how deep ??  Need to control it, and yamlable is easiest
* turn on / off
* use [sys.excepthook](https://docs.python.org/3/library/sys.html#sys.excepthook) to catch exceptions and show stack trace with variables



[JSON is the best log format](https://www.loggly.com/blog/why-json-is-the-best-application-log-format-and-how-to-switch/)