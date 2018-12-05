#:::::::::::::::::::::::::
#::
#:: ProjectDependencies.py
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
# Basic Imports
import os, sys


#:::::::::::::::::::::::::
# Import Setup
script_dir      = os.path.dirname( os.path.realpath( __file__ ) ).replace( os.sep, '/' ) + '/'  # The directory in which the script is located.
parent_repo_dir = os.path.realpath( script_dir + "../" ).replace( os.sep, '/' )                 # The parent repository in which ProjectDependencies is located.
sys.path.append( script_dir )                                                                   # Add script dir to sys path in order to import relative modules.
# Import local relative utils module.
import ProjectDependencies.utils


#:::::::::::::::::::::::::
# Gather Files Paths
files = {}
# Local files in ProjectDependencies submodule
files["keys"]       = script_dir        + ".keys"       # Contains internal key specs for commands.
files["stage"]      = script_dir        + ".stage"       # Contains internal private staging data.
# External files outside ProjectDependencies submodule
files["config"]     = parent_repo_dir   + ".config"     # Contains ProjectDependencies config for parent repo.
files["pconfig"]    = parent_repo_dir   + ".pconfig"    # Contains ProjectDependencies private config for parent repo.
files["ignore"]     = parent_repo_dir   + ".ignore"     # Contains ProjectDependencies ignore for parent repo.
files["index"]      = parent_repo_dir   + ".index"      # Contains ProjectDependencies index for parent repo.
files["track"]      = parent_repo_dir   + ".track"      # Contains ProjectDependencies track for parent repo.


#:::::::::::::::::::::::::
# Bake required keys
required_config_keys    = [ "remote", "file", "root", "tmp" ]
required_keys_keys      = [ "keys" ]


#:::::::::::::::::::::::::
# Gather config and keys
config  = ProjectDependencies.utils.load_json_with_keys_checked( files["config"],   required_config_keys )
keys    = ProjectDependencies.utils.load_json_with_keys_checked( files["keys"],     required_keys_keys )

#:::::::::::::::::::::::::
# Gather Dirs
dirs = {}
dirs["root"]    = os.path.realpath( script_dir + config["root"] ).replace( os.sep, '/' )    # The root of the parent repository.
dirs["tmp"]     = parent_repo_dir + config["tmp"]                                           # The location of tmp in parent repository.
dirs["script"]  = script_dir                                                                # The location of the script directory.


#:::::::::::::::::::::::::
# Parse args
command = ""
args    = []
if len( sys.argv ) > 1:
    command = sys.argv[1]   # Gather command
    args    = sys.argv[2:]  # Gather args


#:::::::::::::::::::::::::
# Exec
for entry in keys["keys"]:
    # Check if the input command is a registered key.
    if command == entry["name"] or command == entry["alias"]:
        # Import only the module we need dynamically.
        module = __import__( "ProjectDependencies." + entry["name"], fromlist=[ "ProjectDependencies" ] )
        # Find the command in the module and execute it
        getattr( modules[entry["name"]], "command" )( args, files, config, dirs, keys )
        sys.exit()


#:::::::::::::::::::::::::
# Error handling
ProjectDependencies.utils.fatal_error_command( command )
