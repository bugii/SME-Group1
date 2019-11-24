import pickle
import docker
import os

import requests
import yaml

client = docker.from_env()

def save_obj(obj, dir):
    with open(dir, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(dir):
    with open(dir, 'rb') as f:
        return pickle.load(f)


def get_microservice_size(details, project_path):

    try:
        if 'build' in details:
            build = details['build']
            # if image is also specified: only name is different -> no change in size
            # subarray
            if 'context' in build and 'dockerfile' in build:
                docker_file_loc = project_path + "/" + (build['context'] + "/" + build['dockerfile']).replace('./', '').replace('Dockerfile', '.')
                #print('building from', docker_file_loc)
                docker_img = client.images.build(path=docker_file_loc)

            elif 'context' in build:
                docker_file_loc = project_path + "/" + build['context'].replace('./', '')
                #print('building from', docker_file_loc)
                docker_img = client.images.build(path=docker_file_loc)

            else:
                # no subarray
                docker_file_loc = project_path + "/" + build.replace('./', '')
                #print('building from', docker_file_loc)
                docker_img = client.images.build(path=docker_file_loc)
                # Get the size of the built image

            print('Success: Built', docker_file_loc)

        elif 'image' in details:
            image = details['image']
            docker_img_loc = project_path + "/" + image
            #print('pulling from', docker_img_loc)
            if ':' not in image:
                image += ':latest'

            docker_img = client.images.pull(image)

            print('Success: Pulled', docker_img_loc)

        else:
            docker_img = None

        if isinstance(docker_img, tuple):
            docker_img_size = docker_img[0].attrs['Size']
        elif isinstance(docker_img, list):
            # if no tag is specified, all images are downloaded -> just look at first one
            docker_img_size = docker_img[0].attrs['Size']
        else:
            docker_img_size = docker_img.attrs['Size']

        return docker_img_size

    except docker.errors.ImageNotFound as e:
        print('Error:', project_path, 'Private image, cannot download: ', e)
        return -1
    except docker.errors.BuildError as e:
        print('Error:', project_path, 'Cannot be built, ignore:', e)
        return -1
    except docker.errors.NotFound as e:
        print('Error:', project_path, 'Cannot find image, ignore:', e)
        return -1
    except TypeError as e:
        print('Error:', project_path, 'Cannot handle {} (variables) inside path, ignore:', e)
        return -1
    except AttributeError as e:
        print('Error:', project_path, 'Neither image nor build:', e)
        return -1
    except requests.exceptions.HTTPError as e:
        print('Error:', project_path, 'Dockerfile not found', e)


def load_yaml(path):
    with open(path, 'r') as stream:
        try:
            res = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return

    return res


def run_analysis(dir):
    project = load_obj(dir + '/project.pkl')

    # go into repo, only directory in this directory
    project_dir = os.listdir(dir)
    project_dir.remove('project.pkl')
    project_dir = project_dir[0]

    # yaml file sits always in top directory (the way I chose the projects)
    docker_compose_file = load_yaml(dir + "/" + project_dir + '/docker-compose.yml')

    # reset fields
    project.microservices = []
    project.depends_on = 0

    try:
        # get needed data, such as # deps between microservices and # microservices and size
        if 'services' in docker_compose_file:
            for i in docker_compose_file['services']:
                name = i
                details = docker_compose_file['services'][i]

                size = get_microservice_size(details, dir + "/" + project_dir)
                project.add_microservice({
                    'name': name,
                    'size': size
                })

                if 'depends_on' in details:
                    nr_of_deps = len(details['depends_on'])
                    project.increase_dependencies(nr_of_deps)

        else:
            print('Error:', dir + ': No services found for this project, at least not at top level')

        # save it again
        save_obj(project, dir + '/project.pkl')

    except TypeError as e:
        print('Error:', dir, "Docker-compose file is most likely empty:", e)


if __name__ == '__main__':
    dirs = os.listdir('repositories')
    for d in dirs:
        run_analysis('repositories/' + d)

