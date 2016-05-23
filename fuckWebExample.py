import csv
import os
import sys
import codecs

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
        break

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
    count = 1
    """
    insert mail info, then add a new record in relation table t_user_mail
    """
    for line in f:
        # print(len(line))
        if len(line) > 0:
            vals = nullify(line)
            # print(vals)
            try:
                cursor.execute(insertMail, vals)
                cursor.execute(insertUserMail)

            except Exception:
                print(Exception)

            if count % 20 == 0:
                conn.commit()
            count += 1

    conn.commit()

    print(count)


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
