# rholog
Basic python logging/micotracing inspired by [mulog/mutrace](https://github.com/BrunoBonacci/mulog).

## Demo
```python
$ python3 demo1.py
{
  "name": "main",
  "levelname": "INFO",
  "message": "TRACE",
  "trace": "step1",
  "duration": 1.001368522644043,
  "root_id": "c6872ec8c6894e70a4c574c1f9fb1d92",
  "trace_id": "2d7bd1dd-e47b-4b7f-8178-c1c321b090c6",
  "parent_id": "af5688b0-a971-45b8-b792-645ef387e3ea",
  "timestamp": "2023-10-26T06:00:18.635020+00:00"
}
{
  "name": "main",
  "levelname": "INFO",
  "message": "TRACE",
  "trace": "step2_substep1",
  "duration": 1.0013329982757568,
  "root_id": "c6872ec8c6894e70a4c574c1f9fb1d92",
  "trace_id": "6dfd9827-22fc-4186-bafa-38f9f2131514",
  "parent_id": "c868b7ea-c6c9-456f-9b0b-f4a9484491c3",
  "timestamp": "2023-10-26T06:00:19.637312+00:00"
}
{
  "name": "main",
  "levelname": "INFO",
  "message": "long sleep time",
  "root_id": "c6872ec8c6894e70a4c574c1f9fb1d92",
  "trace_id": "7b936e3d-2faf-4985-a1c8-f8ae27a20c47",
  "parent_id": "c868b7ea-c6c9-456f-9b0b-f4a9484491c3",
  "timestamp": "2023-10-26T06:00:20.639565+00:00"
}
{
  "name": "main",
  "levelname": "INFO",
  "message": "done sleeping",
  "root_id": "c6872ec8c6894e70a4c574c1f9fb1d92",
  "trace_id": "7b936e3d-2faf-4985-a1c8-f8ae27a20c47",
  "parent_id": "c868b7ea-c6c9-456f-9b0b-f4a9484491c3",
  "timestamp": "2023-10-26T06:00:24.644570+00:00"
}
{
  "name": "main",
  "levelname": "INFO",
  "message": "TRACE",
  "trace": "step2_substep2",
  "duration": 4.005673885345459,
  "root_id": "c6872ec8c6894e70a4c574c1f9fb1d92",
  "trace_id": "7b936e3d-2faf-4985-a1c8-f8ae27a20c47",
  "parent_id": "c868b7ea-c6c9-456f-9b0b-f4a9484491c3",
  "timestamp": "2023-10-26T06:00:24.645213+00:00"
}
{
  "name": "main",
  "levelname": "INFO",
  "message": "TRACE",
  "trace": "step2",
  "duration": 6.009850263595581,
  "root_id": "c6872ec8c6894e70a4c574c1f9fb1d92",
  "trace_id": "c868b7ea-c6c9-456f-9b0b-f4a9484491c3",
  "parent_id": "af5688b0-a971-45b8-b792-645ef387e3ea",
  "timestamp": "2023-10-26T06:00:24.645694+00:00"
}
{
  "name": "main",
  "levelname": "INFO",
  "message": "TRACE",
  "trace": "main",
  "duration": 7.012592315673828,
  "root_id": "c6872ec8c6894e70a4c574c1f9fb1d92",
  "trace_id": "af5688b0-a971-45b8-b792-645ef387e3ea",
  "timestamp": "2023-10-26T06:00:24.646099+00:00"
}
```
