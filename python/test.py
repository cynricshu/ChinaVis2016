import re
import datetime

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
    datetime_obj = datetime.datetime.strptime('2015/6/6 3:39', '%Y/%m/%d %H:%M')
    print(datetime_obj.timetuple())

def main():
    datetimeTest()


if __name__ == '__main__':
    main()
