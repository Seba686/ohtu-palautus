from urllib import request
from project import Project
import toml

class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):
        # tiedoston merkkijonomuotoinen sisältö
        content = request.urlopen(self._url).read().decode("utf-8")
        print(content)
        parsed = toml.loads(content)
        print(parsed)
        dependencies = []
        dev_dependencies = []
        authors = []
        for key in parsed["tool"]["poetry"]["dependencies"].keys():
            dependencies.append(key)
        for key in parsed["tool"]["poetry"]["group"]["dev"]["dependencies"].keys():
            dev_dependencies.append(key)
        for author in parsed["tool"]["poetry"]["authors"]:
            authors.append(author)

        # deserialisoi TOML-formaatissa oleva merkkijono ja muodosta Project-olio sen tietojen perusteella
        return Project(parsed["tool"]["poetry"]["name"], parsed["tool"]["poetry"]["description"], 
                       parsed["tool"]["poetry"]["license"], authors, dependencies, dev_dependencies)
