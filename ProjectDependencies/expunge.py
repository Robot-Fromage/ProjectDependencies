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
        print( "Nothing specified, nothing done." )
        return

    # Processing with path parsing, simulate regexp
    if arg_path.endswith( '*' ):
        arg_path = arg_path[:-1]

    # Bake substr index
    substr_index_root_dir = len( iDirs["root"] )

    # Strip absolute if needed
    if arg_path[:substr_index_root_dir] == iDirs["root"]:
        arg_path = arg_path[substr_index_root_dir:]

    # Our arg path is ready, bake index for string matching
    substr_index_arg_path = len( arg_path )

    # Gather index
    index_list = OdysseyDependencies.utils.gather_list( iFiles["index"] )

    # Trim from stage if needed
    sorted_expunge_index = []
    for entry in index_list:
        if not entry[:substr_index_arg_path] == arg_path:
            # If the entry doesn't match path, we keep it in the new stage
            sorted_expunge_index.append( entry )
        else:
            # Else we notify it was not kept
            print( "    Expunging file: " + entry )

    # Write new stage to disk
    with open( iFiles["index"], 'w') as f:
        for item in sorted_expunge_index:
            f.write("%s\n" % item)