create or replace function get_day_of_week(new_d date,
                                             current_d date, day_of_week integer)
    returns integer as
$$
    declare result integer:=day_of_week;
    begin
        if new_d < current_d::date then
           result:=day_of_week-1;
        elseif new_d > current_d then
           result:=day_of_week+1;
        end if;

        if result=0 then
           result:=7;
        elseif result=8 then
           result:=1;
        end if;

         return result;
     end;
$$  LANGUAGE plpgsql immutable