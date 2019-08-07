PORT=8080

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	name '*~' -exec rm --force {}

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

build:
	yes | sudo apt install python3-pip
	yes | sudo apt install libbz2-dev
	yes | sudo apt install liblzma-dev
	yes | sudo pip3 install pip --upgrade
	yes | sudo pip3 install -r requirements.txt

	mkdir -p msbwtStorage

run:
	nohup waitress-serve --port $(PORT) --call 'msbwtCloud:create_app' >> msbwtCloud.log &

stop:
	killall waitress-serve && echo "Stopped" || echo "No instances running..."

restart: stop run
	


.PHONY: clean-pyc clean-build build run restart




