import pickle


def save_obj(obj, name):
    with open('repositories/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('repositories/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def run_analysis(dir):
    # TODO: implement analysis, write to dict to disk with following fields
    # keys of the dictionary:
    # number of dependencies between microservices
    # number of microservices
    # total size of all images
    # date of last commit
    pass

