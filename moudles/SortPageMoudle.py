# For sort and page bar
# XUZhengyi, 24/01/2018

import tornado.web


class SortPageMoudle(tornado.web.UIModule):
    def render(self, page, updown):
        return self.render_string("modules/sort_page_bar.html", page=page, updown=updown)
