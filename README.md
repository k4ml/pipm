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
```

[1]:https://dev.to/k4ml/python-local-packages-a-la-npm-nodemodules-3240
