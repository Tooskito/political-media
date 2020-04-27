from pytrends.request import TrendReq
from biases import biases_filtered
from datetime import date, timedelta
from time import time, sleep
import pandas as pd

''' CREATE POPULARITY DATAFRAME '''
# Build function to grab time.
current_time_millis = lambda: int(round(time() * 1000))

# Init requester with EST timezone, retries, and backoff to be safe.
pytrends = TrendReq(hl='en-US', tz=300, timeout=(10, 25), retries=5, backoff_factor=0.1)

# Build keyword list.
kw_list = list( biases_filtered.keys() )

# Max keyword batch size is 5. Group by 5.
batch_size = 5
group = lambda my_list: [
    my_list[i:min(len(kw_list), i+batch_size)] \
        for i in range(0, len(kw_list), batch_size) ] 

# Build list of dates around election day.
election_day = date(2016, 11, 8)
date_list = [ [(election_day - timedelta(days=x+1)).strftime("%Y-%m-%d"), \
    (election_day - timedelta(days=x)).strftime("%Y-%m-%d")] for x in range(30)][::-1]
timeframe_list = [' '.join(dates) for dates in date_list]
print("Loaded dates.")
print(timeframe_list)

# Prepare for loop.
start = current_time_millis()
composite = None

# For each date interval, request all newspaper interest by batch.
for timeframe in timeframe_list:
    # Grab batch of newspaper interest for a given day.
    frames = []
    for batch in group(kw_list):
        pytrends.build_payload(batch, cat=0, timeframe=timeframe, geo='US', gprop='')
        frames.append(pytrends.interest_by_region())
        print("Got response for", batch)
    result = pd.concat(frames, axis=1)
    # Add to composite.
    if composite is None:   composite = result
    else:   composite = composite.add(result)
    # Sleep so we don't get denied.
    print('Composite is now', composite)
    print('Done. Sleeping for 10 seconds.')
    sleep(10)

# Report how long it took.
end = current_time_millis()
print('All data retrieved in', end-start, 'ms')

# Save to file.
name = 'popularity-data.csv'
print('Saving result to', name)
with open(name, 'w') as file:
    file.write(composite.to_csv())