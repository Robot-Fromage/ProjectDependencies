#:::::::::::::::::::::::::
#::
#:: ProjectDependencies/reset.py
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

def command( iArgs, iFiles, iConfig, iDirs, iKeys ):
    # Check args
    if len( iArgs ) > 1:
        print( "Additional arguments were ignored for this command" )

    # Arg parsing
    arg_path = ""
    if len( iArgs ):
        arg_path = iArgs[0]

    if arg_path == "":
        # Erase, reset all
        open( iFiles["stage"], 'w').close()
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

    ProjectDependencies.utils.smart_gather_wtree_resolve_all_hash_inconsistencies( iDirs, iFiles )
    resolved_stage_list_with_hash = ProjectDependencies.utils.gather_list_with_hash( iFiles["stage"] )

    # Trim from stage if needed
    sorted_reset_stage = []
    for entry in resolved_stage_list_with_hash:
        if not entry["file"][:substr_index_arg_path] == arg_path:
            # If the entry doesn't match path, we keep it in the new stage
            sorted_reset_stage.append( entry )
        else:
            # Else we notify it was not kept
            print( "    Unstaging file: " + entry["file"] )

    # Write new stage to disk
    with open( iFiles["stage"], 'w') as f:
        for item in sorted_reset_stage:
            f.write("%s\n" % item)
