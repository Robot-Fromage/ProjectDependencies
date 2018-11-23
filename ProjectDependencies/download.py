#:::::::::::::::::::::::::
#::
#:: OdysseyDependencies/download.py
#::_______________________
#::
#:: Author: Clement BERTHAUD
#::
#:: This piece of script is licensed under the WTFPL licence:
#::
#::  DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#::                    Version 2, December 2004
#::
#:: Copyright (C) 2018 - End of the Universe, Praxinos <code@praxinos.coop>
#::
#:: Everyone is permitted to copy and distribute verbatim or modified 
#:: copies of this license document, and changing it is allowed as long 
#:: as the name is changed. 
#::
#::            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#::   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 
#::
#:: 0. You just DO WHAT THE FUCK YOU WANT TO.
#::
#:::::::::::::::::::::::::
import OdysseyDependencies.utils
import urllib.request as urlreq
import os, io
import shutil
import tarfile
from colorama import Fore, Back, Style
from colorama import init as init_colorama
init_colorama()

def command( iArgs, iConfig, iDirs, iFiles ):
    OdysseyDependencies.utils.notify_ignore_args( iArgs )

    # Bake utility strings from gathered information
    src = iConfig["url"] + iConfig["file"]
    dst = iDirs["tmp"] + iConfig["file"]
    OdysseyDependencies.utils.check_create_dir( iDirs["tmp"] )

    # Bake request
    resp = urlreq.urlopen(src)
    length = resp.headers['content-length']
    blocksize = 1000000 # arbitrary size

    if length:
        length = int(length)
        blocksize = max( 4096, length//100 )

    # Async req dl
    buffer = io.BytesIO()
    size = 0
    while True:
        block = resp.read( blocksize )
        if not block:
            break
        buffer.write( block )
        size += len( block )
        if length: # Avoid divide by 0
            # Print feedback
            print( "Downloading file '{0}' from remote '{1}': {2:2.1%}".format( iConfig["file"], iConfig["url"], size / length ), end="\r" )
    print("")

    # Dump to file, write binary
    handle = open( dst, "wb" )
    handle.write( buffer.getvalue() )
    handle.close()

    # Extract tar.gz
    print( "Extracting downloaded archive")
    tar = tarfile.open( dst, 'r:gz' )
    tar.extractall( iDirs["tmp"] )
    tar.close()
    
    # Install
    index_list = OdysseyDependencies.utils.gather_list( iFiles["index"] )
    total = len( index_list )
    count = 0
    bFoundMissing = False
    missing_list = []
    num_installed_files = 0
    for entry in index_list:
        tmp_file = iDirs["tmp"] + entry
        install_file = iDirs["root"] + entry
        if not os.path.exists( tmp_file ):
            bFoundMissing = True
            missing_list.append( entry )
        else:
            num_installed_files += 1
            shutil.copyfile( tmp_file, install_file )

        count += 1
        if total:
            print( "Installing files {:2.1%}".format( count / total ), end="\r" )
    print( "" )

    if bFoundMissing:
        print( "warning: indexed entries are missing from downloaded dependencies")
        print( Fore.RED )
        for entry in missing_list:
            print( OdysseyDependencies.utils.make_offset( 4 ) + "missing from dependency: " + entry )
        print( Style.RESET_ALL )

    
    shutil.rmtree( iDirs["tmp"] )

    print( "Done. Installed {0} files".format( num_installed_files ) )
    