import json
import re
import datetime

from bson import json_util

import util.helper as helper


def regexTest():
    pattern = re.compile("^\[!.*\].*")

    array = ["[!QQE-628-34831]: Assignment - Problem to udate agent",
             "hahaha",
             "Emergenza guasto? Soluzioni a noleggio immediate per ogni esigenza",
             "About FAEdisk synch and AVs",
             "[LUS-914-77967]: Exploit 9/10",
             "The Cyber Security Forum Initiative CSFI/CWFI www.csfi.us"
             ]

    for s in array:
        if re.fullmatch(pattern, s) is not None:
            print("match")
        else:
            print("not match")


def datetimeTest():
    datetime1 = datetime.datetime.strptime('2014/12/11 19:18:00', helper.datetimeFullFormat)
    datetime2 = datetime.datetime.strptime('2015/6/6 3:39:00', helper.datetimeFullFormat)
    datetime3 = datetime.datetime.strptime('2015/6/6 11:19:35', helper.datetimeFullFormat)
    print(type(datetime1.year))
    print(datetime1.month)
    print(datetime1.year)
    # print(datetime1.timetuple())
    # print(datetime2.timetuple())
    # if datetime1 > datetime2:
    #     print("1 > 2")
    # else:
    #     print("2 > 1")


def jsonTest():
    print(datetime.datetime.today())
    subjectdict = {'date': datetime.datetime.now()}
    print(subjectdict)
    with open("data/topic/weight&date/subject_count_date.json", "w") as outfile:
        json.dump(subjectdict, outfile, default=json_util.default)


def main():
    # datetimeTest()
    # jsonTest()
    for i in range(min(0, 10)):
        print(i)


if __name__ == '__main__':
    main()
