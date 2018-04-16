from pymongo import MongoClient,errors
class sv_mongo():
        def __init__(self,db,collection):
                self.client = MongoClient()
                self.Client = self.client[db]
                self.db = self.Client[collection]

        def push_content(self,aid,title,message):
                try:
                        result = self.db.insert({'aid':aid,'title':title,'message':message})
                        print('插入评论成功')
                except Exception as e:
                        print(e)


