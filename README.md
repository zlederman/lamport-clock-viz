# Lamport Clock Vizualizer
This project is intended to simulate a series of message passing nodes in an effort to visualize a real time lamport diagram on the web. 
# A primer on Lamport Clocks

Lamport clocks are a way to keep track of progress in a distributed system. They are a form of logical clocks that upholds the `clock consistency property`.
The `clock consistency property` says that if an event A causally preceds event B then the timestamp for event A must be less than  the timestamp for event B.
More Formally:

```
a -> b => T(a) < T(b)
```

# The Node Class
The Node class is a Subclass of `multiprocessing.Process` it implements a run method which is a statemachine. This statemachine can be in 3 states

`INTERNAL`
- Internal Events are just that, they don't effect the larger system but the increment a node's logical clock

`SEND`
- Send Events fire an event to another Node with the timestamp equal to the current time

`RECV`
- Receive events are events that trigger a Node to read from its message queue and evaluate the timestamp of this message. The Lamport implementation is `max(T(Send_Message), Current_Time)`

The node class accepts a few params to its constructor:
```
def __init__(self, node_id: str, max_messages: int, queue_map: Dict[str, "mp.Queue[SendEvent]"], log_queue: mp.Queue, *args, **kwargs)
```
`node_id: str`
- the id of the node used to further order the nodes from the partial order to a lexicographic ordering + timestamp ordering

`max_messages: int`
- A proxy for how long the system runs for

`queue_map: Dict[str, "mp.Queue[SendEvent]"]`
- essentially a Phone book for where a node can drop a message

`log_queue: mp.Queue[str] `
- the sink for all of a nodes events to be streamed
