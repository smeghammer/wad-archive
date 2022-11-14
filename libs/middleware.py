import io
import os
import base64
from os import path
import gzip
from libs.database import WadArchiveDatabase

class Middleware():
    
    def __init__(self,settings):
        self.db = WadArchiveDatabase(settings)
        self.path_to_archives = settings['archive_root_path']
        
    def filecount(self):
        return self.db.getFilecount()
    
    def files(self,page_size=50,page_num=0, filter=None):
        # If we find filter, build regex to search against filename[0]
        f = {}
        if filter:
            f = {'filenames.0':{'$regex':filter}}
        return self.db.getPagedFilenames(page_size,page_num, f)
    
    def details(self,guid):
        details = {
            'record_identifier':guid,
            'record_filename':self.db.getFilename(guid),
            'record_path':self.path(guid),
            'record_readme':self.readme(guid),
            'record_graphics' : self.b64imagelist(guid, 'GRAPHICS'),
            'record_maps' : self.b64imagelist(guid, 'MAPS'),
            'record_screenshots' : self.b64imagelist(guid, 'SCREENSHOTS')
        }
        return details
    
    def file(self,guid,type='wad'):
        ''' I can get teh type from the filenames extension '''
        print('in middleware.file, ',guid)
        file_name = self.db.getFilename(guid)
        # # open the folder conaining the archives
        file_dir = guid[0:2:1]
        file_name_prefix = guid[2:]
        # archives_path = path.join(self.path_to_archives,guid[0:2:1],guid[2:])
        archives_path = self.path(guid)
        # open the zipped file (folder/folder/fname). need to test for .wad.gz and .pk3.gz
        try_pk3 = path.join(archives_path, ''.join([file_dir, file_name_prefix, '.pk3.gz']))
        try_wad =  path.join(archives_path, ''.join([file_dir, file_name_prefix, '.wad.gz']))
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

        return None, None
    
    def b64imagelist(self,guid,dir):
        ''' return a list of base64 encoded files (assume .pngs only) in the specified directory '''
        _out = {}
        #build path
        filepath = path.join(self.path(guid),dir)
        _out['path'] = filepath
        _out['data'] = []
        #test for files in path
        try:
            _files = os.listdir(filepath)
            for _f in _files:
                print('trying ',os.path.join(filepath,_f))
                with open(os.path.join(filepath,_f),'rb') as image:
                    if image:
    
                        _img = image.read()
                        _b64 = base64.b64encode(_img)
                        _decoded = _b64.decode('ascii')
                        print('B64 encoded: ',_b64.decode('ascii'))
                        _out['data'].append(
                            {'file':_f,
                             'b64': _decoded
                        # base64.b64encode(  image.read() ).decode('ascii')
                             }
                        )
                    else:
                        print(os.path.join(filepath,_f),' not opened!')
        except FileNotFoundError as ex:
            print('dir not found')
            return {}
        #return b64 encoded strings for each as a list
        return _out
    
    def readme(self,guid):
        return self.db.readme(guid)
    
    def path(self,guid):
        file_name = self.db.getFilename(guid)
        file_dir = guid[0:2:1]
        file_name_prefix = guid[2:]
        archives_path = path.join(self.path_to_archives,guid[0:2:1],guid[2:])
        return archives_path
    