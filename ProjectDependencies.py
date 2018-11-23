#:::::::::::::::::::::::::
#::
#:: OdysseyDependencies.py
#::_______________________
#::
#:: Author: Clement BERTHAUD
#::
#:: This piece of script is licensed under the WTFPL licence:
#::
#::  DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#::                    Version 2, December 2004
#::
#:: Copyright (C) 2018 - End of the Universe, Praxinos <code@praxinos.coop>
#::
#:: Everyone is permitted to copy and distribute verbatim or modified
#:: copies of this license document, and changing it is allowed as long
#:: as the name is changed.
#::
#::            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#::   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#::
#:: 0. You just DO WHAT THE FUCK YOU WANT TO.
#::
#:::::::::::::::::::::::::
import os, sys

# Import setup
working_dir = os.path.dirname( __file__ ).replace( os.sep, '/' ) + '/'
sys.path.append( working_dir )
import OdysseyDependencies.utils

# Gather Files
files = {}
files["config"]  = working_dir + ".OdysseyDependencies-config"
files["pconfig"] = working_dir + ".OdysseyDependencies-config-private"
files["ignore"]  = working_dir + ".OdysseyDependencies-ignore"
files["index"]   = working_dir + ".OdysseyDependencies-index"
files["pstage"]  = working_dir + ".OdysseyDependencies-stage-private"

# Gather Dirs
dirs = {}
dirs["root"]                = os.path.realpath( working_dir + "../../" ).replace( os.sep, '/' )
dirs["tmp"]                 = working_dir + "tmp/"
dirs["script"]              = working_dir

# Gather config
required_entries = [ "url", "file", "targets", "doc-files", "keys" ]
config = OdysseyDependencies.utils.load_config( files["config"], required_entries )
if config == 0:
    OdysseyDependencies.utils.config_error()
    sys.exit()

# Gather commands
modules  = {}
commands = {}
for entry in config["keys"]: modules[ entry["name"]] = __import__( "OdysseyDependencies." + entry["name"], fromlist=[ "OdysseyDependencies" ] )
for entry in config["keys"]: commands[entry["name"]] = getattr( modules[entry["name"]], "command" )

# Parse args
command = ""
args    = []
if len( sys.argv ) > 1:
    command = sys.argv[1]   # Gather command
    args    = sys.argv[2:]  # Gather args

# Exec
for entry in config["keys"]:
    if command == entry["name"] or command == entry["alias"]:
        commands[ entry["name"] ]( args, config, dirs, files )
        sys.exit()

OdysseyDependencies.utils.command_error( command )
