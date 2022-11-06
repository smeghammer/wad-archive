from pymongo import MongoClient


class WadArchiveDatabase():
    
    def __init__(self):
        ''' instantiate the database object '''
        print('init database')
        self.db = MongoClient().wadarchive
    
    def getFilecount(self):
        return self.db['filenames'].count_documents({})
    
    # def getFilenames(self):
    #     return self.db['filenames'].find({}).sort('_id',1)
    
    def getPagedFilenames(self, page_size,page_num):
        pagination_data = {
            'item_count' : self.getFilecount(),
            'page_num' : page_num,
            'page_size' : page_size,
            'page_data' : list(self.db['filenames'].find({}).sort('_id',1).skip(page_size * page_num).limit(page_size))
            }
        return pagination_data
    
    ''' {'_id': '0007b6fb74d66c33dff5a0c4de73642a5c8d3899', 'count': 1, 'filenames': ['atf-beta3.wad']} '''
    def getFilename(self,uuid):
        print(uuid)
        res = dict(self.db['filenames'].find_one({'_id':uuid}))
        if res['count']:
            return res['filenames'][0]
        return 'No filename found!'