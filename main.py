import tkinter as tk
import configparser
import discord.ext.commands
import threading


class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.client = None
        self.start_discord()

        serverlist = self.ServerList(self.client)
        serverlist.grid(column=0, row=0)

    def start_discord(self):
        self.client = discord.ext.commands.Bot(command_prefix='32423')
        keyfile = configparser.ConfigParser()
        keyfile.read('keys.config')

        x = threading.Thread(target=self.client.run, args=(keyfile['Discord']['jummybot'],), daemon=True)
        x.start()
        return x

    class ServerList(tk.Frame):
        def __init__(self, client):
            tk.Frame.__init__(self)
            self.client = client
            self.update_list()

        def update_list(self):
            server_list = [x.id for x in self.client.guilds]
            button_list = [v.id for k, v in self.children.items()]

            for item in [x for x in server_list if x not in button_list]:
                button = self.Button(self, item)
                button['text'] = self.client.get_guild(item)
                button.grid()

            remove = [v for k, v in self.children.items() if v.id not in server_list]
            for button in remove:
                button.destroy()

            self.after(1000, self.update_list)

        class Button(tk.Button):
            def __init__(self, master, ident):
                tk.Button.__init__(self, master)
                self.id = ident


app = MainApp()
app.mainloop()
