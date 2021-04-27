FROM ghcr.io/linuxserver/code-server

RUN apt-get update && apt-get install -y \
	build-essential docker-compose git golang tmux vim zsh && \
	apt-get -y clean && apt-get -y autoremove

RUN mv /usr/local/share/.config/yarn/global/node_modules/code-server/lib/vscode/product.json \
	/usr/local/share/.config/yarn/global/node_modules/code-server/lib/vscode/product.json-ORIG
COPY product.json /usr/local/share/.config/yarn/global/node_modules/code-server/lib/vscode/product.json

RUN groupmod -g 65536 docker && usermod -aG docker abc
