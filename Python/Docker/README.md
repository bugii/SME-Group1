## How to run

### Fetching projects from Github

Note: Before running the script make sure that you have all the dependencies installed. Do:

```shell script
pip install -r requirements.txt
```

The data can be fetched using the following command:

```shell script
python repo_fetching.py
```

Note, that you change the API_KEY variable to one of your own Github API keys before running the script and that
you have all dependencies installed specified in the requirements.txt file.

### Analyzing microservices

If you don't have enough space on your hard disk or in case you want to use an external disk, follow the next step.
On Ubuntu, the default location for storing docker images can be changed by creating the following file:
/etc/docker/deamon.json. Put into the file:

```json
{
    "data-root": "/mnt/hdd/docker"
}
```

After that, you can run the analysis with the following command:

```shell script
python get_services_size.py
```

Note: In order to be able to run the script, it may be required to allow docker to run commands as a non-root user. In
Linux this is done via the following commands:

```shell script
sudo groupadd docker
sudo usermod -aG docker $USER
```

### Plotting

The plotting.py file contains the code we used to plot our results. Feel free to adjust it to your needs.