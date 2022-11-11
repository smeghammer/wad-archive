import io
import os
from os import path
import gzip
from libs.database import WadArchiveDatabase

class Middleware():
    
    def __init__(self,settings):
        self.db = WadArchiveDatabase(settings)
        self.path_to_archives = 'E:\wad-archive dump\DATA'
        
    def filecount(self):
        return self.db.getFilecount()
    
    def files(self,page_size=50,page_num=0, filter=None):
        # If we find filter, build regex to search against filename[0]
        f = {}
        if filter:
            f = {'filenames.0':{'$regex':filter}}
        return self.db.getPagedFilenames(page_size,page_num, f)
    
    
    def file(self,guid,type='wad'):
        ''' I can get teh type from the filenames extension '''
        print(guid)
        file_name = self.db.getFilename(guid)
        # open the folder conaining the archives
        archives_path = path.join(self.path_to_archives,guid[0:2:1],guid[2:])
        
        # open the zipped file (folder/folder/fname). need to test for .wad.gz and .pk3.gz
        try_pk3 = path.join(archives_path, ''.join([guid[0:2:1], guid[2:], '.pk3.gz']))
        try_wad =  path.join(archives_path, ''.join([guid[0:2:1], guid[2:], '.wad.gz']))
        try_zip =  path.join(archives_path, ''.join([guid[0:2:1], guid[2:], '.zip']))
        # return try_pk3
        try:
            with gzip.open(path.join(archives_path,try_pk3),mode='rb') as file:
                if file:
                    print('pk3 file found')
                    return_file = file
                    # uncompress it first:
                    uncompressed_return_file = return_file.read()
                    outfile = io.BytesIO(uncompressed_return_file)
                    return outfile, file_name
        except FileNotFoundError as err:
            print(err," trying for .WAD...")
            
            try:
                with gzip.open(path.join(archives_path,try_wad),mode='rb') as file:
                    if file:
                        print('wad file found')
                        return_file = file
                        # uncompress it first:
                        uncompressed_return_file = return_file.read()
                        outfile = io.BytesIO(uncompressed_return_file)
                        return outfile, file_name
            except FileNotFoundError as err:
                print(err," giving up..")
                
        
        # if file:
        #     return_file = file
        #     # uncompress it first:
        #     uncompressed_return_file = return_file.read()
        #     outfile = io.BytesIO(uncompressed_return_file)
        #     return outfile, file_name
        return None, None
    
    def _get_dir_name(self,guid):
        return guid[0,2,1]