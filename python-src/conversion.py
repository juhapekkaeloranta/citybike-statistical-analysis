import datetime

def getTimeStampFromBikedataTimeHour(time):
    return datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

def getTimeStampFromWeatherdataTime(row):
    return datetime.datetime(year=int(row.Year), month=int(row.Month), day=int(row.Day), hour=int(row.HourMin.split(':')[0]), minute=int(row.HourMin.split(':')[1]))

def getTimeStampFromTmarkedTime(time):
    return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

def getUTCTimeStampFromTimeStampString(timestamp):
    return str(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").isoformat()) + 'Z'


def main():
    test = "2017-09-30 23:00:00"
    print(test)
    print(getUTCTimeStampFromTimeStamp(test))

if __name__ == "__main__":
    main()
