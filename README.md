# pds-cli-cp

## prerequisites
 python 3.8 or higher
 
 ```
 pip install pyyaml requests tx-functional
 ```

## how to run the code

To use the cli tools, if your mapper runs on a local host, put your spec under `config`. Put your custom python functions under a sub dir in that dir. 

If your mapper runs on a remote host you need to manually copy them to the `config` dir.

There is a `cli.py`. You can run it as

```
python cli.py <file containing your spec> <a yaml file containing resource types> <a yaml file contains pids> <timestamp> --libraryPath <sub dir containing custom python functions> --nthreads <number of threads> --level <level> --pdsHost <pds plugin host> --pdsPort <pds plugin port> --configDir <mapper config dir>
```

For example,

```
python cli.py spec.py ../resourceTypes.yaml ../patientIds.yaml "2000-01-01T00:00:00Z" --libraryPath module --nthreads 4 --level 1 --pdsHost pds --pdsPort 1234 --configDir ../pdspi-mapper-parallex-example/config
```

In this example, you would put your spec in `config/spec.py`. Any python module under the `config/modules` directory can be imported in your spec. For example, if you have `config/modules/clivar.py`, you can reference functions in that module in various ways, for example `from clivar import *`. `../resourceTypes.yaml` contains a list of resource types. `../patientIds.yaml` contains a list of patient ids. Your spec should output the format that the api specifies. See `config/spec4.py`'s `return` statement for example. `<level>` specifies the number of nested for loops to parallelize. It automatically copies the config files in the `config` dir to `../pdspi-mapper-parallex-example/config`.
