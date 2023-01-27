import pandas as pd
from config import conn
import numpy as np

# connects to PostgreSQL
cur = conn.cursor()
# writes SQL query to only select flights that were not cancelled or diverted 
cur.execute("SELECT * FROM real_flights WHERE cancelled = 'False' and diverted = 'False'")

#gets all rows 
rows = cur.fetchall()

#closes curser and connection
cur.close()
conn.close()

# create dataframe 
df = pd.DataFrame(rows, columns=[desc.name for desc in cur.description])

# Delayed columnn shows if flight has been with , delayed = 1 or not = 0
df['delayed'] = np.where((df['arr_del15'] == df['dep_del15']), np.where(df['arr_del15']==True,1,0), np.nan)

# groups the OP_UNIQUE_CARRIER and the ratio of its flight delaying  
op_df = df.groupby('op_unique_carrier')['delayed'].aggregate(['mean'])

# sorts the delayed ratios from each airline desending order
op_df.sort_values(by='mean', ascending=False, inplace=True)

# groups the ORIGIN_AIRPORT_ID and the ratio of its flight delaying 
origin_df = df.groupby('origin_airport_id')['delayed'].aggregate(['mean'])

# sorts the delayed ratios from each airline desending order
origin_df.sort_values(by='mean', ascending=False, inplace=True)



