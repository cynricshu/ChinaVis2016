import codecs
import csv
import os
import sys

import pymysql


def main():
    try:
        conn = getconn()
    except Exception as e:
        print(e)
        sys.exit(1)

    cursor = conn.cursor()

    # sql = "INSERT INTO t_user (username) VALUES (%s)"
    # id = cursor.execute(sql, ('very-secret'))
    # conn.commit()
    # print(id)

    fileList = os.listdir("data")

    for filename in fileList:
        loadcsv(conn, cursor, "data/", filename)

    cursor.close()
    conn.close()


def getconn():
    conn = pymysql.connect("localhost",
                           "root",
                           "root",
                           "chinavis")

    return conn


def nullify(L):
    """Convert empty strings in the given list to None."""

    # helper function
    def f(x):
        if (x == ""):
            return None
        else:
            return x

    return [f(x) for x in L]


def loadcsv(conn, cursor, dir, filename):
    """
    Open a csv file and load it into a sql table.
    Assumptions:
     - the first line in the file is a header
    """

    # insert username, which is the same as filename
    query = "insert into t_user (username) values (%s) "
    cursor.execute(query, filename)
    conn.commit()

    f = csv.reader(codecs.open(dir + filename, "r", "iso-8859-1"))
    header = f.__next__()
    numfields = len(header)

    insertMail = buildInsertMailSql(numfields)
    insertUserMail = "insert into t_user_mail (userid, mailid) values (" \
                     " (select max(userid) from t_user), " \
                     " (select max(mailid) from t_mail) " \
                     ")"
    count = 0
    """
    insert mail info, then add a new record in relation table t_user_mail
    """
    maxSubLen = 0
    maxFromLen = 0
    maxToDisLen = 0
    maxToLen = 0
    maxCcDisLen = 0
    maxCCLen = 0
    maxBccLen = 0
    maxBccDisLen = 0
    maxAttachLen = 0
    for line in f:
        if len(line) > 1:
            # if len(line) < 15:
            #     print("line " + str(count) + " of file " + filename + " less than 15: " + str(len(line)))
            #     print(line)
            #     continue
            vals = nullify(line)

            # get the longest length of ccaddress and toaddress

            # if vals[2] is not None:
            #     maxFromLen = max(maxFromLen, len(vals[2]))
            # if vals[4] is not None:
            #     maxToLen = max(maxToLen, len(vals[4]))
            # if vals[6] is not None:
            #     maxCCLen = max(maxCCLen, len(vals[6]))
            # if vals[8] is not None:
            #     maxBccLen = max(maxBccLen, len(vals[8]))

            # if vals[0] is not None:
            #     maxSubLen = max(maxSubLen, len(vals[0]))
            # if vals[3] is not None:
            #     maxToDisLen = max(maxToDisLen, len(vals[3]))
            # if vals[5] is not None:
            #     maxCcDisLen = max(maxCcDisLen, len(vals[5]))
            # if vals[7] is not None:
            #     maxBccDisLen = max(maxBccDisLen, len(vals[7]))
            # if vals[14] is not None:
            #     maxAttachLen = max(maxAttachLen, len(vals[14]))

            try:
                cursor.execute(insertMail, vals)
                cursor.execute(insertUserMail)

            except Exception as e:
                print(e)

            if count % 20 == 0:
                conn.commit()
            count += 1
    conn.commit()

    print("legal record count in " + filename + ": " + str(count))
    # print("max fromaddress: " + str(maxFromLen))
    # print("max todisplay: %s" % str(maxToDisLen))
    # print("max toaddress: " + str(maxToLen))
    # print("max cc display: %s" % str(maxCcDisLen))
    # print("max ccaddress: " + str(maxCCLen))
    # print("max bccaddress: " + str(maxBccLen))
    # print(("max subject: %s" % maxSubLen))
    # print("max bcc display : %s" % maxBccDisLen)
    # print("max attachment: %s" % maxAttachLen)


def buildInsertMailSql(numfields):
    """
    Create a query string with the given table name and the right
    number of format placeholders.

    example:
    >>> buildInsertCmd("foo", 3)
    'insert into foo values (%s, %s, %s)'
    """
    assert (numfields > 0)
    placeholders = (numfields - 1) * "%s, " + "%s"
    query = "insert into t_mail (" \
            "subject, " \
            "fromdisplay, " \
            "fromaddress, " \
            "todisplay, " \
            "toaddress, " \
            "ccdisplay, " \
            "ccaddress, " \
            "bccdisplay, " \
            "bccaddress, " \
            "creatorname, " \
            "importance, " \
            "datesent, " \
            "datereceive, " \
            "size, " \
            "attachmentnames) " + \
            (" values (%s)" % placeholders)
    return query


if __name__ == '__main__':
    # commandline execution

    # args = sys.argv[1:]
    # if (len(args) < 5):
    #     print('error: arguments: user \"password\" db table csvfile')
    #     sys.exit(1)

    main()
