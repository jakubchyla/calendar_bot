FROM python:3.12-alpine

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

COPY --chmod= entrypoint.sh /opt/bot/entrypoint.sh

# switch to non root user
RUN addgroup asdf && adduser -G asdf -D -H asdf
USER asdf

ENTRYPOINT [ "/opt/bot/entrypoint.sh" ]

