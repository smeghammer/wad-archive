settings = {
    # for UNC paths on Ubuntu, please see 
    # https://linuxize.com/post/how-to-mount-an-nfs-share-in-linux/
    'archive_root_path' : '/var/wad-archive-mount/DATA',
    'records_per_page' : 40,
    'metadata_database_name' : 'wadarchive',
    'metadata_database_address' : '192.168.1.115',
    'metadata_database_port' : 27017
}

# nfs://192.168.1.20/mnt/USB/USB1_c2/wad-archive-dump

# Manual:
# sudo mount -t nfs 192.168.1.20://mnt/USB/USB1_c2/wad-archive-dump /var/wad-archive-mount
