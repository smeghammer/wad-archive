from pymongo import MongoClient

class WadArchiveDatabase():
    
    def __init__(self,settings):
        ''' instantiate the database object '''
        self.db = MongoClient(host=''.join([settings['metadata_database_address'],':',str(settings['metadata_database_port'])]))[settings['metadata_database_name']]
    
    def getFilecount(self,filter):
        return self.db['filenames'].count_documents(filter)
    
    def getPagedFilenames(self, page_size,page_num, filter):
        ''' paged '''
        filter = filter
        pagination_data = {
            'item_count' : self.getFilecount(filter),
            'page_num' : page_num,
            'page_size' : page_size,
            'page_data' : list(self.db['filenames'].find(filter).sort('_id',1).skip(page_size * page_num).limit(page_size))
            }
        return pagination_data
    
    def getFilename(self,uuid):
        res = dict(self.db['filenames'].find_one({'_id':uuid}))
        if res['count']:
            return res['filenames'][0]
        return None
    
    def readme(self,uuid):
        try:
            res = dict(
                self.db['readmes'].find_one({'_id':uuid}))
            if res['count']:
                return res['readmes'][0]
        except Exception as ex:
            return None