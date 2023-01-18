# In This model we tried to implement a Hexagunal architecture

We had :
  - Three level of tests(unit, integration, e2e)
  - A bus which decide to pass a command/query to its handler based on config(just like events and queries)
  - Each event binds to n listeners
  - Each command binds to a command-handler
  - Each query binds to a query-handler
