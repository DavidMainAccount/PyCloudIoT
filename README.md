# PyCloudIoT-DSN
PyCloudIoT infrastructure described at the DSN submitted conference paper

# Description
In this repository, we will present the code that goes with the paper submited to DSN about PyCloudIoT.
PyCloudIoT is a Edge cloud computing model in which the computing farm is composed by IoT devices (in this case ESP32).

![main_scheme](documentation_images\esquema_articulo-Page-5-big.jpg)

As we can see on the diagram, the infrastructure follows a dispatcher/worker-like distribution. 
This infrastructure is conceived for the execution of FaaS stateless functions.

# Repository organisation
Inside the /src folder we can find the code of the project. Inside this folder we can see:
- client_side: code to be executed by the client
- dispatcher: code to be executed by the dispatcher
- environment: used by client and dispatcher and makes it easier to adapt the code to a new infrastructure
- utils: classes used by both client and dispatcher
- worker_side: code to be executed by the worker
  
# How to execute
## Dispatcher

## Worker

## Client
# Benchmarking
