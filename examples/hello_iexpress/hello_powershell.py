from distbuilder import IExpressPackageProcess, ConfigFactory

f = configFactory  = ConfigFactory()
f.productName      = "Hello PowerShell Example"
f.description      = "A Distribution Builder Example"
f.companyTradeName = "Some Company"
f.companyLegalName = "Some Company Inc."    
f.binaryName       = "HelloPowerShell"
f.version          = (1,0,0,0)
f.iconFilePath     = "../hello_world_tk/demo.ico" 
f.entryPointScript = "hello.ps1"  

p = IExpressPackageProcess( configFactory, isDesktopTarget=True )
p.isExeTest=True
p.run()       

