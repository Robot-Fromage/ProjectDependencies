#:::::::::::::::::::::::::
#::
#:: OdysseyDependencies/status.py
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
import os
import OdysseyDependencies.utils
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

    # Trim staged and indexed from working tree
    sorted_working_tree_list = []
    for entry in working_tree_list:
        if not entry in stage_list and not entry in index_list:
            sorted_working_tree_list.append( entry )

    # If there are files in stage, print them with info
    if len( stage_list ):
        # Print info
        print( "Staged changes:")
        print( OdysseyDependencies.utils.make_offset( 4 ) + "( Use 'OdysseyDependencies reset <path>' to unstage )" )

        # Print stage
        print( Fore.GREEN )
        for entry in stage_list:
            print( OdysseyDependencies.utils.make_offset( 8 ) + "staged: " + entry )
        print(Style.RESET_ALL)

    # If there are files in both stage and sorted working tree, print a blank line beetween the reports
    if len( stage_list ) and len( sorted_working_tree_list ):
        print( "" )

    # If there are files in sorted working tree, print them with info
    if len( sorted_working_tree_list ):
        # Print info
        print( "Unstaged changes:")
        print( OdysseyDependencies.utils.make_offset( 4 ) + "( Use 'OdysseyDependencies add <path>' to stage )" )

        # Print sorted working tree
        print( Fore.RED )
        for entry in sorted_working_tree_list:
            print( OdysseyDependencies.utils.make_offset( 8 ) + "unstaged: " + entry )
        print(Style.RESET_ALL)

    if not len( stage_list ) and not len( sorted_working_tree_list ):
        print( "Nothing to show.")
