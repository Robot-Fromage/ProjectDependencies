#:::::::::::::::::::::::::
#::
#:: ProjectDependencies/push.py
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
import os
import shutil
import tarfile
import ftplib
import getpass
from colorama import Fore, Back, Style
from colorama import init as init_colorama
init_colorama()

def command( iArgs, iFiles, iConfig, iDirs, iKeys ):
    ProjectDependencies.utils.notify_ignore_args( iArgs )

    # Gather track & ignore & git track
    track_list          = ProjectDependencies.utils.gather_list( iFiles["track"] )
    ignore_list         = ProjectDependencies.utils.gather_list( iFiles["ignore"] )
    git_tracked_files   = ProjectDependencies.utils.gather_git_tracked_files( iDirs["root"] )
    # Concatenate ignore with git tracked
    ignore_list.extend( git_tracked_files )

    # Gather working tree, index and stage
    working_tree_list_with_hash = ProjectDependencies.utils.gather_working_tree_list_with_hash( iDirs["root"], track_list, ignore_list )
    stage_list_with_hash        = ProjectDependencies.utils.gather_list_with_hash( iFiles["stage"] )
    index_list_with_hash        = ProjectDependencies.utils.gather_list_with_hash( iFiles["index"] )

    tpr = ProjectDependencies.utils.resolve_inconsistencies( working_tree_list_with_hash, [ stage_list_with_hash, index_list_with_hash ] )
    sorted_working_tree_list_with_hash = tpr[0]
    sorted_stage_list_with_hash = tpr[1][0]
    sorted_index_list_with_hash = tpr[1][1]

    # Write new lists
    ProjectDependencies.utils.update_list_with_hash( iFiles["stage"], sorted_stage_list_with_hash )
    ProjectDependencies.utils.update_list_with_hash( iFiles["index"], sorted_index_list_with_hash )

    # Gather anew
    stage_list_with_hash        = ProjectDependencies.utils.gather_list_with_hash( iFiles["stage"] )
    index_list_with_hash        = ProjectDependencies.utils.gather_list_with_hash( iFiles["index"] )

    # Check for inconsistencies in stage against working directory
    inconsistent_stage_list = []
    bFoundInconsistenciesInStage = False
    for entry in stage_list_with_hash:
        absolute_entry = iDirs["root"] + entry["file"]
        if not os.path.exists( absolute_entry ):
            bFoundInconsistenciesInStage = True
            inconsistent_stage_list.append( entry )

    # Check for inconsistencies in index against working directory
    inconsistent_index_list = []
    bFoundInconsistenciesInIndex = False
    for entry in index_list_with_hash:
        absolute_entry = iDirs["root"] + entry["file"]
        if not os.path.exists( absolute_entry ):
            bFoundInconsistenciesInIndex = True
            inconsistent_index_list.append( entry )

    if bFoundInconsistenciesInStage:
        print( "Inconsistencies were found in stage, the following files do not appear to be part of the working tree:" )
        print( Fore.RED )
        for entry in inconsistent_stage_list:
            print( ProjectDependencies.utils.make_offset( 8 ) + "missing: " + entry["file"] )
        print( Style.RESET_ALL )
        print( ProjectDependencies.utils.make_offset( 4 ) + "Remove them using ProjectDependencies reset <path> before pushing.")

    if bFoundInconsistenciesInIndex:
        print( "Inconsistencies were found in index, the following files do not appear to be part of the working tree:" )
        print( Fore.RED )
        for entry in inconsistent_index_list:
            print( ProjectDependencies.utils.make_offset( 8 ) + "missing: " + entry["file"] )
        print( Style.RESET_ALL )
        print( ProjectDependencies.utils.make_offset( 4 ) + "Solve this by checkout with git or download again or remove them from index manually." )

    # Move stage to index
    for entry in stage_list_with_hash:
        print( ProjectDependencies.utils.make_offset( 8 ) + "indexing: " + entry["file"] )
        index_list_with_hash.append( entry )
    
    # Write new stage to disk
    with open( iFiles["index"], 'w') as f:
        for item in index_list_with_hash:
            strw = item["hash"] + ";" + item["file"]
            f.write("%s\n" % strw)

    # Erase stage
    open( iFiles["stage"], 'w').close()

    # Gathering dependencies in TMP
    if os.path.exists( iDirs["tmp"] ):
        shutil.rmtree( iDirs["tmp"], ignore_errors=True )

    while True:
        if not os.path.exists( iDirs["tmp"] ):
            break

    ProjectDependencies.utils.check_create_dir( iDirs["tmp"] )

    # Gather index anew
    index_list_with_hash        = ProjectDependencies.utils.gather_list_with_hash( iFiles["index"] )
    for entry in index_list_with_hash:
        src = iDirs["root"] + entry["file"]
        dst = iDirs["tmp"] + entry["file"]
        parentdst = os.path.dirname( dst )
        if not os.path.exists( parentdst ):
            os.makedirs( parentdst )
        shutil.copy( src, dst )

    # Compress
    with tarfile.open( iDirs["tmp"] + iConfig["file"], "w:gz") as tar:
        for entry in os.listdir( iDirs["tmp"] ):
                if os.path.isdir( entry ):
                    tar.add( iDirs["tmp"] + entry, arcname=os.path.basename( iDirs["tmp"] + entry ) )

    # Upload
    ftp_host = ""
    ftp_user = ""
    ftp_pass = ""
    ftp_wdir = ""
    ftp_port = 21

    if os.path.exists( iFiles["pconfig"] ):
        pconfig = ProjectDependencies.utils.load_json_with_keys( iFiles["pconfig"], [] )
        if pconfig:
            if "host" in pconfig: ftp_host = pconfig["host"]
            if "user" in pconfig: ftp_user = pconfig["user"]
            if "pass" in pconfig: ftp_pass = pconfig["pass"]
            if "wdir" in pconfig: ftp_wdir = pconfig["wdir"]
            if "port" in pconfig: ftp_port = pconfig["port"]

    if ftp_host == "": ftp_host = input( "host: " )
    if ftp_user == "": ftp_user = input( "user: " )
    if ftp_pass == "": ftp_pass = getpass.getpass('pass: ')
    if ftp_wdir == "": ftp_wdir = input( "wdir: " )

    print( "Uploading to remote FTP" )
    session = ftplib.FTP( ftp_host, ftp_user, ftp_pass )
    to_send = open( iDirs["tmp"] + iConfig["file"],'rb' )
    #session.cwd( ftp_wdir )
    session.storbinary( "STOR " + ftp_wdir + iConfig["file"], to_send)
    to_send.close()

    # Cleanup behind
    if os.path.exists( iDirs["tmp"] ):
        shutil.rmtree( iDirs["tmp"], ignore_errors=True )

    print( "Done" )
