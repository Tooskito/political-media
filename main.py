from util import query_user, code_to_name, name_to_code

''' DEFINE NEWSPAPER BIASES '''
from biases import biases_raw, biases_filtered

''' RETRIEVE ELECTION DATA '''
import pandas as pd
import plotly.express as px

# Taken from:
# https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/42MVDX
election_raw = pd.read_csv("1976-2016-president.csv")

# Then only grab the data corresponding to the 20XX elections.
years = [2004, 2008, 2012, 2016]
election_filtered = election_raw[ election_raw.year.isin(years) ]

# Now only grab 'republican' or 'democrat'ic candidates.
election_filtered = election_filtered[ election_filtered.party.isin(['republican', 'democrat']) ]

# Drop everything we don't want.
election_filtered = election_filtered.drop(
    labels=['state_fips', 'state_cen', 'state_ic', 'office', 'writein', 'version', 'notes'], axis=1 )

# Create new column 'percentagevotes' -> the percentage of total state votes that a given party garnered.
election_filtered['percentagevotes'] = election_filtered.apply(
    lambda row: row.candidatevotes / row.totalvotes, axis=1 )

# Get all state codes.
state_codes = pd.unique( election_filtered["state_po"].values.ravel() )
election_axis = pd.DataFrame(columns=['year', 'state_po', 'axis'])

for year in years:
    for code in state_codes:
        
        # "Scope" in on specific year and state.
        bool_series = (election_filtered['year'] == year) & (election_filtered['state_po'] == code)
        scoped_df = election_filtered.loc[bool_series]
        
        # Calculate republican-democratic differential.
        democrat = scoped_df.loc[scoped_df['party'] == 'democrat']['percentagevotes'].sum()
        republican = scoped_df.loc[scoped_df['party'] == 'republican']['percentagevotes'].sum()
        
        # "Axis" represents how much a state leaned towards republican or democrat.
        election_axis = election_axis.append({'year': year, 'state_po': code, 'axis': republican-democrat}, ignore_index=True)
        #print(year, code, republican-democrat)

print(election_axis)

# Display results.
fig = px.choropleth(
    election_axis,
    locations='state_po', locationmode='USA-states', 
    color='axis', color_continuous_midpoint=0,
    title='2004-2016 Popular Election Results on Left-Right Scale',
    scope='usa', color_continuous_scale='Bluered',
    animation_frame='year',
)
fig.show()

query_user("Enter anything to continue. ")

fig = px.line(
    election_axis,
    x='year', y='axis',
    color='state_po'
)
fig.show()

query_user("Enter anything to continue. ")

''' COMBINE DATA '''
composite = None
for year in years:
    # Get year of multiplier.
    election_by_year = election_axis.loc[election_axis['year'] == year]
    
    # Get popularity data.
    popularity = pd.read_csv(f"popularity-data-{year}.csv").set_index('geoName')
    for newspaper, multiplier in biases_filtered.items():
        popularity[newspaper] *= multiplier
    
    popularity = popularity.transpose()

    # Multiply state by how it voted.
    for column in popularity.columns:
        popularity[column] *= election_by_year.loc[election_by_year['state_po'] == name_to_code[column]].squeeze()['axis']
    popularity['score'] = popularity.sum(axis=1)
    
    # Drop all columns we don't need.
    popularity.reset_index(inplace=True)
    popularity.drop(popularity.columns.difference(['index', 'score']), axis=1, inplace=True)
    popularity['year'] = year

    if composite is None:   composite = popularity
    else:   composite = pd.concat([composite, popularity], ignore_index=True)


# Add text column for readability.
composite['axis'] = composite.apply(
    lambda row: biases_raw[row['index']], axis=1 )

print('Composite finalized.')
print(composite)

# Display results.
fig = px.bar(
    composite, x='index', y='score', color='score',
    range_y=(-8000, 8000), text='axis', animation_frame='year',
    title='Most Positively-Influential Newspaper One Month up to the 2004-2016 Presidental Elections',
)
fig.show()
