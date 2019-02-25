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
import sys, os, glob, json, hashlib, subprocess

#:::::::::::::::::::::::::
# System command
def system(*args, **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, err = proc.communicate()
    return out

#:::::::::::::::::::::::::
# Path checks
def ensureValidPathEnding( iPath ):
    outPath = iPath
    if not outPath.endswith( '/' ):
        outPath = outPath + '/'
    return outPath

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
    json_data = load_json_with_keys( iPath, iRequiredKeys )
    if not json_data:
        fatal_error_file_bad_config( iPath )
    return json_data

#:::::::::::::::::::::::::
# Hash Utils
def sha256sum( iFilePath ):
    h = hashlib.sha256()
    with open( iFilePath, 'rb', buffering=0 ) as f:
        for b in iter( lambda : f.read( 128*1024 ), b'' ):
            h.update( b )
    return h.hexdigest()

#:::::::::::::::::::::::::
# GUI Feedback
def notify_ignore_args( iArgs ):
    if len( iArgs ):
        print( "Additional arguments were ignored: " + str( iArgs ) )

#:::::::::::::::::::::::::
# Filesystem OP
def check_create_file( iFilePath ):
    # Create stage file if it doesn't exist
    if not os.path.isfile( iFilePath ):
        print( "create mode: " + iFilePath )
        handle = open( iFilePath, 'w')
        handle.close()

def check_create_dir( iDirPath ):
     if not os.path.exists( iDirPath ):
        os.makedirs( iDirPath )

def mkdirtree( iDst ):
    parent = os.path.dirname( iDst )
    if not os.path.exists( parent ):
        mkdirtree( parent )

    if not os.path.exists( iDst ):
        os.mkdir( iDst )

#:::::::::::::::::::::::::
# High level funks
def gather_working_tree_list_with_hash( iRootDir, iTrackList, iIgnoreList ):
    working_tree_list   = []
    all_files_pattern   = "**/*"
    substr_index        = len( iRootDir )
    count               = 0

    if not len( iTrackList ):
        print( "No target specified." )

    for target in iTrackList:
        for filename in glob.iglob( iRootDir + target + all_files_pattern, recursive=True ):
            if os.path.isfile( filename ):
                relative_filename = filename[substr_index:].replace( os.sep, '/' )
                bIgnored = False
                for entry in iIgnoreList:
                    # Simulate regexp
                    ignore_entry = entry
                    if ignore_entry.endswith( '*' ):
                        ignore_entry = ignore_entry[:-1]
                    substr_ignore_entry = len( ignore_entry )
                    # If match with ignored entry
                    if relative_filename[:substr_ignore_entry] == ignore_entry:
                        # We ignore
                        bIgnored = True
                # If not ignored, compute hash and append
                if not bIgnored:
                    fhash = sha256sum( filename )
                    working_tree_list.append( { "file": relative_filename, "hash": fhash } )
            # Print feedback
            count += 1
            print( "Parsing elements in working directory: {0}".format( count ), end="\r" )
    # Pretty line break
    if len( iTrackList ):
        print("")
    # Ret
    return working_tree_list

def smath_gather_wtree( iDirs, iFiles ):
    # Gather track & ignore & git track
    track_list              = gather_list( iFiles["track"] )
    extended_ignore_list    = gather_extended_ignore_list( iDirs["root"], iFiles["ignore"] )
    # Gather working tree
    return gather_working_tree_list_with_hash( iDirs["root"], track_list, extended_ignore_list )

def smart_gather_wtree_resolve_all_hash_inconsistencies( iDirs, iFiles ):
    # Gather working tree, index and stage
    working_tree_list_with_hash         = smath_gather_wtree( iDirs, iFiles )
    stage_list_with_hash                = gather_list_with_hash( iFiles["stage"] )
    index_list_with_hash                = gather_list_with_hash( iFiles["index"] )
    tuple_ret                           = resolve_hash_inconsistencies( working_tree_list_with_hash, [ stage_list_with_hash, index_list_with_hash ] )
    sorted_working_tree_list_with_hash  = tuple_ret[0]
    sorted_stage_list_with_hash         = tuple_ret[1][0]
    sorted_index_list_with_hash         = tuple_ret[1][1]
    # Write new lists
    update_list_with_hash( iFiles["stage"], sorted_stage_list_with_hash )
    update_list_with_hash( iFiles["index"], sorted_index_list_with_hash )
    return sorted_working_tree_list_with_hash

def gather_list( iFilePath ):
    check_create_file( iFilePath )
    with open( iFilePath ) as f:
        result_list = f.readlines()
    result_list = [ x.strip() for x in result_list ]
    return result_list

def gather_list_with_hash( iFilePath ):
    check_create_file( iFilePath )
    with open( iFilePath ) as f:
        result_list = f.readlines()
    result_list = [ x.strip() for x in result_list ]
    result_list_with_hash = []
    for entry in result_list:
        entry_arr = entry.split( ';' )
        entry_hash = entry_arr[0]
        entry_file = entry_arr[1]
        result_list_with_hash.append( { "file": entry_file, "hash": entry_hash } )
    return result_list_with_hash

def gather_git_tracked_files( iRootDir ):
    bak_path = os.getcwd()
    os.chdir( iRootDir )
    strfiles = system( "git", "ls-files" ).decode('utf-8').strip()
    os.chdir( bak_path )
    return strfiles.split('\n')

def gather_extended_ignore_list( iRootDir, iIgnoreFile ):
    ignore_list         = gather_list( iIgnoreFile )
    git_tracked_files   = gather_git_tracked_files( iRootDir )
    # Concatenate ignore with git tracked
    ignore_list.extend( git_tracked_files )
    return ignore_list

def resolve_hash_inconsistencies( iMainList, iResolveLists ):
    # Trim staged from working tree, and check for updated hashes
    result_list = []

    if not len( iResolveLists ):
        return

    for entry in iMainList:
        bFoundAnywhere = False
        for resolveList in iResolveLists:
            obsolete_resolve_hashes = []
            for resolve_entry in resolveList:
                if entry["file"] == resolve_entry["file"]:
                    if  entry["hash"] == resolve_entry["hash"]:
                        bFoundAnywhere = True
                    else:
                        obsolete_resolve_hashes.append( resolve_entry )
            for obs_entry in obsolete_resolve_hashes:
                resolveList.remove( obs_entry )

        if not bFoundAnywhere:
            result_list.append( entry )
    return result_list, iResolveLists

def update_list_with_hash( iFilePath, iList ):
    # Write new stage to disk
    with open( iFilePath, 'w') as f:
        for item in iList:
            stritem = item["hash"] + ";" + item["file"]
            f.write( "%s\n" % stritem )
