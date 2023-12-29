# In This Model We Tried To Implement Hexagonal Architecture With Python

We had :
  - Three level of tests(unit, integration, e2e).
  - A bus that decides to pass a command/query/event to its handler(or listener) based on config.
  - Each event binds to n listeners.
  - Each command binds to its command handler.
  - Each query binds to its query handler (listener).
