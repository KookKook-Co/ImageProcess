import psycopg2
from Image import Image

# DB_URI = 'postgres://postgres:password@128.199.211.41:5432/postgres'
DB_URI = 'postgres://user1:password@tested.c8atso85ojy4.ap-southeast-1.rds.amazonaws.com:5432/chicken_farm'

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(DB_URI)
            self.cursor = self.conn.cursor()
        except:
            self.conn = None
            self.cursor = None
    
    def getCamera(self):
        # return list of cid
        try:
            query = 'SELECT DISTINCT ON ("cid") "cid"\
                    FROM "Image"\
                    WHERE "amountDead" is NULL'
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            data = [e[0] for e in data]
            return data
        except Exception as e:
            return str(e)
    
    def getImage(self, cid=None):
        # return all image links or links of cid, hid that amountDead is NULL
        try:
            extra = ''
            if cid is not None:
                cid = "\'" + str(cid) + "\'"
                extra = f'AND "cid" = {cid}'
            query = f'SELECT "cid", "timestamp", "url", "amountDead"\
                    FROM "Image"\
                    WHERE "amountDead" = 0\
                    {extra}\
                    ORDER BY "timestamp";'
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            data = [Image(e) for e in data]
            return data
        except Exception as e:
            return str(e)
    
    def updateAmountDead(self, image):
        try:
            cid = "\'" + str(image.cid) + "\'"
            update = f'UPDATE "Image"\
                    SET "amountDead" = {image.amountDead}\
                    WHERE cid = {cid} AND timestamp = \'{image.timestamp}\';'
            self.cursor.execute(update)
            self.conn.commit()
        except Exception as e:
            return str(e)

db = Database()
a = db.getImage(cid='1')
for e in a:
    print(e)
# for e in data:
#     e.setAmountDead(11)
#     db.updateAmountDead(e)
#     print(e)