SHELL := /bin/bash
VENV_SRC = ../manage/venv-activate.sh


venv:
	source $(VENV_SRC)

fstrun:
	source $(VENV_SRC) \
	python manage.py makemigrations personnel items messaging \
	python manage.py migrate \
	python manage.py createsuperuser 

tstdb:	
	source $(VENV_SRC) \
	python manage.py gentestdata

run:
	source $(VENV_SRC) \
	python manage.py runserver 

sh:
	source $(VENV_SRC) \
	python manage.py shell_plus 

dep:	
	source $(VENV_SRC) \
	pip install -r requirements.txt 

backup:
	tar -cvpzf ./../backup.tar.gz --exclude=./backup.tar.gz --one-file-system ./

# for lazy
push:
	expect ../manage/loc2rem.sh

pull:
	expect ../manage/rem2loc.sh

sshdev:
	expect ../manage/udelgi-a-dev.sh

sshroot:
	expect ../manage/udelgi-a-root.sh


