  Not B
∧ Not E
⇒ ? Eligible(BE001)

  B
∧ C
⇒ Eligible(BE001)

  Not B
∧ Not C
⇒ ? Eligible(BE001)

  Not F
∧ B
⇒ ? Eligible(BE001)

  B
∧ E
⇒ Eligible(BE001)

  Not B
∧ C
∧ E
⇒ Not Eligible(BE001)

  Not C
∧ Not E
∧ B
∧ F
⇒ Not Eligible(BE001)

end of decision table
Traceback (most recent call last):
  File "test.py", line 63, in generateZ3
    idp.execute()
  File "IDP-Z3/idp_engine/Run.py", line 122, in execute
    exec(main, mybuiltins, mylocals)
  File "<string>", line 2, in <module>
  File "IDP-Z3/idp_engine/Run.py", line 101, in myprint
    for i, xi in enumerate(x):
  File "IDP-Z3/idp_engine/Run.py", line 88, in decision_table
    for model in problem.decision_table(goal_string, timeout, max_rows,
  File "IDP-Z3/idp_engine/Problem.py", line 510, in decision_table
    assert not goal_string or goal.value is not None, \
AssertionError: The goal is not always determined by the theory

