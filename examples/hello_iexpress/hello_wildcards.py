from distbuilder import( IExpressPackageProcess, ConfigFactory, 
                         ExecutableScript, allPathPattern, extPathPattern )

f = configFactory  = ConfigFactory()
f.productName      = "Hello Wildcards Example"
f.description      = "A Distribution Builder Example"
f.companyTradeName = "Some Company"
f.companyLegalName = "Some Company Inc."    
f.binaryName       = "HelloWildcards"
f.version          = (1,0,0,0)
f.iconFilePath     = "../hello_world_tk/demo.ico" 
f.entryPointScript = ExecutableScript( 
    "popup", extension=ExecutableScript.BATCH_EXT, script=(
    r'start "Message" /wait cmd /c '
        '"echo PWD: %CD% & echo RES: %RES_DIR% & pause"') ) 

# If embedding, check the contents of the "RES_DIR" (temp director) upon 
# running the program.  That path will be displayed at runtime by the entry 
# script.  It will be deleted when the program has terminated.     
IS_EMBEDDED = True

# Note: Paths are implicitly relative to the executing script's directory. 
# You may use straight forward, literal glob patterns. 
#RES_PATTERN     = "test_res/*"
#SCRIPTS_PATTERN = "test_scr/*.bat"
# Or, you may employ path / pattern building functions.  
RES_PATTERN     = allPathPattern( "test_res" )
SCRIPTS_PATTERN = extPathPattern( "bat", "test_scr" )

if not IS_EMBEDDED: 
    f.distResources = [ RES_PATTERN, SCRIPTS_PATTERN ]
 
class BuildProcess( IExpressPackageProcess ):
    def onIExpressConfig(self, cfg):
        if IS_EMBEDDED:
            cfg.embeddedResources = [ RES_PATTERN ]
            cfg.scriptImports     = [ SCRIPTS_PATTERN ]

p = BuildProcess( configFactory, isDesktopTarget=True, 
                  isZipped=(not IS_EMBEDDED) )
p.isExeTest=True 
p.run()       
