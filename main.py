import wx
import discord.ext.commands
import configparser
import threading


def start_discord():
    client = discord.ext.commands.Bot(command_prefix='32423')
    keyfile = configparser.ConfigParser()
    keyfile.read('keys.config')

    x = threading.Thread(target=client.run, args=(keyfile['Discord']['jummybot'],), kwargs={'bot': True},
                         daemon=True)
    x.start()
    return client


class Main(wx.Frame):
    def __init__(self, client):
        super().__init__(parent=None, title='Discord.py Viewer')
        self.main_sizer = wx.GridSizer(2)
        propviewer = self.PropViewer(self)
        guilds = self.Guilds(self, client, propviewer)

        self.main_sizer.Add(guilds, 1, wx.ALL | wx.CENTER | wx.EXPAND, 5)
        self.main_sizer.Add(propviewer, 0, wx.ALL | wx.CENTER | wx.EXPAND, 5)

        self.SetSizer(self.main_sizer)
        self.Show()

    class Guilds(wx.ScrolledWindow):
        def __init__(self, parent, client, propviewer):
            super().__init__(parent=parent)
            self.propviewer = propviewer
            self.client = client
            self.SetScrollRate(0, 20)
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.SetSizer(self.sizer)
            self.sizer.SetMinSize(wx.Size(200, 200))

            self.update_guilds()

        def update_guilds(self):
            server_list = [str(x.id) for x in self.client.guilds]
            button_list = [v.Name for v in self.GetChildren()]

            for x in [int(x) for x in server_list if x not in button_list]:
                guild = self.client.get_guild(x)
                if guild.name is not None:
                    my_btn = self.Button(self, guild, self.propviewer)
                    my_btn.SetLabel(str(guild.name))
                    my_btn.SetName(str(guild.id))
                    my_btn.Bind(wx.EVT_BUTTON, my_btn.OnClicked)
                    self.sizer.Add(my_btn, 0, wx.ALL | wx.LEFT, 5)
                    self.GetParent().Layout()

            remove = [button for button in self.GetChildren() if button.Name not in server_list]
            for button in remove:
                button.Destroy()
                self.sizer.Layout()
            wx.CallLater(1000, self.update_guilds)

        class Button(wx.Button):
            def __init__(self, parent, object, propviewer):
                super().__init__(parent=parent)
                self.object = object
                self.propviewer = propviewer

            def OnClicked(self, event):
                self.propviewer.items = []
                self.propviewer.page = 1
                self.propviewer.update_frame(self.object)

    class PropViewer(wx.ScrolledWindow):
        def __init__(self, parent):
            super().__init__(parent=parent)
            self.obj = None
            self.page = 1
            self.items = []

            self.SetScrollRate(20, 20)

            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.sizer.SetMinSize(wx.Size(200, 200))
            self.SetSizer(self.sizer)

        def update_frame(self, obj):
            for c in self.GetChildren():
                c.Destroy()

            self.obj = obj
            if not self.items:
                self.populate()

            self.create_items(self.items[self.page - 1])

            count = len(self.items)
            if count > 5:
                pg = wx.Panel(parent=self)
                pg_sizer = wx.BoxSizer(wx.HORIZONTAL)
                pg.SetSizer(pg_sizer)

                class PgButton(wx.Button):
                    def __init__(self, parent, propviewer, i):
                        super().__init__(parent=parent)
                        self.propviewer = propviewer
                        self.i = i

                    def OnClicked(self, event):
                        self.propviewer.items = []
                        self.propviewer.page = self.i
                        self.propviewer.update_frame(self.propviewer.obj)

                if self.page <= 3:
                    for i in range(1, 5):
                        bttn = PgButton(pg, self, i)
                        bttn.SetLabel(str(i))
                        bttn.Bind(wx.EVT_BUTTON, bttn.OnClicked)
                        pg_sizer.Add(bttn, 1, wx.ALL | wx.LEFT, 5)
                    lbl = wx.StaticText(parent=pg, label='...')
                    pg_sizer.Add(lbl, 1, wx.ALL | wx.LEFT, 5)
                    last_bttn = PgButton(pg, self, count)
                    last_bttn.SetLabel(str(count))
                    last_bttn.Bind(wx.EVT_BUTTON, last_bttn.OnClicked)
                    pg_sizer.Add(last_bttn, 1, wx.ALL | wx.LEFT, 5)

                elif self.page >= count - 2:
                    first_bttn = PgButton(pg, self, 1)
                    first_bttn.SetLabel(str(1))
                    first_bttn.Bind(wx.EVT_BUTTON, first_bttn.OnClicked)
                    pg_sizer.Add(first_bttn, 1, wx.ALL | wx.LEFT, 5)

                    lbl = wx.StaticText(parent=pg, label='...')
                    pg_sizer.Add(lbl, 1, wx.ALL | wx.LEFT, 5)

                    for i in range(count-4, count+1):
                        bttn = PgButton(pg, self, i)
                        bttn.SetLabel(str(i))
                        bttn.Bind(wx.EVT_BUTTON, bttn.OnClicked)
                        pg_sizer.Add(bttn, 1, wx.ALL | wx.LEFT, 5)

                else:
                    first_bttn = PgButton(pg, self, 1)
                    first_bttn.SetLabel(str(1))
                    first_bttn.Bind(wx.EVT_BUTTON, first_bttn.OnClicked)
                    pg_sizer.Add(first_bttn, 1, wx.ALL | wx.LEFT, 5)

                    lbl = wx.StaticText(parent=pg, label='...')
                    pg_sizer.Add(lbl, 1, wx.ALL | wx.LEFT, 5)

                    for i in range(self.page-2, self.page+3):
                        bttn = PgButton(pg, self, i)
                        bttn.SetLabel(str(i))
                        bttn.Bind(wx.EVT_BUTTON, bttn.OnClicked)
                        pg_sizer.Add(bttn, 1, wx.ALL | wx.LEFT, 5)

                    lbl = wx.StaticText(parent=pg, label='...')
                    pg_sizer.Add(lbl, 1, wx.ALL | wx.LEFT, 5)
                    last_bttn = PgButton(pg, self, count)
                    last_bttn.SetLabel(str(count))
                    last_bttn.Bind(wx.EVT_BUTTON, last_bttn.OnClicked)
                    pg_sizer.Add(last_bttn, 1, wx.ALL | wx.LEFT, 5)

                self.sizer.Add(pg, 0, wx.ALL | wx.CENTER, 5)
                self.sizer.Layout()

            self.GetParent().Layout()

        def populate(self):
            obj_type = type(self.obj).__name__
            attrs = []
            if obj_type == 'list':
                for item in self.obj:
                    attrs.append([item, item, obj_type])
            elif obj_type == 'dict':
                for k, v in self.obj.items():
                    attrs.append([k, v, obj_type])
            elif obj_type in ['bool', 'int']:
                attrs.append([str(self.obj), '', obj_type])
            else:
                x = dir(self.obj)
                for prop in x:
                    try:
                        attr = getattr(self.obj, prop)
                        attr_type = type(attr).__name__
                        if attr_type not in ['method-wrapper', 'method', 'builtin_function_or_method'] and prop[0] != '_':
                            attrs.append([prop, attr, attr_type])
                    except AttributeError as e:
                        print(e)

            i = 0
            self.items = []
            group = []
            for attr in attrs:
                if i < 50:
                    group.append(attr)
                    i += 1
                else:
                    i = 0
                    self.items.append(group)
                    group = []
            if i != 0 or self.items == []:
                self.items.append(group)

        def create_items(self, attrs):
            labels = []
            buttons = []
            for attr in attrs:
                if attr[2] in ['str', 'int', 'NoneType', 'bool']:
                    if attr[0][0] == '_':
                        label = f'{attr[0][1:]}: {attr[1]}'
                    else:
                        label = f'{attr[0]}: {attr[1]}'
                    label = label.replace('_', ' ')
                    label = label.capitalize()
                    disp = wx.StaticText(self, label=label)
                    labels.append(disp)
                else:
                    disp = self.Button(self, attr[1], self)
                    label = f'{attr[0]}'
                    label = label.replace('_', ' ')
                    label = label.capitalize()
                    disp.SetLabel(label)
                    disp.Bind(wx.EVT_BUTTON, disp.OnClicked)
                    buttons.append(disp)

            for disp in labels:
                self.sizer.Add(disp, 0, wx.ALL | wx.LEFT, 5)

            for disp in buttons:
                self.sizer.Add(disp, 0, wx.ALL | wx.LEFT, 5)

        class Button(wx.Button):
            def __init__(self, parent, object, propviewer):
                super().__init__(parent=parent)
                self.object = object
                self.propviewer = propviewer

            def OnClicked(self, event):
                self.propviewer.items = []
                self.propviewer.page = 1
                self.propviewer.update_frame(self.object)

if __name__ == '__main__':
    app = wx.App()
    client = start_discord()
    frame = Main(client)
    app.MainLoop()
