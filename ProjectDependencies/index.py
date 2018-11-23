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
import os
from colorama import Fore, Back, Style
from colorama import init as init_colorama
init_colorama()

def command( iArgs, iConfig, iDirs, iFiles ):
    OdysseyDependencies.utils.notify_ignore_args( iArgs )

    # Gather working tree and index
    working_tree_list = OdysseyDependencies.utils.gather_working_tree_list( iDirs["root"], iConfig["targets"] )
    index_list = OdysseyDependencies.utils.gather_list( iFiles["index"] )

    # Check for inconsistencies in index against working directory
    inconsistent_index_list = []
    bFoundInconsistenciesInIndex = False
    for entry in index_list:
        absolute_entry = iDirs["root"] + entry
        if not os.path.exists( absolute_entry ):
            bFoundInconsistenciesInIndex = True
            inconsistent_index_list.append( entry )

    # Print index
    if len( index_list ):
        print( "Indexed files:")
        for entry in index_list:
            print( OdysseyDependencies.utils.make_offset( 4 ) + "indexed: " + entry )
    else:
        print( "Nothing to show")

    if bFoundInconsistenciesInIndex:
        print( "The following files appear to be missing in the working tree:")
        print( Fore.RED )
        for entry in inconsistent_index_list:
            print( OdysseyDependencies.utils.make_offset( 4 ) + "missing: " + entry )
        print(Style.RESET_ALL)
