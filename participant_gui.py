import tkinter as tk
import participantid
# import participantid

class App_Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.current_rin = ""
        self.current_sid = ""
        self.connection = participantid.connect_to_database('test.db')

        self.frame = tk.Frame(self)
        self.frame.pack(side="top", fill="both", expand=True)
        self.pages = {}

        rin_search = {
            "enter_label" : tk.Label(self, text="Enter subjects RIN: "),
            "search_box" : tk.Entry(self, width=50),
            "search_button" : tk.Button(self, text="Search or generate", command=lambda: self.find_number(rin_search['search_box'].get(), self.connection))
        }


        sid_not_found = {
            "not_found" : tk.Label(self, text="Subject is not currently in the system."),
            "generate" : tk.Button(self, text="Generate SID", command=lambda: self.generate_number(self.connection))
        }

        sid_found = {
            "rin" : tk.Label(self, text="Subject with rin %s has sid:" % self.current_rin),
            "sid" : tk.Label(self, text="%s" % self.current_sid)
        }

        self.rin_label = tk.Label(self, text="Subject ID goes here")

        self.pages['rin_search'] = rin_search
        self.pages['sid_not_found'] = sid_not_found
        self.pages['sid_found'] = sid_found
        self.setPage('rin_search')

    def find_number(self, rin, connection):
        self.current_rin = rin
        self.current_sid = participantid.find_sid(self.current_rin, connection)
        found = False
        if self.current_sid != None:
            found = True
        if found:
            self.setPage('sid_found')
        else:
            self.setPage('sid_not_found')

    def generate_number(self, connection):
        # add to database
        participantid.add_to_database((self.current_rin, participantid.next_sid(connection)), connection)

        # now call find_number
        self.setPage('sid_found')

    def setPage(self, page):
        """
        takes the name of a page to show
        """
        for p in self.pages.items():
            for item in p[1].values():
                if(p[0] != page):
                    item.pack_forget()
                else:
                    item.pack()




# gui startup
app = App_Gui()
app.mainloop()
