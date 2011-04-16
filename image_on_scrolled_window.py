#!/usr/bin/env python

# example basictreeview.py

import pygtk
pygtk.require('2.0')
import gtk

class image_on_scrolled_window(gtk.ScrolledWindow):
    def set_from_path(self, path):
        self.pixbuf = gtk.gdk.pixbuf_new_from_file(path)        
        self.image.set_from_pixbuf(self.pixbuf)
        #scaled_buf = pixbuf.scale_simple(900,600,gtk.gdk.INTERP_BILINEAR)

    
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.set_border_width(0)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        self.image = gtk.Image()

        self.add_with_viewport(self.image)
        

    
class scrolled_image_example(object):
    # close the window and quit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False


    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Image on ScrolledWindow Example")

        self.window.set_size_request(600, 500)

        self.window.connect("delete_event", self.delete_event)

        self.image_on_sw = image_on_scrolled_window()
        # When the button receives the "clicked" signal, it will call the
        # function hello() passing it None as its argument.  The hello()
        # function is defined above.

        self.image_on_sw.set_from_path('/home/ryan/Pictures/unsorted/900by600/DSC_8730.jpg')
        self.image_on_sw.show()
        self.window.add(self.image_on_sw)

        self.window.show_all()


    def main(self):
        gtk.main()


if __name__ == "__main__":
    example = scrolled_image_example()
    example.main()
