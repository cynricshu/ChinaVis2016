import codecs
import re

excludeSet = {"", ":", "?", ",", "{", "}", "(", ")", "[", "]", "<", ">", "|",
              "!", "...", ";", "#", "&", "+", ".", "\"", "@", "'", "`", "=",
              "the", "a", "or", "and", "for", "in", "on", "to", "is", "was",
              "with", "by", "at", "about", "under"
              }
specialSet = {"¨", "¤", "¬", "¯", "¡", "®", "¦"}

regexList = {
    re.compile("<<#.*#>>"): "",
    re.compile("\[.*\]"): "",
    # re.compile("\s+/+\s+|/+\s+|/+$|\s+/+"): " ",
    # re.compile("\s+-+\s+|-+\s+|-+$|\s+-+"): " ",
    # re.compile("\s+_+\s+|_+\s+|_+$|\s+_+"): " ",
    # re.compile("\s+\.+\s+|\.+\s+|\.+$|\s+\.+"): " ",
}

nltkPattern = r"""(?x)                   # set flag to allow verbose regexps
    (?:[A-Za-z]\.)+           # abbreviations, e.g. U.S.A.
    |\d+(?:\.\d+)+%?       # numbers, incl. currency and percentages
    |\w+(?:[-']\w+)*       # words w/ optional internal hyphens/apostrophe
    |\.\.\.                # ellipsis
    |(?:[.,;"'?():-_`])    # special characters with meanings
  """

keywords = ["Re: ", "RE: ", "Fwd: ", "FWD: ", "R: ", "I: ", "FW: ", "Fw: ", "i: "]


def loadEmployeeSet():
    """
    :return: dict
    """
    nameDict = dict()
    f = codecs.open("data/internal_staff.txt", "r", "iso-8859-1")
    for line in f:
        data = str(line)[0:-2].split(",")
        if len(data) == 1:
            nameDict[data[0].lower()] = data[0].lower()
            nameDict[data[0].lower() + "@hackingteam.it"] = data[0].lower()
        else:
            nameDict[data[0].lower()] = data[0].lower()
            nameDict[data[0].lower() + "@hackingteam.it"] = data[0].lower()
            nameDict[data[1].lower()] = data[0].lower()
            nameDict[data[1].lower() + "@hackingteam.it"] = data[0].lower()

    print(len(nameDict))
    # for item in nameSet:
    #     print(item)
    f.close()
    return nameDict


def isInternal(display, address, nameDict):
    if not address.strip().startswith("/O=HACKINGTEAM/OU"):
        display = display.strip().lower()
        if display not in nameDict and "@hackingteam.it" not in display:
            return False
    return True
