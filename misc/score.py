from github_conglomerate.Views import Repos

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


r = Repos('{ "created_at": "2015-03-30T23:26:03", "repos": [] }')
for i in range(0, 110):
    print i, "\t", get_count_points(i), "\t", r.get_count_points(i)

