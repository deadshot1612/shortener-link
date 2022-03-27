from datetime import datetime, timedelta

p1 = datetime.now()
p2 = datetime.now()
p2 = p2 +  timedelta(minutes=5)
if p2 > p1:
    print(p2)