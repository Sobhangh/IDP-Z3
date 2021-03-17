  q
⇒ p

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
  File "IDP-Z3/idp_engine/Problem.py", line 546, in decision_table
    verify_models(known, models, goal_string)
  File "IDP-Z3/idp_engine/Problem.py", line 544, in verify_models
    assert solver.check() == unsat, \
AssertionError: The DMN table does not cover the full domain

