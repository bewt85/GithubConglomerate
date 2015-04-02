from math import log

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

def get_count_points_ln(count):
    return int(log(abs(i)+1)*2.1668*100 + 0.5)/100.0
    # abs(i) + 1 : now we can work on any int
    # 2.1668     : factor to match previous step algorithm at 100 => 10.0
    # then round to 2dp

for i in range(0, 110):
    print i, "\t", get_count_points(i), "\t", get_count_points_ln(i)

