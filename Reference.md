# Distribution Builder (distbuilder) 
### Reference Manual 

#### BUILDING STAND-ALONE EXECUTABLES
        
To build a stand-alone binary distribution of a Python
program, invoke the buildExecutable function: 

    buildExecutable( name, entryPointPy, 
        			 opyConfig=None, 
        			 pyInstConfig=PyInstallerConfig(),
				     distResources=[], distDirs=[] )
    
Returns (binDir, binPath): a tuple containing:
    the absolute path to the package created,
    the absolute path to the binary created  

name: The name to give your resulting executable 
    and package distribution directory.  
    
entryPointPy: The path to the Python script where 
    execution begins.             
    
opyConfig: An (optional) OpyConfig object, 
    to dictate code obfuscation details using 
    the Opy Library. If omitted, no obfuscation 
    will be performed.  
    
pyInstConfig: An (optional) PyInstallerConfig 
    object to dictate extended details for building 
    the binary using the PyInstaller Utility. If 
    omitted, default settings will be used.
    See "SUPPORT CLASSES" for more details.  
    
distResources: An (optional) list of external 
    resources to bundle into the distribution package 
    containing the binary. You may use a simple 
    list of strings containing simply file/directory 
    names/paths relative to the original project 
    directory. Else, you may provide a list of two 
    element tuples, with a specific source and 
    destination.  The source may be an absolute path 
    from another location on your file system. The 
    destination maybe whatever name/path you want
    specified relative to the package being created.    
    
distDirs: An (optional) list of directories to 
    create within the package.  Note distResources
    implicitly does this for you when there is 
    a source to copy.  This additional option is
    for adding new empty directories.  
                    
-------------------------------------------------------
To generate an obfuscated version of your project, without 
converting it to binary, invoke obfuscatePy:

    obfuscatePy( name, entryPointPy, opyConfig )

Returns (obDir, obPath): a tuple containing:
    the absolute path to the obfuscated directory,
    the absolute path to the obfuscated entry point script  

See the buildExecutable description for more info.  This
is an optional sub operation within that.
    
Upon invoking this, you will be left with an "obfuscated"
directory adjacent to build.py.  This is a useful 
preliminary step to take, prior to running buildExecutable, 
so that you may inspect and test the obfuscation results 
before building the final distribution package.

-------------------------------------------------------
Upon creating a binary or Python obfuscation, use the
following to test the success of those operations:  
    
    run( binPath, args=[], isDebug=False )      
    runPy( pyPath, args=[] )
    
Note that the path is returned by buildExecutable and
obfuscatePy, which allows the results of those to flow
directly into these functions.  

The working directory will be automatically set to 
to the directory of the path specified.  

The (optional) args parameter is an open ended
list (or string) to pass along to your program.  

Set isDebug=True to debug a PyInstaller binary which
was created with pyInstConfig.isGui set to True.
Normally, when this configuration is used, messages 
sent to the console (e.g. print statements or uncaught 
exceptions) are not visible even when launching
the application from a terminal. The isDebug option, 
however, will expose those messages to you. This can 
be invaluable for debugging problems that are unique 
to a stand-alone binary, and not present when run in 
the original raw script form.  
            
#### BULDING INSTALLERS

Upon creating a distribution (especially a stand-alone binary), 
the    next logical progression is to bundle that into a full-scale 
installer. This library is designed to employ the open source,
cross platform utility: Qt IFW  (i.e. "Qt Installer Framework") 
for such purposes. While the prototypical implementation of this
tool is with a Qt C++ program, it is equally usable for a Python
program (even more so if using "Qt for Python", and perhaps a
QML driven interface...).  (Currently) to create an installer, 
you must first define it using framework, but once that has been 
done you may simply invoke buildInstaller to run the utility:

    buildInstaller( qtIfwConfig, 
                    qtIfwConfigXml=None, isPkgSrcRemoved=False )

Returns: the absolute path to the setup executable created.  

qtIfwConfig: A (required) QtIfwConfig object which dictates 
     the details for building an installer. Perhaps most
     critically, this object includes a "qtIfwDirPath"
     attribute. As this utility's path is not readily
     resolvable, such allows the user to define that.
     If omitted, the library will look for an 
     environmental variable instead, named "QT_IFW_DIR".
     Defining such is arguably the better option (since
     all your build scripts may then draw upon that)
     and your project collaborators may independently 
     define their own paths.
     Note also the need to define a "pkgName" which is
     the sub directory where your content will be 
     dynamically copied, and the "pkgSrcDirPath", which 
     will typically be the "binDir" returned by 
     buildExecutable. See "SUPPORT CLASSES" for more details.                    
        
qtIfwConfigXml: An (optional) QtIfwConfigXml object which
    defines the contents of a config.xml which will be 
    dynamically generated at build time.  This file is 
    represents the highest level definition of a Qt IFW 
    installer, containing information such as the product 
    name and version. If omitted, it is assumed this
    file is already present in the installer definition.
    See "SUPPORT CLASSES" for more details.            
    
isPkgSrcRemoved: A "convenience" option denoting if the 
    package source content directory should be deleted 
    after successfully building the installer.   
        
Note: To debug a Qt IFW installer, the following two options 
    are available:  
    1) Manually run the installer with the "-v" switch 
       argument. Or, if running it via this library using the
       run(...) function, you can pass the QT_IFW_VERBOSE_SWITCH 
       constant as an argument.    
    2) If the build process is failing before you can run 
       the installer, try setting qtIfwConfig.isDebugMode 
       to True for verbose output.
    
#### DISTRIBUTING & INSTALLING LIBRARIES

To generate an obfuscated version of your project, which 
you can then distribute as an importable library, invoke 
obfuscatePyLib:
 
    obfuscatePyLib( name, opyConfig, 
                    isExposingPackageImports=True, 
                    isExposingPublic=True )

Returns (obDir, setupPath): a tuple containing:
    the absolute path to the obfuscated directory,
    the absolute path to the (non obfuscated) setup.py 
    script within the prepared package  

name: The name of your library.  
opyConfig: An OpyConfig object, to dictate code 
    obfuscation details using the Opy Library. 
    See "SUPPORT CLASSES" for more details.  
    
isExposingPackageImports: Option to not obfuscate 
    any of the imports defined in the package 
    entry point modules (i.e. __init__.py files).
    This is the default mode for a library.  
    
isExposingPublic: Option to not obfuscate anything 
    which it is naturally granting public access 
    (e.g. module constants, functions, classes, 
    and class members).  All locals and those 
    identifiers prefixed with a double underscore
    (denoting private) will be still be obfuscated.     
    This is the default mode for a library.

-------------------------------------------------------
To install a library (via pip), simply invoke installLibrary: 
    
    installLibrary( name, opyConfig=None, pipConfig=PipConfig() )
    
Returns: None

name: The name/source of the library.  If the
    library is your current project itself, supply
    the name you are giving it.  If you are NOT
    obfuscating it, specify "." instead.  Otherwise,
    you may specific a remote package name registered
    with pip (i.e. the typical way pip is used),
    or a local path, or a url (http/git). See
    pip documentation for details.               
    
opyConfig: An (optional) OpyConfig object, 
    to dictate code obfuscation details using 
    the Opy Library. If omitted, no obfuscation 
    will be performed.  If you are building
    an obfuscated version of your project 
    as a importable library, this function is useful 
    for testing the operations    of your library 
    post-obfuscation/pre-distribution.  This will  
    run obfuscatePyLib with default arguments, 
    install the library, and remove the temporary 
    obfuscation from the working directory.                 
    See "SUPPORT CLASSES" for more details.            
    
pipConfig: An (optional) PipConfig object, to dictate
    extended installation details.  If omitted,
    the library is simply installed in the standard
    manner to your (global) Python site packages.
    Notable attributes include "incDpndncsSwitch",
    "destPath" and "asSource".  These allow you to 
    skip dependency gathering if desired, install to 
    a specific path such as a temp build directory,
    and to request raw .py scripts be placed there.
    Note that remote raw pip packages will require an 
    alternate "vcs url" be supplied to "development" 
    repository in place of the simple package name.  
    See https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs
    See "SUPPORT CLASSES" for more details.            
        
    uninstallLibrary( name )

Returns: None

Simply uninstalls a library from Python site packages
in the basic/traditional pip manner.    

    vcsUrl( name, baseUrl, vcs="git", subDir=None )  

Convenience function to build vcsUrls from their
component parts. This is to be used in conjunction
with the PipConfig attribute asSource.
See https://pip.pypa.io/en/stable/reference/pip_install/#vcs-support

#### ADDITIONAL OBFUSCATION FEATURES 

The Opy Library contains an OpyConfig class, which has been extended
by this library (and aliased with the same name).  The revised /
extended class contains attributes for patching the obfuscation and
for bundling the source of external libraries (so that they too maybe 
obfuscated). This new configuration type has the additional attributes:
 
    bundleLibs 
    sourceDir
    patches

Patching:

Opy is not perfect.  It has known bugs, and can require a bit of 
effort in order to define a "perfect" configuration for it. In the 
event you are struggling to make it work exactly as desired, an
"easy out" has been provided by way of "patching" the results. If 
you have already determined exactly which files/lines/bugs
you are encountering, you may simply define a list of "OpyPatch"
objects for the configuration.  They will be applied at the end 
of the process to fix any problems. An OpyPatch is created via:

    OpyPatch( relPath, patches, parentDir=OBFUS_DIR_PATH )
    
relPath: The relative file path within the obfuscation 
results that you wish to change.  

patches: A list of tuples. 2 element tuples in the form 
(line number, line) will be utilized for complete line 
replacements. Alternatively, 3 element tuples in the form 
(line number, old, new) will perform a find/replace operation
on that line (to just swap out an identifier typically).  

parentDir: An (optional) path to use a directory other 
than the standard obfuscation results path. 

Library Bundling:
         
The sourceDir defaults to THIS_DIR.  If bundleLibs is defined, it is 
used in combination with sourceDir to create a "staging directory".
The bundleLibs attributes may be either None or a list of     
"LibToBundle" objects. LibToBundle objects maybe created via: 

    LibToBundle( name, localDirPath=None, pipConfig=None, 
                 isObfuscated=False )

That class has attributes named likewise, which may be set after 
creating such an object as well.    

name: The name of the library, i.e. the name to be given to the 
    bundled package.  
    
localDirPath: If this library may be simply copied from a local 
    source, this is the path to that source.  Otherwise, leave 
    this as None.  
    
pipConfig: A PipConfig object defining how to download and 
    install the library.  The destination will be automatically 
    set to the "staging    directory" for the obfuscation process.   
    
isObfuscated: A boolean indicating if the library is already 
    obfuscated,    and therefore may be bundled as is.  

In the event that defining bundleLibs for an OpyConfig object will 
not suffice to setup your staging directory, you may instead call:      

    createStageDir( bundleLibs=[], sourceDir=THIS_DIR )

Returns: the path to the newly created staging directory.

After doing this, you may perform any extended operations that you 
require, and then set an OpyConfig object's sourceDir to that 
staging path while leaving bundleLibs as None in the configuration.

Note that the OpyConfig external_modules list attribute must still 
be set in such a manner to account for the libraries which were 
bundled, or which remain as "external" imports.

#### FINAL PACKAGING & RESULT STORAGE

Once you have a fully built distribution package, the 
following functions provide an easy means for further 
preparing the program for distribution:   

    toZipFile( sourceDir, zipDest=None, removeScr=True )
    
sourceDir: the directory to convert to a zip
    (typically the binDir).   
    
zipDest: (optional) full path to the zip file to
    be created.    If not specified, it will be
    named with same base as the source, and 
    created    adjacent to it.          
    
removeScr: Option to delete the sourceDir after
    creating the zip of it.    Note this is the 
    default behavior.

    moveToDesktop( path )            
    
Returns: the new path to the file or directory.        

Moves a file or directory to the desktop.
(Note: it *moves* the path specified, it does
not leave a copy of the source).
*Replaces* any existing copy found at the 
destination path (i.e. on the desktop).
        
TODO: Add git commit/push...    
                                                                  
#### LOW LEVEL UTILITIES

The following low level "utilities" are also provided for 
convenience, as they maybe useful in defining the build 
parameters, further manipulating the package, or testing 
the results, etc.   

    THIS_DIR 
    
The path to the directory running the build script. 
(This should be the path to your project directory.) 

    absPath( relPath )
    
The absolute path relative to THIS_DIR (which is not 
necessarily the current working directory).  

    modulePath( moduleName )
    
The absolute path to an importable module's source.
(Note the moduleName argument should be a string, not 
an unquoted, direct module reference.)            
This is useful for dynamically resolving the path to 
external modules which you may wish to copy / "bundle" 
for obfuscation.  Returns None if the name is invalid 
and/or the path cannot be resolved.
Note that this often resolves the path to a library's
package entry point (i.e. an __init__.py) file where 
the module is initially imported, rather than literal 
module path. Normally modulePackagePath will be more 
useful...   

    modulePackagePath( moduleName )

Similar to modulePath, but this return the module's 
parent directory.  More often than not, a module 
will have dependencies within the package / library
where it resides. As such, resolving the package path
can be more useful than the specific module.  
   
    sitePackagePath( packageName )

Similar to modulePackagePath, but takes the package
name rather than a module within it AND is specific
to the site packages collection of libraries, rather
than a more universal path resolution.        

    isImportableModule( moduleName )
    isImportableFromModule( moduleName, memberName )            

Attempts the import, and returns a boolean indication
of success without raising an exception upon failure.  
Like the related functions here, the arguments are 
expected to be strings (not direct references).  
The purpose of this to test for library installation
success, or to preemptively confirm the presence
of dependencies.

    printErr( msg, isFatal=False )

Roughly emulates the print command, but writes to
stderr.  Optionally, exits the script with a return
code of 1 (i.e. general error).

    printExc( e, isDetailed=False, isFatal=False )

Analogous to printErr, but prints an exception's 
more detailed repr() information.  Optionally, 
prints a stack trace as well when isDetailed=True.
Note: use printErr( e ) to print just an exception 
"message". 

    Library Function       Alias For (Standard Function)
                
        exists                 os.path.exists 
        isFile                 os.path.isfile
        isDir                  os.path.exists and not os.path.isfile
        copyFile               shutil.copyFile 
        removeFile             os.remove
        makeDir                os.makedirs
        copyDir                shutil.copytree     
        removeDir              shutil.rmtree
        move                   shutil.move
        rename                 os.rename
        tempDirPath            tempfile.gettempdir()    
        dirPath                os.path.dirname
        joinPath               os.path.join
        splitPath              os.path.split
        splitExt               os.path.splitext 
 
#### SUPPORT CLASSES

The following classes are used to create objects which
are generally used as arguments to various functions in
this library.

-------------------------------------------------------
PyInstallerConfig    

Objects of this type define *optional* details for building 
binaries from .py scripts using the PyInstaller utility 
invoked via the buildExecutable function. 

Constructor: 

    PyInstallerConfig()

Attributes & default values:        

    pyInstallerPath = "pyinstaller"  (i.e. on system path)
    name            = None
    distDirPath     = None
    isOneFile       = True     (note this differs from PyInstaller default)
    isGui           = False
    versionFilePath = None 
    iconFilePath    = None     
    importPaths     = []
    hiddenImports   = []
    dataFilePaths   = []
    binaryFilePaths = []
    isAutoElevated  = False        
    otherPyInstArgs = ""  (open ended argument string)    

-------------------------------------------------------
QtIfwConfig 

Objects of this type define the details for building 
an installer using the QtIFW utility invoked via the
buildInstaller function. 

Constructor: 

    QtIfwConfig( pkgSrcDirPath=None, pkgSrcExePath=None,                  
                 pkgName=None, installerDefDirPath=None,
                 setupExeName=DEFAULT_SETUP_NAME ) 
                     
Attributes & default values:                                               

    (basic installer definition)
        pkgName             = None
        installerDefDirPath = "installer"
    (content)
        pkgSrcDirPath   = None
        pkgSrcExePath   = None
        othContentPaths = None                     
    (exe names)
        exeName      = None   
        setupExeName = DEFAULT_SETUP_NAME ("setup.exe")
    (IFW tool path) 
        qtIfwDirPath = None    (attempt to use environmental variable QT_IFW_DIR)
    (other IFW command line options)
        isDebugMode    = False
        otherqtIfwArgs = ""
    (Qt C++ Content extended details / requirements)
        isQtCppExe     = False
        isMingwExe     = False
        qtBinDirPath   = None  (attempt to use environmental variable QT_BIN_DIR)
        qmlScrDirPath  = None  (for QML projects only)                    

QtIfwConfigXml 

Objects of this type define the contents of a QtIFW 
config.xml which will be dynamically generated 
when invoking the buildInstaller function. This file 
represents the highest level definition of a QtIFW 
installer, containing information such as the product 
name and version. Most of the attributes in these 
objects correspond directly to the name of tags 
added to config.xml.  Attributes will None values
will not be written, otherwise they will be.

Constructor:                

    QtIfwConfigXml( name, exeName, version, publisher, 
                    iconFilePath=None, 
                    isDefaultTitle=True, isDefaultPaths=True ) 
              
Attributes:    

    exeName (used indirectly)
    iconFilePath  (used indirectly)
    Name                     
    Version                  
    Publisher                
    InstallerApplicationIcon  (icon base name, i.e. omit extension)
    Title                    
    TargetDir                
    StartMenuDir             
    RunProgram               
    RunProgramDescription    
    runProgramArgList  (used indirectly)
    otherElements (open end dictionary of key/value pairs to inject)

Convenience functions:

    setDefaultVersion()
    setDefaultTitle()    
    setDefaultPaths()
 
-------------------------------------------------------      
PipConfig

Objects of this type define the details for downloading
and/or installing Python libraries via the pip utility.
These objects are used directly by the installLibrary 
function as well indirectly via the obfuscation functions
and support classes.
    
Constructor:

    PipConfig( source = None
             , version = None
             , verEquality = "==" 
             , destPath = None
             , asSource = False
             , incDependencies = True        
             , isForced= False                
             , isUpgrade = False
             , otherPipArgs = "" ) 

Attributes:                        

    pipPath = "pip"  (i.e. on the system path)
    source          
    version         
    verEquality     
    destPath        
    asSource        
    incDependencies       
    isForced                  
    isUpgrade      
    otherPipArgs  (open ended argument string)      
         
------------------------------------------------------- 
OpyConfig i.e. OpyConfigExt( OpyConfig )
    
Objects of this type define obfuscation details for 
use by the Opy Library. Refer to the documentation 
for that library for details.

This library extends the natural OpyConfig, however,
adding the attributes / features described below.
See "ADDITIONAL OBFUSCATION FEATURES" for a 
description of how objects of this type are used.

Constructor:        

    OpyConfig( bundleLibs=None, sourceDir=None, patches=None )

Attributes:                

    bundleLibs (list of LibToBundle objects)
    sourceDir (dynamically defined when ommited)
    patches (list of OpyPatch objects)

OpyPatch

See "ADDITIONAL OBFUSCATION FEATURES" for a 
description of how objects of this type are used.
    
Constructor:

    OpyPatch( relPath, patches, parentDir=OBFUS_DIR_PATH )
        
Attributes:                    

    relPath 
    path    
    patches 
    
Convenience functions:

    obfuscatePath( obfuscatedFileDict )        
    apply()

LibToBundle 

See "ADDITIONAL OBFUSCATION FEATURES" for a 
description of how objects of this type are used.

Constructor:

    LibToBundle( name, localDirPath=None, pipConfig=None, isObfuscated=False )
    
Attributes:                    

    name         
    localDirPath 
    pipConfig    
    isObfuscated 
