# Simple HTTP Server

HTTP Server that can handle a `POST /delineation` request:
The user must send a csv file passing `delineation_file` as param and the `record_datetime` as query param.


CLI to test the API:
````
curl -X POST -F "delineation_file=@record.csv" "http://127.0.0.1:5000/delineation?record_datetime=2023-01-17%2012:00:00"
````

The heart rate calculation was done using the distance of two QRS waves in sequence, based on the onset time.

To handle some data problems I used the `normal_beats_threshold` variable, a value that represents the number of normal heartbeats (P - QRS - T waves in a row) before starting to count valid heartbeats, which will be used for our calculations and response. Also, `last_p` / `last_qrs` are variables to help ensure we find normal heartbeats. 

I concluded that tags play a more informative role and maybe we can show some information or percentages about them, but the tagged waves are still valid for our calculation.

As it is supposed to be a simple HTTP server and API, all the code is written in main.py and there is no validation, request/response schemas or error handling for this API.

##  Can you think of a more efficient way to achieve this? For example, what if the client is continuously sending delineation and the file is 10 times larger?

A more efficient way to achieve this is implementing streaming processing. We are now reading the entire file, keeping it in the memory and then doing the calculation line by line. One solution is to receive this file in chunks and so process it by smaller parts. It is also possible to implement a distributed processing entity, this way we can split our big file and parallelize the processing of its small pieces.