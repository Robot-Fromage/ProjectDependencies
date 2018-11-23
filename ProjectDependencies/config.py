#:::::::::::::::::::::::::
#::
#:: OdysseyDependencies/config.py
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

def command( iArgs, iConfig, iDirs, iFiles ):
    OdysseyDependencies.utils.notify_ignore_args( iArgs )

    def print_entry( iEntry ):
        name    = iEntry + ":"
        value   = iConfig[iEntry]

        lname   = len( name )
        iname = 4
        ivalue = 16

        if isinstance( value, str):
            offset0 = OdysseyDependencies.utils.make_offset( iname )
            offset1 = OdysseyDependencies.utils.make_offset( ivalue - lname - iname )
            print( offset0 + name + offset1 + value )
        
        if isinstance( value, list ):
            offset0 = OdysseyDependencies.utils.make_offset( iname )
            offset1 = OdysseyDependencies.utils.make_offset( ivalue )
            print( offset0 + name )
            for entry in value:
                 print( offset1 + entry )
                
    exclude = [ "keys" ]
    for entry in iConfig:
        if not entry in exclude:
            print_entry( entry )
    