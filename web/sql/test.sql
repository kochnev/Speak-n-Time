select 
  au.username,
  au.first_name,
  au.last_name,
  upr.website,
  upr.picture
from 
  main_userprofile upr 
join 
  auth_user au
on au.id = upr.user_id

