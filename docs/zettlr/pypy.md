–-
title: pypy
tags: #Perf
Date: 20200616172332
–-

Done:
* sudo snap install --classic pypy3
* pypy3 -m ensurepip
* pypy3 -m pip install --upgrade pip → pip 20.1.1
* pypy3 -m pip install -r requirements.txt

–-> pyp3 test.py generate is slower ! 3.7 sec to 12 sec !
pypy3 main.py is also 2x slower on Djordje's abstract: 
