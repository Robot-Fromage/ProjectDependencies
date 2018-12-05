#:::::::::::::::::::::::::
#::
#:: ProjectDependencies/index.py
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
import os
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

    # Gather index anew
    index_list_with_hash        = ProjectDependencies.utils.gather_list_with_hash( iFiles["index"] )

    # Check for inconsistencies in index against working directory
    missing_index_list = []
    bFoundMissingIndexedFile = False
    for entry in index_list_with_hash:
        absolute_entry = iDirs["root"] + entry["file"]
        if not os.path.exists( absolute_entry ):
            bFoundMissingIndexedFile = True
            missing_index_list.append( entry )

    # Print index
    if len( index_list_with_hash ):
        print( "Indexed files:")
        for entry in index_list_with_hash:
            print( ProjectDependencies.utils.make_offset( 4 ) + "indexed: " + "<" + entry["hash"] + "> " + entry["file"] )
    else:
        print( "Nothing to show")

    if bFoundMissingIndexedFile:
        print( "The following files appear to be missing in the working tree:")
        print( Fore.RED )
        for entry in missing_index_list:
            print( ProjectDependencies.utils.make_offset( 4 ) + "missing: " + entry["file"] )
        print(Style.RESET_ALL)
