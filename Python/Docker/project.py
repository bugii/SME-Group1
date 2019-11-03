class Project:

    def __init__(self, name, url, last_updated):
        self.name = name
        self.url = url
        self.last_updated = last_updated

    def __str__(self):
        return self.name

