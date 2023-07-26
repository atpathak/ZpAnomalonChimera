# ZpAnomalon Analysis - RJR to Plots

This is the repo of the third, fourth, and plotting  steps of the ZpAnomalon Analysis. In this analysis, We are using Recrusive Jigsaw Reconstruction to generate the mass estimators of each daughter particle in the Z' decay chain. This calculcation is done with the Restframes package, whose installation details are outlined below. A c++ TMakeClass analyzer is used to calculate the RJR quantiies, and flatten the output trees from [trimmerShed](https://github.com/gracecummings/trimmerShed). The flattened trees are passed to a python native dataframe based analyzer, which creates the analysis object histograms.

## Setting up the analysis environment

The following python packages are required:

+ pyroot
+ uproot3
+ pandas
+ numpy
+ boost-histogram
+ configparser

if you already have Python 3 working with ROOT, with the above dependences, skip to "Download Repository and Setup Restframes." If you do not, you can follow the environment instructions below.

### Using LCG

We want to use cvmfs and stuff so this works on the LPC because my conda stuff got stale and no longer works.

trying to find an LCG environment with the packages I want: https://lcginfo.cern.ch/

trying LCG: need ROOT 6.22 to work with the RestFrames -> checked with 6.22/08

source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc10-opt/setup.sh -> 6.22/06

## Download Repository and Setup Restframes

We use the [RestFrames](http://restframes.com/) package to calculate the mass esitmators of the Z' cascade decay.

I install RestFrames in the repo directory, to make it easy to keep track, and to avoid possible conflicts on my larger system.

```bash
git clone git@github.com:crogan/RestFrames.git
cd RestFrames
./configure --prefix=$PWD
make
make install
```
Compiling restframes should take about 10 minutes, so do not panic.