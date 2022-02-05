import random
import string
import os.path
import getopt
import sys
import jsonpickle
from model.contact import Contact


try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of contacts", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n = 5
f = "data/contacts.json"

for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


testdata = [Contact(firstname="", middlename="", lastname="",
                    nickname="", title="",
                    company="", address="",
                    home="", mobile="", work="", phone2="",
                    email="", email2="", email3="")] + [
               Contact(firstname=random_string("firstname", 15), middlename=random_string("middlename", 20),
                       lastname=random_string("lastname", 15),
                       nickname=random_string("nick", 25), title=random_string("title", 15),
                       company=random_string("company", 15), address=random_string("address", 20),
                       home=random_string("phone", 15), mobile=random_string("mobile", 15),
                       work=random_string("work", 15), phone2=random_string("phone2", 15),
                       email=random_string("email", 20), email2=random_string("email2", 25),
                       email3=random_string("email3", 15))
               for i in range(n)

           ]

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)


with open(file, "w") as out:
    jsonpickle.set_encoder_options("json", indent=2)
    out.write(jsonpickle.encode(testdata))