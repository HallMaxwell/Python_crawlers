import os
import tkinter as tk
import webbrowser
import requests
import tkinter.messagebox as messagebox
import PySimpleGUI as sg
from tkinter import ttk
from retrying import retry


class SetUI(object):
    """
    Music Popup Interface
    """

    def __init__(self, width=1000, height=600):
        self.ui_width = width
        self.ui_height = height
        self.title = "Music Cracking Software"
        self.ui_root = tk.Tk(className=self.title)
        self.ui_url = tk.StringVar()
        self.ui_var = tk.IntVar()
        self.ui_var.set(1)
        self.show_result = None
        self.song_num = None
        self.response_data = None
        self.song_url = None
        self.song_name = None
        self.song_author = None

    def set_ui(self):
        """
        Set up a simple UI interface
        :return:
        """
        # Frame widgets
        frame_1 = tk.Frame(self.ui_root)
        frame_2 = tk.Frame(self.ui_root)
        frame_3 = tk.Frame(self.ui_root)
        frame_4 = tk.Frame(self.ui_root)

        # UI menu design
        ui_menu = tk.Menu(self.ui_root)
        self.ui_root.config(menu=ui_menu)
        file_menu = tk.Menu(ui_menu, tearoff=0)
        ui_menu.add_cascade(label='Menu', menu=file_menu)
        file_menu.add_command(label='Instructions', command=lambda: webbrowser.open('www.example.com'))
        file_menu.add_command(label='About the Author', command=lambda: webbrowser.open('www.example.com'))
        file_menu.add_command(label='Exit', command=self.ui_root.quit)

        # Widget content settings
        choice_channel = tk.Label(frame_1, text='Select Music Search Channel:', padx=10, pady=10)
        channel_button_1 = tk.Radiobutton(frame_1, text='KuWo', variable=self.ui_var, value=1, width=10, height=3)
        channel_button_2 = tk.Radiobutton(frame_1, text='NetEase Cloud', variable=self.ui_var, value=2, width=10, height=3)
        channel_button_3 = tk.Radiobutton(frame_1, text='QQ Music', variable=self.ui_var, value=3, width=10, height=3)
        channel_button_4 = tk.Radiobutton(frame_1, text='Kugou', variable=self.ui_var, value=4, width=10, height=3)
        input_text = tk.Label(frame_2, text="Enter Song Name or Artist:")
        entry_style = tk.Entry(frame_2, textvariable=self.ui_url, highlightcolor='Fuchsia', highlightthickness=1,
                               width=35)
        label2 = tk.Label(frame_2, text=" ")
        play_button = tk.Button(frame_2, text="Search", font=('Arial', 11), fg='Purple', width=2, height=1,
                                command=self.get_KuWoMusic)
        label3 = tk.Label(frame_2, text=" ")
        # Table style
        columns = ("Number", "Artist", "Song", "Album")
        self.show_result = ttk.Treeview(frame_3, height=20, show="headings", columns=columns)
        # Download
        download_button = tk.Button(frame_4, text="Download", font=('Arial', 11), fg='Purple', width=6, height=1, padx=5,
                                    pady=5, command=self.download_music)

        # Widget layout
        frame_1.pack()
        frame_2.pack()
        frame_3.pack()
        frame_4.pack()
        choice_channel.grid(row=0, column=0)
        channel_button_1.grid(row=0, column=1)
        channel_button_2.grid(row=0, column=2)
        channel_button_3.grid(row=0, column=3)
        channel_button_4.grid(row=0, column=4)
        input_text.grid(row=0, column=0)
        entry_style.grid(row=0, column=1)
        label2.grid(row=0, column=2)
        play_button.grid(row=0, column=3, ipadx=10, ipady=10)
        label3.grid(row=0, column=4)
        self.show_result.grid(row=0, column=4)
        download_button.grid(row=0, column=5)

        # Set table headings
        self.show_result.heading("Number", text="Number")
        self.show_result.heading("Artist", text="Artist")
        self.show_result.heading("Song", text="Song")
        self.show_result.heading("Album", text="Album")
        # Set columns
        self.show_result.column("Number", width=100, anchor='center')
        self.show_result.column("Artist", width=200, anchor='center')
        self.show_result.column("Song", width=200, anchor='center')
        self.show_result.column("Album", width=300, anchor='center')

        # Mouse click event
        self.show_result.bind('<ButtonRelease-1>', self.get_song_url)

    @retry(stop_max_attempt_number=5)
    def get_KuWoMusic(self):
        """
        Get music from KuWo
        :return:
        """
        # Clear table data in treeview
        for item in self.show_result.get_children():
            self.show_result.delete(item)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'en-US, en;q=0.9',
            'cache-control': 'no-cache',
            'Connection': 'keep-alive',
            'csrf': 'HH3GHIQ0RYM',
            'Referer': 'http://www.kuwo.cn/search/list?key=ZhouJieLun',
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/99.0.4844.51 Safari/537.36',
            'Cookie': '_ga=GA1.2.218753071.1648798611; _gid=GA1.2.144187149.1648798611; _gat=1; '
                      'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1648798611; '
                      'Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1648798611; kw_token=HH3GHIQ0RYM'
        }
        search_input = self.ui_url.get()
        if len(search_input) > 0:
            search_url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?'
            search_data = {
                'key': search_input,
                'pn': '1',
                'rn': '80',
                'httpsStatus': '1',
                'reqId': '858597c1-b18e-11ec-83e4-9d53d2ff08ff'
            }
            try:
                self.response_data = requests.get(search_url, params=search_data, headers=headers, timeout=20).json()
                songs_data = self.response_data['data']['list']
                if int(self.response_data['data']['total']) <= 0:
                    messagebox.showerror(title='Error', message='Search: {} does not exist.'.format(search_input))
                else:
                    for i in range(len(songs_data)):
                        self.show_result.insert('', i, values=(i + 1, songs_data[i]['artist'], songs_data[i]['name'],
                                                               songs_data[i]['album']))
            except TimeoutError:
                messagebox.showerror(title='Error', message='Search timed out. Please try again!')
        else:
            messagebox.showerror(title='Error', message='No song or artist entered. Please enter and search!')

    def get_song_url(self, event):
        """
        Get the download URL of the song
        :return:
        """
        # Left click in the treeview
        for item in self.show_result.selection():
            item_text = self.show_result.item(item, "values")
            # Get
            self.song_num = int(item_text[0])
        # Get the download URL of the song
        if self.song_num is not None:
            songs_data = self.response_data['data']['list']
            songs_req_id = self.response_data['reqId']
            song_rid = songs_data[self.song_num - 1]['rid']
            music_url = 'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={}&type=convert_url3' \
                        '&httpsStatus=1&reqId={}' \
                .format(song_rid, songs_req_id)
            response_data = requests.get(music_url).json()
            self.song_url = response_data['data'].get('url')
            self.song_name = songs_data[self.song_num - 1]['name']
            self.song_author = songs_data[self.song_num - 1]['artist']
        else:
            messagebox.showerror(title='Error', message='No song selected. Please choose one.')

    def download_music(self):
        """
        Download music
        :return:
        """
        if not os.path.exists('./wangYiYun'):
            os.mkdir("./wangYiYun/")
        if self.song_num is not None:
            song_name = self.song_name + '--' + self.song_author + ".mp3"
            try:
                save_path = os.path.join('./wangYiYun/{}'.format(song_name)) \
                    .replace('\\', '/')
                true_path = os.path.abspath(save_path)
                resp = requests.get(self.song_url)
                with open(save_path, 'wb') as file:
                    file.write(resp.content)
                    messagebox.showinfo(title='Download Successful', message='Song: %s, saved at %s' % (self.song_name, true_path))
            except Exception:
                messagebox.showerror(title='Error', message='Folder to store songs not found')
        else:
            messagebox.showerror(title='Error', message='No song selected. Please choose and then download.')

    def progress_bar(self, file_size):
        """
        Task loading progress bar
        :return:
        """
        layout = [[sg.Text('Task Completion Progress')],
                  [sg.ProgressBar(file_size, orientation='h', size=(40, 20), key='progressbar')],
                  [sg.Cancel()]]

        # Just load the custom layout into the window. The first parameter is the window title.
        window = sg.Window('Robot Execution Progress', layout)
        # Get the progress bar using the key value
        _progress_bar = window['progressbar']
        for i in range(file_size):  
            event, values = window.read(timeout=10)
            if event == 'Cancel' or event is None:
                break
            _progress_bar.UpdateBar(i + 1)

    def ui_center(self):
        """
        UI window settings: center
        """
        ws = self.ui_root.winfo_screenwidth()
        hs = self.ui_root.winfo_screenheight()
        x = int((ws / 2) - (self.ui_width / 2))
        y = int((hs / 2) - (self.ui_height / 2))
        self.ui_root.geometry('{}x{}+{}+{}'.format(self.ui_width, self.ui_height, x, y))

    def loop(self):
        """
        Function to wait for user events in a loop
        """
        self.ui_root.resizable(False, False)  
        self.ui_center()  
        self.set_ui()
        self.ui_root.mainloop()


if __name__ == '__main__':
    ui_instance = SetUI()
    ui_instance.loop()
