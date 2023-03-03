from burp import IBurpExtender, IContextMenuFactory, IHttpRequestResponse, ITab
from java.io import PrintWriter
from java.io import File as JFile
from java.util import ArrayList
from javax.swing import JMenuItem, JFileChooser, JButton, JOptionPane
from java.awt import Toolkit, BorderLayout
from java.awt.datatransfer import StringSelection
from javax.swing import JOptionPane, JPanel
import time
import os.path
import os
from datetime import datetime

class BurpExtender(IBurpExtender, IContextMenuFactory, IHttpRequestResponse, ITab):

    CUT_TEXT = "**TRUNCATED**"
    PATH = ""
    FILE_NAME = ""

    def str_to_array(self, string):
        return [ord(c) for c in string]

    def registerExtenderCallbacks(self, callbacks):
        callbacks.setExtensionName("Pr00f_me")
        print("For saving proofs ->\n1. Go to pr00f_me_tab to specify the folder where to save the proofs.\n2. Right click on request -> Extensions -> pr00f_me -> Save request & response.\n3. When a pop up window appears, enter a name for the proof. Extension will create a sub folder in specified working folder with a name of the proof. If the folder allready exists, it will append to that folder.\n4. Save format of the request and response is name + req/resp + time (_Y_m_d_H_M_S).")

        stdout = PrintWriter(callbacks.getStdout(), True)
        stderr = PrintWriter(callbacks.getStderr(), True)

        self.helpers = callbacks.getHelpers()
        self.callbacks = callbacks
        callbacks.registerContextMenuFactory(self)

        callbacks.addSuiteTab(self)

    # Implement ITab
    def getTabCaption(self):
        return "Pr00f_me_tab"
    
    def getUiComponent(self):
        panel = JPanel(BorderLayout())

        def b1Click (event):
            fc = JFileChooser()
            fc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
            res = fc.showOpenDialog(panel)
            if (res == JFileChooser.APPROVE_OPTION):
                if (fc.getSelectedFile().isDirectory()) :
                    self.PATH = JFile.getAbsolutePath(fc.getSelectedFile())
                    print ("Path to save proofs: " + self.PATH)
                    
            return
        # Button is ugly, need to fix that
        b1 = JButton("Set folder to save the proofs!", actionPerformed=b1Click)
        panel.add(b1, BorderLayout.PAGE_START)
        

        return panel

    # Implement IContextMenuFactory
    def createMenuItems(self, invocation):
        self.context = invocation
        menuList = ArrayList()

        menuList.add(JMenuItem("Copy HTTP Request (Full)",
                actionPerformed=self.copyRequest))
        menuList.add(JMenuItem("Copy HTTP Response (Full)",
                actionPerformed=self.copyResponse))
        menuList.add(JMenuItem("Save HTTP Request & Response",
                actionPerformed=self.saveRequestFullResponseFull))
        menuList.add(JMenuItem("Copy HTTP Request (Header)",
                actionPerformed=self.copyRequest_Header))
        menuList.add(JMenuItem("Copy HTTP Response (Header)",
                actionPerformed=self.copyResponse_Header))

        return menuList

    def saveRequestFullResponseFull(self, event):
        httpTraffic = self.context.getSelectedMessages()[0]
        httpRequest = httpTraffic.getRequest()
        httpResponse = httpTraffic.getResponse()

        req = self.stripTrailingNewlines(httpRequest)
        resp = self.stripTrailingNewlines(httpResponse)

        self.FILE_NAME = self.InfoBox()

        self.write_to_file_req(req)
        self.write_to_file_resp(resp) 

    def copyRequest(self, event):
        httpTraffic = self.context.getSelectedMessages()[0]
        httpRequest = httpTraffic.getRequest()

        data = self.stripTrailingNewlines(httpRequest)

        self.copyToClipboard(data)

    def copyResponse(self, event):
        httpTraffic = self.context.getSelectedMessages()[0]
        httpResponse = httpTraffic.getResponse()

        data = self.stripTrailingNewlines(httpResponse)

        self.copyToClipboard(data)

    def copyRequest_Header(self, event):
        httpTraffic = self.context.getSelectedMessages()[0]
        httpRequest = httpTraffic.getRequest()

        data = self.stripTrailingNewlines(httpRequest)
        data.append(13)
        data.extend(self.str_to_array(self.CUT_TEXT))

        self.copyToClipboard(data)
    
    def copyResponse_Header(self, event):
        httpTraffic = self.context.getSelectedMessages()[0]
        httpResponse = httpTraffic.getResponse()

        data = self.stripTrailingNewlines(httpResponse)
        data.append(13)
        data.extend(self.str_to_array(self.CUT_TEXT))

        self.copyToClipboard(data)

    def copyToClipboard(self, data, sleep=False):
        if sleep is True:
            time.sleep(1.5)

        # Fix line endings of the headers
        data = self.helpers.bytesToString(data).replace('\r\n', '\n')

        systemClipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
        systemSelection = Toolkit.getDefaultToolkit().getSystemSelection()
        transferText = StringSelection(data)
        systemClipboard.setContents(transferText, None)
        systemSelection.setContents(transferText, None)

    def stripTrailingNewlines(self, data):
        while data[-1] in (10, 13):
            data = data[:-1]
        return data
    
    def write_to_file_req(self, data):

        time = datetime.now()
        path = self.PATH

        file_name = self.FILE_NAME
        full_path = path + "/" + file_name

        if os.path.exists(full_path) == True:
            completeName = os.path.join(full_path,file_name)
            data = self.helpers.bytesToString(data).replace('\r\n', '\n')
            f = open(completeName + "_request_" + time.strftime("%Y%m%d%H%M%S") +".txt", 'w')
            f.write(data)
            f.close()
        else:
            os.makedirs(full_path)
            completeName = os.path.join(full_path,file_name)
            data = self.helpers.bytesToString(data).replace('\r\n', '\n')
            f = open(completeName + "_request_" + time.strftime("%Y%m%d%H%M%S") +".txt", 'w')
            f.write(data)
            f.close()


    
    def write_to_file_resp(self, data):
        time = datetime.now()
        path = self.PATH

        file_name = self.FILE_NAME
        full_path = path + "/" + file_name

        if os.path.exists(full_path) == True:
            completeName = os.path.join(full_path,file_name)
            data = self.helpers.bytesToString(data).replace('\r\n', '\n')
            f = open(completeName + "_response_" + time.strftime("%Y%m%d%H%M%S") +".txt", 'w')
            f.write(data)
            f.close()
        else:
            os.makedirs(full_path)
            completeName = os.path.join(full_path,file_name)
            data = self.helpers.bytesToString(data).replace('\r\n', '\n')
            f = open(completeName + "_response_" + time.strftime("%Y%m%d%H%M%S") +".txt", 'w')
            f.write(data)
            f.close()
    
    def InfoBox(event):
        titleBar = "Name"
        name = JOptionPane.showInputDialog(titleBar, "")
        return name