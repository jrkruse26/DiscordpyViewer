import tkinter as tk
import configparser
import discord.ext.commands
import threading


class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.client = None
        self.start_discord()

        master = tk.Canvas(self, height=1000, width=1200)
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

        x = threading.Thread(target=self.client.run, args=(keyfile['Discord']['jummybot'],), daemon=True)
        x.start()
        return x

    class ServerList(tk.Frame):
        def __init__(self, master, client, propviewer):
            tk.Frame.__init__(self, master)
            self.client = client
            self.update_list()
            self.propviewer = propviewer

        def update_list(self):
            server_list = [x.id for x in self.client.guilds]
            button_list = [v.id for k, v in self.children.items()]

            for item in [x for x in server_list if x not in button_list]:
                button = self.Button(self, self.client.get_guild(item), self.propviewer)
                button['text'] = self.client.get_guild(item)
                button['command'] = button.on_press
                button.pack()

            remove = [v for k, v in self.children.items() if v.id not in server_list]
            for button in remove:
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

        class InnerFrame(tk.Frame):
            def __init__(self, parent, obj):
                tk.Frame.__init__(self, parent)
                self.obj = obj

                self.canvas = tk.Canvas(self, borderwidth=0, height=400, width=300)
                self.frame = tk.Frame(self.canvas)
                self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
                self.canvas.configure(yscrollcommand=self.vsb.set)

                self.vsb.pack(side="right", fill="y")
                self.canvas.pack(side="left", fill="both", expand=True)
                self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                          tags="self.frame")

                self.frame.bind("<Configure>", self.onFrameConfigure)

                self.populate()

                self.canvas.bind('<Enter>', self._bound_to_mousewheel)
                self.canvas.bind('<Leave>', self._unbound_to_mousewheel)

                return

            def _bound_to_mousewheel(self, event):
                self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

            def _unbound_to_mousewheel(self, event):
                self.canvas.unbind_all("<MouseWheel>")

            def _on_mousewheel(self, event):
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            def onFrameConfigure(self, event):
                """Reset the scroll region to encompass the inner frame"""
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))

            def populate(self):
                x = dir(self.obj)
                attrs = []
                for prop in x:
                    attr = getattr(self.obj, prop)
                    attr_type = type(attr).__name__
                    if attr_type not in ['method-wrapper', 'method', 'builtin_function_or_method'] and prop[:2] != '__':
                        attrs.append([prop, attr, attr_type])

                for attr in attrs:
                    if attr[2] in ['str', 'int', 'NoneType']:
                        disp = tk.Label(text=f'{attr[0]}: {attr[1]}', master=self.frame)
                    else:
                        disp = tk.Button(text=f'{attr[0]}', master=self.frame)
                    disp.grid()

        def update_viewer(self, obj):
            if self.innerframe is not None:
                self.innerframe.destroy()
                self.innerframe = self.InnerFrame(self, obj)
                self.innerframe.pack()

            else:
                self.innerframe = self.InnerFrame(self, obj)
                self.innerframe.pack()


app = MainApp()
app.geometry('800x400')
app.mainloop()
