import tkinter as tk
from tkinter import ttk
import requests
from REST_API import Item


url = "http://127.0.0.1:8000/recommend/"

class Application(tk.Frame):
    def __init__(self,master, options=[], function=None):
        super().__init__(master)
        self.grid()
        self.options = options
        self.function = function
        self.keys = self.options.keys()
        # self.master.geometry("800x300")
        self.master.title("Case-based recommender system")
        s = ttk.Style(self)
        s.theme_use('winnative')
        s.configure("TSeparator", background="gray")
        s.configure('raised.TMenubutton', borderwidth=1)

        self.create_widgets()


    # Create Widgets function
    def create_widgets(self):
        padx = 10

        br = 2
        self.stringList = []
        for i in self.options:

            #Label
            self.label = ttk.Label(self)
            self.label.configure(text=i+':')
            self.label.grid(row = 0, column = br, pady = 2, padx = padx)

            #Dropdown
            string = tk.StringVar()
            string.set(self.options[i][0])
            self.stringList.append(string)

            self.dropdown1 = ttk.OptionMenu(self, string, self.options[i][0], *self.options[i])
            self.dropdown1.grid(row = 1, column = br, sticky = tk.W, pady = 2, padx = padx)


            br+=1

        #Empty label
        self.label_n = ttk.Label(self)
        self.label_n.configure(text='')
        self.label_n.grid(row = 0, rowspan=2,columnspan=2, column = 0, pady = 2, padx = 5)


        #Button
        self.button_hello = ttk.Button(self)
        self.button_hello.configure(text="Submit")
        self.button_hello.configure(command = self.submit) #do not forget to add self!
        self.button_hello.grid(rowspan=2,row=0, columnspan=2, column=len(self.options)+2, padx=padx)

    # Event Callback Function
    def submit(self):
        for label in self.grid_slaves():
            if int(label.grid_info()["row"]) > 2:
                label.grid_forget()
        #Line
        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.grid(row=3, columnspan=len(self.options)+4, sticky='ew', padx=5, pady=5)

        padx = 8

        #Label n
        self.label_n = ttk.Label(self)
        self.label_n.configure(text='n')
        self.label_n.grid(row = 4, column = 0,sticky='w', pady = 2, padx = 5)

        #Label id
        self.label_id = ttk.Label(self)
        self.label_id.configure(text='ID')
        self.label_id.grid(row = 4, column = 1, pady = 2, padx = 4)

        br = 2
        for i in self.options:

            #Label
            self.label = ttk.Label(self)
            self.label.configure(text=i)
            self.label.grid(row = 4, column = br, pady = 2, padx = padx)

            br+=1

        #Label rec
        self.label_rec = ttk.Label(self)
        self.label_rec.configure(text='Recommended')
        self.label_rec.grid(row = 4, column = len(self.options)+2, pady = 2, padx = padx)

        #Label sim
        self.label_sim = ttk.Label(self)
        self.label_sim.configure(text='Similarity')
        self.label_sim.grid(row = 4, column = len(self.options)+3, pady = 2, padx = padx, sticky='e')

        #Line
        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.grid(row=5, columnspan=len(self.options)+4, sticky='ew', padx=5, pady=5)

        #Getting the input
        input = []
        for i in self.stringList:
            input.append(i.get())
        # print(len(input))

        data = {}
        schema = Item.schema()['properties']
        for count, i in enumerate(schema):
            # print(i,input[count])
            temp = input[count]
            if schema[i]["type"] == "number":
                temp = float(temp)
            elif schema[i]["type"] == "integer":
                temp = int(temp)
            data[i] = temp
        # data = {
        #     "query": input
        # }
        headers = {}

        response = requests.request("GET", url, headers=headers, json=data)

        output = response.json()
        # output = self.function(input)


        #Label
        bri = 0
        for i in output:
            sim = i[1]
            values = i[0][:-1]
            rec = i[0][-1]
            brj = 1
            self.label_click=ttk.Label(self, text = str(bri+1)+ '.')
            self.label_click.grid(row=6+bri, column=0, sticky='w', padx=5, pady=10)
            for j in values:


                self.label_click=ttk.Label(self, text = str(j).capitalize())
                self.label_click.grid(row=6+bri, column=brj, padx=5, pady=10)

                brj +=1
            self.label_click=ttk.Label(self, text = str(rec))
            self.label_click.grid(row=6+bri, column=len(self.options)+2, padx=3, pady=10)

            self.label_click=ttk.Label(self, text = str(sim)[:4])
            self.label_click.grid(row=6+bri, column=len(self.options)+3, padx=3, pady=10)

            bri+=1

        # self.label_click.configure(text=self.string1.get())



def GUI(options, function):

    root = tk.Tk()
    app = Application(master=root, options = options, function=function)
    app.mainloop()