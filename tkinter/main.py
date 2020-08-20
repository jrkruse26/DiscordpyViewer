import tkinter as tk
import configparser
import discord.ext.commands
import threading
from tkinter import scroller


class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.client = None
        self.start_discord()

        master = tk.Canvas(self, height=1000, name='!master', borderwidth=10)
        master.pack()
        master.pack_propagate(0)

        propviewer = self.PropViewer(master)
        propviewer.grid(column=1, row=0, rowspan=1)

        serverlist = self.ServerList(master, self.client, propviewer)
        serverlist.grid(column=0, row=0, sticky='n')

    def start_discord(self):
        self.client = discord.ext.commands.Bot(command_prefix='32423')
        keyfile = configparser.ConfigParser()
        keyfile.read('keys.config')

        x = threading.Thread(target=self.client.run, args=(keyfile['Discord']['jummybot'],), kwargs={'bot': True}, daemon=True)
        x.start()
        return x

    class ServerList(tk.Frame):
        def __init__(self, master, client, propviewer):
            tk.Frame.__init__(self, master)
            self.server_scroller = None
            self.client = client
            self.update_list()
            self.propviewer = propviewer

        def update_list(self):
            if self.server_scroller is None:
                self.server_scroller = scroller.Scroller(self)
                self.server_scroller.canvas.configure(width=200)
                self.server_scroller.pack()
            server_list = [x.id for x in self.client.guilds]
            button_list = [v.id for k, v in self.server_scroller.frame.children.items()]

            for item in [x for x in server_list if x not in button_list]:
                if self.client.get_guild(item) is not None:
                    button = self.Button(self.server_scroller.frame, self.client.get_guild(item), self.propviewer)
                    button['text'] = self.client.get_guild(item).name
                    button['command'] = button.on_press
                    button['anchor'] = 'w'
                    button.pack(fill=tk.X)

            remove = [v for k, v in self.server_scroller.frame.children.items() if v.id not in server_list]
            for button in remove:
                pass
                button.destroy()

            self.after(1000, self.update_list)

        class Button(tk.Button):
            def __init__(self, master, obj, propviewer):
                tk.Button.__init__(self, master)
                self.obj = obj
                self.id = obj.id
                self.propviewer = propviewer

            def on_press(self):
                self.propviewer.update_viewer(self.obj)

    class PropViewer(tk.Frame):
        def __init__(self, parent):
            tk.Frame.__init__(self, parent)
            self.innerframe = None
            self.obj = None

        def update_viewer(self, obj):
            self.obj = obj
            if self.innerframe is not None:
                self.innerframe.destroy()
                self.innerframe = scroller.Scroller(self)
                self.innerframe.pack()
                self.populate()

            else:
                self.innerframe = scroller.Scroller(self)
                self.innerframe.pack()
                self.populate()

        def populate(self):

            obj_type = type(self.obj).__name__

            attrs = []
            if obj_type == 'list':
                for item in self.obj:
                    attrs.append(['', item, obj_type])
            elif obj_type == 'dict':
                for k, v in self.obj.items():
                    attrs.append([k, v, obj_type])
            else:
                x = dir(self.obj)
                for prop in x:
                    attr = getattr(self.obj, prop)
                    attr_type = type(attr).__name__
                    if attr_type not in ['method-wrapper', 'method', 'builtin_function_or_method'] and prop[:2] != '__':
                        attrs.append([prop, attr, attr_type])

            for attr in attrs:
                if attr[2] in ['str', 'int', 'NoneType']:
                    disp = tk.Label(text=f'{attr[0]}: {attr[1]}', master=self.innerframe.frame, anchor='w')
                else:
                    disp = self.Button(self.innerframe.frame, attr[1], self)
                    disp['text'] = f'{attr[0]}'
                    disp['anchor'] = 'w'
                disp.pack(fill=tk.X)

        class Button(tk.Button):
            def __init__(self, master, obj, propviewer):
                tk.Button.__init__(self, master)
                self.obj = obj
                self.propviewer = propviewer
                self['command'] = self.on_press

            def on_press(self):
                self.propviewer.update_viewer(self.obj)


app = MainApp()
app.geometry('800x500')
app.mainloop()
