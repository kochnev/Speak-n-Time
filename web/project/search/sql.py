
main_search_query_text="""
select
upr.*,
round((t1.min_count/t2.min_count) * 100) as intersection_percent
from
(
    select
    t.partner_id,
    sum(EXTRACT('epoch' FROM t.end_time - t.start_time) / 60) as min_count
    from
    (
       select * from get_intersection_detail(%(userId)s) 
       where (partner_id=%(partnerId)s or %(partnerId)s is null)
       
    )t
    group by t.partner_id
)t1
cross join
(
    select
       upr.user_id,
       sum(EXTRACT('epoch' FROM wsch.time_to - wsch.time_from) / 60) as min_count
    from
    schedule_weeklyschedule wsch
    join main_userprofile upr
         on wsch.user_profile_id = upr.id
    where  upr.user_id = %(userId)s
    group by upr.user_id
)t2
join main_userprofile upr 
  on upr.user_id = t1.partner_id
order by round((t1.min_count/t2.min_count) * 100) desc
;
"""