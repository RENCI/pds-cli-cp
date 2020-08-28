## how to write a spec

the following variables are provided to the spec

`data`: this is the fhir data, it is an array of fhir bundles, each bundle contains all fhir resources to a patient

`patientIds`: this is a list of patient ids

`timestamp`: this is a timestamp



## Never leave a large project running without monitoring disk and cpu and memory usage

### disk usage

open a window and run 

```watch df```

look for usage percentange in the disks


### cpu usage and memory usage

run

```htop```



### resolving a disk usage problem
if they get above say certain threshold that you're not expecting (e.g., 80%) then stop the script and docker containers

delete containers
```docker rm -f $(docker ps -qa)```

delete images
```docker rmi -f $(docker images -q)```

delete volumes
```docker volumn prune -f```

delete networks
```docker network prune -f```
