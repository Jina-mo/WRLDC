import datetime as dt
import pandas as pd

from function import VQ_violation, PQ_violation, chunk, data

# Output path of excel
filepath2 = data['output_path']

# Block for getting start and end time
current_datetime = dt.datetime.now()
req_date = dt.datetime.strptime(data['specific_date'], '%Y-%m-%d')
start_time = dt.datetime.combine(req_date, current_datetime.time())
end_time = start_time - dt.timedelta(hours=int(data['hour_gap_for_end']),
                                     minutes=int(data['minute_gap_for_end']), seconds=int(data['seconds_gap_for_end']))

filtered_list = list()  # List for making output dataframe

for generator in data['substation_data']:  # iterate over substation data fed from json config file
    call_data = ['Substation_Voltage', 'substation_Q', 'farm_P', 'farm_Q', 'time']

    voltList = chunk(generator[call_data[0]], start_time, end_time)
    # voltage check
    for index, volt in enumerate(voltList):
        if volt > 220:
            mvarList = chunk(generator[call_data[1]], start_time, end_time)
            if VQ_violation(volt, mvarList[index]):
                farm_p_list = chunk(generator[call_data[2]], start_time, end_time)
                farm_q_list = chunk(generator[call_data[3]], start_time, end_time)
                if PQ_violation(farm_p_list[index], farm_q_list[index]):

                    ### This is to fetch time at which violation has occured
                    time_list = chunk(generator[call_data[4]], start_time, end_time)
                    ###
                    filtered_list.append([generator['Farm_name'], volt, mvarList[index], farm_p_list[index], farm_q_list[index], time_list[index]])


filtered_data = pd.DataFrame(filtered_list, columns=list(data['substation_data'][0].keys()))
filtered_data.to_excel(filepath2, index=False)