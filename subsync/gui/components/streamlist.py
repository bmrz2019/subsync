import wx
import wx.lib.mixins.listctrl


class StreamList(wx.ListCtrl, wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin.__init__(self)
        self.InsertColumn(0, _('id'), format=wx.LIST_FORMAT_RIGHT, width=40)
        self.InsertColumn(1, _('language'), width=80)
        self.InsertColumn(2, _('type'), width=120)
        self.InsertColumn(3, _('description'), width=320)

    def setStreams(self, streams, types=None):
        self.DeleteAllItems()

        row = 0
        for no in sorted(streams):
            s = streams[no]
            if types == None or s.type in types:
                lang = s.lang if s.lang else ''

                self.InsertItem(row, str(s.no + 1))
                self.SetItem(row, 1, lang)
                self.SetItem(row, 2, s.type)
                self.SetItem(row, 3, s.title)
                self.SetItemData(row, s.no)
                row += 1

    def selectStream(self, no):
        sel = self.GetFirstSelected()
        if sel != wx.NOT_FOUND and no == self.GetItemData(sel):
            return True

        for sel in range(self.GetItemCount()):
            if no == self.GetItemData(sel):
                self.Select(sel)
                return True

        return False

    def getSelectedStream(self):
        sel = self.GetFirstSelected()
        return self.GetItemData(sel) if sel != wx.NOT_FOUND else None
