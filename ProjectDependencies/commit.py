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
import os

def command( iArgs, iFiles, iConfig, iDirs, iKeys ):
    ProjectDependencies.utils.notify_ignore_args( iArgs )

    # Gather working tree, index and stage
    stage_list_with_hash        = ProjectDependencies.utils.gather_list_with_hash( iFiles["stage"] )
    index_list_with_hash        = ProjectDependencies.utils.gather_list_with_hash( iFiles["index"] )

    tpr = ProjectDependencies.utils.resolve_inconsistencies( stage_list_with_hash, [ index_list_with_hash ] )
    sorted_stage_list_with_hash = tpr[0]
    sorted_index_list_with_hash = tpr[1][0]

    # Gather list anew
    resolved_index_list_with_hash = ProjectDependencies.utils.gather_list_with_hash( iFiles["index"] )

    # Complete stage list
    for entry in sorted_stage_list_with_hash:
        print( ProjectDependencies.utils.make_offset( 8 ) + "comitting: " + "<" + entry["hash"] + "> " + entry["file"] )
        resolved_index_list_with_hash.append( entry )

    # Erase stage
    open( iFiles["stage"], 'w').close()

    # Write new index to disk
    ProjectDependencies.utils.update_list_with_hash( iFiles["index"], resolved_index_list_with_hash )
