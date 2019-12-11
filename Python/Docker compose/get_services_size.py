import pickle
import shutil
import docker
import os
import subprocess
import datetime

import requests
import yaml

client = docker.from_env()


def save_obj(obj, dir):
    with open(dir, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(dir):
    with open(dir, 'rb') as f:
        return pickle.load(f)


def get_microservice_size(details, project_dir_lvl2, project_dir_lvl1):

    try:
        if 'build' in details:
            build = details['build']
            # if image is also specified: only name is different -> no change in size
            # subarray
            if 'context' in build and 'dockerfile' in build:
                docker_file_loc = project_dir_lvl2 + "/" + (build['context'] + "/" + build['dockerfile']).replace('./', '').replace('Dockerfile', '.')
                print(datetime.datetime.now(), 'building from', docker_file_loc)
                docker_img = client.images.build(path=docker_file_loc)

            elif 'context' in build:
                docker_file_loc = project_dir_lvl2 + "/" + build['context'].replace('./', '')
                print(datetime.datetime.now(), 'building from', docker_file_loc)
                docker_img = client.images.build(path=docker_file_loc)

            else:
                # no subarray
                docker_file_loc = project_dir_lvl2 + "/" + build.replace('./', '')
                print(datetime.datetime.now(), 'building from', docker_file_loc)
                docker_img = client.images.build(path=docker_file_loc)
                # Get the size of the built image

            print('Success: Built', docker_file_loc)

        elif 'image' in details:
            image = details['image']
            docker_img_loc = project_dir_lvl2 + "/" + image
            print(datetime.datetime.now(), 'pulling from', docker_img_loc)
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

        # remove all images after each step, because 2TB storage was not enough sadly
        # subprocess.run('docker system prune -a -f', shell=True)
        return docker_img_size

    except (docker.errors.ImageNotFound, docker.errors.BuildError, docker.errors.NotFound,
            TypeError, AttributeError, requests.exceptions.HTTPError, requests.exceptions.ReadTimeout,
            FileNotFoundError) as e:
        print('Deleted:', project_dir_lvl2, e)
        # delete entire project if errors occurred
        shutil.rmtree(project_dir_lvl1)
        return -1


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
    project_dir_lvl2 = os.listdir(dir)
    project_dir_lvl2.remove('project.pkl')
    project_dir_lvl2 = project_dir_lvl2[0]

    # yaml file sits always in top directory (the way I chose the projects)
    docker_compose_file = load_yaml(dir + "/" + project_dir_lvl2 + '/docker-compose.yml')

    # reset fields
    project.microservices = []
    project.depends_on = 0

    try:
        # get needed data, such as # deps between microservices and # microservices and size
        if 'services' in docker_compose_file:
            for i in docker_compose_file['services']:
                name = i
                details = docker_compose_file['services'][i]

                size = get_microservice_size(details, dir + "/" + project_dir_lvl2, dir)
                project.add_microservice({
                    'name': name,
                    'size': size
                })

                if size == -1:
                    # as soon as one microservice of a project has an error the whole directory is deleted.
                    # thus break out of the loop here
                    break

                if 'depends_on' in details:
                    nr_of_deps = len(details['depends_on'])
                    project.increase_dependencies(nr_of_deps)

        else:
            shutil.rmtree(dir)
            print('Deleted:', dir + ': No services found for this project, at least not at top level')

        # save it again
        try:
            save_obj(project, dir + '/project.pkl')
        except FileNotFoundError:
            pass

    except TypeError as e:
        shutil.rmtree(dir)
        print('Deleted:', dir, "Docker-compose file is most likely empty:", e)


if __name__ == '__main__':
    dirs = os.listdir('repositories')

    # create a list with already completed projects.
    # This way the script can be stopped at any time without starting all over again.
    if not os.path.exists('completed.pkl'):
        completed_projects = []
        save_obj(completed_projects, 'completed.pkl')

    completed_projects = load_obj('completed.pkl')
    completed_count = 0

    for d in dirs:
        print('------------------------------------------------------------------')

        if d not in completed_projects:
            run_analysis('repositories/' + d)
            completed_projects.append(d)
            save_obj(completed_projects, 'completed.pkl')
        else:
            completed_count += 1
            print('#{} '.format(completed_count) + 'Already done:', d)
            obj = load_obj('repositories/' + d + '/project.pkl')
            print('Details:')
            print('Created:', obj.created)
            print('Last updated:', obj.last_updated)
            print('Microservices:', obj.microservices)
            print('Dependencies:', obj.depends_on)
            print('Language:', obj.language)
            print('Contributors:', obj.contributors)
            print('Commits:', obj.commits)
