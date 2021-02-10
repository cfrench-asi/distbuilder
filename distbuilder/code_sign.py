from distbuilder import util    # @UnusedImport
from distbuilder.util import *  # @UnusedWildImport

_PS_SELF_CERT_VER_REQ = 4 # found on Windows 8.1+
__isPsSelfCert = None
def _isPsSelfCertMethod():
    global __isPsSelfCert
    if __isPsSelfCert is None:
        __isPsSelfCert = (
            util._powerShellMajorVersion() >= _PS_SELF_CERT_VER_REQ )
    return __isPsSelfCert

_RES_DIR_PATH = util._toLibResPath( joinPath( "code_sign_res", 
    ("linux" if IS_LINUX else "macos" if IS_MACOS else "windows") ) )

# WINDOWS CODE SIGNING
#------------------------------------------------------------------------------
SIGNTOOL_PATH_ENV_VAR = "SIGNTOOL_PATH"
            
class SignToolConfig:

    DEFAULT_DIGEST           = "sha256"
    DEFAULT_TIMESTAMP_SERVER = "http://timestamp.digicert.com"
    
    __RES_DIR_NAME = "signtool"
    __MSI_NAME     = "Windows SDK Signing Tools-x86_en-us.msi"
    
    __WINDOWS_KITS_DIR = r"Windows Kits\10\bin\10.0.19041.0" 
    __INTEL_32BIT_DIR  = "x86"
    __INTEL_64BIT_DIR  = "x64"
    __ARM_32BIT_DIR    = "arm"
    __ARM_64BIT_DIR    = "arm64"
    __SIGNTOOL_NAME    = "signtool.exe"

    @staticmethod
    def _builtInInstallerPath():    
        return joinPath( _RES_DIR_PATH, 
            SignToolConfig.__RES_DIR_NAME, SignToolConfig.__MSI_NAME )

    @staticmethod
    def _defaultSignToolPath( isVerified=False ):    
        if IS_ARM_CPU:
            subDirName =( SignToolConfig.__ARM_32BIT_DIR 
                          if IS_32_BIT_CONTEXT else 
                          SignToolConfig.__ARM_64BIT_DIR )
        else:
            subDirName =( SignToolConfig.__INTEL_32BIT_DIR 
                          if IS_32_BIT_CONTEXT else 
                          SignToolConfig.__INTEL_64BIT_DIR )                  
        path = joinPath( util._winProgs86DirPath(), 
            SignToolConfig.__WINDOWS_KITS_DIR, subDirName, 
            SignToolConfig.__SIGNTOOL_NAME )
        if isVerified and not isFile( path ): path = None            
        return path 

    def __init__( self, pfxFilePath=None, pfxPassword=None ):
  
        self.pfxFilePath  = absPath( pfxFilePath )
        self.pfxPassword  = pfxPassword
 
        self.signToolPath = None # if None, this will be auto resolved 
       
        self.fileDigest         = SignToolConfig.DEFAULT_DIGEST        
        self.timeStampDigest    = SignToolConfig.DEFAULT_DIGEST
        self.timeStampServerUrl = SignToolConfig.DEFAULT_TIMESTAMP_SERVER
        self.otherSignToolArgs  = ""
        
        self.isDebugMode = True

    def __str__( self ) :
        if not isFile( self.pfxFilePath ):
            raise Exception( 
                "Missing or invalid pfx path in SignToolConfig: %s" %
                (self.pfxFilePath,) )        
        operation       = "sign"        
        verbose         = '/v' if self.isDebugMode else ''
        fileDigest      = "/fd %s" % (self.fileDigest,)
        timeStampServer = "/tr %s" % (self.timeStampServerUrl,)
        timeStampDigest = "/td %s" % (self.timeStampDigest,)
        pfxFilePath     = '/f "%s"' % (self.pfxFilePath,)
        pfxPassword     =('/p "%s"' % (self.pfxPassword,) 
                          if self.pfxPassword else "" )                                
        tokens = (operation, verbose, fileDigest, 
                  timeStampServer, timeStampDigest, pfxFilePath, pfxPassword,
                  self.otherSignToolArgs)
        return ' '.join( (('%s ' * len(tokens)) % tokens).split() )        

def __useSignTool( exePath, signToolConfig ):
    __validateSignToolConfig( signToolConfig )
    cmd = '"%s" %s "%s"' % ( signToolConfig.signToolPath, 
                             str(signToolConfig), exePath )
    if not util._isSystemSuccess( cmd ): 
        raise Exception( 'FAILED to code sign "%s"' % (exePath,) )
    print( "Signed successfully!" )
    return exePath           

def __validateSignToolConfig( cfg ):
    if not isFile( cfg.pfxFilePath ):         
        raise Exception( "Missing or invalid PFX file path: %s" % 
                         (cfg.pfxFilePath,) )
    if cfg.signToolPath is None: 
        cfg.signToolPath = getenv( SIGNTOOL_PATH_ENV_VAR )    
    if cfg.signToolPath is None: 
        cfg.signToolPath = (
            SignToolConfig._defaultSignToolPath( isVerified=True ) )    
    if cfg.signToolPath is None: 
        cfg.signToolPath = __installSignTool()   
    if cfg.signToolPath is None: 
        raise Exception( "Valid SignTool path required" )

def __installSignTool():
    print( "Installing SignTool utility...\n" )
    if not util._isSystemSuccess( SignToolConfig._builtInInstallerPath() ): 
        raise Exception( "SignTool installation FAILED" )
    return SignToolConfig._defaultSignToolPath( isVerified=True )

#------------------------------------------------------------------------------
MAKECERT_PATH_ENV_VAR = "MAKECERT_PATH"
            
class SelfSignedCertConfig:

    NO_MAX_CHILDREN      = 0
    LIFETIME_SIGNING_EKU = '1.3.6.1.5.5.7.3.3,1.3.6.1.4.1.311.10.3.13'
    DEFAULT_END_DATE     = '12/31/2050'
        
    __RES_DIR_NAME = "makecert"

    __INTEL_32BIT_DIR  = "x86"
    __INTEL_64BIT_DIR  = "x64"
    __ARM_32BIT_DIR    = "arm" # Not actually present...
    __ARM_64BIT_DIR    = "arm64"
    __MAKECERT_NAME    = "makecert.exe"

    __CA_CERT_EXT      = ".cer"
    __SUBJECT_KEY_EXT  = ".pvk"
    __PFX_EXT          = ".pfx"
   
    @staticmethod
    def _builtInMakeCertPath( isVerified=False ):    
        if IS_ARM_CPU:
            subDirName =( SelfSignedCertConfig.__ARM_32BIT_DIR 
                          if IS_32_BIT_CONTEXT else 
                          SelfSignedCertConfig.__ARM_64BIT_DIR )
        else:
            subDirName =( SelfSignedCertConfig.__INTEL_32BIT_DIR 
                          if IS_32_BIT_CONTEXT else 
                          SelfSignedCertConfig.__INTEL_64BIT_DIR )                  
        path = joinPath( _RES_DIR_PATH, 
            SelfSignedCertConfig.__RES_DIR_NAME, subDirName, 
            SelfSignedCertConfig.__MAKECERT_NAME )
        if isVerified and not isFile( path ): path = None            
        return path 

    def __init__( self, companyTradeName, destDirPath=None ):
    
        self.commonName  = companyTradeName
        self.endDate     = SelfSignedCertConfig.DEFAULT_END_DATE

        self.destDirPath = destDirPath if destDirPath else THIS_DIR        
        outputRoot = companyTradeName.replace(" ", "").replace(".", "")        
        self.caCertPath     = joinPath( self.destDirPath, 
            joinExt( outputRoot, SelfSignedCertConfig.__CA_CERT_EXT) )
        self.privateKeyPath = joinPath( self.destDirPath, 
            joinExt( outputRoot, 
                SelfSignedCertConfig.__PFX_EXT if _isPsSelfCertMethod() else 
                SelfSignedCertConfig.__SUBJECT_KEY_EXT ) )
        
        self.makeCertPath = None # if None, this will be auto resolved 

        self._maxCertChildren  = SelfSignedCertConfig.NO_MAX_CHILDREN       
        self._enhancedKeyUsage = SelfSignedCertConfig.LIFETIME_SIGNING_EKU        
        self.otherArgs         = ""
        self.isDebugMode = True

    def __str__( self ) :
        name               = '/n "CN=%s"' % (self.commonName,)
        selfSignedRootCert = '/r'
        maxCertChildren    = '/h %d' % (self._maxCertChildren,)
        enhancedKeyUsage   = '/eku %s' % (self._enhancedKeyUsage,)
        endDate            = '/e %s' % (self.endDate,)
        privateKeyPath     = '/sv "%s"' % (self.privateKeyPath,)
        caCertPath         = '"%s"' % (self.caCertPath,)                       
        tokens = (name, selfSignedRootCert, maxCertChildren,
                  enhancedKeyUsage, endDate, self.otherArgs,
                  privateKeyPath, caCertPath )
        return ' '.join( (('%s ' * len(tokens)) % tokens).split() )        

def __useMakeCert( certConfig, isOverwrite ):
    __validateSelfSignedCertConfig( certConfig, isOverwrite )
    cmd = '"%s" %s' % ( certConfig.makeCertPath, str(certConfig) )
    if( not util._isSystemSuccess( cmd ) or
        not isFile( certConfig.caCertPath ) or
        not isFile( certConfig.privateKeyPath ) ): 
        raise Exception( 'FAILED to generate code signing certificates' )
    print( "Generated code signing certificates successfully!" )
    return certConfig.caCertPath, certConfig.privateKeyPath

def __usePsSelfSignedCertScript( certConfig, pfxPassword, isOverwrite ):
    __validateSelfSignedCertConfig( certConfig, isOverwrite )
    util._runPowerShell([
         'New-SelfSignedCertificate '
            '-CertStoreLocation Cert:\CurrentUser\My '
            '-Type "CodeSigningCert" '
            '-Subject "CN={commonName}" '
            '-FriendlyName "{commonName}" '
            '-KeyExportPolicy Exportable '
            '-NotAfter "{endDate}" {otherArgs}'
        ,'$newCert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert | '
            'Where-Object Subject -EQ "CN={commonName}"'    
        ,'Export-Certificate -Cert $newCert -FilePath "{caCertPath}"'
    ] + ([
         '$pwd = ConvertTo-SecureString -String "{pfxPassword}" -Force -AsPlainText'
        ,'Export-PfxCertificate -Cert $newCert -FilePath "{privateKeyPath}" '
            '-Password $pwd'
    ] if pfxPassword else [
        'Export-PfxCertificate -Cert $newCert -FilePath "{privateKeyPath}"'
    ]) + [
        '$newCert | Remove-Item'        
    ]            
    , replacements={ "commonName"    : certConfig.commonName
                   , "endDate"       : certConfig.endDate
                   , "otherArgs"     : certConfig.otherArgs
                   , "caCertPath"    : certConfig.caCertPath
                   , "privateKeyPath": certConfig.privateKeyPath
                   , "pfxPassword"   : pfxPassword
    })
    if( not isFile( certConfig.caCertPath ) or
        not isFile( certConfig.privateKeyPath ) ): 
        raise Exception( 'FAILED to generate code signing certificates' )
    print( "Generated code signing certificates successfully!" )
    return certConfig.caCertPath, certConfig.privateKeyPath

def __validateSelfSignedCertConfig( cfg, isOverwrite ):
    if isDir( cfg.destDirPath ): 
        if isOverwrite:
            removeFromDir( baseFileName(cfg.caCertPath),     cfg.destDirPath )
            removeFromDir( baseFileName(cfg.privateKeyPath), cfg.destDirPath )
        else:
            if isFile( cfg.caCertPath ):
                raise Exception( "File exists: %s" % (cfg.caCertPath,) )
            if isFile( cfg.privateKeyPath ):
                raise Exception( "File exists: %s" % (cfg.privateKeyPath,) )
    else: makeDir( cfg.destDirPath )                                        
    
    if _isPsSelfCertMethod(): return
    if cfg.makeCertPath is None: 
        cfg.makeCertPath = getenv( MAKECERT_PATH_ENV_VAR )    
    if cfg.makeCertPath is None: 
        cfg.makeCertPath = SelfSignedCertConfig._builtInMakeCertPath()
    if cfg.makeCertPath is None: 
        raise Exception( "Valid MakeCert path required" )

#------------------------------------------------------------------------------
PVK2PFX_PATH_ENV_VAR = "PVK2PFX_PATH"
            
class Pvk2PfxConfig:

    __RES_DIR_NAME         = "sdk_tools"
    __INTEL_32BIT_MSI_NAME = "Windows SDK Desktop Tools x86-x86_en-us.msi"
    __INTEL_64BIT_MSI_NAME = "Windows SDK Desktop Tools x64-x86_en-us.msi"
    __ARM_32BIT_MSI_NAME   = "Windows SDK ARM Desktop Tools-x86_en-us.msi"
    __ARM_64BIT_MSI_NAME   = "Windows SDK Desktop Tools arm64-x86_en-us.msi"
    
    __WINDOWS_KITS_DIR = r"Windows Kits\10\bin\10.0.19041.0" 
    __INTEL_32BIT_DIR  = "x86"
    __INTEL_64BIT_DIR  = "x64"
    __ARM_32BIT_DIR    = "arm"
    __ARM_64BIT_DIR    = "arm64"
    __PVK2PFX_NAME     = "pvk2pfx.exe"
    
    _PFX_EXT = ".pfx"

    @staticmethod
    def _builtInInstallerPath():    
        return joinPath( util._RES_DIR_PATH, 
            Pvk2PfxConfig.__RES_DIR_NAME, Pvk2PfxConfig.__MSI_NAME )

    @staticmethod
    def _defaultPvk2PfxPath( isVerified=False ):    
        if IS_ARM_CPU:
            subDirName =( Pvk2PfxConfig.__ARM_32BIT_DIR 
                          if IS_32_BIT_CONTEXT else 
                          Pvk2PfxConfig.__ARM_64BIT_DIR )
        else:
            subDirName =( Pvk2PfxConfig.__INTEL_32BIT_DIR 
                          if IS_32_BIT_CONTEXT else 
                          Pvk2PfxConfig.__INTEL_64BIT_DIR )                  
        path = joinPath( util._winProgs86DirPath(), 
            Pvk2PfxConfig.__WINDOWS_KITS_DIR, subDirName, 
            Pvk2PfxConfig.__PVK2PFX_NAME )
        if isVerified and not isFile( path ): path = None            
        return path 

    def __init__( self, caCertPath, privateKeyPath, 
                  pfxPassword=None, pfxFilePath=None ):

        self.caCertPath     = absPath( caCertPath )        
        self.privateKeyPath = absPath( privateKeyPath )
        self.pfxPassword    = pfxPassword  
        self.pfxFilePath    =( pfxFilePath if pfxFilePath else
            joinExt( splitExt( privateKeyPath )[0], Pvk2PfxConfig._PFX_EXT ) )
 
        self.pvk2PfxPath = None # if None, this will be auto resolved 
       
        self.otherArgs  = ""
        
        self.isDebugMode = True

    def __str__( self ) :
        if not isFile( self.privateKeyPath ):
            raise Exception( 
                "Missing or invalid private key path in Pvk2PfxConfig: %s" %
                (self.privateKeyPath,) )        
        if not isFile( self.caCertPath ):
            raise Exception( 
                "Missing or invalid CA cert path in Pvk2PfxConfig: %s" %
                (self.caCertPath,) )                
        privateKeyPath =  '/pvk "%s"' % (self.privateKeyPath,)
        caCertPath     =  '/spc "%s"' % (self.caCertPath,)
        pfxFilePath    =  '/pfx "%s"' % (self.pfxFilePath,)
        pfxPassword    =( '/pi "%s"'  % (self.pfxPassword,) 
                          if self.pfxPassword else "" )
        tokens = (privateKeyPath, caCertPath, pfxFilePath, pfxPassword,
                  self.otherArgs)
        return ' '.join( (('%s ' * len(tokens)) % tokens).split() )        

def __usePvk2Pfx( pvk2PfxConfig, isOverwrite ):
    __validatePvk2PfxConfig( pvk2PfxConfig, isOverwrite )
    cmd = '"%s" %s' % ( pvk2PfxConfig.pvk2PfxPath, str(pvk2PfxConfig) )
    if( not util._isSystemSuccess( cmd ) or 
        not isFile( pvk2PfxConfig.pfxFilePath ) ): 
        raise Exception( 'FAILED convert private key to PFX file' )
    print( "Generated Personal Information Exchange (PFX) file successfully!" )
    return pvk2PfxConfig.pfxFilePath

def __validatePvk2PfxConfig( cfg, isOverwrite ):
    if not isFile( cfg.privateKeyPath ):
        raise Exception( 
            "Missing or invalid private key path in Pvk2PfxConfig: %s" %
            (cfg.privateKeyPath,) )        
    if not isFile( cfg.caCertPath ):
        raise Exception( 
            "Missing or invalid CA cert path in Pvk2PfxConfig: %s" %
            (cfg.caCertPath,) )
    if isOverwrite:
        removeFromDir( baseFileName( cfg.pfxFilePath ), 
                            dirPath( cfg.pfxFilePath ) )
    elif isFile( cfg.pfxFilePath ):
        raise Exception( "File exists: %s" % (cfg.pfxFilePath,) )
    else: makeDir( cfg.destDirPath )                                         
                        
    if cfg.pvk2PfxPath is None: 
        cfg.pvk2PfxPath = getenv( PVK2PFX_PATH_ENV_VAR )    
    if cfg.pvk2PfxPath is None: 
        cfg.pvk2PfxPath = (
            Pvk2PfxConfig._defaultPvk2PfxPath( isVerified=True ) )    
    if cfg.pvk2PfxPath is None: 
        cfg.pvk2PfxPath = __installPvk2Pfx()   
    if cfg.pvk2PfxPath is None: 
        raise Exception( "Valid Pvk2Pfx path required" )

def __installPvk2Pfx():
    print( "Installing Pvk2Pfx utility...\n" )
    if not util._isSystemSuccess( Pvk2PfxConfig._builtInInstallerPath() ): 
        raise Exception( "Pvk2Pfx installation FAILED" )
    return Pvk2PfxConfig._defaultPvk2PfxPath( isVerified=True )

#------------------------------------------------------------------------------
def generateTrustCerts( certConfig, pfxPassword=None, isOverwrite=False ):
    """ Returns CA Cert Path, PFX Path """
    print( "Generating code signing certificates...\n" )
    if IS_WINDOWS:
        if _isPsSelfCertMethod():
            caCertPath, pfxPath = __usePsSelfSignedCertScript( 
                certConfig, pfxPassword, isOverwrite )
        else :
            caCertPath, privKeyPath = __useMakeCert( certConfig, isOverwrite )            
            pfxConfig = Pvk2PfxConfig( 
                caCertPath, privKeyPath, pfxPassword=pfxPassword )
            pfxPath = __usePvk2Pfx( pfxConfig, isOverwrite )
        return caCertPath, pfxPath            
    #TODO: SUPPORT OTHER PLATFORMS!!!
    util._onPlatformErr()

def buildTrustCertInstaller( companyTradeName, caCertPath, pfxFilePath,
            pfxPassword=None,
            companyLegalName=None, version=(1,0,0,0), iconFilePath=None, 
            isDesktopTarget=False, isHomeDirTarget=False,
            isSilent=False, isTest=False ):
    """
    Returns path to installer
    """
    print( "Building Trust Certificate Installer..." )    
    #TODO: SUPPORT OTHER PLATFORMS!!!
    if not IS_WINDOWS: util._onPlatformErr()
    
    from distbuilder.master import ConfigFactory, PyToBinPackageProcess
        
    script = ExecutableScript( "__installTrustCert", extension="py", script=[
         'import sys, os, traceback'
        ,'from subprocess import( check_call, check_output,'
        ,'    STARTUPINFO, STARTF_USESHOWWINDOW )'
        ,'try: from subprocess import DEVNULL' 
        ,'except ImportError: DEVNULL = open(os.devnull, "wb")'
        ,''
        ,'CA_PATH        = os.path.join( sys._MEIPASS, "{caFileName}" )'
        ,'ICON_PATH      = os.path.join( sys._MEIPASS, "{iconFileName}" )'
        ,'CERT_UTIL_PATH = "certutil"'
        ,'CERT_STORE     = "Root"'
        ,'CN_SEARCH      = b"Issuer: CN={commonName}"'
        ,'SUCCESS_TITLE  = "Installed Successfully"'
        ,'SUCCESS_MSG    = "{commonName} products will now be trusted on this PC!"'
        ,'SUCCESS_CODE   = 0'
        ,'FAILURE_TITLE  = "Installation Error"'
        ,'FAILURE_MSG    = "Could not install the {commonName} trust certificate!"'
        ,'FAILURE_CODE   = 1'
        ,'' 
        ,'startupInfo = STARTUPINFO()'
        ,'startupInfo.dwFlags |= STARTF_USESHOWWINDOW'
        ,'try:'       
        ,'    check_call( "\\"%s\\" -addStore \\"%s\\" \\"%s\\"" % '
        ,'        (CERT_UTIL_PATH, CERT_STORE, CA_PATH), '
        ,'        shell=False, startupinfo=startupInfo )'
        ,'    storeOutput = check_output( "\\"%s\\" -store \\"%s\\"" % '
        ,'        (CERT_UTIL_PATH, CERT_STORE), '
        ,'        shell=False, startupinfo=startupInfo, '
        ,'        stdin=DEVNULL, stderr=DEVNULL )'
        ,'    isSuccess = CN_SEARCH in storeOutput'                                        
        ,'except Exception as e: '              
        ,'    sys.stderr.write( traceback.format_exc() + "\\n\\n" )'  
        ,'    isSuccess = False'
        ,'if isSuccess: sys.stdout.write( SUCCESS_MSG )'    
        ,'else: sys.stderr.write( FAILURE_MSG )'
        ] + ([] if isSilent else [ 
         'try:    #PY3'
        ,'    from tkinter import Tk'
        ,'    import tkinter.messagebox as tkMessageBox' 
        ,'except: #PY2'
        ,'    from Tkinter import Tk'
        ,'    import tkMessageBox'
        ,'tkRoot = Tk()'
        ,'tkRoot.overrideredirect( 1 )'
        ,'if os.path.exists( ICON_PATH ): tkRoot.iconbitmap( ICON_PATH )'
        ,'tkRoot.withdraw()'
        ,'if isSuccess:'
        ,'    tkMessageBox.showinfo( SUCCESS_TITLE, SUCCESS_MSG,'
                                   ' parent=tkRoot )'
        ,'else:'
        ,'    tkMessageBox.showerror( FAILURE_TITLE, FAILURE_MSG,'
                                    ' parent=tkRoot )'              
        ]) +
        ['sys.exit( SUCCESS_CODE if isSuccess else FAILURE_CODE )'], 
        replacements={ "caFileName"   : baseFileName( caCertPath ) 
                     , "iconFileName" : baseFileName( iconFilePath )
                     , "commonName"   : companyTradeName } 
    )
    script.write( THIS_DIR )    
    
    compressedCompName = companyTradeName.replace(" ","").replace(".","")
    
    f = configFactory  = ConfigFactory()
    f.productName      = "Trust %s" % (companyTradeName,)
    f.description      = "Trust Certificate Installer"
    f.binaryName       = "Trust%s" % (compressedCompName,)
    f.companyTradeName = companyTradeName 
    f.companyLegalName = companyLegalName
    f.isGui            = not isSilent    
    f.iconFilePath     = iconFilePath 
    f.version          = version
    f.isOneFile        = True                   
    f.entryPointPy     = script.fileName()  
    
    class TrustInstallerBuilderProcess( PyToBinPackageProcess ):               
        def onPyInstConfig( self, cfg ): 
            cfg.isAutoElevated = True
            cfg.dataFilePaths  = [ caCertPath ]            
            
        def onFinalize( self ):
            removeFromDir( script.fileName(), THIS_DIR )
            # sign the installer itself
            signConfig = SignToolConfig( pfxFilePath=absPath( pfxFilePath ),
                                         pfxPassword=pfxPassword ) 
            signExe( self.binPath, signConfig )                                                                
    p = TrustInstallerBuilderProcess( configFactory )       
    p.run()     
    
    if isDesktopTarget:   installerPath = moveToDesktop( p.binPath )
    elif isHomeDirTarget: installerPath = moveToHomeDir( p.binPath )    
    else :                installerPath = moveToDir( p.binPath, THIS_DIR )
    removeDir( p.binDir )    
    if isTest: run( installerPath, isElevated=True, isDebug=True )
    return installerPath 
         
def signExe( exePath, signToolConfig ):
    exePath = normBinaryName( exePath, isPathPreserved=True )
    print( "Code signing %s...\n" % (exePath,) )
    if IS_WINDOWS: return __useSignTool( exePath, signToolConfig )    
    #TODO: SUPPORT OTHER PLATFORMS!!!
    util._onPlatformErr()
        