# ZpAnomalon Analysis - RJR to Plots

This is the repo of the third, fourth, and plotting  steps of the ZpAnomalon Analysis. In this analysis, We are using Recrusive Jigsaw Reconstruction to generate the mass estimators of each daughter particle in the Z' decay chain. This calculcation is done with the Restframes package, whose installation details are outlined below. A c++ TMakeClass analyzer is used to calculate the RJR quantiies, and flatten the output trees from [trimmerShed](https://github.com/gracecummings/trimmerShed). The flattened trees are passed to a python native dataframe based analyzer, which creates the analysis object histograms.

## Setting up the analysis environment

The following python packages are required:

+ pyroot
+ uproot
+ pandas
+ numpy
+ boost-histogram
+ configparser

if you already have Python 3 working with ROOT, with the above dependences, skip to "Download Repository and Setup Restframes." If you do not, you can follow the environment instructions below.

### Using LCG

We want to use cvmfs and stuff so this works on the LPC because the original conda environment pre-2023 got stale and no longer works. To find an LCG environment with the packages we want, we need to check the LCG page: https://lcginfo.cern.ch/ . Each step uses different LCG environments -- I am sure this could be alleviated but it was easier to use different LCG environments for the different steps than to significanntly rewrite the framework. 

```
source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc10-opt/setup.sh
```

## Making Topiary - RJR calculation and tree trimming (and flattening)

In principle, everything should be updated to run on the lateset supported versions of things, but principles do not always matter. The analysis originally ran with ROOT version 6.22/08. The closest LCG environment that works uses ROOT 6.22/06, so that is the one we will use! While running on the LPC or lxplus (though these instructions are not tested on lxplus), cvmfs is mounted, so to source the environment (in bash), run

```
source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc10-opt/setup.sh
```

### Setting up the dependencies

Topiary has a lot of dependencies that make it tricker to setup and run, but we will get there. Most of this only has to be done once. I am sure there are better ways to do this, but this was the best compromise of ease and expedience I could produce.

#### RestFrames Installation

We use the [RestFrames](http://restframes.com/) package to calculate the mass esitmators of the Z' cascade decay. RestFrames is run in the 'topiary' step, which is setup to be run as a condor bacth job. Therefore, all of the topiary-step dependencies are built in the `condorbatch/topiary_jobs` directory. MAKE SURE THE ABOVE ENOVIRONMENT IS SOURCED. To build `RestFrames` in the topiary environment, do:

```bash
cd condorbatch/topiary_jobs/RestFrames
./configure --prefix=$PWD
make
make install
```
Compiling restframes can take up to 10 minutes, so do not panic.

#### UHH2 for Jet Systematics Installation

The University of Hamburg has a nice ntuplizer that does the heavy lifting of the JEC systematic and the JER systematics for you. Because of this, we use bits and pieces of the their framework at the topiary level, and we do some compiler things to make it work. To build, starting from the `ZpAnomalonChimera` top directory do:

```bash
cp Makefile.common condorbatch/topiary_jobs/UHH2/.
cd condorbatch/topiary_jobs/UHH2/JetMETObjects/
make
sed -i '\/#include <UHH2\/JetMETObjects\/interface\/JetResolutionObject.h>/c\#include <JetResolutionObject.h>' interface/JetResolution.h
```

This will build the parts of the `UHH2` we need. We probably could get away with all of the parts of the repository, but this works, and that is what matters to me in the present moment.

#### Linking it all together

If you peruse the `topiary_jobs` subdirectory in the `condorbatch` directory, you will quickly see many subdirectories. These all hold the scale factors applied in this analysis. They came from a wide variety of places, and some were custom generated. That documentation is found in the note. Initially, and after any change to the topiary class, the whole directory must be compiled. And for that to work, several things must happen. Now that the dependencies are built, the `TreeMakerTopiary` class must be compiled. To compile,

```bash
cd condorbatch/topiary_jobs/
source setup_RestFrames.sh
make
```

This *will throw warnings*, they can be ignored. For now. I am sure this will bite at some point, but right now, that it is just a warning. If it throws an error, that is not expected. Fix it. This will give you a setup that will run both as a batch job and interactively. If any changes are made to the class, the class will have to be be recompiled with `make` again.

### Runnings Topiary

The Topiary code runs on the *skims* that are stored in the lpcboostres directory on the cmslpc eos. The code in its base form can be run either interactively or as batch job (only testing on the cmslpc Condor cluster). Regardless of what you do, it is good to make sure you have a valid GRID proxy, 

```
voms-proxy-init --rfc --voms cms -valid 192:00
```

and type in your grid passphrase. You probably only need to do it for batch job submission, but, eh. Do it regularly, do not forget your pass phrase! The skims that are available to run over are listed in the

```
condorbatch/samples
```

and all have the form `skim_locations_YEAR_TYPE.json`, where `YEAR` is `20161,2017`, or `2018`, and the `TYPE` is `MC`, 'Signal, or `Data`. The `.txt` files of the same name are the handmade files with the `eos` directories where the skims reside. All the samples and datasets used in the analysis should have `json` files. To make new `json` files, first, make a `.txt` file that lists each of the directories in the `lpcboostres` space that has the desired skims. The skim directories must have the complete skim set included -- *skims will not be connected across directories at this step.* The directory names must each be on a new line. To create the `.json`, run

```bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc10-opt/setup.sh
python makeSkimJson.py -f TEXTFILE -n YEAR_TYPE 
```

#### Runnings as a batch job on the LPC



## Running Jobs on the lpc Condor Cluster

All processing can now be run as jobs. Things can be run interactively as well, but it takes a bit of finagling to get the command line options correct (mostly need the full path for accessing files on eos). As always, one has to make sure they have a valid grid certificate and proxy active, so you might as well run it for the max time by executing:

```
voms-proxy-init --rfc --voms cms -valid 192:00
```

### Topiary Jobs

These are really complicated with a lot of dependecies. Working on make this setup smoother.

### Selection jobs

