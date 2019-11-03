import pickle


def save_obj(obj, dir):
    with open(dir, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(dir):
    with open(dir, 'rb') as f:
        return pickle.load(f)


def run_analysis(dir):
    # TODO: implement analysis, write to dict to disk with following fields

    project = load_obj(dir + '/project.pkl')
    # go into repo, only directory in this directory
    # get needed data, such as # deps between microservices and # microservices
    # get image size (look at all possible cases: build, download, etc.)

    print('Analyzing', project)

    # add, modify etc the project object
    # save it again
    # save_obj(dir + '/project.pkl')

    # delete all but pickle file
