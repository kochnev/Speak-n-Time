search_query_text = """drop table if exists temp1;
--Сохраним во временную таблицу "нормализованную" таблицу с расписаниями
CREATE TEMP TABLE schedule_utc AS
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
        sch.day_of_week,
        (current_timestamp::date + sch.time_from) at time zone upr.timezone as dt_from_utc,
        (current_timestamp::date + sch.time_to) at time zone upr.timezone as dt_to_utc
    from schedule_weeklyschedule sch
    join main_userprofile upr
         on sch.user_profile_id = upr.id
    join auth_user u
         on u.id = upr.user_id
    where 1=1 {{clause}}
)t
;

--хак: если начальное время и конечно перенеслись на новую дату, выставляем текущую дату
update schedule_utc
set
dt_from_utc = CURRENT_DATE + dt_from_utc::time,
dt_to_utc = CURRENT_DATE + dt_to_utc::time
where day_from = day_to;

--Получаем пересечение расписания текущего юзера с расписаниями из временной таблицы.
select
    sch_user.userId,
    sch_user.username,
    sch_utc.userId as partner_id,
    sch_utc.username as partner_user_name,
    sch_user.day_of_week,
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
    select  * from schedule_utc
    where userId=%(userId)s
) sch_user
join schedule_utc sch_utc
   on (sch_utc.day_from = sch_user.day_from and sch_utc.day_to = sch_user.day_to and sch_utc.userId <> %(userId)s)
where
   sch_user.dt_from_utc < sch_utc.dt_to_utc and sch_user.dt_to_utc > sch_utc.dt_from_utc
;
"""