# Simple HTTP Server

HTTP Server that can handle a `POST /delineation` request:
The user must send a csv file passing `delineation_file` as param and the `record_datetime` as query param.


CLI to test the API:
````
curl -X POST -F "delineation_file=@record.csv" "http://127.0.0.1:5000/delineation?record_datetime=2023-01-17%2012:00:00"
````

The heart rate calculation was done using the distance of two QRS waves in sequence, based on the onset time.

To handle some data problems I used the `normal_beats_threshold` variable, a value that represents the number of normal heartbeats (P - QRS - T waves in a row) before starting to count valid heartbeats, which will be used for our calculations and response. Also, `last_p` / `last_qrs` are variables to help ensure we find normal heartbeats. 

As it is supposed to be a simple HTTP server, all the code is written in main.py.