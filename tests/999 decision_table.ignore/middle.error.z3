  Not r()
⇒ Not q()

  p()
⇒ q()

⇒ ? q()

end of decision table
Traceback (most recent call last):
  File "test.py", line ??, in generateZ3
    idp.execute()
  File "idp_engine/Run.py", line ??, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line ??, in <module>
  File "idp_engine/Run.py", line ??, in pretty_print
    for i, xi in enumerate(x):
  File "idp_engine/Run.py", line ??, in decision_table
    models, timeout_hit = problem.decision_table(goal_string, timeout_seconds,
  File "idp_engine/Theory.py", line ??, in decision_table
    assert not goal_string or goal.value is not None, \
AssertionError: The goal is not always determined by the theory

