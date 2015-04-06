import math

from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class OriginalScorer(object):
  def get_count_points(self, count):
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
  
  def get_date_points(self, when):
    now = datetime.now()
    this_week = now - timedelta(days=7)
    this_month = now - timedelta(days=28)
    three_months_ago = now - timedelta(days=90)
    six_months_ago = now - timedelta(days=180)
    this_year = now - timedelta(days=365)

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

class McastScore(object):
  def get_date_points(self, when):
    now = datetime.now()
    if not isinstance(when, datetime):
      return 0
    else:
      age_delta = abs(now - when)
      # abs: if the repo is somehow in the future, reflect it into the past across now
      age_hours = age_delta.days * 24 + age_delta.seconds / 3600
      age_hours += 4 # aiming for stability in the face of very recent times
      return max(0.25, 5 - math.sqrt(age_hours) * 2 / 46.5 )
      # 5        : max score
      # 2 / 46.5 : scale to lose 2 points at 90 days old

  def get_count_points(self, count):
    return int(math.log(abs(count)+1)*2.1668*100 + 0.5)/100.0
    # abs(count) + 1 : now we can work on any int
    # 2.1668         : factor to match previous step algorithm at 100 => 10.0
    # then round to 2dp

class MinorChangesScore(object):
  def get_date_points(self, when):
    now = datetime.now()
    if not isinstance(when, datetime):
      return 0
    elif now < when:
      return 5 # This shouldn't happen
    else:
      age_delta = now - when
      age_hours = age_delta.days * 24 + age_delta.seconds / 3600
      age_hours += 4 # aiming for stability in the face of very recent times
      return max(0, 5 - math.sqrt(age_hours) * 2 / 46.5 )
      # 5        : max score
      # 2 / 46.5 : scale to lose 2 points at 90 days old

  def get_count_points(self, count):
    return math.log(count+1)*2.1668
    # 2.1668         : factor to match previous step algorithm at 100 => 10.0

if __name__ == '__main__':
  original = OriginalScorer()
  mcast = McastScore()
  minor = MinorChangesScore()

  xs = range(110)

  plt.plot(xs, map(original.get_count_points, xs), 'r')
  plt.plot(xs, map(mcast.get_count_points, xs), 'g')
  plt.plot(xs, map(minor.get_count_points, xs), 'bx')
  plt.show()

  DAYS = 24 * 60 * 60

  xs = range(0, 2*365*DAYS, 1*DAYS)
  xs_time = map(lambda d: datetime.now() - timedelta(seconds=d), xs)

  plt.plot(xs, map(original.get_date_points, xs_time), 'r')
  plt.plot(xs, map(mcast.get_date_points, xs_time), 'g')
  plt.plot(xs, map(minor.get_date_points, xs_time), 'bx')
  plt.show()
