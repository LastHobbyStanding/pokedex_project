import pandas as pd
import sqlite3
import os
# Try the path for when called from main project folder
if os.path.exists('Data/pokemon_stats.db'):
    conn = sqlite3.connect('Data/pokemon_stats.db')
# Otherwise use the path for when called from Data folder
else:
    conn = sqlite3.connect('pokemon_stats.db')

# # Check the actual table structure
# cursor = conn.cursor()
# cursor.execute("PRAGMA table_info(all_pokemon_stats)")
# columns_info = cursor.fetchall()
# print("Database columns:")
# for col in columns_info:
#     print(f"  {col[1]} ({col[2]})")  # col[1] is column name, col[2] is type
#
df = pd.read_sql(sql='SELECT * FROM all_pokemon_stats', con=conn)
# print("DataFrame columns:", df.columns.tolist())

# Min, max and average stats

# stats_summary = df[['hp','attack','defense','sp_attack','sp_defense','speed']].agg(['min','max','mean'])
# print(stats_summary)
#
hp_rank = df[['pokemon_id','pokemon_name','hp']].copy()
hp_rank['hp_rank'] = df['hp'].rank(method='min',ascending=False)


attack_rank = df[['pokemon_id','pokemon_name','attack']].copy()
attack_rank['attack_rank'] = df['attack'].rank(method='min',ascending=False)


defense_rank = df[['pokemon_id','pokemon_name','defense']].copy()
defense_rank['defense_rank'] = df['defense'].rank(method='min',ascending=False)


sp_attack_rank = df[['pokemon_id','pokemon_name','sp_attack']].copy()
sp_attack_rank['sp_attack_rank'] = df['sp_attack'].rank(method='min',ascending=False)


sp_defense_rank = df[['pokemon_id','pokemon_name','sp_defense']].copy()
sp_defense_rank['sp_defense_rank'] = df['sp_defense'].rank(method='min',ascending=False)


speed_rank = df[['pokemon_id','pokemon_name','speed']].copy()
speed_rank['speed_rank'] = df['speed'].rank(method='min',ascending=False)
