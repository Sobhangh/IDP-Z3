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
    verify_models(known, models, goal_string)
  File "idp_engine/Theory.py", line ??, in verify_models
    assert solver.check() == unsat, \
AssertionError: The DMN table does not cover the full domain

