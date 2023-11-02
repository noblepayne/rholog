# rholog
Basic python logging/micotracing inspired by [mulog/mutrace](https://github.com/BrunoBonacci/mulog).

## Demo
```python
> pdm run demos/demo4.py
{
  "name": "I guess I still want to log?",
  "levelname": "WARNING",
  "root_id": "aaf18e40a5884426bf33fdc43fca0e90",
  "parent_id": "ece05497436e4810af8e488ac1cc8359",
  "trace_id": "132d4941f2cb41f1be1b55264f087e2a",
  "filename": "/home/wes/src/rholog/demos/demo4.py",
  "lineno": 19,
  "warning": true,
  "status": "OK",
  "start_time": 1698920811.0047772,
  "end_time": 1698920811.004778,
  "duration": 7.152557373046875e-07,
  "message": "TRACE",
  "timestamp": "2023-11-02T10:26:51.004792+00:00"
}
{
  "name": "inside substep_1",
  "levelname": "INFO",
  "root_id": "aaf18e40a5884426bf33fdc43fca0e90",
  "parent_id": "62fa033409d147d8865cf6007200e914",
  "trace_id": "cef94e58be0e44d3ba56f4743ef701e1",
  "filename": "/home/wes/src/rholog/demos/demo4.py",
  "lineno": 12,
  "status": "OK",
  "start_time": 1698920813.0070255,
  "end_time": 1698920813.0070376,
  "duration": 1.2159347534179688e-05,
  "message": "TRACE",
  "timestamp": "2023-11-02T10:26:53.007177+00:00"
}
{
  "name": "__main__.substep_1",
  "levelname": "INFO",
  "root_id": "aaf18e40a5884426bf33fdc43fca0e90",
  "parent_id": "ece05497436e4810af8e488ac1cc8359",
  "trace_id": "62fa033409d147d8865cf6007200e914",
  "filename": "/home/wes/src/rholog/demos/demo4.py",
  "lineno": 9,
  "module": "__main__",
  "function": "substep_1",
  "status": "OK",
  "start_time": 1698920812.0061796,
  "end_time": 1698920814.0092332,
  "duration": 2.003053665161133,
  "message": "TRACE",
  "timestamp": "2023-11-02T10:26:54.009272+00:00"
}
{
  "name": "subcomponent-1",
  "levelname": "INFO",
  "root_id": "aaf18e40a5884426bf33fdc43fca0e90",
  "parent_id": "fe792e6b3f464445b2868fde04b74589",
  "trace_id": "ece05497436e4810af8e488ac1cc8359",
  "filename": "/home/wes/src/rholog/demos/demo4.py",
  "lineno": 18,
  "param1": 12,
  "status": "OK",
  "start_time": 1698920811.004765,
  "end_time": 1698920815.0105977,
  "duration": 4.005832672119141,
  "message": "TRACE",
  "timestamp": "2023-11-02T10:26:55.010729+00:00"
}
{
  "name": "__main__.main",
  "levelname": "INFO",
  "root_id": "aaf18e40a5884426bf33fdc43fca0e90",
  "parent_id": "d696d5a05c004af0b12fab791e167e33",
  "trace_id": "fe792e6b3f464445b2868fde04b74589",
  "filename": "/home/wes/src/rholog/demos/demo4.py",
  "lineno": 16,
  "module": "__main__",
  "function": "main",
  "status": "OK",
  "start_time": 1698920811.0047514,
  "end_time": 1698920815.0113723,
  "duration": 4.00662088394165,
  "message": "TRACE",
  "timestamp": "2023-11-02T10:26:55.011419+00:00"
}
{
  "name": "__main__",
  "levelname": "INFO",
  "root_id": "aaf18e40a5884426bf33fdc43fca0e90",
  "trace_id": "d696d5a05c004af0b12fab791e167e33",
  "filename": "/home/wes/src/rholog/demos/demo4.py",
  "lineno": 30,
  "status": "OK",
  "start_time": 1698920811.004735,
  "end_time": 1698920815.0119102,
  "duration": 4.0071752071380615,
  "message": "TRACE",
  "timestamp": "2023-11-02T10:26:55.011948+00:00"
}
```
