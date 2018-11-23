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
import os
import shutil
import tarfile
import ftplib
import getpass
from colorama import Fore, Back, Style
from colorama import init as init_colorama
init_colorama()

def command( iArgs, iConfig, iDirs, iFiles ):
    OdysseyDependencies.utils.notify_ignore_args( iArgs )

    # Gather working tree, index and stage
    working_tree_list = OdysseyDependencies.utils.gather_working_tree_list( iDirs["root"], iConfig["targets"] )
    index_list = OdysseyDependencies.utils.gather_list( iFiles["index"] )
    OdysseyDependencies.utils.check_create_file( iFiles["pstage"] )
    stage_list = OdysseyDependencies.utils.gather_list( iFiles["pstage"] )

    # Check for inconsistencies in stage against working directory
    inconsistent_stage_list = []
    bFoundInconsistenciesInStage = False
    for entry in stage_list:
        absolute_entry = iDirs["root"] + entry
        if not os.path.exists( absolute_entry ):
            bFoundInconsistenciesInStage = True
            inconsistent_stage_list.append( entry )

    # Check for inconsistencies in index against working directory
    inconsistent_index_list = []
    bFoundInconsistenciesInIndex = False
    for entry in index_list:
        absolute_entry = iDirs["root"] + entry
        if not os.path.exists( absolute_entry ):
            bFoundInconsistenciesInIndex = True
            inconsistent_index_list.append( entry )

    if bFoundInconsistenciesInStage:
        print( "Inconsistencies were found in stage, the following files do not appear to be part of the working tree:" )
        print( Fore.RED )
        for entry in inconsistent_stage_list:
            print( OdysseyDependencies.utils.make_offset( 8 ) + "missing: " + entry )
        print( Style.RESET_ALL )
        print( OdysseyDependencies.utils.make_offset( 4 ) + "Remove them using OdysseyDependencies reset <path> before pushing.")

    if bFoundInconsistenciesInIndex:
        print( "Inconsistencies were found in index, the following files do not appear to be part of the working tree:" )
        print( Fore.RED )
        for entry in inconsistent_index_list:
            print( OdysseyDependencies.utils.make_offset( 8 ) + "missing: " + entry )
        print( Style.RESET_ALL )
        print( OdysseyDependencies.utils.make_offset( 4 ) + "Solve this by checkout with git or download again or remove them from index manually." )

    # Move stage to index
    for entry in stage_list:
        print( OdysseyDependencies.utils.make_offset( 8 ) + "indexing: " + entry )
        index_list.append( entry )
    
    # Write new stage to disk
    with open( iFiles["index"], 'w') as f:
        for item in index_list:
            f.write("%s\n" % item)

    # Erase stage
    open( iFiles["pstage"], 'w').close()

    # Gathering dependencies in TMP
    if os.path.exists( iDirs["tmp"] ):
        shutil.rmtree( iDirs["tmp"], ignore_errors=True )

    while True:
        if not os.path.exists( iDirs["tmp"] ):
            break

    OdysseyDependencies.utils.check_create_dir( iDirs["tmp"] )

    # Gather index anew
    index_list = OdysseyDependencies.utils.gather_list( iFiles["index"] )
    for entry in index_list:
        src = iDirs["root"] + entry
        dst = iDirs["tmp"] + entry
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
        pconfig = OdysseyDependencies.utils.load_config( iFiles["pconfig"], [] )
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
