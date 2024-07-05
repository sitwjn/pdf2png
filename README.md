
<h1 align="center">
  Pdf2PngSvc
  <br>
</h1>

<h4 align="center">An instance of restful API for converting PDF format file(s) to PNG format image(s).</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#build-a-container-image">Build a container image</a> •
  <a href="#credits">Credits</a> •
  <a href="#authors">Authors</a> •
  <a href="#license">License</a>
</p>

## Key Features

* Restful API - Resources, Uniform Interface, Stateless, Cacheable, Layered System
  - Restful API make the converting result of PNG format file(s) as a uniform resource to be simple, lightweight and fast.
* Based on Flask - Lightweight, Flexible, Web framework
  - Simple and easy to use is the core philosophy of Flask. It is also called microframework for  Python, which can be deployed easily as a microservice based on those characteristics.
* Convert by Pdfplumber - Excellent PDF resolving tool
  - Text, rectangle or line in a PDF file can be extracted normally by Pdfplumber. The effect of Converting a PDf file to PNG format images page by page is also stunning.

## How To Use

To clone and run this instance, you'll need [Git](https://git-scm.com) and [Python](https://www.python.org/downloads/)  installed on your computer at first, The version of Python must be ≥ v3.9, and the v3.9 is recommended. And then, from your command line:

``` bash
# install Flask and pdfplumber
pip install --upgrade pip setuptools
pip install pdfplumber Flask waitress Flask-Markdown
```

Download python file of [pdf2png.py](https://github.com/sitwjn/pdf2png/blob/main/pdf2png.py) to a directory in local. In this guid, The file put into directory of /var/flask for example:

``` bash
# create directory to save souce files
mkdir /var/flask
cd /var/flask
wget https://raw.githubusercontent.com/sitwjn/pdf2png/main/pdf2png.py 
```

To start pdf2png service by command:

``` bash
python pdf2png.py
```

The definition of upload single file API in [pdf2png.py](https://github.com/sitwjn/pdf2png/blob/main/pdf2png.py) as below:

``` python
@app.route('/upload', methods=['POST'])
def upload_file():
```

The definition of upload multi files API in [pdf2png.py](https://github.com/sitwjn/pdf2png/blob/main/pdf2png.py) as below:

``` python
@app.route('/uploads', methods=['POST'])
def upload_files():
```

If you want to get read me info and example about how to use this python script in detail. There are two files must be download into directory of /var/flask in advance:

``` bash
wget https://raw.githubusercontent.com/sitwjn/pdf2png/main/README.md
wget https://raw.githubusercontent.com/sitwjn/pdf2png/main/example.html
```

> **Note**
> The files downloaded above can be cloned by [Git](https://git-scm.com) also:

``` git
git clone https://github.com/sitwjn/pdf2png.git
```

An example about how to call API in [pdf2png.py](https://github.com/sitwjn/pdf2png/blob/main/pdf2png.py) in the page of [example.html](https://github.com/sitwjn/pdf2png/blob/main/example.html), including two API for upload file which PDF format are given as below:

- Sample codes for calling to upload single PDF file API in html page:

``` html
<form action="/upload" method="post" enctype="multipart/form-data">
	<input type="file" name="file">
	<select class="custom-select" name="resolution">
		<option value="100">100</option>
		<option value="200">200</option>
		<option value="300">300</option>
		<option value="400">400</option>
	 </select><span>&nbsp;px</span>
	<input type="submit" value="Upload">
</form>
```

- Sample codes for calling to upload multiple PDF files API in html page:

``` html
<form action="/uploads" method="post" enctype="multipart/form-data">
	<input type="file" name="files" multiple>
	<select name="resolution">
		<option value="100">100</option>
		<option value="200">200</option>
		<option value="300">300</option>
		<option value="400">400</option>
	</select><span>px</span>
	<input type="submit" value="Upload">
</form>
```

> **Note**
> The example form of calling API is an ajax submit action with async effect in the page of [example.html](https://github.com/sitwjn/pdf2png/blob/main/example.html).

## Build a container image

Pdf2Png is a lightweight service written by flask framework in language of Python. It is suitable to build as a container image for deploying in container runtime, such as docker or containerd. In that case, Pdf2Png can easily working as a microservice flexibly and conveniently on a container platform such as K8s, K3s or Nomad etc.

An example of [Dockerfile](https://github.com/sitwjn/pdf2png/blob/main/Dockerfile) for built as a docker image is given in this project. After the project is obtained as whether a git repository or zip package, it can be built as a docker image after all of files are put in a directory.

The docker image also can be built without other files but single **Dockerfile** as below:

``` dockerfile
FROM python:3.9

ARG HOME_PATH
ENV ENV_HOME_PATH=$HOME_PATH

RUN pip install --upgrade pip setuptools; \
    pip install pdfplumber Flask waitress Flask-Markdown; \
    mkdir $HOME_PATH

ADD https://raw.githubusercontent.com/sitwjn/pdf2png/main/pdf2png.py https://raw.githubusercontent.com/sitwjn/pdf2png/main/README.md https://raw.githubusercontent.com/sitwjn/pdf2png/main/example.html $HOME_PATH

WORKDIR $HOME_PATH

ENTRYPOINT python pdf2png.py ${ENV_HOME_PATH}
```

The image build command such as below for example:

``` bash
docker build --build-arg "HOME_PATH=/var/flask/" -t pdf2png:1.0.0 . -f Dockerfile
```

> **Note**
> To Make a smaller docker image, the original image in [Dockerfile](https://github.com/sitwjn/pdf2png/blob/main/Dockerfile) can be built based on [docker-library/python/3.9/alpine3.20](https://github.com/docker-library/python/blob/master/3.9/alpine3.20/Dockerfile) by your self.

## Credits

This project uses the following open source packages:

- [Python](https://www.python.org/downloads/)
- [Flask](https://flask.palletsprojects.com/)
- [pdfplumber](https://pypi.org/project/pdfplumber/)
- [waitress](https://pypi.org/project/waitress/)
- [Flask-Markdown](https://pythonhosted.org/Flask-Markdown/)

## Authors

* **Jianai Wang** - *Initial work* - [pdf2png](https://github.com/sitwjn/pdf2png)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/sitwjn/pdf2png/blob/main/LICENSE) file for details

