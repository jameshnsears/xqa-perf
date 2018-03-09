cumulative_size_sql = """
-- total size of all data sent through
select count(distinct(cast((info->>'size') as bigint))) as cumulative_size
from events
where info->>'size' is not null;
"""

service_time_sql = """
select (max(creationtime) - min(creationtime)) / 1000 as service_time_seconds
from (
select cast((info->>'creationTime') as bigint) as creationtime
from events
where info->>'%s' like 'ingest/%'
order by events.when asc
) as creationtime;
"""
