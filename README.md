# DFCX-STTE: Dialogflow CX Speech-to-Text Enhancements

Dialogflow provides a simple and effective way to handle proper nouns with built-in Speech-to-Text and extensible system entities. 

In many cases this approach is sufficient; sometimes, though, the sheer diversity of proper nouns extends beyond what regionally optimized model can handle effectively.  

This github repository provides an example of how to address those challenges using two machine learning algorithms (Term Frequency - Inverse Document Frequency and k-Nearest Neighbors) to enhance Dialogflow's native speech-to-text capabilities.

# Requirements

* Google Cloud Platform
* Service access to Dialogflow CX, Cloud Build, and Cloud Run. *May require other roles and permissions*

# DFCX-STTE: Instructions

Getting started with DFCX-STTE is as simple as cloning the repo and issuing a gcloud builds submit.  The service has one endpoint "/name-provided" which is expecting a session variable `caller-name` that has the callers sys.person information (typically a full name).  

```console
git clone https://github.com/YvanJAquino/dfcx-stte.git
gcloud builds submit
```

Since the included model is based off randomly generate caller names, you can use a name from the names list located under data `data/full_names.json`.  When experimenting with the model, you can add variance to the provided name to see how the model performs.  For example, instead of providing `Craig Penny Jackson` try `Craig Jackson` instead.  

For more details, see the Dockerfile and the cloudbuild.yaml

