ok
p:={->false}
q:={->false}

p:={->false}
q:={->true}

p:={->true}
q:={->true}


No more models.

Traceback (most recent call last):
  File "test.py", line 221, in api
    problem.assert_("p()", True, S.GIVEN)
AttributeError: 'Structure' object has no attribute 'GIVEN'

