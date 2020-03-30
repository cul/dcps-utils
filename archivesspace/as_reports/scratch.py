# Testing getting updated records based on current time - x hours
import ASFunctions as asf
from datetime import datetime, date, timedelta, timezone
from pprint import pprint

asf.setServer('Prod')


repos = [2, 3, 4, 5]

now1 = datetime.utcnow().replace(tzinfo=timezone.utc)
# print(type(now1))
start_time = str(now1)
end_time = ''  # set later
# today_str = str(date.today().strftime("%Y%m%d"))

yesterday = (now1 - timedelta(hours=72))
yesterday = yesterday.replace(
    tzinfo=timezone.utc).replace(microsecond=0).isoformat()
print(now1.isoformat())
yest_str = str(yesterday)
print(yesterday)
print(" ")


for r in repos:
    print('Repo = ' + str(r))
    the_date = yest_str
    the_fields = ['id', 'title', 'identifier', 'system_mtime', 'publish']
    x = asf.getByDate(r, the_date, date_type='mtime',
                      comparator='greater_than', filter='resources', fields=the_fields)

    pprint(x)
