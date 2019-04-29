#:::::::::::::::::::::::::
#::
#:: ProjectDependencies/download.py
#::_______________________
#::
#:: Author: Clement BERTHAUD
#::
#:: MIT License
#:: Copyright (c) 2018 ProjectDependencies - Clément BERTHAUD
#::
#:: Permission is hereby granted, free of charge, to any person obtaining a copy
#:: of this software and associated documentation files (the "Software"), to deal
#:: in the Software without restriction, including without limitation the rights
#:: to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#:: copies of the Software, and to permit persons to whom the Software is
#:: furnished to do so, subject to the following conditions:
#::
#:: The above copyright notice and this permission notice shall be included in all
#:: copies or substantial portions of the Software.
#::
#:: THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#:: IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#:: FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#:: AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#:: LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#:: OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#:: SOFTWARE.
#::
#:::::::::::::::::::::::::
import ProjectDependencies.utils
import urllib.request as urlreq
import os, io
import shutil
import tarfile
import ssl
from colorama import Fore, Back, Style
from colorama import init as init_colorama
init_colorama()

def command( iArgs, iFiles, iConfig, iDirs, iKeys ):
    ProjectDependencies.utils.notify_ignore_args( iArgs )

    ProjectDependencies.utils.smart_gather_wtree_resolve_all_hash_inconsistencies( iDirs, iFiles )

    # Bake utility strings from gathered information
    src = iConfig["remote"] + iConfig["file"]
    dst = iDirs["tmp"]      + iConfig["file"]

    # Create tmp dir
    ProjectDependencies.utils.mkdirtree( iDirs["tmp"] )

    # Bake request
    resp        = urlreq.urlopen( src, context=ssl._create_unverified_context() )
    length      = resp.headers['content-length']
    blocksize   = 1000000 # arbitrary size

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
            print( "Downloading file '{0}' from remote '{1}': {2:2.1%}".format( iConfig["file"], iConfig["remote"], size / length ), end="\r" )
    print("")

    # Dump file, write binary
    handle = open( dst, "wb" )
    handle.write( buffer.getvalue() )
    handle.close()

    # Extract tar.gz
    print( "Extracting downloaded archive")
    tar = tarfile.open( dst, 'r:gz' )
    tar.extractall( iDirs["tmp"] )
    tar.close()

    # Install
    index_list          = ProjectDependencies.utils.gather_list_with_hash( iFiles["index"] )
    total               = len( index_list )
    count               = 0
    bFoundMissing       = False
    missing_list        = []
    num_installed_files = 0

    for entry in index_list:
        tmp_file        = iDirs["tmp"]  + entry["file"]
        install_file    = iDirs["root"] + entry["file"]

        if not os.path.exists( tmp_file ):
            # Error, file indexed but not in dep
            bFoundMissing = True
            missing_list.append( entry["file"] )
        else:
            # Cool: we can install file, prepare its dir and copy
            num_installed_files += 1
            dstdir = os.path.dirname( os.path.realpath( install_file ) )
            ProjectDependencies.utils.mkdirtree( dstdir )
            shutil.copyfile( tmp_file, install_file )
        count += 1
        if total: # Avoid divide by 0
            # Print feedback
            print( "Installing files {:2.1%}".format( count / total ), end="\r" )
    print( "" )

    # Report errors
    if bFoundMissing:
        print( "warning: some indexed entries are missing from downloaded dependencies" )
        print( Fore.RED )
        for entry in missing_list:
            print( ProjectDependencies.utils.make_offset( 4 ) + "missing from dependency: " + entry )
        print( Style.RESET_ALL )

    # Clean behin, delete tmp
    shutil.rmtree( iDirs["tmp"] )

    # Report install
    print( "Done. Installed {0} files".format( num_installed_files ) )
