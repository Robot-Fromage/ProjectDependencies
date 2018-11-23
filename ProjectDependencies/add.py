#:::::::::::::::::::::::::
#::
#:: ProjectDependencies/add.py
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
    working_tree_list = ProjectDependencies.utils.gather_working_tree_list( iDirs["root"], iConfig["targets"] )
    index_list = ProjectDependencies.utils.gather_list( iFiles["index"] )
    ProjectDependencies.utils.check_create_file( iFiles["pstage"] )
    stage_list = ProjectDependencies.utils.gather_list( iFiles["pstage"] )

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
        print( ProjectDependencies.utils.make_offset( 8 ) + "staging: " + entry )
        stage_list.append( entry )

    # Write new stage to disk
    with open( iFiles["pstage"], 'w') as f:
        for item in stage_list:
            f.write("%s\n" % item)
