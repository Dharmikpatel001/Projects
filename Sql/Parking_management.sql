use parking_usage;

CREATE INDEX idx_entry_time ON parking_usage(entry_time);
CREATE INDEX idx_slot ON parking_usage(slot_id);

show tables; 
select * from parking_lot;
select * from parking_slot;
select * from parking_usage;
select * from parking_zone;
select * from vehicle;

# Total records in parking usage
select count(*) as total_parking_records
from parking_usage;

# date range of parking data
select min(entry_time) as first_entry, max(leaving_time) as last_exit
from parking_usage;

# parking duration analysis
select usage_id, slot_id, timestampdiff(minute, entry_time, leaving_time) as parking_minutes
from parking_usage;

# average parking duration
select round(avg(timestampdiff(minute, entry_time, leaving_time)), 2) as avg_parking_minutes
from parking_usage;

# parking entries per hour
select hour(entry_time) as entry_hour, count(*) as total_entries
from parking_usage
group by entry_hour	
order by total_entries desc;

# average parking duration per hour
select hour(entry_time) as entry_hour, round(avg(timestampdiff(minute, entry_time, leaving_time)), 2) as avg_duration
from parking_usage
group by entry_hour
order by entry_hour;

# total parking usage per zone

select z.zone_name, count(u.usage_id) as total_parkings
from parking_usage u
join parking_slot s on u.slot_id = s.slot_id
join parking_zone z on s.zone_id = z.zone_id
group by z.zone_name
order by total_parkings desc;

# average parking duration per zone

select z.zone_name, round(avg(timestampdiff(minute, u.entry_time, u.leaving_time)), 2) as avg_duration_minutes
from parking_usage u
join parking_slot s on u.slot_id = s.slot_id
join parking_zone z on s.zone_id = z.zone_id
group by z.zone_name;

# total parking by vehicle type

select v.vehicle_type, count(u.usage_id) as total_parkings
from parking_usage u
join vehicle v on u.vehicle_id = v.vehicle_id
group by v.vehicle_type
order by total_parkings desc;

# average duration by vehicle type

select v.vehicle_type, round(avg(timestampdiff(minute, u.entry_time, u.leaving_time)), 2) as avg_minutes
from parking_usage u
join vehicle v on u.vehicle_id = v.vehicle_id
group by v.vehicle_type;

# zone capacity vs total usage

select z.zone_name, z.total_slots, count(u.usage_id) as total_parkings
from parking_zone z
left join parking_slot s on z.zone_id = s.zone_id
left join parking_usage u on s.slot_id = u.slot_id
group by z.zone_name, z.total_slots
order by total_parkings desc;

# vehicles parked more than 6 hours

select u.usage_id, v.vehicle_type, timestampdiff(hour, u.entry_time, u.leaving_time) as parked_hours
from parking_usage u
join vehicle v on u.vehicle_id = v.vehicle_id
where timestampdiff(hour, u.entry_time, u.leaving_time) > 6;

# top 10 most frequent vehicles

select vehicle_id, count(*) as visit_count
from parking_usage
group by vehicle_id
order by visit_count desc
limit 10;

# daily parking count
select date(entry_time) as parking_date, count(*) as total_parkings
from parking_usage
group by parking_date
order by parking_date;

# revenue per parking
select usage_id, round((timestampdiff(minute, entry_time, leaving_time) / 60) * 20, 2) as revenue
from parking_usage;

# zone-wise revenue
select z.zone_name, round(sum((timestampdiff(minute, u.entry_time, u.leaving_time) / 60) * 20), 2) as total_revenue
from parking_usage u
join parking_slot s on u.slot_id = s.slot_id
join parking_zone z on s.zone_id = z.zone_id
group by z.zone_name
order by total_revenue desc;

# top 3 busiest zones
select zone_name, total_parkings
from (
	select z.zone_name, count(u.usage_id) as total_parkings, dense_rank() over (order by count(u.usage_id) desc) as rnk
    from parking_usage u
    join parking_slot s on u.slot_id = s.slot_id
    join parking_zone z on s.zone_id = z.zone_id
    group by z.zone_name
) ranked_zones
where rnk <= 3;


