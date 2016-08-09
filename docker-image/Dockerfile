FROM python:3.5

RUN useradd -ms /bin/bash readonly
#RUN cd && cp -R .bash_profile .bashrc .gitconfig .profile scripts /home/readonly

ADD . /home/readonly/app
RUN chown -R root:root /home/readonly

ENV HOME /home/readonly
WORKDIR /home/readonly/app

USER readonly
CMD python telnetd.py 7890
EXPOSE 7890
