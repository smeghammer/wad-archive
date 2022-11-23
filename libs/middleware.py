import io
import os
import base64
from os import path
import gzip
import zipfile
from zipfile import ZipFile, Path
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
            'record_archive_path':self.relative_path(guid).replace('\\','/'),
            'record_readme':self.readme(guid),
            'record_graphics' : self.b64imagelist_archived(guid, 'GRAPHICS'),
            'record_maps' : self.b64imagelist_archived(guid, 'MAPS'),
            'record_screenshots' : self.b64imagelist_archived(guid, 'SCREENSHOTS')
        }
        return details
    
    #  un-gzip the archived file. Needed when returing a file directly form the zipped archiove:
    def get_uncompressed_file(self,compressed_file):
        return_file = compressed_file
        data = gzip.decompress(return_file.read())
        outfile = io.BytesIO(data)
        return outfile
    
    def file(self,guid,type='wad'):
        ''' I can get the type from the filenames extension '''
        ''' Replace this loading from directory to loading from a zip archive,
        so we don't need to unzip everything first '''
        file_name = self.db.getFilename(guid)
        file_dir = guid[0:2:1]
        file_name_prefix = guid[2:]
        archives_path = self.path(guid)
        
        ''' the zip archive is also the directory name, with a .zip extension 
        with zipfile.ZipFile("sample.zip", mode="r") as archive:
        OK this works, but I need to adapt the image/readme bits to do the same thing:
        '''
        try:
            relative_path = self.relative_path(guid)
            with ZipFile(''.join([path.join(self.path_to_archives,file_dir),'.zip']), mode='r') as archive:
                # if the archive opened OK, proceed tgo determine the filepath to retrieve:
                # open the zipped file (folder/folder/fname). need to test for .wad.gz and .pk3.gz
                try_relative_pk3 = (path.join(relative_path,''.join([file_dir, file_name_prefix, '.pk3.gz']))).replace('\\','/')
                try_relative_wad = path.join(relative_path,''.join([file_dir, file_name_prefix, '.wad.gz'])).replace('\\','/')              
        
                try:
                    with archive.open( try_relative_pk3, mode='r'  ) as returnfile:
                        return self.get_uncompressed_file(returnfile), file_name 
                except:
                    try:
                        with archive.open( try_relative_wad, mode='r'    ) as returnfile:
                            return self.get_uncompressed_file(returnfile), file_name
                    except Exception as ex:
                        print('failed')

        except FileNotFoundError as ex:
            # throw error up stack here!!
            print('warning: ', str(ex))
        return None, None
    
    def b64imagelist_archived(self,guid,dir):
        _out = {}
        _out['path'] = dir
        _out['data'] = []
        file_dir = guid[0:2:1]
        record = guid[2:]
        
        try:
            with ZipFile(''.join([path.join(self.path_to_archives,file_dir),'.zip']), mode='r') as archive:
                image_key_prefix = file_dir + '/' + record + '/' + dir + '/'
                contents = archive.infolist()
                namelist = archive.namelist()
                recordlist = []
                for entry in namelist:
                    # append to working list if archive path key matches a file
                    if image_key_prefix in entry and len(entry) > len(image_key_prefix):
                        recordlist.append(archive.getinfo(entry))
    
                for record in recordlist:
                    with archive.open( record, mode='r'  ) as returnfile:
                        if returnfile:
                            _img = returnfile.read()
                            _b64 = base64.b64encode(_img)
                            _decoded = _b64.decode('ascii')
                            _out['data'].append({'file':record.filename.split('/')[-1], 'b64': _decoded  }  )
        except FileNotFoundException as ex:
            _out['data'] = "error" 
        return _out
            # now list contents at this location:

    def readme(self,guid):
        return self.db.readme(guid)
    
    def path(self,guid):
        ''' build full filepath to uncompressed archive directory'''
        file_name = self.db.getFilename(guid)
        file_dir = guid[0:2:1]
        file_name_prefix = guid[2:]
        archives_path = path.join(self.path_to_archives,guid[0:2:1],guid[2:])
        return archives_path
    
    def relative_path(self,guid):
        ''' build relative path for zip archive contents file retrieval '''
        file_name = self.db.getFilename(guid)
        file_dir = guid[0:2:1]
        file_name_prefix = guid[2:]
        zip_archives_path = path.join(guid[0:2:1],guid[2:])
        return zip_archives_path
    