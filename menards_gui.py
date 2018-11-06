import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
import menards_price_plot as mpp

LARGE_FONT= ("Verdana", 12)


class MenardsGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry('750x750')

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Menards Price Analyzer")
        
        container = tk.Frame(self)
        
        container.pack(side="top", fill=None, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        p = ttk.Panedwindow(parent, orient='HORIZONTAL')
        # first pane, which would get widgets gridded into it:
        item_search = ttk.Labelframe(p, text='Item Search', width=375, height=375)
        item_history = ttk.Labelframe(p, text='Item Info', width=375, height=375)   # second pane
        p.add(item_search)
        p.add(item_history)


        label = tk.Label(self, text="Menards Price Tracker", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()

        ttk.Entry(self)


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        
        graph_button = ttk.Button(self, text="Back to Home",
                            command=lambda: canvas.show())
        graph_button.pack()
        
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)

        x,y = mpp.get_plot()
        a.plot(x,y)
        
        #a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        
        canvas = FigureCanvasTkAgg(f, self)
        
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        #toolbar = NavigationToolbar2TkAgg(canvas, self)
        #toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
def command_line_use():
    
    counter = int(1)

    print("Welcome to Menards price scraper")
    
    user_input = str()
    
    while user_input is not 'exit':
        user_input = input('{} >> '.format(counter))

        print(user_input)
        counter += 1
    
    print("ok bye")
    exit()

if __name__ == '__main__':
    command_line_use()

app = MenardsGUI()
app.mainloop()