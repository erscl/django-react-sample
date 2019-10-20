FROM python:3.7.5-alpine3.10

# Apache2、mod_wsgiのインストール
RUN apk add apache2 apache2-dev musl-dev gcc make g++ file
RUN pip3 install mod-wsgi

# yarnのインストール
RUN apk add bash curl nodejs
RUN touch ~/.bashrc \
    && curl -o- -L https://yarnpkg.com/install.sh | bash \
    && ln -s "$HOME/.yarn/bin/yarn" /usr/local/bin/yarn

COPY . /webapp/

# frontend用のyarn依存関係を入れておく
# (後続のRUNと分けてるのはそれなりに時間かかるのでキャッシュ有効とするため。)
# (後続のbuildはあとから実行するのはそちらはdjango用のcollectstaticなども同時にやっているため。)

RUN cd /webapp/frontend/ && \
    yarn install

# Python依存関係のインストール、及びアプリケーションのビルド

RUN cd /webapp/ && \
    pip3 install -r requirements.txt && \
    python3 manage.py build
RUN cd /webapp/ && \
    pip3 install -r requirements.txt

# 初期実行コマンド
CMD ["/usr/sbin/httpd", "-D", "FOREGROUND", "-f", "/webapp/httpd.conf"]
