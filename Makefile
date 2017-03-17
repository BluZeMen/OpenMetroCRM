SHELL := /bin/bash

fstrun:
	python manage.py makemigrations personnel items messaging registration \
	python manage.py migrate \
	python manage.py createsuperuser 

initdbd:	
	python manage.py gentestdata

run:
	python manage.py runserver 

sh:
	python manage.py shell_plus 

instr:	
	pip install -r requirements.txt 

backup:
	tar -cvpzf ./../backup.tar.gz --exclude=./backup.tar.gz --one-file-system ./




