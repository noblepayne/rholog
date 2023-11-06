# rholog
Basic python logging/micotracing inspired by [mulog/mutrace](https://github.com/BrunoBonacci/mulog).

## Demo
```python
> pdm run uvicorn demos.tracedapi:app
> curl http://localhost:8000/1222?b=abc
{
  "name": "demos.tracedapi.get_code",
  "levelname": "INFO",
  "root_id": "b2aa8a32b3684ca486b6108dfda0471a",
  "span_id": "2c8ac12bb4ca427c9586dd3499455b15",
  "parent_id": "b2aa8a32b3684ca486b6108dfda0471a",
  "filename": "/home/wes/src/rholog/demos/tracedapi.py",
  "lineno": 56,
  "module": "demos.tracedapi",
  "function": "get_code",
  "start_time": 1699246057.6110692,
  "end_time": 1699246057.6110835,
  "duration": 1.430511474609375e-05,
  "message": "TRACE",
  "timestamp": "2023-11-06T04:47:37.611108+00:00"
}
{
  "name": "demos.tracedapi.dumbroute",
  "levelname": "INFO",
  "root_id": "b2aa8a32b3684ca486b6108dfda0471a",
  "span_id": "881a1c12e1e347648806ade1ce655b5b",
  "parent_id": "b2aa8a32b3684ca486b6108dfda0471a",
  "filename": "/home/wes/src/rholog/demos/tracedapi.py",
  "lineno": 61,
  "module": "demos.tracedapi",
  "function": "dumbroute",
  "start_time": 1699246057.6109014,
  "end_time": 1699246057.611309,
  "duration": 0.0004076957702636719,
  "message": "TRACE",
  "timestamp": "2023-11-06T04:47:37.611327+00:00"
}
{
  "name": "dumbroute__a__get",
  "levelname": "INFO",
  "root_id": "b2aa8a32b3684ca486b6108dfda0471a",
  "span_id": "b2aa8a32b3684ca486b6108dfda0471a",
  "filename": "/home/wes/src/rholog/demos/tracedapi.py",
  "lineno": 24,
  "http.method": "GET",
  "http.url": "http://localhost:8000/1222?b=abc",
  "http.raw_path": "b'/1222'",
  "http.path_params": {},
  "http.query_params": "b=abc",
  "http.host": "127.0.0.1",
  "http.port": 55544,
  "status_code": 200,
  "http.path": "/{a}",
  "start_time": 1699246057.6097927,
  "end_time": 1699246057.6117902,
  "duration": 0.0019974708557128906,
  "message": "TRACE",
  "timestamp": "2023-11-06T04:47:37.611803+00:00"
}
```


```python
> pdm run demos/demo4.py
{
  "name": "I guess I still want to log?",
  "levelname": "WARNING",
  "root_id": "a765ddc432cb42e58d826b727f01ad56",
  "span_id": "13e5e97a34374ccf8b1e46f1c9af40fd",
  "parent_id": "3cb14e9026f04e69a7d3b97358f091ff",
  "filename": "/home/wes/src/rholog/demos/demo4.py",
  "lineno": 20,
  "event": true,
  "warning": true,
  "start_time": 1699246082.0306184,
  "end_time": 1699246082.0306196,
  "duration": 1.1920928955078125e-06,
  "message": "TRACE",
  "timestamp": "2023-11-06T04:48:02.030635+00:00"
}
{
  "name": "inside substep_1",
  "levelname": "INFO",
  "root_id": "a765ddc432cb42e58d826b727f01ad56",
  "span_id": "1935f2e6d66c4ef8b00181f8ed7563b1",
  "parent_id": "14e3adb823a444489698278150e0a381",
  "filename": "/home/wes/src/rholog/demos/demo4.py",
  "lineno": 13,
  "event": true,
  "start_time": 1699246084.0335872,
  "end_time": 1699246084.0335896,
  "duration": 2.384185791015625e-06,
  "message": "TRACE",
  "timestamp": "2023-11-06T04:48:04.033619+00:00"
}
{
  "name": "__main__.substep_1",
  "levelname": "INFO",
  "root_id": "a765ddc432cb42e58d826b727f01ad56",
  "span_id": "14e3adb823a444489698278150e0a381",
  "parent_id": "3cb14e9026f04e69a7d3b97358f091ff",
  "filename": "/home/wes/src/rholog/demos/demo4.py",
  "lineno": 10,
  "module": "__main__",
  "function": "substep_1",
  "start_time": 1699246083.0324252,
  "end_time": 1699246085.0348742,
  "duration": 2.0024490356445312,
  "message": "TRACE",
  "timestamp": "2023-11-06T04:48:05.034949+00:00"
}
{
  "name": "subcomponent-1",
  "levelname": "INFO",
  "root_id": "a765ddc432cb42e58d826b727f01ad56",
  "span_id": "3cb14e9026f04e69a7d3b97358f091ff",
  "parent_id": "c2fd31133d7a485d9d061a1e56545c50",
  "filename": "/home/wes/src/rholog/demos/demo4.py",
  "lineno": 19,
  "param1": 12,
  "start_time": 1699246082.0305867,
  "end_time": 1699246086.036531,
  "duration": 4.00594425201416,
  "message": "TRACE",
  "timestamp": "2023-11-06T04:48:06.036583+00:00"
}
{
  "name": "__main__.main",
  "levelname": "INFO",
  "root_id": "a765ddc432cb42e58d826b727f01ad56",
  "span_id": "19a62b724e6540789c7abdfb7abdfe8a",
  "parent_id": "c2fd31133d7a485d9d061a1e56545c50",
  "filename": "/home/wes/src/rholog/demos/demo4.py",
  "lineno": 17,
  "module": "__main__",
  "function": "main",
  "start_time": 1699246082.0305507,
  "end_time": 1699246086.037117,
  "duration": 4.006566286087036,
  "message": "TRACE",
  "timestamp": "2023-11-06T04:48:06.037142+00:00"
}
{
  "name": "__main__",
  "levelname": "INFO",
  "root_id": "a765ddc432cb42e58d826b727f01ad56",
  "span_id": "c2fd31133d7a485d9d061a1e56545c50",
  "filename": "/home/wes/src/rholog/demos/demo4.py",
  "lineno": 32,
  "start_time": 1699246082.0304847,
  "end_time": 1699246086.0373485,
  "duration": 4.006863832473755,
  "message": "TRACE",
  "timestamp": "2023-11-06T04:48:06.037367+00:00"
}

```
