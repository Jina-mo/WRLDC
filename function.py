import numpy as np
import pandas as pd
import json

# Reading from json
with open('config.json') as f:
    data = json.load(f)

filepath = data['input_path']
df = pd.read_excel(filepath, sheet_name="Sheet1")


def VQ_violation(voltage, MVAr):
    if voltage > 220 and MVAr < 0:
        return True


def PQ_violation(real_power, reactive_power):
    if reactive_power > 0:
        return True

    else:
        try:
            pf = np.cos(np.atan(reactive_power / real_power))
            if pf > 0.95:
                return True
        except ZeroDivisionError:
            return False  # This should something else i guess


def chunk(farm_data, starttime, endtime):
    ###  TIme filtering
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            time_column = col
            break
    ###
    filtered_values = df[df[time_column].between(endtime, starttime)][farm_data].tolist()
    return filtered_values