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

def command( iArgs, iConfig, iDirs, iFiles ):
    ProjectDependencies.utils.notify_ignore_args( iArgs )

    # Gather working tree and index
    working_tree_list = ProjectDependencies.utils.gather_working_tree_list( iDirs["root"], iConfig["targets"], iFiles["ignore"] )
    index_list = ProjectDependencies.utils.gather_list( iFiles["index"] )

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
            print( ProjectDependencies.utils.make_offset( 4 ) + "indexed: " + entry )
    else:
        print( "Nothing to show")

    if bFoundInconsistenciesInIndex:
        print( "The following files appear to be missing in the working tree:")
        print( Fore.RED )
        for entry in inconsistent_index_list:
            print( ProjectDependencies.utils.make_offset( 4 ) + "missing: " + entry )
        print(Style.RESET_ALL)
