#:::::::::::::::::::::::::
#::
#:: OdysseyDependencies/help.py
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
import OdysseyDependencies.utils
from colorama import Fore, Back, Style
from colorama import init as init_colorama
init_colorama()

def command( iArgs, iConfig, iDirs, iFiles ):

    style_title = Back.WHITE + Fore.BLACK
    style_text  = Back.BLACK + Fore.WHITE

    def print_title():
        print( style_title + "Usage: OdysseyDependencies <command> [<args>]" )
        print( style_text  )

    def print_entry( iEntry ):
        name    = iEntry["name"]
        alias   = iEntry["alias"]
        args    = iEntry["args"]
        short   = iEntry["short"]
        if alias    is None:    alias   = ""
        if args     is None:    args    = ""
        lname   = len( name )
        lalias  = len( alias )
        largs   = len( args )
        lshort  = len( short )
        iname = 4
        ialias = 16
        iargs = 24
        ishort = 40
        offset0 = OdysseyDependencies.utils.make_offset( iname )
        offset1 = OdysseyDependencies.utils.make_offset( ialias - lname - iname )
        offset2 = OdysseyDependencies.utils.make_offset( iargs - lalias - ialias )
        offset3 = OdysseyDependencies.utils.make_offset( ishort - largs - iargs )
        print( offset0 + name + offset1 + alias + offset2 + args + offset3 + short )

    # help command
    def help():
        print_title()
        print( "These are the available commands:" )
        print( "" )
        for entry in iConfig["keys"]:
            print_entry( entry )

    # Parse args
    help_command = ""
    if len( iArgs ):
        help_command = iArgs[0]

    # Exec
    if help_command == "":
        help()
        return

    bFound = False
    for entry in iConfig["keys"]:
        if help_command == entry["name"] or help_command == entry["alias"]:
            bFound = True
            print_title()
            print_entry( entry )
            print( "" )
            print( entry["doc"] )
            break
    
    if not bFound: OdysseyDependencies.utils.command_error( help_command )
