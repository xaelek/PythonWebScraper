from Tkinter import *
from ttk import *
from bs4 import BeautifulSoup
from urllib2 import *

class weatherDataFrontend:

    def __init__(self, master):
        self.master = master
        self._createGUI()
        self.master.protocol("WM_DELETE_WINDOW", self._safe_close)

    def _createGUI(self):
        bgcolor = '#CCCCFF'
        self.master.configure(background = bgcolor)
        self.master.title('Tag Scraper')
        self.master.minsize(100, 100)
        self.master.resizable(True, True)
        self.style = Style()
        self.style.configure('TFrame', background = bgcolor)
        self.style.configure('TButton', background = bgcolor, font = ('Arial Black', 10))
        self.style.configure('TLabel', background = bgcolor, font = ('Arial Black', 10))

        self.frame_header = Frame(self.master)
        self.frame_header.pack(side = TOP)
        Label(self.frame_header).pack(side = TOP)

        self.frame_input = Frame(self.master)
        self.frame_input.pack(side = TOP)
        Label(self.frame_input, text = 'Enter a URL:').grid(row = 0)
        self.url_entry = Entry(self.frame_input, width = 50)
        self.url_entry.grid(row = 0, column = 1, sticky = W)

        Label(self.frame_input, text = 'Enter a filter:').grid(row = 1)
        self.filter_entry = Entry(self.frame_input, width = 10)
        self.filter_entry.grid(row = 1, column = 1, sticky = W)
        Button(self.frame_input, text = 'Get Text',
                command = self.get_text).grid(row = 1, column = 2, sticky = W)

        self.frame_output = Frame(self.master)
        self.frame_output.pack(side = TOP)
        self.output = Text(self.frame_output)
        self.output.grid(row = 2, column = 0, sticky = W)


        self.frame_button = Frame(self.master)
        self.frame_button.pack(side = BOTTOM)

        Button(self.frame_button, text = 'Go',
                command = self.print_html).grid(row = 2, column = 0)
        Button(self.frame_button, text = 'Close',
                command = self._safe_close).grid(row = 2, column = 1)

    
    def print_html(self):
        html_tags = self.get_html()
        self.output.delete('1.0', END)
        if type(html_tags) != NoneType:
            if len(html_tags) == 0:
                print 'No \'%s\' tags on this page' % self.filter_entry.get()
                self.output.insert(END, ('No \'%s\' tags on this page' % self.filter_entry.get()))
                return
            for tag in html_tags:         
                print tag
                self.output.insert(END, str(tag) + '\n')
        
    def get_text(self):
        try:
            response = urlopen(self.url_entry.get())
        except:
            print 'Not a valid url.'
            self.output.delete('1.0', END)
            self.output.insert(END, 'Not a valid url.')
        else:
            html = response.read()
            filtered_html = BeautifulSoup(html, "lxml")
            self.output.delete('1.0', END)
            self.output.insert(END, filtered_html.get_text())

    def get_html(self):
        try:
            response = urlopen(self.url_entry.get())
        except:
            print 'Not a valid url.'
            self.output.delete('1.0', END)
            self.output.insert(END, 'Not a valid url.')
        else:
            html = response.read()
            filtered_html = BeautifulSoup(html, "lxml").find_all(self.filter_entry.get())
            return filtered_html

    def _safe_close(self):
        self.master.destroy()

def main():
    root = Tk()
    app = weatherDataFrontend(root)
    root.mainloop()

if __name__ == "__main__": main()