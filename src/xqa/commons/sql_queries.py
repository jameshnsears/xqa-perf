count_items = """
-- ingest | ingestbalancer | shard
select count(*)
from events
where info->>'serviceId' like '%s/%%' and info->>'state' = 'END'
"""

get_ingest_count = """
select count(distinct(cast((info->>'size') as bigint))) as cumulative_size
from events
"""

get_ingest_size = """
select sum(distinct(cast((info->>'size') as bigint))) as cumulative_size
from events
"""

how_long_service_took_to_process_test_data = """
select (max(creationtime) - min(creationtime)) / 1000 as service_time_seconds
from (
    select cast((info->>'creationTime') as bigint) as creationtime
    from events
    where info->>'serviceId' like '%s/%%'
    order by events.when asc
) as creationtime;
"""

item_count_to_shard_distribution = """
select info->>'serviceId' as service_id, count(info->>'storage_size') as storage_size
from events
where info->>'serviceId' like 'shard/%%'
  and info->>'state' = 'END'
group by info->>'serviceId';
"""
