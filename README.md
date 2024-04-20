# Load Balancer to Redis Server (read-only) - Group 7

In this project, we have built a system that enables the loading of
the balancer to the Redis Server. Redis (Remote Dictionary Server) is a
source-available, in-memory storage that offers fast and efficient
data retrieval. It is the most popular NoSQL database specifically
and one of the most popular ones in general. As good as it may seem,
with the growing number of data and concurrent requests, a single
Redis Server might be insufficient where there might be the case of
bottleneck. To resolve this, people have come up with the idea of
leveraging a load balancer that can distribute the requests to multiple
servers, improving the performance and availability.

## System Requirements

Require to be able to distribute client connection to each server. 

## System Design

In this, we built a load balancer in Python. The load balancer 
uses the least connection algorithm to distribute load to each server.

For handling multiple clients, we also added multithreading which 
will be used for each client when they request to the server.

## Application Example

### Setup
For the small scenario we have designed, we use data which is 
about a lot of actors each includes 4 attributes: first_name, 
last_name, date_of_birth, and of course their IDs. The data has 
in total of 1319 samples.

We also create three servers to test our load balancer system

### Demo video

## Guideline to build + run code:
The code is optimized for Linux users and MacOS and Windows.

First, do: 
```shell
bash load_data.sh
```
This will create the Redis databases server for demo interaction. 
Each of these databases includes the same data across all the servers.

Next, run:
```shell
python main.py
```

This implements our load balancer.

To get the data (read-only). On your browser open: localhost:(Port of Load Balancer)

You can also view by key and value:

For example open: localhost:(Port of Load Balancer)/actor:

And so on.

If it doesn’t work, you can mimic it on another terminal by:
```shell
curl --http0.9 http://127.0.0.1:(Port of Load Balancer)
```

Example:

```shell
curl --http0.9 http://127.0.0.1:1310
```

To mimic several clients accessing the load balancer at the same time. Do
```shell
curl --http0.9 127.0.0.1:1310/actor:1 &
curl --http0.9 127.0.0.1:1310/actor:1 &
curl --http0.9 127.0.0.1:1310/actor:1 &
curl --http0.9 127.0.0.1:1310/actor:1 &
curl --http0.9 127.0.0.1:1310/actor:1 &
curl --http0.9 127.0.0.1:1310/actor:1 &
curl --http0.9 127.0.0.1:1310/actor:1 &
```

This shows you how the load balancer distributes the requests to each server.
