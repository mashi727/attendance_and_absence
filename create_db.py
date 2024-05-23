import sqlite3

dbname = 'idm_and_name.db'
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# personsというtableを作成してみる
# 大文字部はSQL文。小文字でも問題ない。
cur.execute(
    'CREATE TABLE persons(idm STRING, name STRING)')


conn.commit()
cur.execute(
    'INSERT INTO persons values("0139727fffb7e6f5", "増野")')


# データベースへコミット。これで変更が反映される。
conn.commit()
conn.close()
