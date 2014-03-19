from . import Controller


class Permalink(Controller):

    name = 'permalink'

    def __call__(self, target, url=None):

        if url: url = self.convert_style(url)

        # Controller can be called in three different ways.
        # First is calling only with one argument. It means that all page items will
        # used this argument as a permalink.
        if url is None:

            url = self.convert_style(target)

            for item in self.site.items:
                if item.is_page():
                    item.permalink = url
                    self.site.save_item(item)

        # Second is calling with two argument and first is item source. Find this
        # item and modify it permalink.
        if isinstance(target, str):

            for item in self.site._get(target):
                item.permalink = url
                self.site.save_item(item)

        # Third is calling with two arguments but first argument is item object.
        # Change permalink directly.
        else:
            target.permalink = url
            self.site.save_item(target)


    @staticmethod
    def convert_style(permalink):
        if permalink == 'pretty':
            return '/:path/:name/index.html'
        elif permalink == 'default' or permalink == 'ugly':
            return '/:path/:filename'
        return permalink
