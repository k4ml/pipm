PoC for method described in this [article][1].


## Installation

```
git clone https://github.com/k4ml/pipm.git
cd pipm
sudo cp pipm.py /usr/local/bin/pipm
```

## Usage

Now we can run it as `pipm`. For example:-

```
mkdir myproject
cd myproject
pipm install django
pipm run django startproject myproject .
pipm run python manage.py runserver

## OR
pipm install httpie
pipm run httpie https://httpbin.org/post address=kb go=lang

## generate requirements.txt
pipm freeze | tee requirements.txt
certifi==2019.9.11
chardet==3.0.4
Django==2.2.7
httpie==1.0.3
idna==2.8
Pygments==2.5.1
pytz==2019.3
requests==2.22.0
sqlparse==0.3.0
urllib3==1.25.7
```

[1]:https://dev.to/k4ml/python-local-packages-a-la-npm-nodemodules-3240
