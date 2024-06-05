# UwU Dating

This is a total rewrite of UwU.tours app by [larsmm](https://github.com/larsmm) and [jarainf](https://github.com/jarainf).
[Original UwU.tours](https://github.com/jarainf/UwU.tours)


This rewrite features:
- 
- Easy to access settings / configuration files for both server and templates
- A resilliant web socket based chat application
- Enhanced accessibility on mobile devices
- Light mode
- Varius comfort and quality of life improvements
- And more

How to get started:
-
Just use the docker-compose file to spin up a docker container using `sudo docker-compose up -d`, while you are in the projects root directory.<br>
Alternatively go into src/python, install all requirements and start main.py

```bash
cd src/python
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python3 ./main.py
```
