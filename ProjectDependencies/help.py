#:::::::::::::::::::::::::
#::
#:: ProjectDependencies/help.py
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
from colorama import Fore, Back, Style
from colorama import init as init_colorama
init_colorama()

def command( iArgs, iFiles, iConfig, iDirs, iKeys ):
    style_title = Back.WHITE + Fore.BLACK
    style_text  = Back.BLACK + Fore.WHITE

    def print_title():
        print( style_title + "Usage: ProjectDependencies <command> [<args>]" )
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
        offset0 = ProjectDependencies.utils.make_offset( iname )
        offset1 = ProjectDependencies.utils.make_offset( ialias - lname - iname )
        offset2 = ProjectDependencies.utils.make_offset( iargs - lalias - ialias )
        offset3 = ProjectDependencies.utils.make_offset( ishort - largs - iargs )
        print( offset0 + name + offset1 + alias + offset2 + args + offset3 + short )

    # help command
    def help():
        print_title()
        print( "These are the available commands:" )
        print( "" )
        for entry in iKeys["keys"]:
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
    for entry in iKeys["keys"]:
        if help_command == entry["name"] or help_command == entry["alias"]:
            bFound = True
            print_title()
            print_entry( entry )
            print( "" )
            print( entry["doc"] )
            break
    
    if not bFound: ProjectDependencies.utils.command_error( help_command )
