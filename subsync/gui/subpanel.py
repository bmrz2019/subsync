import subsync.gui.layout.subpanel
import wx
import os
from subsync.synchro import SubFile, RefFile
from subsync.settings import settings
from subsync.gui import openwin
from subsync.gui.components import filedrop
from subsync.gui.errorwin import error_dlg


class InputPanel(subsync.gui.layout.subpanel.SubtitlePanel):
    ''' This is subtitle or reference panel used on MainWin
    '''
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        filedrop.setFileDropTarget(self, OnDropFile=self.onDropSubFile)
        self.stream = None
        self.defaultLangKey = None

    @error_dlg
    def onButtonSubOpenClick(self, event):
        stream = self.stream
        if not stream.isOpen():
            stream = openwin.showOpenFileDlg(self, self.stream)
        self.showOpenWin(stream)

    def showOpenWin(self, stream):
        if stream != None and stream.isOpen():
            defaultLang = settings().get(self.defaultLangKey)
            with openwin.OpenWin(self, stream, defaultLang=defaultLang) as dlg:
                if dlg.ShowModal() == wx.ID_OK and dlg.file.isOpen():
                    self.setStream(dlg.file)
                    settings().setValue(self.defaultLangKey, dlg.defaultLang)

    def onChoiceSubLang(self, event):
        lang = self.m_choiceSubLang.GetValue()
        self.stream.lang = lang
        settings().setValue(self.defaultLangKey, lang)

    def onDropSubFile(self, x, y, filename):

        @error_dlg
        def showOpenWinWithFile(filename):
            stream = openwin.readStream(self, self.stream, filename)
            settings().lastdir = os.path.dirname(filename)
            self.showOpenWin(stream)

        # this is workaround for Windows showing drag&drop cursor inside OpenWin
        # and locking explorer window from where the file was dragged
        wx.CallAfter(showOpenWinWithFile, filename)
        return True

    def setStream(self, stream):
        if stream != None and stream.isOpen():
            self.stream = stream
            self.m_textSubPath.SetValue('{}:{}'.format(self.stream.path, self.stream.no + 1))
            self.m_textSubPath.SetInsertionPoint(self.m_textSubPath.GetLastPosition())
            self.m_choiceSubLang.SetValue(self.stream.lang)


class SubPanel(InputPanel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.stream = SubFile()
        self.defaultLangKey = 'lastSubLang'


class RefPanel(InputPanel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.stream = RefFile()
        self.defaultLangKey = 'lastRefLang'
