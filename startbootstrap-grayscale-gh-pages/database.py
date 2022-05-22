from distutils.util import execute
import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''create table QA (
    qid int,
    uid int,
    ques varchar(100),
    ans varchar(50),
    star boolean
    )''')
conn.execute("insert into QA (qid, uid, ques, ans, star)\
            values(1, 1, '死的人是誰？', '約瑟夫', true)")
conn.execute("insert into QA (qid, uid, ques, ans, star)\
            values(2, 1, '真的存在鬼嗎？', '不假', false)")

conn.execute('''create table Feedback (
    ftype varchar(50),
    ftext varchar(200),
    uid int
    )''')
            
result = conn.execute("select * from QA")
for row in result:
    print("{}, {}, {}, {}, {}".format(row[0], row[1], row[2], row[3], row[4]))
conn.commit()