#!/usr/bin/env python

# example basictreeview.py

import pygtk
pygtk.require('2.0')
import gtk

class listbox(gtk.TreeView):
    """This is my attempt to package a ListStore, TreeView, and
    TreeSelection together into a functioning listbox."""
    def append(self, items):
        if type(items) == str:
            items = [items]
        for item in items:
            self.liststore.append(['%s' % item])
            

    def get_selected(self):
        model, rows = self.treeselection.get_selected_rows()
        selected = []
        for path in rows:
            myiter = self.liststore.get_iter(path)
            item  = self.liststore.get_value(myiter, 0)
            selected.append(item)
        self.selected = selected
        return selected
    

    def selection_changed(self, *args, **kwargs):
        #print('I believe you changed the selection')
        model, rows = self.treeselection.get_selected_rows()
        #iter_list = self.treeselection.get_selected()
        #print('model = ' + str(model))
        #print('rows = ' + str(rows))
        items = self.get_selected()
        print('selected items = ' + str(items))


    def clear(self, *args, **kwargs):
        self.liststore.clear()


    def set_items(self, items):
        self.clear()
        self.append(items)
        
    
    def __init__(self, label='Column A', initial_data=None):
        self.liststore = gtk.ListStore(str)

        if initial_data is not None:
            for item in initial_data:
                self.liststore.append(['%s' % item])

        gtk.TreeView.__init__(self, self.liststore)

        # create the TreeViewColumn to display the data
        self.tvcolumn = gtk.TreeViewColumn(label)

        # add tvcolumn to treeview
        self.append_column(self.tvcolumn)

        # create a CellRendererText to render the data
        self.cell = gtk.CellRendererText()

        # add the cell to the tvcolumn and allow it to expand
        self.tvcolumn.pack_start(self.cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.tvcolumn.add_attribute(self.cell, 'text', 0)

        # make it searchable
        self.set_search_column(0)

        # Allow sorting on the column
        self.tvcolumn.set_sort_column_id(0)

        # Allow drag and drop reordering of rows
        #self.set_reorderable(True)

        self.treeselection = self.get_selection()
        self.treeselection.set_mode(gtk.SELECTION_MULTIPLE)
        self.treeselection.connect("changed", self.selection_changed)
    


class listbox_on_scrollwindow(gtk.ScrolledWindow):
    """This class put a listbox on a scrolledwindow in case the list
    contents overflow the available space"""
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
    
    
class listbox_example:
    # close the window and quit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False


    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_title("Basic TreeView Example")

        self.window.set_size_request(200, 200)

        self.window.connect("delete_event", self.delete_event)

        # create a TreeStore with one string column to use as the model
        #self.treestore = gtk.TreeStore(str)

        self.clear_button = gtk.Button("Clear")

        self.listbox = listbox('Year', initial_data=['1990','1991','1997'])
        # When the button receives the "clicked" signal, it will call the
        # function hello() passing it None as its argument.  The hello()
        # function is defined above.
        self.clear_button.connect("clicked", self.listbox.clear, None)

        vbox = gtk.VBox(False, 2)
        vbox.pack_start(self.listbox, True)
        vbox.pack_start(self.clear_button, False)
        self.window.add(vbox)

        self.window.show_all()


    def main(self):
        gtk.main()


if __name__ == "__main__":
    example = listbox_example()
    example.main()
