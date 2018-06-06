# MMOpt-Gen
[![Build Status](https://travis-ci.org/Ant-man74/MMOpt-Gen.svg?branch=master)](https://travis-ci.org/Ant-man74/MMOpt-Gen)

Multi objective genetic algorythm to optimize the 3-MMOPT problem

## Dependency

To install all dependency needed to run the algorythm use:

    make install

## Other Command

To view what option you can use:

    make help

To launch the optimization algorythm use:

    make main
  
## Note

As of rigth now only one kernel can be treated at a time, to change it, go into schedulerHandler.py and change:

 - l33 : SchedulingHandler.extractTiles('fileName',Number) 
 - l69 : SchedulingHandler.extractTiles('fileName',Number) 

