PORT=8181

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	name '*~' -exec rm --force {}

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

build:
	yes | sudo -H apt install python3-pip
	yes | sudo -H apt install libbz2-dev
	yes | sudo -H apt install zlib1g-dev
	yes | sudo -H apt install liblzma-dev
	yes | sudo -H pip3 install pip --upgrade
	yes | sudo -H pip3 install -r requirements.txt

	mkdir -p msbwtStorage

open:
	sudo -H iptables -A INPUT -p tcp --dport $(PORT) -j ACCEPT

destroy:

	mkdir -p ../msbwtStorage
	mv msbwtStorage/* ../msbwtStorage/
	cd ..
	yes | rm -rf msbwtCloud/
	@echo "BWTs preserved in msbwtStorage one level up"


run:
	nohup waitress-serve --port=$(PORT) --call 'msbwtCloud:create_app' >> msbwtCloud.log &

stop:
	killall waitress-serve && echo "Stopped" || echo "No instances running..."

restart: stop run
	


.PHONY: clean-pyc clean-build build run restart




