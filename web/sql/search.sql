﻿drop table if exists temp1;

CREATE TEMP TABLE temp1 AS
select
     t.*,
     CASE
           WHEN t.dt_from_utc::date < current_timestamp::date THEN
                CASE
                    WHEN t.day_of_week=1 THEN 7
                    ELSE t.day_of_week-1
                END
           WHEN t.dt_from_utc::date > current_timestamp::date THEN
                 CASE
                    WHEN t.day_of_week=7 THEN 1
                    ELSE t.day_of_week+1
                 END
           ELSE t.day_of_week
     END as  day_from,
     CASE
           WHEN t.dt_to_utc::date < current_timestamp::date THEN
                CASE
                    WHEN t.day_of_week=1 THEN 7
                    ELSE t.day_of_week-1
                END
           WHEN t.dt_to_utc::date > current_timestamp::date THEN
                 CASE
                    WHEN t.day_of_week=7 THEN 1
                    ELSE t.day_of_week+1
                 END
           ELSE t.day_of_week
     END as  day_to

from
(
    select
        u.id as userId,
        u.username,
        sch.day_of_week,
        (current_timestamp::date + sch.time_from) at time zone upr.timezone as dt_from_utc,
        (current_timestamp::date + sch.time_to) at time zone upr.timezone as dt_to_utc
    from schedule_weeklyschedule sch
    join main_userprofile upr
         on sch.user_profile_id = upr.id
    join auth_user u
         on u.id = upr.user_id
)t
;

update temp1
set
dt_from_utc = CURRENT_DATE + dt_from_utc::time,
dt_to_utc = CURRENT_DATE + dt_to_utc::time
where day_from = day_to;


select
     *
     ,
    case
        when sch.dt_from_utc >= t1.dt_from_utc  then sch.dt_from_utc
        else t1.dt_from_utc
     end as startTime,
     case
        when sch.dt_to_utc <= t1.dt_to_utc  then sch.dt_to_utc
        else t1.dt_to_utc
     end as endTime
from
(
select  * from temp1
where userId=71
) sch
join temp1 t1
   on (t1.day_from = sch.day_from and t1.day_to = sch.day_to and t1.userId <> 71)
where
   (sch.dt_from_utc >= t1.dt_from_utc and sch.dt_from_utc <= t1.dt_to_utc)
   or
   (sch.dt_to_utc >= t1.dt_from_utc and sch.dt_to_utc <= t1.dt_to_utc)
;





