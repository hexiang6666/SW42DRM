SW42DRM
===========================

### Usage

SW42DRM is a programme that parse the output ([SAC](https://ds.iris.edu/files/sac-manual/manual/file_format.html) file)ground motion data from [SW4](https://computation.llnl.gov/projects/serpentine-wave-propagation/software) and spatially interpolate free field motion to DRM nodes and generate DRM input file while usig [Doamin Reduction Method](http://www.bssaonline.org/content/93/2/817.short)for Earthquake Soil Structure Interaction Analysis with [REAL ESSI](http://sokocalo.engr.ucdavis.edu/~jeremic/Real_ESSI_Simulator/)(UC Davis Earthquake-Soil-Structure-Interaction Simmulator). 

### Installation

#### Building Dependencies

1) Boost and Python

```bash
sudo apt-get install libboost1.48-all-dev
sudo apt-get install build-essential
sudo apt-get install python-dev 
```
2) Matlab (R2014b or later version)

#### Compiling

1) Get the latest version of gmESSI from github

```bash
git clone https://github.com/hexiang6666/SW42DRM.git
```

2) Compile

```bash
cd SW42DRM
make
```

#### Running Examples 

1) Run an example to check the correctness of installation

---
[UCD CompGeoMech](http://sokocalo.engr.ucdavis.edu/~jeremic/)

Created by: Hexiang Wang

Request for adding features on hexwang@ucdavis.edu
