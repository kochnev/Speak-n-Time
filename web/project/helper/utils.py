from collections import defaultdict
from schedule.models import WeeklySchedule


def pivot_schedule(user_schedule):
    """Pivot data for convenient table representation"""

    user_schedule_dict = defaultdict(list)

    # example dict data: {'Mo':[(time_from1, time_to1),(time_from2, time_to2)], 'Fr':[(time_from3, time_to3)]}
    for item in user_schedule:
        user_schedule_dict[item[0]].append((item[1], item[2]), )

    days_of_week = [day[0] for day in WeeklySchedule.DAY_OF_WEEK]

    # example columns: [[(time_from1,time_to2)],[],[],[(time_from3,time_from3),(time_from4,time_to4)],[],[],[]]
    columns = [user_schedule_dict[day] for day in days_of_week]

    # get the length of the longest column
    max_len = len(max(columns, key=len))

    for col in columns:
        # padding the short columns with None
        col += [None, ] * (max_len - len(col))

    # Then rotate the structure...
    rows = [[col[i] for col in columns] for i in range(max_len)]

    return rows
