class Project:

    def __init__(self, name, url, last_updated):
        self.name = name
        self.url = url
        self.last_updated = last_updated
        self.microservices = []
        self.depends_on = 0

    def __str__(self):
        return self.name

    def add_microservice(self, service):
        self.microservices.append(service)

    def increase_dependencies(self, amount):
        self.depends_on += amount
