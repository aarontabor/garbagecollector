# Exploring Garbage Collection in Python

This project comprises two main phases:

1. A simulation of garbage collection policies currently used in the JVM and other high-level languages (implemented in Python)
2. A preliminary exploration of concurrent garbage collection in the cPython interpreter (v3.x)


## Simulating Existing Garbage Collection Policies

Garbage collection is a central component of the memory management systems used in many high-level programming languages. The role of garbage collection is to reclaim memory which is no longer accessible from a running program's execution stack, recycling and reusing it to minimize the program's overall memory footprint.

In this phase of the project, I implement a memory management simulator that can be configured to use one of many common garbage collection policies. The simulator accepts real-world program execution logs as input and allows us to empirically evaluate system behavior and performance under different environment configurations (e.g., using different heap sizes).

This phase of the project was completed using Python v3.x (also see https://github.com/GarCoSim/TraceFileSim, which is a similar project I've contributed to in C++). The simulator was implemented in a series of assignments, each of which invloved conducting a performance experiment. These experiments have been automated using shell scripts. These scripts will be named following the convention: 'assignment<x>.sh' and canbe found in the `./assignment_scripts` directory. For correct functionality, please invoke these scripts from the top-level directory. For example (from the top-level directory):

    ./assignment_scripts/assignment1.sh <args> <go> <here>

The simulator also includes a test-suite, which was implemented using the pytest module. All tests can be run using the command in the top-level directory:

    py.test

To run a single test file, specify the filename:

    py.test <filename>


## Exploring Concurrent Garbage Collection in cPython

In this phase of the project, I conduct a survery of methods for addressing the concurreny limitations of cPython (i.e., the standard implementation of Python in use). While the python language supports multi-threaded applications, "true" concurreny is not possible in the language because of a structure known as the Global Interpreter Lock (or GIL), which restricts the python interpreter to a single thread of execution at a time. Given that the garbage collection policy employed in python is a particularly challenging obstacle that prevents the GIL from being removed, I explore how python's garbage collection could be adapted to better support concurrency.

More information can be found in the [project report](https://drive.google.com/file/d/1RJNERZzvQnM_aKjiL4XrBbyP0kn7hD2y/view?usp=sharing): 


