#:::::::::::::::::::::::::
#::
#:: ProjectDependencies/track.py
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

def command( iArgs, iFiles, iConfig, iDirs, iKeys ):
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

    # Bake substring indexes
    substr_index_root_dir = len( iDirs["root"] )

    ProjectDependencies.utils.smart_gather_wtree_resolve_all_hash_inconsistencies( iDirs, iFiles )

    # Preprocess arg path
    if arg_path.endswith( '*' ):
            arg_path = arg_path[:-1]
    if arg_path[:substr_index_root_dir] == iDirs["root"]:
        arg_path = arg_path[substr_index_root_dir:]
    if not arg_path.endswith( '/' ):
        arg_path = arg_path + '/'

    # Gather track
    ProjectDependencies.utils.check_create_file( iFiles["track"] )
    track_list = ProjectDependencies.utils.gather_list( iFiles["track"] )

    # Check if exists
    bEntryExists = False
    if arg_path in track_list:
        bEntryExists = True

    if not bEntryExists:
        print( "The specified path did not match any tracked directory." )
        return

    # Complete track list
    print( ProjectDependencies.utils.make_offset( 8 ) + "untracking: " + arg_path )
    track_list.remove( arg_path )

    # Write new track to disk
    with open( iFiles["track"], 'w') as f:
        for item in track_list:
            f.write("%s\n" % item)
