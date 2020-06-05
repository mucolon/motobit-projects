# line-follower

### `main.py`

A script that commands the SparkFun [micro:bot](https://www.sparkfun.com/products/16275) to follow a 2 inch wide black line. This file imports the MotoBit class. Thus both `main.py` and `motobit.py` need to be flashed to have a functioning line following robot.

### `motobit.py`

This file contains the MotoBit class imported in the `main.py` file. The MotoBit class performs low-level actions to simplify programming the micro:bit.

## Installation

Your computer needs `python3` and `pip3`, most computers should have it by default. Insert command below to install `uflash` and `ufs`. `$` symbolizes an input line.

```
$ sudo pip3 install microfs uflash
```

## Before Flashing

Before flashing, make sure both files above are in the same local directory.

For example, within your terminal console. Type `pwd` and the ouput should look similar to what is displayed below.

```
$ pwd
/path/to/directory/line-follower
```

Also when you type `ls`, the output should be similar to what is shown.

```
$ ls
main.py    microbit   motobit.py
```

If not, use the `cd` command to change into the correct directory.

```
$ cd path/to/directoy/line-follower
```

**or**

```
$ cd path
$ cd to
$ cd directory
$ cd line-follower
```

Remember you can use `ls` to see what directories you can jump into next.

If this is still confusing, please watch this video below to learn how to use a Linux terminal.

> [Introduction to Linux and Basic Linux Commands for Beginners](https://www.youtube.com/watch?v=IVquJh3DXUA)

## Flashing

If you have installed the micro:bit VS Code extension, then flash your `main.py` file by clicking the `Build current file to Micro:Bit` button on the top right of your window.

Then flash the `motobit.py` file with the command below in your terminal screen.

```
$ ufs put motobit.py
```

**or**

Flash both files with the commands below in your terminal screen.

```
$ uflash main.py
$ ufs put motobit.py
```
