  Not r()
⇒ Not q()

  p()
⇒ q()

⇒ ? q()

end of decision table
Traceback (most recent call last):
  File "test.py", line 63, in generateZ3
    idp.execute()
  File "IDP-Z3/idp_engine/Run.py", line 129, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line 2, in <module>
  File "IDP-Z3/idp_engine/Run.py", line 107, in pretty_print
    for i, xi in enumerate(x):
  File "IDP-Z3/idp_engine/Run.py", line 88, in decision_table
    for model in problem.decision_table(goal_string, timeout, max_rows,
  File "IDP-Z3/idp_engine/Problem.py", line 587, in decision_table
    assert not goal_string or goal.value is not None, \
AssertionError: The goal is not always determined by the theory

