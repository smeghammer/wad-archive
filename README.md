# wad-archive
Python wrapper for WAD Archive internet archive dump

## branch 'zipped archives'
Contains code for accessing data from the double-zipped large archive files. I don't really want to maintain code that both handles the unzipped and the zipped archive. I will branch off from master again to have a clean branch that contains code that handles the UNZIPPED large archive

## Summary
A read-only wrapper for the WAD Archive data dump from 2022. Details of this can be found in [this Doomworld thread](https://www.doomworld.com/forum/topic/130650-closing-wad-archive/).

TODO: 
 - convert list to navigation, that opens apage displaying map, screenshots and a download link, and readme/IDGames readme if found.
 - in LH list, highlight the selected entry
 - catch and alert if archive is not found
 - TEST UNC path!!

# venv

  - `> source bin/activate`
  - `> deactivate`


  ## NFS
  https://github.com/sahlberg/libnfs-python - this one?
  https://pypi.org/project/pyNfsClient/