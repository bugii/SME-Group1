class Project:

    def __init__(self, name, url, created, last_updated, language, contributors, commits):
        self.name = name
        self.url = url
        self.created = created
        self.last_updated = last_updated
        self.microservices = []
        self.depends_on = 0
        self.language = language
        self.contributors = contributors
        self.commits = commits

    def __str__(self):
        return self.name

    def add_microservice(self, service):
        self.microservices.append(service)

    def increase_dependencies(self, amount):
        self.depends_on += amount
