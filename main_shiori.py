# Created by yuerua at 19/02/2021
# Description: desktop Shiori
import random
import tkinter as tk
from tkinter import ttk
import re
import os

import pandas as pd
import requests
from bs4 import BeautifulSoup
import webbrowser
import numpy as np

from chatterbot import ChatBot

# main body: https://medium.com/analytics-vidhya/create-your-own-desktop-pet-with-python-5b369be18868

class desk_top_App(tk.Tk):
    def __init__(self, x=1400,
                cycle = 0, check = 1,
                idle_num = range(3),
                sleep_num = range(3,9), #change to the mode if random num fell within the range
                event_number = random.randint(0,2), #initialize with idle
                impath = "."
                ):

        tk.Tk.__init__(self)

        self.x = x
        self.cycle = cycle
        self.check = check
        self.idle_num = idle_num
        self.sleep_num = sleep_num
        self.event_number = event_number
        self.impath = impath
        self.x_dif = 0

        # https://stackoverflow.com/questions/19080499/transparent-background-in-a-tkinter-window
        self.new_geometry = "+"+str(self.x)+"+700"
        self.geometry(self.new_geometry)
        self.call("wm", "attributes", ".", "-topmost", "true")
        #self.wm_attributes("-transparent", True)
        #self.config(bg='systemTransparent')
        self.title("")

        # call buddy's action gif
        # Range: check timeline of gif in ps
        self.idle = [tk.PhotoImage(file=os.path.join(self.impath, 'Shiori.gif'), format='gif -index %i' % (i)) for i in range(32)]  # idle gif
        self.sleep = [tk.PhotoImage(file=os.path.join(self.impath, 'Shiori.gif'), format='gif -index %i' % (i)) for i in range(32)]  # sleep gif

        self.label = tk.Label(self)

        self.after(0, self.gif_update)
        self.after(0, self.widget_drag_free_bind)

        if os.environ.get('DISPLAY', '') == '':
            print('no display found. Using :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')

        # Can't make these work on mac...,haven't been tested on windows
        if os.name == 'nt':
            self.config(highlightbackground='black')
            self.overrideredirect(True)
            self.wm_attributes('-transparentcolor', 'black')


    def widget_drag_free_bind(self):
        """Bind any widget or Tk master object with free drag"""
        # https://stackoverflow.com/questions/4055267/tkinter-mouse-drag-a-window-without-borders-eg-overridedirect1

        self.bind("<B1-Motion>", self.mouse_motion)  # Hold the left mouse button and drag events
        self.bind("<Button-1>", self.mouse_press)

        self.x_, self.y_ = 0, 0

    def mouse_motion(self, event):
        # Positive offset represent the mouse is moving to the lower right corner, negative moving to the upper left corner
        offset_x, offset_y = event.x - self.x_, event.y - self.y_

        new_x = self.winfo_x() + offset_x
        new_y = self.winfo_y() + offset_y
        self.new_geometry = f"+{new_x}+{new_y}"
        self.geometry(self.new_geometry)

    def mouse_press(self, event):
        #count = time.time()
        self.x_, self.y_ = event.x, event.y

    def event(self):
        #control playing speed
        if self.event_number in self.idle_num:
            self.check = 0
            # print('idle')
            self.after(110, self.gif_update)

        elif self.event_number in self.sleep_num:
            self.check = 1
            # print('sleep')
            self.after(110, self.gif_update)

    # making gif work
    def gif_work(self, frames, first_num, last_num):
        if self.cycle < len(frames) - 1:
            self.cycle += 1
        else:
            self.cycle = 0
            self.event_number = random.randrange(first_num, last_num, 1)

    def gif_update(self):
        # idle
        if self.check == 0:
            self.frame = self.idle[self.cycle]
            self.gif_work(self.idle, 0, 8)
            self.x_dif = 0
        # sleep
        elif self.check == 1:
            self.frame = self.sleep[self.cycle]
            self.gif_work(self.sleep, 0, 2)
            self.x_dif = 0

        new_x = int(self.new_geometry.split("+")[1]) + self.x_dif
        new_y = int(self.new_geometry.split("+")[2])
        self.new_geometry = f"+{new_x}+{new_y}"

        self.geometry(self.new_geometry)
        self.after(0, self.event)

        self.label.configure(image=self.frame)
        self.label.config(bg='black')#systemTransparent
        self.label.pack()

class additional_function(desk_top_App):
    def __init__(self,
                 window_w = 200,
                 window_h = 300,
                 major='cs',
                 keyword = "Computer Vision and Pattern Recognition (cs.CV)"):

        super().__init__()

        self.bind("<Button-2>", self.right_click)
        self.bind("<Button-3>", self.right_click)

        self.window_w = window_w
        self.window_h = window_h
        self.major = major
        self.keyword = keyword

        self.break_msg()

    def right_click(self, event):

        m = tk.Menu(self, tearoff=0)
        m.add_command(label="Note", command = self.note_pad)
        m.add_command(label="Regex", command = self.regex_helper)
        m.add_command(label="Paper", command = self.find_paper)
        m.add_command(label="Chat", command = self.chat_box)
        m.add_separator()
        m.add_command(label="Quit", command=self.destroy)

        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()

    def regex_helper(self):
        win = tk.Toplevel()
        win.wm_title("Regex helper")
        #win.attributes("-topmost", True)

        win_x = int(self.new_geometry.split("+")[1]) - 230
        win_y = int(self.new_geometry.split("+")[2]) - 230

        win_geo = f"+{win_x}+{win_y}"
        win.geometry(win_geo)

        tk.Canvas(win, width = self.window_w,  height =self.window_h)
        win.resizable(width=0, height=0)

        label1 = tk.Label(win, text='Your regular expression:')
        label1.config(font=('helvetica', 10))
        label1.grid(row=0, column=0, pady=2, padx=2)

        entry1 = tk.Entry(win, width = 20)
        entry1.grid(row=1, column=0, pady=2, padx=5)

        label2 = tk.Label(win, text="Your test string:")
        label2.config(font=('helvetica', 10))
        label2.grid(row=2, column=0, pady=2, padx=2)

        entry2 = tk.Entry(win, width = 20)
        entry2.grid(row=3, column=0, pady=2, padx=5)

        def match_regex():
            re_exp = str(entry1.get().strip('"'))
            test_str = str(entry2.get().strip('"'))

            if not re_exp or not test_str:
                output = re_exp
                output_command = test_str
            else:
                try:
                    output = re.search(r'%s'%re_exp, test_str).group()

                    output_command = "re.search(r'%s', x).group()"%re_exp
                except:
                    output = "No matches."
                    output_command = "No matches."

            Output1 = tk.Text(win, font=('helvetica', 10, 'bold'), height = 3,
              width = 30)

            Output2 = tk.Text(win, font=('helvetica', 10, 'bold'), height = 3,
              width = 30)

            Output1.insert(tk.INSERT, output)
            Output2.insert(tk.INSERT, output_command)

            Output1.grid(row=6, column=0, pady=2, padx=2)
            Output2.grid(row=7, column=0, pady=2, padx=2)

            # Output1.pack()
            # Output2.pack()
            #
            # canvas1.create_window(self.window_w/2, 25*8.5, window=Output1)
            # canvas1.create_window(self.window_w/2, 25*10.8, window=Output2)

            # label5 = tk.Text(win, text=output_command, font=('helvetica', 10, 'bold'))
            # canvas1.create_window(200, 250, window=label5)

        def match_regex_return(event):
            match_regex()

        button1 = tk.Button(win, text='Match', command=match_regex, bg='white', fg='black',
                            font=('helvetica', 8, 'bold'))
        win.bind("<Return>", match_regex_return)
        button1.grid(row=5, column=0, pady=8)
        #canvas1.create_window(self.window_w/2, 25*5.4, window=button1)

        link1 = tk.Label(win, text="Regex Cheat Sheet", fg="blue", cursor="hand2")
        link1.config(font=('helvetica', 8))
        link1.bind("<Button-1>", lambda e: webbrowser.open_new("https://pythex.org/"))
        link1.grid(row=4, column=0, pady=2)


    def break_msg(self, show_interval=0.05, hide_interval=60):
        #https://stackoverflow.com/questions/25007961/create-a-tkinter-window-every-x-minutes-and-then-automatically-close-it-after-y

        win = tk.Toplevel()
        win_x = int(self.new_geometry.split("+")[1]) - 210
        win_y = int(self.new_geometry.split("+")[2])

        win_geo = f"+{win_x}+{win_y}"
        win.geometry(win_geo)
        win.attributes("-topmost", True)

        def hide():
            win.withdraw()  # Hide the window
            win.after(int(1000*60 * hide_interval), show)  # Schedule self.show() in hide_int seconds

        def show():
            win.deiconify()  # Show the window
            win.after(int(1000*60 * show_interval), hide)  # Schedule self.hide in show_int seconds

        tk.Frame(win, width=150, height=50).pack()
        tk.Label(win, text='Time for a break~').place(x=5, y=10)
        win.after_idle(hide)  # Schedules self.show() to be called when the mainloop starts


    def find_paper(self):
        #https://www.jianshu.com/p/43acc04a9a86
        self.win = tk.Toplevel()
        self.win.wm_title("Paper Hunter")

        win_x = int(self.new_geometry.split("+")[1]) - 230
        win_y = int(self.new_geometry.split("+")[2]) - 230

        win_geo = f"+{win_x}+{win_y}"
        self.win.geometry(win_geo)
        #self.win.attributes("-topmost", True)

        self.canvas1 = tk.Canvas(self.win, width=self.window_w, height=self.window_h)
        #self.canvas1.pack(fill=tk.BOTH, expand=tk.YES)
        self.win.resizable(width=0, height=0)

        self.url = 'https://arxiv.org/list/%s/recent'%self.major

        header = {
            'Host': 'arxiv.org',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }

        r1 = requests.get(self.url, headers=header)

        soup = BeautifulSoup(r1.content, 'lxml')

        text_dl = soup.select('div#dlpage > h3')
        text_ds = text_dl[0].get_text()
        text_d = text_ds.split()

        self.date = text_d
        self.total = int(text_d[8])

        # 25 papers per page
        self.page, self.rest = divmod(self.total, 25)

        self.list_page = range(1, self.page + 1)

        date = '_'.join(self.date[1:4])

        if os.path.isfile("arxiv_%s.csv"%date):
            paper_csv = pd.read_csv("arxiv_%s.csv"%date)
            self.linkall = paper_csv["linkall"]
            self.titleall = paper_csv["titleall"]
            self.number = paper_csv["number"]
            self.keywall = paper_csv["keywall"]
        else:
            self.get_paper_save()

        # Choosing for keywords
        #https://blog.csdn.net/ever_peng/article/details/102563786
        ddb_default_L = tk.Label(self.win, text='Key words：')
        ddb_default_L.config(font=('helvetica', 9, 'bold'))
        ddb_default_L.grid(row=2, column=0, pady=2)
        #self.canvas1.create_window(self.window_w / 2, 137, window=ddb_default_L)


        self.ddb_default = ttk.Combobox(self.win, font=('helvetica', 9))
        self.win.option_add('*TCombobox*Listbox.font', ('helvetica', 9))
        self.ddb_default['value'] = tuple(np.unique(self.keywall))

        deafult_idex = np.where(np.unique(self.keywall)==self.keyword)[0][0]
        self.ddb_default.current(deafult_idex)
        self.ddb_default.grid(row=3, column=0, pady=2)
        #self.ddb_default.pack()
        #self.canvas1.create_window(self.window_w / 2, 160, window=self.ddb_default)

        # Next button
        self.get_random_paper()

        next_button = tk.Button(self.win, text='Get me another one', command=self.get_random_paper, bg='white',
                                fg='black',
                                font=('helvetica', 9, 'bold'))
        next_button.grid(row=5, column=0, pady=5)
        #self.canvas1.create_window(self.window_w / 2, 240, window=next_button)


    # Grab the data from url
    def get_all_this_page(self, url):
        header = {
            'Host': 'arxiv.org',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        rr = requests.get(url, headers=header)
        soup2 = BeautifulSoup(rr.content, 'lxml')
        linkall0 = soup2.select('div#dlpage > dl > dt > span > a:nth-child(1)')

        titleall0 = soup2.select(
            'div#dlpage > dl > dd > div > div.list-title.mathjax')

        keywall0 = soup2.select(
            'div#dlpage > dl > dd > div > div.list-subjects')

        number0 = soup2.select('div#dlpage > dl > dt > a')

        return linkall0, titleall0, number0, keywall0

    def get_paper_save(self):
        self.linkall = []
        self.titleall = []
        self.number = []
        self.keywall = []

        fir = self.get_all_this_page(self.url)

        # get the first page
        linkfir = fir[0]
        titlefir = fir[1]
        numberfir = fir[2]
        keywfir = fir[3]

        find_kw = re.compile(r'<span class="primary-subject">(.*?)</span>')

        for i in range(0, 25):
            keywfir[i] = re.findall(find_kw, str(keywfir[i]))[0]
            self.linkall.append(linkfir[i].get('href'))
            self.titleall.append(titlefir[i].get_text())
            self.number.append(numberfir[i].get_text())
            self.keywall.append(keywfir[i])

        # Get link to evey page
        for ii in self.list_page:
            urlmid = 'https://arxiv.org/list/%s/pastweek?skip='%self.major + str(
                ii * 25) + '&show=25'

            mid = self.get_all_this_page(urlmid)
            linkmid = mid[0]
            titlemid = mid[1]
            numbermid = mid[2]
            keywmid = mid[3]

            if ii < self.page:
                for jj in range(0, 25):
                    keywmid[jj] = re.findall(find_kw, str(keywmid[jj]))[0]
                    # for kw in self.keyword:
                    #     if kw in keywmid[jj]:
                    self.linkall.append(linkmid[jj].get('href'))
                    self.titleall.append(titlemid[jj].get_text())
                    self.number.append(numbermid[jj].get_text())
                    self.keywall.append(keywmid[jj])
            else:
                for jj in range(0, self.rest):
                    keywmid[jj] = re.findall(find_kw, str(keywmid[jj]))[0]
                    self.linkall.append(linkmid[jj].get('href'))
                    self.titleall.append(titlemid[jj].get_text())
                    self.number.append(numbermid[jj].get_text())
                    self.keywall.append(keywmid[jj])

        for pp in range(0, len(self.linkall)):
            link = 'https://arxiv.org/' + self.linkall[pp]
            self.linkall[pp] = link

        # write data
        paper_data = {'number': self.number, 'linkall':self.linkall, "titleall": self.titleall, "keywall": self.keywall}

        df = pd.DataFrame.from_dict(paper_data)

        date = '_'.join(self.date[1:4])
        df.to_csv('arxiv_%s.csv'%date)


    def get_random_paper(self):
        self.keyword =self.ddb_default.get()
        kw_i = np.where(np.array(self.keywall) == self.keyword)[0]
        i = random.choice(kw_i)
        label1 = tk.Label(self.win, text="%i new papers found" % self.total)
        label1.config(font=('helvetica', 9, 'bold'))
        label1.grid(row=0, column=0, pady=2)
        #self.canvas1.create_window(self.window_w / 2, 12, window=label1)

        paper_t = tk.Text(self.win, font=('helvetica', 10), height = 6,
              width = 26, wrap=tk.WORD)
        paper_t.insert(tk.INSERT, re.findall(r'Title: (.*?)$', self.titleall[i])[0])
        paper_t.grid(row=1, column=0, padx=5, pady=2)
        #paper_t.pack()
        #self.canvas1.create_window(self.window_w/2, 75, window=paper_t)

        # paper_kw = tk.Text(self.win, font=('helvetica', 10), height = 6,
        #       width = 30)
        # paper_kw.insert(tk.INSERT, "Key words: \n"+self.keywall[i])
        # paper_kw.pack()
        # self.canvas1.create_window(self.window_w/2, 150, window=paper_kw)

        paper_link = tk.Label(self.win, text=self.linkall[i], fg="blue", cursor="hand2")
        paper_link.config(font=('helvetica', 9))
        paper_link.bind("<Button-1>", lambda e: webbrowser.open_new(self.linkall[i]))
        paper_link.grid(row=4, column=0, pady=2)
        #self.canvas1.create_window(self.window_w/2, 200, window=paper_link)

    def chat_box(self):
        #https://zhuanlan.zhihu.com/p/78714067

        win = tk.Toplevel()
        win.title("Chat")
        win_x = int(self.new_geometry.split("+")[1]) - 210
        win_y = int(self.new_geometry.split("+")[2])

        win_geo = f"+{win_x}+{win_y}"
        win.geometry(win_geo)
        win.attributes("-topmost", True)
        win.resizable(width=0, height=0)

        chat_bot = ChatBot("Amiya")

        canvas1 = tk.Canvas(win, width = 200,  height =100)

        entry1 = tk.Text(win, font=('helvetica', 10), height=3, width=25, wrap=tk.WORD)
        entry1.grid(row=0, column=0, pady=2, padx=5, sticky=tk.W)

        def get_answer(event):
            question = (entry1.get("1.0",'end-1c')).rstrip()
            if question:
                answer = chat_bot.get_response(question)
            else:
                answer = "おはよう, Dr."

            Output = tk.Text(win, font=('helvetica', 10), height=3,
                             width=25, wrap=tk.WORD)
            Output.insert(tk.INSERT, answer)
            Output.grid(row=1, column=0, pady=2, padx=5, sticky=tk.W)
        
        get_answer("_")
        win.bind("<Return>", get_answer)

    def note_pad(self):
        win = tk.Toplevel()
        win.title("Note pad")
        win_x = int(self.new_geometry.split("+")[1]) - 45
        win_y = int(self.new_geometry.split("+")[2]) - 210

        win_geo = f"+{win_x}+{win_y}"
        win.geometry(win_geo)
        win.attributes("-topmost", True)

        canvas1 = tk.Canvas(win)
        #canvas1.pack()

        note = tk.Text(win, font=('helvetica', 11), height=13, width=27, wrap=tk.WORD)
        #note.pack(expand=tk.YES, fill='both')
        #canvas1.create_window(100,100, window=note)
        note.grid(row=0, column=0, pady=2, padx=5)

        label = tk.Label(win, text = "Press Ctrl+s to save", font=('helvetica', 10))
        #label.pack()
        #canvas1.create_window(100, 204, window=label)
        label.grid(row=1, column=0, pady=2)

        def default_label():
            label['text'] = ""

        def write_to_note(event):
            note_entry = note.get("1.0",'end-1c')
            if note_entry:
                with open('note_pad.txt', 'a') as f:
                    f.write("\n" + note_entry + '\n')
                    label['text'] = "Note saved!"
                    win.after(2000, default_label)

        win.bind("<Control-s>", write_to_note)


if __name__ == "__main__":
    window = additional_function(window_w = 200,
                 window_h = 300,
                 major='cs', #supports subjects at arxiv.org
                 keyword = "Computer Vision and Pattern Recognition (cs.CV)")

    window.mainloop()
