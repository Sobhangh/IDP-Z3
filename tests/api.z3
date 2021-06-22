ok
p:={->false}
q:={->false}

p:={->false}
q:={->true}

p:={->true}
q:={->true}


No more models.

Traceback (most recent call last):
  File "/home/pcarbonn/Documents/repos/IDP-Z3/test.py", line 221, in api
    problem.assert_("p()", True, S.GIVEN)
AttributeError: 'Structure' object has no attribute 'GIVEN'

