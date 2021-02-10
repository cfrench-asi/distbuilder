from distbuilder import( SelfSignedCertConfig, 
                         getPassword, generateTrustCerts, buildTrustCertInstaller ) 

companyTradeName = "Some Company"
companyLegalName = "Some Company Inc."
iconFilePath     = "../../hello_world_tk/demo.ico"
password         = getPassword( isGuiPrompt=True )

# generate code signing files to retain (securely!) in house
caCertPath, pfxFilePath = generateTrustCerts( 
    SelfSignedCertConfig( companyTradeName ), pfxPassword=password, isOverwrite=True )

# build an installer to distribute to users
buildTrustCertInstaller( 
    companyTradeName, caCertPath, pfxFilePath, pfxPassword=password,
    companyLegalName=companyLegalName, iconFilePath=iconFilePath, 
    isSilent=False, isDesktopTarget=True, isTest=True )