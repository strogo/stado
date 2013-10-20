from tests.plugins import TestPlugin


class TestAfter(TestPlugin):

    def test_path_argument(self):
        """Plugin after should call function with correct path argument."""

        # site.py

        @self.app.after('page.html')
        def test(path, data):
            return path
        self.app.run()

        # tests

        with open('page.html') as page:
            self.assertEqual('page.html', page.read())


    def test_data_argument(self):
        """Plugin after should call function with correct data argument."""

        # site.py

        @self.app.after('page.html')
        def test(path, data):
            return data
        self.app.run()

        # tests

        with open('page.html') as page:
            self.assertEqual('badger', page.read())


    def test_filename_matching(self):
        """Plugin after should supports file matching."""

        # site.py

        @self.app.after('*.*')
        def test(path, data):
            return 'test'
        self.app.run()

        # tests

        with open('page.html') as page:
            self.assertEqual('test', page.read())
        with open('yaml.html') as page:
            self.assertEqual('test', page.read())
        with open('json.html') as page:
            self.assertEqual('test', page.read())
        with open('markdown.html') as page:
            self.assertEqual('test', page.read())
