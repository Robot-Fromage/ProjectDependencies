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
import os, sys

# Import setup
script_dir = os.path.dirname( os.path.realpath( __file__ ) ).replace( os.sep, '/' ) + '/'
sys.path.append( script_dir )
import ProjectDependencies.utils

# Gather Files
files = {}
files["config"]     = script_dir + ".config"
files["keys"]       = script_dir + ".keys"
files["ignore"]     = script_dir + ".ignore"
files["index"]      = script_dir + ".index"
files["pstage"]     = script_dir + ".stage"

# Gather config
required_entries = [ "url", "file", "targets", "root", "tmp" ]
if not os.path.exists( files["config"] ):
    print( "error: '.config' not found" )
    sys.exit()
config = ProjectDependencies.utils.load_config( files["config"], required_entries )
if config == 0:
    print( "error: .config lacks some entries" )
    sys.exit()

# Gather Dirs
dirs = {}
dirs["root"]    = os.path.realpath( script_dir + config["root"] ).replace( os.sep, '/' )
dirs["tmp"]     = script_dir + config["tmp"]
dirs["script"]  = script_dir

# Gather keys
if not os.path.exists( files["keys"] ):
    print( "error: '.keys' not found" )
    sys.exit()
keys = ProjectDependencies.utils.load_config( files["keys"], [] )
if keys == 0:
    print( "error: .keys lacks some entries" )
    sys.exit()

# Concatenate keys in config
config["keys"] = keys["keys"]

# Gather commands
modules  = {}
commands = {}
for entry in keys["keys"]: modules[ entry["name"]] = __import__( "ProjectDependencies." + entry["name"], fromlist=[ "ProjectDependencies" ] )
for entry in keys["keys"]: commands[entry["name"]] = getattr( modules[entry["name"]], "command" )

# Parse args
command = ""
args    = []
if len( sys.argv ) > 1:
    command = sys.argv[1]   # Gather command
    args    = sys.argv[2:]  # Gather args

# Exec
for entry in keys["keys"]:
    if command == entry["name"] or command == entry["alias"]:
        commands[ entry["name"] ]( args, config, dirs, files )
        sys.exit()

ProjectDependencies.utils.command_error( command )
