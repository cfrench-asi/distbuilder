:: Uncomment for raw/direct script development
:: Comment out for IExpress Context...
::set "LIB_DIR=."

set "PopupLib=%LIB_DIR%\popup.bat"

Call %PopupLib% ShowInfoPopup "Hello World!"
Call %PopupLib% ShowErrorPopup "Whoops!" 
