# Lamport Clock Vizualizer


Lamport clocks are a way to keep track of progress in a distributed system. They are a form of logical clocks that upholds the `clock consistency property`.
The `clock consistency property` says that if an event A causally preceds event B then the timestamp for event A must be less than  the timestamp for event B.
More Formally:

```
a -> b => T(a) < T(b)
```