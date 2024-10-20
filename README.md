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

## Making Topiary - RJR calculation and tree trimming (and flattening)

In principle, everything should be updated to run on the lateset supported versions of things, but principles do not always matter. The analysis originally ran with ROOT version 6.22/08. The closest LCG environment that works uses ROOT 6.22/06, so that is the one we will use! While running on the LPC or lxplus (though these instructions are not tested on lxplus), cvmfs is mounted, so to source the environment (in bash), run

```
source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc10-opt/setup.sh
```

### Setting up the dependencies - First setup

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

### Running Topiary

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

#### Running Topiary as a batch job on the LPC

To submit jobs, make sure you are in the `condorbatch` folder, and that you have the topiary enviroment sourced using:

```
source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc10-opt/setup.sh
```

To submit all the topiary jobs for all of the samples in the skim, execute something like:

```bash
python submitTopiaryJobs.py -j samples/skim_locations_YEAR_TYPE.json -c CHANNEL 
```

Where `YEAR` is `2016`, `2017`, or `2018`, `TYPE` is `MC`, `Data`, or `Signal`, and `chan` is `mumu`, or `emu`, depending on if you want the dimuon channel or the electron/muon ttbar control region. Additional options can be found with `-h`, like options for systematics (jec, jer, and unclustered MET all must be done at this level), and options to only run for one sample in the json.

This will automatically create an output folder on the cmslpc eos with the name `/store/group/lpcboostres/topiaries_systematics-SYSTEMATICSSTRING_SUBMISSIONDATE`. For example, submitting jobs for the "up" JEC systematic on September 27, 2023, produces and output directory `/store/user/lpcboostres/topiaries_systematics-upjec_2023-09-27`. The `stdout`, `stderr`, and `log` files are dumped into an automatically generated folder in the submission directory called `condorMonitoringOutput`. Outfiles will be in subfolders of the submission date.

To check for failed jobs and resubmit without debug, run the following 

```
python checkForFailedTopiaryJobs.py -d DATE_SUB_IN_YYYY_MM_DD -r True [same command options as the original submission]
```

Where the `-d` is the `YYYY_MM_DD` you submitted the original jobs, `-r` is whether or not you want to resubmit the jobs (True is yes), and use `-h` rto see the other options you need to add to be in line with the original submission. Running without `-r` will just print the missing samples.

General comments:
*   With one submission, only do one systematic (ie, JECs) at one time, to better organize the outfolders on eos (and control job #)
*   Each year has around 12 background MC samples, so one year, nominal, up/dwn jecs, up/dwn jer, and up/dwn unclmet gives 84 jobs 
*   Known bugs in this process have open issues - check there to see if your issue is known

#### Running interactively

Topiary makers can also be run interactively, but are now strealined to run in batch, making running interactively a bit clunky but possible. The topiary runner, `runTopiary.py` in the `topiary_jobs` folder takes a list of paths to skims on eos, so to get those paths, source the topiary LCG environment, and run

```
python submitTopiaryJobs.py -j samples/skim_locations_YEAR_TYPE.json -c chan -s SAMPLENAME -k True
```

where `-k` kills the submission of the jobs and `.jdl` creation, and instead prints the arguments that get passed to the `trimmer.sh` and then to `runTopiary.py`. To run interactively you do not need `trimmer.sh`, but it does not directly print what goes to `runTopiary.py`, so consider yourself warned. Just copying the eos list as is directly is enough.

Once you have the file paths needed to run, to run topiary for one sample interactively,

```bash
cd topiary_jobs
source setup_RestFrames.sh 
python runTopiary.py -s SAMPLE -c CHANNEL -l LISTOFEOS -syst SYST
```

run `python runTopiary.py -h` for more details. Again, pasting directly the list printed by `submitTopiaryJobs.py` should work for the `-l`. This will automatically create a subdirectory in `topiary_jobs` called `analysis_output_zpanomalon` and the output will be in a submission date subdirectory. Make sure to move the output out of the `topiary_jobs` directory to not have it in the tarball made for job submission.

## Doing the selections - cuts, histograms, and event weighting

The topiary step flattens trees and builds/selects our objects. The 'selection' step applies kinematic cuts, separates the regions, and builds histograms. This is done via a Pandas dataframe with Uproot-- but an old version. To run the selections, a different LCG environment is needed:

```
source /cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc10-opt/setup.sh
```

### Running selections

The selection code runs on the *topiaries* that are stored in the lpcboostres directory on the cmslpc eos. The code in its base form can be run either interactively or as batch job (only testing on the cmslpc Condor cluster). Make sure you have a GRID proxy setup by executing

```
voms-proxy-init --rfc --voms cms -valid 192:00
```

and typing in your grid passphrase. The skims that are available to run over are listed in the

```
condorbatch/samples
```

directory and are separated by systematics that have to be applied at the topiary step and those that are added as event weights later. To make new  `.json` files make a `.txt` file that lists each of the directories in the `lpcboostres` space that has the desired skims. The skim directories must have the complete skim set included -- *skims will not be connected across directories at this step.* The directory names must each be on a new line. To create the `.json`, run

```bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc10-opt/setup.sh
python makeTopiaryJson.py -f TEXTFILE -n TYPE_DESCRIPTION 
```

#### Running Selections as a batch job on the LPC

To submit jobs, make sure you are in the `condorbatch` folder, and that you have the topiary enviroment sourced using:

```
source /cvmfs/sft.cern.ch/lcg/views/LCG_100/x86_64-centos7-gcc10-opt/setup.sh
```

To submit all the selection jobs for all of the topiaries in the `.json`, execute something like:

```bash
python submitSelectionJobs.py -j samples/topiary_locations_TYPE_DESCRIPTION.json -c CHANNEL 
```

Where `TYPE` is `MC`, `Data`, or `Signal`, and `CHANNEL` is `mumu`, or `emu`, depending on if you want the dimuon channel or the electron/muon ttbar control region. Additional options can be found with `-h`. To do systematics, as the *last* command line argument, add

```bash
python submitSelectionJobs.py -j samples/topiary_locations_TYPE_DESCRIPTION.json -c CHANNEL -syst syst1 syst2 ...
```

where `syst1 syst2 ...` is a space separated list with options from

```
pdf
qcd
prefire
pumapWeight
pumapPUnum
btag
muid
mutrg
uncl
jec
jer
```

*NOTE* The last three (`uncl, jec, jer`) need to be run on a topiary that has these shifts already implemented. THe others are done as event weights and are run on nominal topiaries. Providing multiple systematics only adds them each to the same job, reducing the number of jobs, but increasing the job length.

This will automatically create an output folder on the cmslpc eos with the name `/store/group/lpcboostres/topiaries_systematics-SYSTEMATICSSTRING_SUBMISSIONDATE`. For example, submitting jobs for the "up" JEC systematic on September 27, 2023, produces and output directory `/store/user/lpcboostres/topiaries_systematics-upjec_2023-09-27`. The `stdout`, `stderr`, and `log` files are dumped into an automatically generated folder in the submission directory called `condorMonitoringOutput`. Outfiles will be in subfolders of the submission date.
