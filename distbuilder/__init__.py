# DOCS > NULL
from ._version import __version__ 

# DOCS > Config Factory.md
from distbuilder.process import ConfigFactory

# DOCS > Qt Installer Framework.md
from distbuilder.process import RobustInstallerProcess
from distbuilder.qt_installer import( 
      QtIfwConfig 
    , QtIfwConfigXml 
    , QtIfwControlScript 
    , QtIfwPackage 
    , QtIfwPackageXml 
    , QtIfwPackageScript 
    , QtIfwShortcut 
    , QtIfwExternalOp 
    , QtIfwKillOp 
    , QtIfwExeWrapper 
    , QtIfwExternalResource 
    , QtIfwUiPage 
    , QtIfwDynamicOperationsPage
    , QtIfwSimpleTextPage 
    , QtIfwTargetDirPage     
    , QtIfwWidget 
    , QtIfwOnFinishedDetachedExec 
    , QtIfwOnFinishedCheckbox 
    , installQtIfw 
    , unInstallQtIfw 
    , buildInstaller 
    , findQtIfwPackage 
    , removeQtIfwPackage 
    , mergeQtIfwPackages 
    , nestQtIfwPackage 
    , joinPathQtIfw 
    , qtIfwDynamicValue 
    , qtIfwOpDataPath 
    , qtIfwDetachedOpDataPath
    , QT_IFW_VERBOSE_SWITCH 
    , QT_IFW_DYNAMIC_VARS 
    , QT_IFW_TARGET_DIR 
    , QT_IFW_DEFAULT_TARGET_DIR 
    , QT_IFW_HOME_DIR 
    , QT_IFW_DESKTOP_DIR  
    , QT_IFW_APPS_DIR 
    , QT_IFW_APPS_X86_DIR 
    , QT_IFW_APPS_X64_DIR 
    , QT_IFW_STARTMENU_DIR 
    , QT_IFW_USER_STARTMENU_DIR 
    , QT_IFW_ALLUSERS_STARTMENU_DIR 
    , QT_IFW_ROOT_DIR 
    , QT_IFW_TEMP_DIR
    , QT_IFW_SCRIPTS_DIR 
    , QT_IFW_INSTALLER_TEMP_DIR 
    , QT_IFW_MAINTENANCE_TEMP_DIR 
    , QT_IFW_INSTALLER_DIR 
    , QT_IFW_INTALLER_PATH
    , QT_IFW_USER 
    , QT_IFW_PRODUCT_NAME 
    , QT_IFW_PRODUCT_VERSION 
    , QT_IFW_TITLE 
    , QT_IFW_PUBLISHER 
    , QT_IFW_URL 
    , QT_IFW_OS 
    , QT_IFW_INTRO_PAGE 
    , QT_IFW_TARGET_DIR_PAGE 
    , QT_IFW_COMPONENTS_PAGE 
    , QT_IFW_LICENSE_PAGE 
    , QT_IFW_START_MENU_PAGE 
    , QT_IFW_READY_PAGE 
    , QT_IFW_INSTALL_PAGE 
    , QT_IFW_FINISHED_PAGE 
    , QT_IFW_REPLACE_PAGE_PREFIX 
    , QT_IFW_PRE_INSTALL 
    , QT_IFW_POST_INSTALL 
)
       
# DOCS > PyInstaller.md       
from distbuilder.process import( 
      PyToBinPackageProcess 
    , PyToBinInstallerProcess
)
from distbuilder.py_installer import( 
      PyInstallerConfig 
    , PyInstSpec 
    , PyInstHook 
    , pyScriptToExe
    , makePyInstSpec 
    , installPyInstaller 
    , uninstallPyInstaller 
    , PyInstallerVersion 
    , PyInstallerMajorVer 
    , PyInstallerMajorMinorVer
)

# DOCS > IExpress.md
from distbuilder.process import( 
      IExpressPackageProcess
    , IExpressInstallerProcess
)
from distbuilder.iexpress import( 
      IExpressConfig
    , batchScriptToExe
    , powerShellScriptToExe
    , vbScriptToExe
    , jScriptToExe  
    , iExpResPath 
    , iExpEmbResPath
    , iExpLibPath
)

# DOCS > Code Signing.md
from distbuilder.code_sign import( 
      SelfSignedCertConfig 
    , CodeSignConfig 
    , TrustInstallerBuilderProcess 
    , SIGNTOOL_PATH_ENV_VAR 
    , MAKECERT_PATH_ENV_VAR 
    , PVK2PFX_PATH_ENV_VAR 
    , trustCertInstallerConfigFactory 
    , generateTrustCerts 
    , signExe 
)

# DOCS > Python Obfuscation.md
from distbuilder.opy_library import( 
      OpyConfigExt as OpyConfig 
    , OpyPatch 
    , LibToBundle 
    , obfuscatePy 
    , opyAnalyze 
    , createStageDir 
    , obfuscatedId 
)

ExtLibHandling = OpyConfig.ExtLibHandling 

# DOCS > Python pip.md
from distbuilder.pip_installer import( 
      PipConfig 
    , updatePip 
    , installLibraries 
    , installLibrary 
    , uninstallLibrary 
    , vcsUrl
)

# DOCS > Qt CPP.md 
""" DOCS > VIRTUAL
from distbuilder.qt_cpp import (
    QtCppConfig, 
    qmakeInit, installDeployTools, renameExe, 
    qmakeMasterConfigFactory, qmakePackageConfigFactory, 
    qmakeArgs, qmakeArgParser 
)
"""
            
# DOCS > Logging.md            
from distbuilder.log import( 
    Logger, startLogging, stopLogging, isLogging, log )

# DOCS > Utility Classes.md            
from distbuilder.util import(
      RawConfigParser, ConfigParser, SafeConfigParser
    , ExecutableScript    
    , WindowsExeVersionInfo        
)

# DOCS > Utility Functions.md            
from distbuilder.util import(
      absPath 
    , homePath
    , desktopPath     
    , toNativePath 
    , exists 
    , isFile 
    , isDir 
    , isParentDir 
    , copyFile 
    , removeFile 
    , makeDir 
    , copyDir 
    , removeDir 
    , move 
    , rename 
    , tempDirPath 
    , reserveTempFilePath 
    , dirPath 
    , joinPath 
    , splitPath 
    , splitExt 
    , joinExt 
    , baseFileName
    , rootFileName 
    , normBinaryName 
    , normIconName 
    , normLibName
    , normConfigName
    , allPathPattern
    , extPathPattern 
    , startsWithPathPattern
    , endsWithPathPattern
    , containsPathPattern
    , copyToDir 
    , moveToDir 
    , removeFromDir 
    , renameInDir 
    , moveToDesktop 
    , copyToDesktop 
    , moveToHomeDir 
    , copyToHomeDir 
    , collectDirs 
    , mergeDirs 
    , getEnv 
    , setEnv 
    , delEnv 
    , isDebug 
    , _run 
    , run 
    , runPy 
    , toZipFile 
    , toCabFile        
    , isImportableModule 
    , isImportableFromModule 
    , modulePath 
    , modulePackagePath 
    , sitePackagePath 
    , importFromPath 
    , printErr 
    , printExc 
    , halt 
    , download 
    , versionTuple 
    , versionStr 
    , versionNo 
    , getPassword 
    , assertMinVer
    , embedExeVerInfo
    , embedExeIcon
    , extractExeIcons
    , copyExeVerInfo
    , copyExeIcon
    , embedManifest
    , embedAutoElevation    
)

def assertBuilderVer( ver ): 
    assertMinVer( __version__, ver, descr="Distribution Builder Library" )

# DOCS > Utility Constants.md            
from distbuilder.util import(
      IS_WINDOWS 
    , IS_LINUX 
    , IS_MACOS 
    , PY2 
    , PY3 
    , BIT_CONTEXT 
    , IS_32_BIT_CONTEXT 
    , IS_64_BIT_CONTEXT 
    , IS_ARM_CPU 
    , IS_INTEL_CPU 
    , THIS_DIR 
    , CURRENT_USER, ALL_USERS 
    , DEBUG_ENV_VAR_NAME, DEBUG_ENV_VAR_VALUE
    , ALL 
)
