#!/usr/bin/env python

# example basictreeview.py

import pygtk
pygtk.require('2.0')
import gtk

import listbox

import copy, pdb

class thumbnail_iconview(gtk.IconView, listbox.listbox):
    def select_new_path(self, inc=1):
        items = self.get_selected_items()
        N = len(self.liststore)
        #print('len(self.liststore) = ' + str(N))
        if items == []:
            if inc >= 0:
                next_ind = 0
            else:
                next_ind = N-1
        else:
            prev_path = items[-1]
            #print('prev_path = ' + str(prev_path))
            prev_ind = prev_path[0]
            next_ind = prev_ind + inc

        self.unselect_all()
        
        if next_ind < 0:
            next_ind = 0
        elif next_ind >= N:
            next_ind = N-1
        next_path = (next_ind,)#a tuple of one item, since our viewer
                               #only has one column
        #print('next_path = ' + str(next_path))
        self.select_path(next_path)
        self.scroll_to_path(next_path, use_align=True, \
                            row_align=0.5, col_align=0.5)
        self.selection_changed()
        
        
    def select_next(self):
        self.select_new_path(inc=1)
        

    def select_previous(self):
        self.select_new_path(inc=-1)
        
        
    def get_selections(self):
        items = self.get_selected_items()
        selected = []
        for path in items:
            ind = path[0]
            print('ind = ' + str(ind))
            thumb_path = self.thumb_paths[ind]
            myiter = self.liststore.get_iter(path)
            item  = self.liststore.get_value(myiter, 0)
            selected.append(thumb_path)
            print('thumb_path = ' + str(thumb_path))
        self.selected_thumb_paths = selected
        return selected

        
    def selection_changed(self, *args, **kwargs):
        self.get_selections()
        if self.parent_selection_method is not None:
            self.parent_selection_method()
        
        
    def __init__(self, parent_selection_method=None):
        self.parent_selection_method = parent_selection_method
        self.liststore = gtk.ListStore(gtk.gdk.Pixbuf)
        gtk.IconView.__init__(self, self.liststore)
        self.set_pixbuf_column(0)

        self.set_selection_mode(gtk.SELECTION_MULTIPLE)
        self.connect("selection-changed", self.selection_changed)

        self.thumb_paths = []



    def append(self, paths):
        if type(paths) == str:
            paths = [paths]
        for path in paths:
            #print('path = ' + str(path))
            self.thumb_paths.append(path)
            pixbuf = gtk.gdk.pixbuf_new_from_file(path)
            self.liststore.append([pixbuf])


    def set_items(self, *args, **kwargs):
        raise NotImplmentedError

    
    def get_selected(self, *args, **kwargs):
        raise NotImplmentedError


    def clear_selected(self, *args, **kwargs):
        raise NotImplmentedError


    def set_from_paths(self, paths):
        self.liststore.clear()
        self.thumb_paths = []
        self.append(paths)


map_list = copy.copy(listbox.map_list)
map_list.extend(['set_from_paths', \
                'get_selections', \
                 'select_next', \
                 'select_previous'])


class thumbnail_iconview_on_scrollwindow(gtk.ScrolledWindow):
    """This class put a listbox on a scrolledwindow in case the list
    contents overflow the available space"""
    def __init__(self, *args, **kwargs):
        gtk.ScrolledWindow.__init__(self)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.set_border_width(0)
        self.thumbnail_iconview = thumbnail_iconview(*args, **kwargs)

        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        #self.add_with_viewport(self.listbox)
        #gtk.Container.add(self, self.thumbnail_iconview)
        self.add(self.thumbnail_iconview)
        self.thumbnail_iconview.show()

        for attr in map_list:
            myfunc = getattr(self.thumbnail_iconview, attr)
            setattr(self, attr, myfunc)



class thumbnail_test(object):
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self, paths=None):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_title("Thumbnail Example")

        self.window.set_size_request(450, 700)

        self.window.connect("delete_event", self.delete_event)

        self.thumbs_on_scrolled = thumbnail_iconview_on_scrollwindow()

        self.window.add(self.thumbs_on_scrolled)

        if paths is not None:
            #print('paths = ' + str(paths))
            self.thumbs_on_scrolled.set_from_paths(paths)

        self.window.show_all()


    def main(self):
        gtk.main()


if __name__ == "__main__":
    import glob
    mypaths = glob.glob('/home/ryan/Pictures/unsorted/thumbnails/DSC_*.jpg')
    example = thumbnail_test(paths=mypaths)
    example.main()


    
    
