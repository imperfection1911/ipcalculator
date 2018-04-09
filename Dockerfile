FROM python:3.4
MAINTAINER Anton Aksenov <imperfection1911@gmail.com>
USER root
RUN pip install PyTelegramBotAPI \
    && pip install redis \
    && groupadd -r bot \
    && useradd -r -g bot bot
COPY ./ipcalculator /ipcalculator
COPY ./entrypoint.sh /
RUN chmod -R 775 /ipcalculator && chown -R bot:bot /ipcalculator && chmod 770 /entrypoint.sh && chown bot:bot /entrypoint.sh
WORKDIR /ipcalculator
USER bot
ENTRYPOINT /entrypoint.sh
