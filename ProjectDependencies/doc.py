#:::::::::::::::::::::::::
#::
#:: OdysseyDependencies/doc.py
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
import webbrowser, os

def command( iArgs, iConfig, iDirs, iFiles ):
    OdysseyDependencies.utils.notify_ignore_args( iArgs )
    # Prepare paths
    doc_dir = iDirs["root"] + "OdysseyTools/Documentation/"

    for entry in iConfig["doc-files"]:
        webbrowser.open( 'file://' + os.path.realpath( doc_dir + entry ) )
    