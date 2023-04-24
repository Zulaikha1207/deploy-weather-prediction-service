[![Build Status](https://travis.ibm.com/Zulikah-Latief-CIC/Introduction-to-MLOps.svg?token=dzz9gFm4edHvqziqXpsS&branch=main)](https://travis.ibm.com/Zulikah-Latief-CIC/Introduction-to-MLOps)


This repo is an introduction to the practices for standardizing the deployment of ML applications. It is an intoduction to the prinicples of MLOps:

The following tasks were done:
- Create poetry environment for ML project (dependency management)
- Follow an Ops-first folder structure (https://ibm.github.io/data-science-best-practices/)
- Develop ML model that estimates ride duration, given information about pickup and drop location (used jupyter notebook)
- Use python scripts to convert non-modular JNs to automated pipeline
- Add and initialise Git repo to version code
- Add and configure DVC to version data
- Set up TravisCI for Continuous Integration (CI) 
- Use mlflow for experiment tracking, model versioning
- Log metrics and parameters (used hyperopt for parameter tuning)
- Containerize the best model, along with dependencies using docker 
- Use flask to build a web service that estimates the ride duration 


