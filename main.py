from util import query_user, code_to_name

''' DEFINE NEWSPAPER BIASES '''
from biases import biases_filtered

''' RETRIEVE ELECTION DATA '''
import pandas as pd
import plotly.express as px

# Taken from:
# https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/42MVDX
election_raw = pd.read_csv("1976-2016-president.csv")

# Then only grab the data corresponding to the 2016 election.
election_filtered = election_raw[election_raw.year == 2016]

# Drop everything we don't want.
election_filtered = election_filtered.drop(
    labels=['year', 'state_fips', 'state_cen', 'state_ic', 'office', 'writein', 'version', 'notes'], axis=1 )

# Now only grab 'republican' or 'democrat'ic candidates.
election_filtered = election_filtered[ election_filtered.party.isin(['republican', 'democrat']) ]

# Create new column 'percentagevotes' -> the percentage of total state votes that a given party garnered.
election_filtered['percentagevotes'] = election_filtered.apply(
    lambda row: row.candidatevotes / row.totalvotes, axis=1 )

# Get all state codes.
state_codes = pd.unique( election_filtered["state_po"].values.ravel() )
election_by_state = dict()

# Create entry for every state code.
for code in state_codes:
    state_df = election_filtered.loc[election_filtered['state_po'] == code]
    democrat = state_df.loc[state_df['party'] == 'democrat']['percentagevotes'].sum()
    republican = state_df.loc[state_df['party'] == 'republican']['percentagevotes'].sum()
    # election_by_state[<EXAMPLE>] represents how much a state leaned towards republican or democrat.
    election_by_state[code] = republican - democrat
    print(code, '=', election_by_state[code])

# Display results.
fig = px.choropleth(
    locations=list(election_by_state.keys()), 
    locationmode='USA-states', color=list(election_by_state.values()), 
    title='2016 Popular Election Results on Left-Right Scale',
    scope='usa', color_continuous_scale='Bluered'
)
fig.show()

# Fun facts!
print('Fun facts.')
print(max(election_by_state, key=election_by_state.get), 'was the most Republican @', max(election_by_state.values()))
print(min(election_by_state, key=election_by_state.get), 'was the most Democratic @', min(election_by_state.values()))

# Pause. Don't want to overwhelm user.
query_user('Enter anything to continue. ')

''' COMBINE DATA AND DISPLAY '''
# Read in popularity data and multiply by right-left biases.
df = pd.read_csv("popularity-data.csv").set_index('geoName')
for key, value in biases_filtered.items():
    df[key] = value * df[key]
df = df.transpose()
print('Newspaper right-left interest.')
print(df)

# Multiply by right-left results of the election.
for key, value in election_by_state.items():
    df[ code_to_name[key] ] *= value
df['sum'] = df.sum(axis=1)
print('Newspaper "Score" by state.')
print(df)

df = df.reset_index()

# Display results.
fig = px.bar(
    df, x='index', y='sum', 
    title='Most Positively-Influential Newspaper One Month up to the 2016 Presidental Election',
    color='sum'
)
fig.show()