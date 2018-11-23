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

def command( iArgs, iConfig, iDirs, iFiles ):
    # Check args
    if len( iArgs ) > 1:
        print( "Additional arguments were ignored for this command" )

    # Arg parsing
    arg_path = ""
    if len( iArgs ):
        arg_path = iArgs[0]

    if arg_path == "":
        print( "Nothing specified, nothing added." )
        return

    # Processing with path parsing, simulate regexp
    bMustBeExact = False
    if arg_path.endswith( '*' ):
        arg_path = arg_path[:-1]
        bMustBeExact = False
    else:
        bMustBeExact = True

    # Bake substring indexes
    substr_index_root_dir = len( iDirs["root"] )

    # If no regexp, path must match a real file or directory withing the working tree
    if bMustBeExact:
        if not arg_path[:substr_index_root_dir] == iDirs["root"]:
            arg_path = iDirs["root"] + arg_path
        if not os.path.exists( arg_path ):
            print( "The specified path did not match any element in the working tree." )
            return

    # Strip absolute if needed, make path relative to root
    if arg_path[:substr_index_root_dir] == iDirs["root"]:
        arg_path = arg_path[substr_index_root_dir:]

    # Our arg path is ready, bake index for string matching
    substr_index_arg_path = len( arg_path )

    # Gather working tree, index and stage
    working_tree_list = OdysseyDependencies.utils.gather_working_tree_list( iDirs["root"], iConfig["targets"] )
    index_list = OdysseyDependencies.utils.gather_list( iFiles["index"] )
    OdysseyDependencies.utils.check_create_file( iFiles["pstage"] )
    stage_list = OdysseyDependencies.utils.gather_list( iFiles["pstage"] )

    # Trim staged and index from working tree
    sorted_working_tree_list = []
    for entry in working_tree_list:
        if not entry in stage_list and not entry in index_list:
            sorted_working_tree_list.append( entry )

    # Gather add list
    add_list = []
    bEntryAdded = False
    for entry in sorted_working_tree_list:
        if entry[:substr_index_arg_path] == arg_path:
            add_list.append( entry )
            bEntryAdded = True

    if bEntryAdded == False:
        print( "The specified path did not match any element in the working tree." )
        return

    # Complete stage list
    for entry in add_list:
        print( OdysseyDependencies.utils.make_offset( 8 ) + "staging: " + entry )
        stage_list.append( entry )

    # Write new stage to disk
    with open( iFiles["pstage"], 'w') as f:
        for item in stage_list:
            f.write("%s\n" % item)
