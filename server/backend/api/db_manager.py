import sys
import os
import fdb
from fastapi import HTTPException


DATABASE_SERVER = os.getenv('DB_SERVER')
DATABASE_PORT = int(os.getenv('DB_PORT'))
DATABASE_PATH = os.getenv('DB_PATH')
DATABASE_USER = "User"
DATABASE_PASSWORD = "123456"


async def open_database():
    con = fdb.connect(host=DATABASE_SERVER, port=DATABASE_PORT, database=DATABASE_PATH, user=DATABASE_USER,
                      password=DATABASE_PASSWORD)
    return con


async def get_language(lang: str, section: str, key: str):
    try:
        try:
            con = await open_database()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error connecting to database: " + str(e))

        if not con:
            raise HTTPException(status_code=404, detail="Database connection error")

        cur = con.cursor()
        sql = "Select " + lang.upper() + " from T_LANGUAGE where (SECTION='" + section.upper() + "') and (KEYWORD='"\
              + key.upper() + "')"
        cur.execute(sql)
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Nothing found for language:" + lang + ", Section:" + section +
                                                        ", Key:" + key)
    finally:
        if con:
            con.close()

    return {"section": section, "key": key, "value": row[0]}


async def set_language(lang: str, section: str, key: str, value: str):
    try:
        try:
            con = await open_database()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error connecting to database: " + str(e))

        cur = con.cursor()
        sql = "Select " + lang.upper() + " from T_LANGUAGE where (SECTION='" + section.upper() + "') and (KEYWORD='"\
              + key.upper() + "')"
        cur.execute(sql)
        row = cur.fetchone()
        if not row:
            sql = "insert into T_LANGUAGE(SECTION, KEYWORD, CZE, ENG, FRE, GER, ITA, NED, POL, RUS, SLO, SPA) values ('" + section.upper() + "', '" + key.upper() + "', '', '', '', '', '', '', '', '', '', '')"
            cur.execute(sql)
            con.commit()
            sql = "update T_LANGUAGE set " + lang.upper() + "='" + value + "' where SECTION='" + section.upper() + "' and KEYWORD='" + key.upper() + "'"
            cur.execute(sql)
            con.commit()
        else:
            sql = "update T_LANGUAGE set " + lang.upper() + "='" + value + "' where SECTION='" + section.upper() + "' and KEYWORD='" + key.upper() + "'"
            cur.execute(sql)
            con.commit()
            cur.close()
    finally:
        if con:
            con.close()

