# Nao6 Voice Assistant Project

This project was developed to make the Nao Robot interect with the users, using Speech Recognition and Object Detection. This code recognizes spoken words, with the robot's front microphone, and answers using a simple dictionary. Also uses Open CV to detect objects using the robot's camera image. 

There are some requirements to run this project in your machine:

1) The code was developed using Python 3.10. Check if your machine has this Python version installed.

2) Check if your machine has the following required libraries:
- library qi https://pypi.org/project/qi/ (Check out the step by step installation file)
- SpeechRecognition https://pypi.org/project/SpeechRecognition/
- PyAudio https://pypi.org/project/PyAudio/
- scp https://pypi.org/project/scp/
- paramiko https://pypi.org/project/paramiko/
- soundfile https://pypi.org/project/soundfile/
- json
- cv2 https://pypi.org/project/opencv-python/

3) When all the libraries are successfully installed, clone the repository.

4) Open the connector.py file:
- insert the username and password of your Nao Robot in the Authenticator class;
- insert the IP and port address of your Nao Robot in the getConnection function.

5) Open the robot.py file:
- insert the IP address (hostname), username and password of your Nao Robot in the ssh connection in the main function.

6) Check out the document "How the code works" to understand the available functions.

6) Turn on your Nao Robot and run the code to start using it. Have fun ;)
