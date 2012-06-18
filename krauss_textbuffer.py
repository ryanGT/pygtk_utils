import gtk


class krauss_textbuffer(gtk.TextView):
    def __init__(self, initial_text=''):
        gtk.TextView.__init__(self)
        self.textbuffer = self.get_buffer()
        self.textbuffer.set_text(initial_text)


    def clear(self):
        start_iter = self.textbuffer.get_start_iter()
        end_iter = self.textbuffer.get_end_iter()
        self.textbuffer.delete(start_iter, end_iter)


    def append(self, msg):
        if msg == '':
            msg = '\n'
        elif msg[-1] != '\n':
            msg += '\n'
        end_iter = self.textbuffer.get_end_iter()
        self.textbuffer.insert(end_iter, msg)


    def get_text(self):
        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        mystr = self.textbuffer.get_text(start,end)
        return mystr


    def set_text(self, msg):
        self.clear()
        self.textbuffer.set_text(msg)

