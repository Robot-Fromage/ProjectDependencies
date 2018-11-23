#:::::::::::::::::::::::::
#::
#:: ProjectDependencies/status.py
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
import os
import ProjectDependencies.utils
from colorama import Fore, Back, Style
from colorama import init as init_colorama
init_colorama()

def command( iArgs, iConfig, iDirs, iFiles ):
    ProjectDependencies.utils.notify_ignore_args( iArgs )

    # Gather working tree, index and stage
    working_tree_list = ProjectDependencies.utils.gather_working_tree_list( iDirs["root"], iConfig["targets"] )
    index_list = ProjectDependencies.utils.gather_list( iFiles["index"] )
    ProjectDependencies.utils.check_create_file( iFiles["pstage"] )
    stage_list = ProjectDependencies.utils.gather_list( iFiles["pstage"] )

    # Trim staged and indexed from working tree
    sorted_working_tree_list = []
    for entry in working_tree_list:
        if not entry in stage_list and not entry in index_list:
            sorted_working_tree_list.append( entry )

    # If there are files in stage, print them with info
    if len( stage_list ):
        # Print info
        print( "Staged changes:")
        print( ProjectDependencies.utils.make_offset( 4 ) + "( Use 'ProjectDependencies reset <path>' to unstage )" )

        # Print stage
        print( Fore.GREEN )
        for entry in stage_list:
            print( ProjectDependencies.utils.make_offset( 8 ) + "staged: " + entry )
        print(Style.RESET_ALL)

    # If there are files in both stage and sorted working tree, print a blank line beetween the reports
    if len( stage_list ) and len( sorted_working_tree_list ):
        print( "" )

    # If there are files in sorted working tree, print them with info
    if len( sorted_working_tree_list ):
        # Print info
        print( "Unstaged changes:")
        print( ProjectDependencies.utils.make_offset( 4 ) + "( Use 'ProjectDependencies add <path>' to stage )" )

        # Print sorted working tree
        print( Fore.RED )
        for entry in sorted_working_tree_list:
            print( ProjectDependencies.utils.make_offset( 8 ) + "unstaged: " + entry )
        print(Style.RESET_ALL)

    if not len( stage_list ) and not len( sorted_working_tree_list ):
        print( "Nothing to show.")
