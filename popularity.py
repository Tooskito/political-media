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


big_start = current_time_millis()

election_days = [ 
    date(2004, 11, 2), 
    date(2008, 11, 4), 
    date(2012, 11, 6), 
    date(2016, 11, 8) ]

for election_day in election_days:
    # Newline because output is chaotic.
    print()

    # Build 30-day interval before election.
    print('Beginning scrape for year:', election_day.year)
    date_list = [ [(election_day - timedelta(days=x+1)).strftime("%Y-%m-%d"), \
        (election_day - timedelta(days=x)).strftime("%Y-%m-%d")] for x in range(30)][::-1]
    timeframe_list = [' '.join(dates) for dates in date_list]
    print("Loaded dates.")
    print(timeframe_list)

    # Set up checkpoints and composite.
    small_start = current_time_millis()
    composite = None

    for timeframe in timeframe_list:
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
        delay = 10
        print('Done. Sleeping for', delay, 'seconds.')
        sleep(delay)
    
    # Report how long it took to make 1500 requests!
    small_end = current_time_millis()
    print('All data for year', election_day.year, 'retrieved in', small_end-small_start, 'ms')

    # Save to file.
    name = f'popularity-data-{election_day.year}.csv'
    print('Saving result to', name)
    with open(name, 'w') as file:
        file.write(composite.to_csv())

# Report how long it took to make all requests.
big_end = current_time_millis()
print('All data written in', big_end-big_start, 'ms')