# Pr00f_me
Small burp extension for easier saving proofs

## Installation
Since this extension is written in Python(Jython), such is needed before installing. For instructions on how to install Jython refer to -> https://portswigger.net/support/how-to-install-an-extension-in-burp-suite.

To install the extension, go to Extender -> Extensions -> Add -> Under extension type select Python -> load Pr00f_me.py.

## Usage
For saving proofs ->
1. Go to pr00f_me_tab to specify the folder where to save the proofs.
2. Right click on request -> Extensions -> pr00f_me -> Save request & response.
3. When a pop up window appears, enter a name for the proof. Extension will create a sub folder in specified working folder with a name of the proof. If the folder allready exists, it will append to that folder.
4. Save format of the request and response is name + req/resp + time (_Y_m_d_H_M_S).
