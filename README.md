# rholog
Basic python logging/micotracing inspired by [mulog/mutrace](https://github.com/BrunoBonacci/mulog).

## Demos
```python
$ python3 demo1.py 
{
  "name": "demo1",
  "levelname": "INFO",
  "trace": true,
  "message": "step1",
  "status": "OK",
  "start_time": 1698379476.9029222,
  "end_time": 1698379477.903977,
  "duration": 1.0010547637939453,
  "root_id": "71d8f72cbe0548a4ac3765bff11192e9",
  "trace_id": "d425b6f2c2f74830b56d5c39737a9458",
  "parent_id": "99f152a3cb78428f98e18b7e602f646a",
  "timestamp": "2023-10-27T04:04:37.904026+00:00"
}
{
  "name": "demo1",
  "levelname": "INFO",
  "trace": true,
  "message": "step2_substep1",
  "status": "OK",
  "start_time": 1698379477.9043963,
  "end_time": 1698379478.9054687,
  "duration": 1.0010724067687988,
  "root_id": "71d8f72cbe0548a4ac3765bff11192e9",
  "trace_id": "94c207c341e94f18a31014767d64801b",
  "parent_id": "5408b06d8e214e6596d85bd2416bee09",
  "timestamp": "2023-10-27T04:04:38.905566+00:00"
}
{
  "name": "demo1",
  "levelname": "INFO",
  "message": "long sleep time",
  "root_id": "71d8f72cbe0548a4ac3765bff11192e9",
  "trace_id": "8a303ed3891042e1bd18e6787b04dfcc",
  "parent_id": "5408b06d8e214e6596d85bd2416bee09",
  "timestamp": "2023-10-27T04:04:39.907521+00:00"
}
{
  "name": "demo1",
  "levelname": "INFO",
  "message": "done sleeping",
  "root_id": "71d8f72cbe0548a4ac3765bff11192e9",
  "trace_id": "8a303ed3891042e1bd18e6787b04dfcc",
  "parent_id": "5408b06d8e214e6596d85bd2416bee09",
  "timestamp": "2023-10-27T04:04:43.908566+00:00"
}
{
  "name": "demo1",
  "levelname": "INFO",
  "trace": true,
  "message": "step2_substep2",
  "status": "OK",
  "start_time": 1698379479.9074495,
  "end_time": 1698379483.9091468,
  "duration": 4.001697301864624,
  "root_id": "71d8f72cbe0548a4ac3765bff11192e9",
  "trace_id": "8a303ed3891042e1bd18e6787b04dfcc",
  "parent_id": "5408b06d8e214e6596d85bd2416bee09",
  "timestamp": "2023-10-27T04:04:43.909191+00:00"
}
{
  "name": "demo1",
  "levelname": "INFO",
  "trace": true,
  "message": "step2",
  "status": "OK",
  "start_time": 1698379477.9043744,
  "end_time": 1698379483.9096248,
  "duration": 6.005250453948975,
  "root_id": "71d8f72cbe0548a4ac3765bff11192e9",
  "trace_id": "5408b06d8e214e6596d85bd2416bee09",
  "parent_id": "99f152a3cb78428f98e18b7e602f646a",
  "timestamp": "2023-10-27T04:04:43.909665+00:00"
}
{
  "name": "demo1",
  "levelname": "INFO",
  "trace": true,
  "message": "main",
  "status": "OK",
  "start_time": 1698379476.9029098,
  "end_time": 1698379483.9100792,
  "duration": 7.007169485092163,
  "root_id": "71d8f72cbe0548a4ac3765bff11192e9",
  "trace_id": "99f152a3cb78428f98e18b7e602f646a",
  "timestamp": "2023-10-27T04:04:43.910132+00:00"
}
```

```python
$ python3 demo2.py 
{
  "name": "demo2",
  "levelname": "INFO",
  "trace": true,
  "message": "long sleep time",
  "status": "OK",
  "start_time": 1698379503.0828867,
  "end_time": 1698379503.0828898,
  "duration": 3.0994415283203125e-06,
  "root_id": "55429a5579e241658566f7c80cf7b4e2",
  "trace_id": "aa0856cf524347369ee2a9ccca2ef274",
  "parent_id": "70fc7aeb56aa40a9a77bc78351e82c67",
  "timestamp": "2023-10-27T04:05:03.082936+00:00"
}
{
  "name": "demo2",
  "levelname": "INFO",
  "trace": true,
  "message": "done sleeping",
  "status": "OK",
  "start_time": 1698379507.0878375,
  "end_time": 1698379507.0878448,
  "duration": 7.3909759521484375e-06,
  "root_id": "55429a5579e241658566f7c80cf7b4e2",
  "trace_id": "e72f4bdcb03f495ea9608a6b9bada759",
  "parent_id": "70fc7aeb56aa40a9a77bc78351e82c67",
  "timestamp": "2023-10-27T04:05:07.087910+00:00"
}
{
  "name": "demo2",
  "levelname": "ERROR",
  "trace": true,
  "message": "main",
  "status": "ERROR",
  "start_time": 1698379500.0800796,
  "end_time": 1698379507.088534,
  "duration": 7.0084545612335205,
  "exception": "division by zero",
  "traceback": "Traceback (most recent call last):\n  File \"/home/wes/src/rholog/rholog.py\", line 144, in trace\n    yield context_log\n  File \"/home/wes/src/rholog/demo2.py\", line 32, in main\n    step2(log)\n  File \"/home/wes/src/rholog/demo2.py\", line 26, in step2\n    step2_substep2(log)\n  File \"/home/wes/src/rholog/demo2.py\", line 20, in step2_substep2\n    1 / 0\nZeroDivisionError: division by zero\n",
  "root_id": "55429a5579e241658566f7c80cf7b4e2",
  "trace_id": "70fc7aeb56aa40a9a77bc78351e82c67",
  "timestamp": "2023-10-27T04:05:07.089697+00:00"
}
Traceback (most recent call last):
  File "/home/wes/src/rholog/demo2.py", line 39, in <module>
    main(log, root_id)
  File "/home/wes/src/rholog/demo2.py", line 32, in main
    step2(log)
  File "/home/wes/src/rholog/demo2.py", line 26, in step2
    step2_substep2(log)
  File "/home/wes/src/rholog/demo2.py", line 20, in step2_substep2
    1 / 0
ZeroDivisionError: division by zero
```

```python
$ python3 -B demo3.py 
{
  "name": "demo3",
  "levelname": "WARNING",
  "trace": true,
  "message": "I guess I still want to log?",
  "status": "OK",
  "start_time": 1698379509.467186,
  "end_time": 1698379509.4671867,
  "duration": 7.152557373046875e-07,
  "root_id": "24e6440c4ccc48c8a087d4889e54227b",
  "trace_id": "5da3e987d89242ac8ff3b70865498af0",
  "parent_id": "1910b4729bb044d9a86a409cc96f0ed9",
  "param1": 12,
  "timestamp": "2023-10-27T04:05:09.467204+00:00"
}
{
  "name": "demo3",
  "levelname": "INFO",
  "trace": true,
  "message": "inside substep_1",
  "status": "OK",
  "start_time": 1698379510.4684293,
  "end_time": 1698379510.4684305,
  "duration": 1.1920928955078125e-06,
  "root_id": "24e6440c4ccc48c8a087d4889e54227b",
  "trace_id": "a1b2208bb8de46a09dbc49d7a5abd901",
  "parent_id": "96fbbc3eed594fa3b1dda76c1f768c18",
  "param1": 12,
  "timestamp": "2023-10-27T04:05:10.468460+00:00"
}
{
  "name": "demo3",
  "levelname": "INFO",
  "trace": true,
  "message": "substep_1",
  "status": "OK",
  "start_time": 1698379510.4684048,
  "end_time": 1698379510.4686453,
  "duration": 0.00024056434631347656,
  "root_id": "24e6440c4ccc48c8a087d4889e54227b",
  "trace_id": "96fbbc3eed594fa3b1dda76c1f768c18",
  "parent_id": "1910b4729bb044d9a86a409cc96f0ed9",
  "param1": 12,
  "timestamp": "2023-10-27T04:05:10.468657+00:00"
}
{
  "name": "demo3",
  "levelname": "INFO",
  "trace": true,
  "message": "subcomponent-1",
  "status": "OK",
  "start_time": 1698379509.4671729,
  "end_time": 1698379510.4687703,
  "duration": 1.0015974044799805,
  "root_id": "24e6440c4ccc48c8a087d4889e54227b",
  "trace_id": "1910b4729bb044d9a86a409cc96f0ed9",
  "parent_id": "023d0c79a0524013b07bf85c6a9df7fc",
  "param1": 12,
  "timestamp": "2023-10-27T04:05:10.468780+00:00"
}
{
  "name": "demo3",
  "levelname": "INFO",
  "trace": true,
  "message": "main",
  "status": "OK",
  "start_time": 1698379509.4671593,
  "end_time": 1698379510.4688866,
  "duration": 1.0017273426055908,
  "root_id": "24e6440c4ccc48c8a087d4889e54227b",
  "trace_id": "023d0c79a0524013b07bf85c6a9df7fc",
  "timestamp": "2023-10-27T04:05:10.468896+00:00"
}
```
