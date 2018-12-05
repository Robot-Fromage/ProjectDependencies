#:::::::::::::::::::::::::
#::
#:: ProjectDependencies/utils.py
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
import xml.etree.ElementTree as xml
import glob
import json
import os
import sys

#:::::::::::::::::::::::::
# Errors
def fatal_error_file_X( iFile, iMessage ):
    print( "error: file '" + iFile + "' " + iMessage )
    sys.exit()

def fatal_error_file_missing( iFile ):
    fatal_error_file_X( iFile, "missing" )

def fatal_error_file_bad_config( iFile ):
    fatal_error_file_X( iFile, "bad config" )

def fatal_error_command( iCommand ):
    print( "error:" + "'" + iCommand + "'" + " is not a valid command. See 'ProjectDependencies help'")
    sys.exit()

#:::::::::::::::::::::::::
# String Utils
def make_offset( iSize ):
    str_offset = ""
    for i in range( iSize ):
        str_offset += " "
    return str_offset

#:::::::::::::::::::::::::
# Json Load
def load_json_with_keys( iPath, iRequiredKeys ):
    json_data = json.load( open( iPath ) )
    for entry in iRequiredKeys:
        if not entry in json_data:
            print( "error: key not configured '" + entry + "'" )
            return 0
    return json_data

def load_json_with_keys_checked( iPath, iRequiredKeys ):
    if not os.path.exists( iPath ):
        fatal_error_file_missing( iPath )
    json_data = ProjectDependencies.utils.load_json_with_keys( iPath, iRequiredKeys )
    if not json_data:
        fatal_error_file_bad_config( iPath )
    return json_data

#:::::::::::::::::::::::::
# GUI Feedback
def fake_progress():
    for x in range( 10000 ):
        print( "Progress {:2.1%}".format( x / 10000 ), end="\r" )

def notify_ignore_args( iArgs ):
    if len( iArgs ):
        print( "Additional arguments were ignored: " + str( iArgs ) )

#:::::::::::::::::::::::::
# Persistent data manipulation
def gather_ue4_dep_list( iRootDir, iTargets ):
    ue4_dep_list = []
    ue4_dep_tree = xml.parse( iRootDir + ".ue4dependencies" )
    ue4_dep_root = ue4_dep_tree.getroot()
    ue4_dep_node = ue4_dep_root.find( "Files" )
    total = len( ue4_dep_node )
    count = 0
    for target in iTargets:
        substr_index = len( target )
        for file in ue4_dep_node.findall( "File" ):
            name = file.get('Name')
            if name[:substr_index] == target:
                ue4_dep_list.append( name )
            count += 1
            print( "Parsing .ue4dependencies {:2.1%}".format( count / total ), end="\r" )
    print("")
    return ue4_dep_list

def gather_working_tree_list( iRootDir, iTargets, iIgnoreFile ):
    #ue4_dep_list = gather_ue4_dep_list( iRootDir, iTargets )
    working_tree_list = []
    all_files_pattern = "**/*"
    substr_index = len( iRootDir )
    count = 0

    ignore_list = gather_list( iIgnoreFile )

    for target in iTargets:
        for filename in glob.iglob( iRootDir + target + all_files_pattern, recursive=True ):
            if os.path.isfile( filename ):
                relative_filename = filename[substr_index:].replace( os.sep, '/' )
                if relative_filename not in ignore_list:
                    working_tree_list.append( relative_filename )
            count += 1
            print( "Parsing elements in working directory: {0}".format( count ), end="\r" )
    print("")
    return working_tree_list

def gather_list( iFilePath ):
    with open( iFilePath ) as f:
        result_list = f.readlines()
    result_list = [ x.strip() for x in result_list ]
    return result_list

def check_create_file( iFilePath ):
    # Create stage file if it doesn't exist
    if not os.path.isfile( iFilePath ):
        print( "create mode: " + iFilePath )
        handle = open( iFilePath, 'w')
        handle.close()

def check_create_dir( iDirPath ):
     if not os.path.exists( iDirPath ):
        os.makedirs( iDirPath )