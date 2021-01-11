from urllib.request import Request, urlopen
import ssl
from bs4 import BeautifulSoup
import sqlite3



# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

con = sqlite3.connect('corona.sqlite3')
cur = con.cursor()
cur.execute("DROP TABLE main")
cur.execute("DROP TABLE continents")
cur.execute('''CREATE TABLE IF NOT EXISTS main(
             country TEXT UNIQUE ,
             totalcase TEXT ,
             newcase TEXT ,
             newdeath TEXT ,
             recovered TEXT ,
             active INTEGER ,
             conti INTEGER  )''')
cur.execute("CREATE TABLE IF NOT EXISTS continents ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)")

data = Request('https://www.worldometers.info/coronavirus/',  headers={'User-Agent': 'XYZ/3.0'} )
webpage = urlopen(data, context=ctx).read()
soup = BeautifulSoup(webpage, "html.parser")
tags = soup('tr')
for i in range(1,230):
    subtags = tags[i]('td')
    count = 0
    subtotal = ""
    subnew = ""
    subname = ""
    subdeath = ""
    subrecovered = ""
    subactive = ""
    subcont = ""
    # try:
    #     subname = subtags[15].contents[0]
    #     subtotal = subtags[2].contents[0]
    #     subnew = subtags[3].contents[0]
    #     subdeath = subtags[4].contents[0]
    #     subrecovered = subtags[6].contents[0]
    #     subactive = subtags[8].contents[0]
    #     print(subname, subtotal, subnew, subdeath, subrecovered, subactive)
    # except:
    #     subname = subtags[1].contents[0]
    #     subtotal = subtags[2].contents[0]
    #     subnew = subtags[3].contents[0]
    #     subdeath = subtags[4].contents[0]
    #     subrecovered = subtags[6].contents[0]
    #     subactive = subtags[8].contents[0]
    #     print(subname, subtotal, subnew, subdeath, subrecovered, subactive)
    for j in subtags:
        x = j('a')
        if count == 1 and x != []:
            subname = j('a')[0].contents[0]
        if count == 2:
            subtotal = j.contents[0]
        if count == 3 and j.contents != []:
            subnew = j.contents[0]
        elif count == 3 and j.contents == []:
            subnew = "Null"
        if count == 4 and j.contents != []:
            subdeath = j.contents[0]
        elif count == 4 and j.contents == []:
            subdeath = "Null"
        if count == 6 and j.contents != []:
            subrecovered = j.contents[0]
        elif count == 6 and j.contents == []:
            subrecovered = "Null"
        if count == 8 and j.contents != []:
            subactive = j.contents[0]
        elif count == 8 and j.contents == []:
            subactive = "Null"
        if count == 15 and j.contents != []:
            subcont = j.contents[0]
            if subcont == "All":
                subname = "World"
            if subname == "":
                subname = subcont


        count = count + 1
    cur.execute("INSERT OR IGNORE INTO continents(name) VALUES(?)", (subcont,))
    cur.execute("SELECT id FROM continents WHERE name = ?", (subcont,))
    cunt = cur.fetchone()
    cunts = int(cunt[0])
    cur.execute("INSERT OR IGNORE INTO main(country,totalcase,newcase, newdeath, recovered, active, conti ) VALUES (?,?,?,?,?,?,?) ", (subname, subtotal, subnew, subdeath, subrecovered, subactive,cunts ))
    print(subname, subcont, "subtotal ", subtotal, "subnew", subnew, "subdeath", subdeath,"subrecovered", subrecovered,"subactive", subactive  )
    con.commit()
    print("*************************************\n")
cur.execute('''SELECT main.country,main.totalcase,main.newcase,main.newdeath,main.active,main.recovered, continents.name 
 FROM main JOIN continents ON main.conti = continents.id''')
con.commit()
cur.close()

