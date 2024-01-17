import csv
from datetime import datetime, timedelta

from flask import Flask, request

app = Flask(__name__)


@app.route('/delineation', methods=['POST'])
def process_delineation():
    delineation_file = request.files['delineation_file']
    delineation_reader = csv.reader(delineation_file.read().decode('utf-8').splitlines())
    record_datetime_query_param = request.args.get('record_datetime')
    record_datetime = datetime.strptime(record_datetime_query_param,
                                        "%Y-%m-%d %H:%M:%S") if record_datetime_query_param else None

    premature_p_waves_count = 0
    premature_qrs_waves_count = 0
    previous_qrs_onset = None
    current_heart_rate = None
    heart_rates = []
    min_heart_rate = float('inf')
    max_heart_rate = float('-inf')
    min_heart_rate_timedelta = None
    max_heart_rate_timedelta = None

    normal_beats_threshold = 4
    last_p = False
    last_qrs = False

    for row in delineation_reader:
        wave_type, wave_onset, wave_offset, *wave_tags = row
        wave_onset, wave_offset = int(wave_onset), int(wave_offset)

        if wave_type == 'P':
            if 'premature' in wave_tags:
                premature_p_waves_count += 1
            last_p = True
            last_qrs = False
        elif wave_type == 'QRS':
            if 'premature' in wave_tags:
                premature_qrs_waves_count += 1
            if last_p:
                if previous_qrs_onset:
                    current_heart_rate = 60000 / (wave_onset - previous_qrs_onset)
                previous_qrs_onset = wave_onset
                last_qrs = True
                last_p = False
                continue
            last_qrs = False
            last_p = False
            normal_beats_threshold = 4
        elif wave_type == 'T':
            if last_qrs:
                normal_beats_threshold -= 1
                if normal_beats_threshold <= 0:
                    heart_rates.append(current_heart_rate)
                    if current_heart_rate < min_heart_rate:
                        min_heart_rate = current_heart_rate
                        min_heart_rate_timedelta = timedelta(milliseconds=wave_onset)
                    if current_heart_rate > max_heart_rate:
                        max_heart_rate = current_heart_rate
                        max_heart_rate_timedelta = timedelta(milliseconds=wave_onset)
                last_qrs = False

    response = {
        'premature_p_waves': premature_p_waves_count,
        'premature_qrs_waves': premature_qrs_waves_count,
        'mean_heart_rate': sum(heart_rates) / len(heart_rates),
        'min_heart_rate': min_heart_rate,
        'min_heart_rate_time': record_datetime + min_heart_rate_timedelta if
        record_datetime else "User must provide 'record_datetime' query param for date information",
        'max_heart_rate': max_heart_rate,
        'max_heart_rate_time': record_datetime + max_heart_rate_timedelta if
        record_datetime else "User must provide 'record_datetime' query param for date information",
    }

    return response


if __name__ == '__main__':
    app.run(debug=True)
