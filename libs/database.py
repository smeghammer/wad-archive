from pymongo import MongoClient

class WadArchiveDatabase():
    
    def __init__(self,settings):
        ''' instantiate the database object '''
        print('init database')
        print(settings)
        self.db = MongoClient(host=''.join([settings['metadata_database_address'],':',str(settings['metadata_database_port'])]))[settings['metadata_database_name']]
    
    def getFilecount(self,filter):
        return self.db['filenames'].count_documents(filter)
    
    def getPagedFilenames(self, page_size,page_num, filter):
        filter = filter
        pagination_data = {
            'item_count' : self.getFilecount(filter),
            'page_num' : page_num,
            'page_size' : page_size,
            'page_data' : list(self.db['filenames'].find(filter).sort('_id',1).skip(page_size * page_num).limit(page_size))
            }
        return pagination_data
    
    ''' {'_id': '0007b6fb74d66c33dff5a0c4de73642a5c8d3899', 'count': 1, 'filenames': ['atf-beta3.wad']} '''
    def getFilename(self,uuid):
        print(uuid)
        res = dict(self.db['filenames'].find_one({'_id':uuid}))
        if res['count']:
            return res['filenames'][0]
        return 'No filename found!'