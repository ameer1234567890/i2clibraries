## How to Install

Install the Quick2Wire libraries and setup the environment. The second two steps will have to be done every time you login:
```
git clone https://github.com/quick2wire/quick2wire-python-api
export QUICK2WIRE_API_HOME=~/myproject/quick2wire-python-api
export PYTHONPATH=$PYTHONPATH:$QUICK2WIRE_API_HOME
```

To easily setup the environment every time you login. Put the two export lines above in a file (quick2wire.env) using an editor such as vi or nano and then source the environment by running:
```
. ./quick2wire.env
```

CD into the directory you are going to create your python code and type:
```
git clone https://bitbucket.org/thinkbowl/i2clibraries
```
