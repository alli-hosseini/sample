# In This model we tried to implement a Hexagunal architecture

we had :
  - three level of tests(unit, integration, e2e)
  - a bus which decide to pass a command/query to its handler based on config(just like events and queries)
  - each event binds to n listeners
  - each command binds to a command-handler
  - each query binds to a query-handler
