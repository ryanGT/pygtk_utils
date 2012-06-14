#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
import glob, os, pdb, socket, shutil, datetime, time, numpy, spreadsheet


class listview_on_scrolledwindow(gtk.ScrolledWindow):
    def set_data(self, data=None, clear=True):
        if data is None:
            data = self.data
        if clear:
            self.model.clear()
        for row in data:
            self.model.append(row)



    # visibility determined by state matching active toggle buttons
    def visible_cb(self, model, iter, data):
        return model.get_value(iter, 1) in data


    def _init_view(self):
        self.modelfilter = self.model.filter_new()
        #self.model.clear()
        # create the TreeView
        self.treeview = gtk.TreeView()


        N = len(self.labels)
        # create the TreeViewColumns to display the data
        self.treeview.columns = [None]*N
        for i, label in enumerate(self.labels):
            self.treeview.columns[i] = gtk.TreeViewColumn(label)

        #self.modelfilter.set_visible_func(self.visible_cb, self.show_states)
        #self.treeview.set_model(self.modelfilter)
        self.treeview.set_model(self.model)

        for n in range(N):
            # add columns to treeview
            self.treeview.append_column(self.treeview.columns[n])
            # create a CellRenderers to render the data
            self.treeview.columns[n].cell = gtk.CellRendererText()
            # add the cells to the columns
            if self.wrap:
                self.treeview.columns[n].cell.props.wrap_width = self.wrap_width
                self.treeview.columns[n].cell.props.wrap_mode = gtk.WRAP_WORD

            self.treeview.columns[n].pack_start(self.treeview.columns[n].cell,
                                                True)
            # set the cell attributes to the appropriate liststore column
            self.treeview.columns[n].set_attributes(
                self.treeview.columns[n].cell, text=n)


        self.states = []
        self.show_states = self.states[:]
        self.modelfilter.set_visible_func(self.visible_cb, self.show_states)

        #print('self.treeview.props = ' + str(self.treeview.props))
        #pdb.set_trace()
        # make treeview searchable
        self.treeview.set_rules_hint( True )
        self.treeview.set_search_column(0)
        

    def __init__(self, data, dtype_list, labels, modelclass=gtk.ListStore, \
                 wrap_width=300, wrap=0):
        gtk.ScrolledWindow.__init__(self)
        #print('data = ' + str(data))
        self.wrap = wrap
        self.data = data
        self.dtype_list = dtype_list
        self.labels = labels
        self.wrap_width = wrap_width
        self.model = modelclass(*self.dtype_list)
        self.set_data()
        self._init_view()
        #gtk.Container.add(self, self.treeview)
        self.add(self.treeview)
        self.show()



class csv_viewer(object):
    #dtype_list = [str]*N
    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "delete event occurred"

        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False


    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        #self.save(settings_path)
        gtk.main_quit()


    def load_data(self, pathin=None):
        if pathin is None:
            pathin = self.pathin
        f = open(pathin,'r')
        mylist = f.read(2000)
        f.close()
        if mylist.find('\t') > -1:
            spreadsheet_class = spreadsheet.TabDelimSpreadSheet
        else:
            spreadsheet_class = spreadsheet.CSVSpreadSheet

        mysheet = spreadsheet_class(pathin)
        mysheet.ReadData()
        self.data = mysheet.alldata
        self.labels = self.data.pop(0)
        self.nc = len(self.labels)

        

    def __init__(self, pathin, wrap_width=300, dtype_list=None):
        # create a new window
        #renderer.props.wrap_width = 100
        #renderer.props.wrap_mode = gtk.WRAP_WORD
        self.wrap_width = wrap_width
        self.pathin = pathin

        self.load_data()
        if dtype_list is None:
            dtype_list = [str]*self.nc
            
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.connect("delete_event", self.delete_event)

        # Here we connect the "destroy" event to a signal handler.  
        # This event occurs when we call gtk_widget_destroy() on the window,
        # or if we return FALSE in the "delete_event" callback.
        self.window.connect("destroy", self.destroy)

        # Sets the border width of the window.
        self.window.set_border_width(2)

        self.main_vbox = gtk.VBox(homogeneous=False, spacing=0)

        self.main_listbox = listview_on_scrolledwindow(self.data, dtype_list, self.labels, \
                                                       wrap_width=self.wrap_width)
        self.main_listbox.show()
        self.main_vbox.pack_start(self.main_listbox, False)


        self.window.add(self.main_vbox)
        self.main_listbox.set_size_request(800,400)
        self.window.set_size_request(1000,500)
        self.window.show_all()
        
    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()


# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    mypath = '/home/ryan/siue/Research/litreview/article_per_day/bibtex_db.csv'
    #mypath = 'test.csv'
    myapp = csv_viewer(mypath)
    myapp.main()
