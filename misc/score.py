from github_conglomerate.Views import Repos
from datetime import datetime, timedelta

def get_count_points(count):
    if count > 100:
        # No more than 10 points
        return 10
    elif count > 50:
        # 7 to 10 points
        return 7 + 3 * (float(count) - 50) / 50
    elif count > 10:
        # 5 to 10 points
        return 5 + 2 * (float(count) - 10) / 40
    elif count > 5:
        # 3 to 5 points
        return 3 + 2 * (float(count) - 5) / 2
    elif count > 4:
        return 2.5
    elif count > 3:
        return 2
    elif count > 0:
        return 1
    else:
        return 0

now = datetime.now()
this_week = now - timedelta(days=7)
this_month = now - timedelta(days=28)
three_months_ago = now - timedelta(days=90)
six_months_ago = now - timedelta(days=180)
this_year = now - timedelta(days=365)
def get_date_points(when):
  if not isinstance(when, datetime):
    return 0
  elif when > this_week:
    return 5
  elif when > this_month:
    return 4
  elif when > three_months_ago:
    return 3
  elif when > six_months_ago:
    return 2
  elif when > this_year:
    return 1
  else:
    return 0

r = Repos('{ "created_at": "2015-03-30T23:26:03", "repos": [] }')
print "# n\tget_count_points_old\tget_count_points\twhen\tget_date_points_old\tget_date_points"
for i in range(0, 720):
    then = now - timedelta(days=i)
    row = (i, get_count_points(i), r.get_count_points(i), '"%s"' % then, get_date_points(then), r.get_date_points(then))
    print "\t".join(str(x) for x in row)
