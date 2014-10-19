port:=9788
activate_venv=source venv/bin/activate
 
debug:
	export mode=local && ./manage.py runserver $(port) --settings=base.settings_local
 
start-uwsgi:
	uwsgi --socket 127.0.0.1:$(port) \
          --chdir $(shell pwd) \
          --wsgi-file base/wsgi.py \
          --master \
          --process 4 \
          --daemonize $(shell pwd)/logs/uwsgi.log \
          --pidfile $(shell pwd)/uwsgi.pid  
 
stop-uwsgi:
	uwsgi --stop uwsgi.pid
 
reload-uwsgi: 
	uwsgi --reload uwsgi.pid
 
collectstatic:
	./manage.py collectstatic --noinput
 
venv:
	virtualenv venv --python=python2.7
	
deps:
	-pip install -r requirements.txt
	-npm install
	-bower install
	
.PHONY: debug \
	deps \
	collectstatic \
	reload-uwsgi \
	start-uwsgi \
	stop-uwsgi
