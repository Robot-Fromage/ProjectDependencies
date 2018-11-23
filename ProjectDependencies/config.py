#:::::::::::::::::::::::::
#::
#:: ProjectDependencies/config.py
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

def command( iArgs, iConfig, iDirs, iFiles ):
    ProjectDependencies.utils.notify_ignore_args( iArgs )

    def print_entry( iEntry ):
        name    = iEntry + ":"
        value   = iConfig[iEntry]

        lname   = len( name )
        iname = 4
        ivalue = 16

        if isinstance( value, str):
            offset0 = ProjectDependencies.utils.make_offset( iname )
            offset1 = ProjectDependencies.utils.make_offset( ivalue - lname - iname )
            print( offset0 + name + offset1 + value )
        
        if isinstance( value, list ):
            offset0 = ProjectDependencies.utils.make_offset( iname )
            offset1 = ProjectDependencies.utils.make_offset( ivalue )
            print( offset0 + name )
            for entry in value:
                 print( offset1 + entry )
                
    exclude = ["keys"]
    for entry in iConfig:
        if not entry in exclude:
            print_entry( entry )
    