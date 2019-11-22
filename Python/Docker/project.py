class Project:

    def __init__(self, name, url, creation, last_updated, language, contributors ):
        self.name = name
        self.url = url
        self.creation = creation
        self.last_updated = last_updated
        self.microservices = []
        self.depends_on = 0
        self.language = language
        self.contributors = contributors

    def __str__(self):
        return self.name

    def add_microservice(self, service):
        self.microservices.append(service)

    def increase_dependencies(self, amount):
        self.depends_on += amount
