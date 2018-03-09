import matplotlib.pyplot as plt
import psycopg2

from xqa.commons.sql import cumulative_size_sql

try:
    conn = psycopg2.connect("dbname='xqa' user='xqa' host='0.0.0.0' password='xqa'")
    cur = conn.cursor()
    cur.execute(cumulative_size_sql)
    rows = cur.fetchall()
    for row in rows:
        print(row[0])
except:
    print('unable to connect to the database')

# how to group things by 

"""
for pool_size in [3, 4, 6]:

    for number_of_shards in [1, 2, 4, 8]:
        run an e2e.sh with correct -pool_size parameter + number_of_shards
        
        wait for all data to have reached the shard(s)
        = use sql
            = have it work with multiple shards
        
        run 3 sql queries
        = store results

    draw chart

--

reun 

"""

number_of_shards = [1, 2, 4, 8]

ingest = [49.48, 73.57, 206.783, 30.133]
ingest_balancer = [44.91, 58.09, 78.07, 107.7]
shard = [449.48, 553.57, 696.783, 870.133]

plt.plot(number_of_shards, ingest, marker='x', color='red', label='ingest')
plt.plot(number_of_shards, ingest_balancer, marker='x', color='grey', label='ingest-balancer')
plt.plot(number_of_shards, shard, marker='x', color='blue', label='shard')

plt.legend(loc=2)
plt.grid()
plt.xlabel('shards')
plt.ylabel('seconds')
plt.title('xxx bytes; n ingest balancer threads; 4 core cpu')

# plt.show()

#plt.savefig('a.png')