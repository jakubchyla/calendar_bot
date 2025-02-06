FROM python:3.12

RUN mkdir -p /opt/bot && chmod 755 /opt && chmod 755 /opt/bot
WORKDIR /opt/bot

# create and activate venv
ENV VIRTUAL_ENV=/opt/bot/venv
RUN python3 -m venv /opt/bot/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy application
COPY src/ /opt/bot/src

ENTRYPOINT [ "/bot/entrypoint.sh" ]

