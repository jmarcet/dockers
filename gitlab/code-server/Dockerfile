FROM ghcr.io/linuxserver/code-server

RUN apt-get update && apt-get install -y \
	build-essential docker-compose flake8 git golang ipython3 tmux vim zsh \
	python3-ipdb python3-ipython python3-flake8 python3-flake8-docstrings \
	python3-flake8-polyfill python3-hacking python3-pep8-naming python3-pydocstyle \
	python3.8 python3.8-dev python3.8-venv && \
	apt-get -y clean && apt-get -y autoremove

RUN mv /usr/local/share/.config/yarn/global/node_modules/code-server/vendor/modules/code-oss-dev/product.json \
	/usr/local/share/.config/yarn/global/node_modules/code-server/vendor/modules/code-oss-dev/product.json-ORIG
COPY product.json /usr/local/share/.config/yarn/global/node_modules/code-server/vendor/modules/code-oss-dev/product.json

RUN groupmod -g 65536 docker && usermod -aG docker abc
