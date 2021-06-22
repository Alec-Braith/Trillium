# Trillium 
This is a project from a distributed systems class where we explore the endangered trillium through satellite data processing 

## Motivations
The [Dwarf Western Trillium][wiki] (Trilium ovatum hibbersonii) is an endangered plant according to the [COSWIC][coswic] list of endangered species. It is known for its three petal flower (hense tri-llium) and grows mostly on Vancouver island but can also grow in other places on the mainland. Our hope is to investigate the issue further by harnessing Sentinel 2 satellite images and processing them to better understand the habitat trilliums grow in. 

## Installation

### Clone the Repo
Press the ![alt text][code_button] button and clone the repo either by:
1) Copying HTTPS URL and opening GitHub Desktop -> File -> Clone repository -> URL -> paste URL and choose location or
2) Copying HTTPS URL and opening your preffered terminal -> cd into location -> run `$ git clone <URL>` or
3) Press Download Zip -> find .zip file -> extract it and place in preffered location.

### Create Virtual Environment (optional)
1) Open terminal and install python virtual environment package
	type: `python3 -m pip install --user virtualenv`
2) cd to project dir and then create a virtual environment
	type: `python3 -m venv env` (env is the name and location of the venv folder)
3) activate the environment 
	type: `source env/bin/activate`
4) check that it worked
	a. it should say (env) to the left
	b. type: `which python` (it should say the location of the env folder)
5) deactivate 
	type: `deactivate` (the `(env)` should go away)

### Install Python Packages
Next install the python packages used in this project with: </br>
`pip install -r requirements.txt`

## Usage
Once cloned onto a local repo:
1) Add personal credentials for sentinel hub API inside the SHconfig.yaml file
2) Run the code with: `python app.py`
3) Choose your inputs
4) A matplotlib annimation will display the images but also in the directory "data" will be downloads of all the images

## Creators
[Tristan Cusi](https://github.com/cusitristan) </br>
[Alec Braithwaite](https://github.com/Alec-Braith) </br>
[Cole Dodd](https://github.com/coledodd)


[wiki]: https://en.wikipedia.org/wiki/Trillium_ovatum
[coswic]: https://www.cosewic.ca/index.php/en-ca/reports/candidate-wildlife-species.html#toc1
[code_button]: https://github.com/cusitristan/Trillium/blob/main/img/github_code_button.png
