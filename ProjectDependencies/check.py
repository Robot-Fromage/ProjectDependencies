#:::::::::::::::::::::::::
#::
#:: ProjectDependencies/check.py
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

    # Gather working tree and index
    working_tree_list = ProjectDependencies.utils.gather_working_tree_list( iDirs["root"], iConfig["targets"], iFiles["ignore"] )
    index_list = ProjectDependencies.utils.gather_list( iFiles["index"] )

    # Check for inconsistencies in index against working directory
    missing_index_list = []
    bFoundMissingIndexedFile = False
    for entry in index_list:
        absolute_entry = iDirs["root"] + entry
        if not os.path.exists( absolute_entry ):
            bFoundMissingIndexedFile = True
            missing_index_list.append( entry )

    if bFoundMissingIndexedFile:
        print( "Yeah, you should run download again." )
        print( "Here is the list of missing indexed files:" )
        print( Fore.RED )
        for entry in missing_index_list:
            print( ProjectDependencies.utils.make_offset( 4 ) + "missing: " + entry )
        print(Style.RESET_ALL)
    else:
        print( "Everything's fine, chill out." )
