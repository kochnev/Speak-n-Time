﻿drop table if exists temp1;
--Сохраним во временную таблицу "нормализованную" таблицу с расписаниями
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
        upr.timezone,
        upr.id as userProfileId,
        sch.day_of_week,
        (current_timestamp::date + sch.time_from) at time zone upr.timezone as dt_from_utc,
        (current_timestamp::date + sch.time_to) at time zone upr.timezone as dt_to_utc
    from schedule_weeklyschedule sch
    join main_userprofile upr
         on sch.user_profile_id = upr.id
    join auth_user u
         on u.id = upr.user_id
    where  u.id = 68 or u.id = 71
)t
;

--хак: если начальное время и конечно перенеслись на новую дату, выставляем текущую дату
update temp1
set
dt_from_utc = CURRENT_DATE + dt_from_utc::time,
dt_to_utc = CURRENT_DATE + dt_to_utc::time
where day_from = day_to;


--Получаем пересечение расписания текущего юзера с расписаниями из временной таблицы
select
t1.user_id,
t1.partner_id,
(t1.min_count/t2.min_count) * 100 as intersection_percent
from
(
    select
    t.user_id,
    t.partner_id,
    sum(EXTRACT('epoch' FROM t.end_time - t.start_time) / 60) as min_count
    from
    (
        select
            sch_user.userId as user_id,
            sch_user.userProfileId as user_profile_id,
            sch_utc.userId as partner_id,
             ((case
                when sch_user.dt_from_utc >= sch_utc.dt_from_utc  then sch_user.dt_from_utc
                else sch_utc.dt_from_utc
             end) at time zone  sch_user.timezone)::time as start_time,
            ((case
                when sch_user.dt_to_utc <= sch_utc.dt_to_utc  then sch_user.dt_to_utc
                else sch_utc.dt_to_utc
             end) at time zone sch_user.timezone)::time as end_time
        from
        (
        select  * from temp1
        where userId=71
        ) sch_user
        join temp1 sch_utc
           on (sch_utc.day_from = sch_user.day_from and sch_utc.day_to = sch_user.day_to and sch_utc.userId <> 71)
        where
              (sch_user.dt_from_utc < sch_utc.dt_to_utc and sch_user.dt_to_utc > sch_utc.dt_from_utc)
    )t
    group by t.user_id, t.partner_id
)t1
join
(
    select
       upr.user_id,
       sum(EXTRACT('epoch' FROM wsch.time_to - wsch.time_from) / 60) as min_count
    from
    schedule_weeklyschedule wsch
    join main_userprofile upr
         on wsch.user_profile_id = upr.id
    where  upr.user_id = 71
    group by upr.user_id
)t2
 on t1.user_id = t2.user_id



    ;









