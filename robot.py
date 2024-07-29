from connector import getConnection
from os import path
from scp import SCPClient
  
import qi
import time
import math
import os
import sys
import random
import paramiko
import json
import soundfile

import speech_recognition as sr

r = sr.Recognizer()
file_path = path.dirname(path.realpath(__file__))
listening = True

# --------------------------- READ FILE FUNCTION -----------------------------------
def get_answers(txt_path):
    file = open(txt_path, "r")
    content = file.read()
    pairs = content.split(';')

    answers = {}
    for pair in pairs:
            if pair.strip():
                key, value = pair.split('=', 1)
                key = key.strip().strip('"')
                value = value.strip().strip('{}')
                value_list = json.loads(value)
                answers[f"answer_{key.replace(' ', '_')}"] = value_list
    return answers


# --------------------------- BASIC ROBOT FUNCTIONS -----------------------------------
def stand_position(posture_service):
    posture_service.goToPosture("StandInit", 1.0)
    return print("Robot is standing")

def sit_position(posture_service):
    posture_service.goToPosture("Sit", 1.0)
    return print("Robot is sitting")

def download_audio_file(file_name, scp):
    scp.get(file_name, local_path=file_path)
    print("[INFO]: File " + file_name + " downloaded")
    scp.close()

def listen(audio_service, scp):
    audio_service.stopMicrophonesRecording()
    print("Say something to the robot")
    
    audio_service.startMicrophonesRecording("/home/nao/speech.wav", "wav", 16000, (0, 0, 1, 0))
    time.sleep(5)
    audio_service.stopMicrophonesRecording
    
    download_audio_file("speech.wav", scp)

    return print("Listened")


# --------------------------- SPEECH RECOGNITION FUNCTIONS -----------------------------
def recognize_speech(services, obj_position, speech, answers):
    memory_service, motion_service, tts, posture_service = services

    speech_lower = speech.lower()

    # Hello Condition
    if (("hello") in speech_lower):
        answer_hello = answers['answer_hello']
        return tts.say(random.choice(answer_hello))

    # What's Your Name Condition
    if (("your name") in speech_lower):
        answer_your_name = answers['answer_your_name']
        return tts.say(random.choice(answer_your_name))
    
    # They say their name Condition
    elif (("my name") in speech_lower):
        name = speech_lower.split()[-1]
        answer_my_name = answers['answer_my_name']
        tts.say(random.choice(answer_my_name) + name)
        return name
    
    # How are you Condition
    elif (("how are you") in speech_lower):
        answer_how_are_you = answers['answer_how_are_you']
        return tts.say(random.choice(answer_how_are_you))
    
    # What can you do Condition
    elif (("what can you") in speech_lower):
        answer_what_can_you = answers['answer_what_can_you']
        return tts.say(random.choice(answer_what_can_you))
    
    # Stand up Condition
    elif (("stand") in speech_lower):
        answer_stand = answers['answer_stand']
        tts.say(random.choice(answer_stand))
        return stand_position(posture_service)

    # Sit down Condition
    elif (("sit") in speech_lower):
        answer_sit = answers['answer_sit']
        tts.say(random.choice(answer_sit))
        return sit_position(posture_service)

    # Thank you Condition
    elif (("thank you") in speech_lower):
        answer_thank_you = answers['answer_thank_you']
        return tts.say(random.choice(answer_thank_you))
    
    # Good job Condition
    elif (("good job") in speech_lower):
        answer_good_job = answers['answer_good_job']
        return tts.say(random.choice(answer_good_job))

    # Bye Condition
    elif (("goodbye") in speech_lower):
        answer_bye = answers['answer_goodbye']
        tts.say(random.choice(answer_bye))
        listening = False
        return motion_service.rest()

    # Walk to 
    elif(("walk") in speech_lower):
        answer_walk = answers['answer_walk']
        tts.say(random.choice(answer_walk))
        return walk_to_object(motion_service, obj_position, posture_service)

    # Can you grab Condition
    elif (("grab") or ("pick up") or ("get") or ("i want") in speech_lower):
        answer_grab_pos = answers['answer_grab_pos']

        answer_grab_neg = answers['answer_grab_neg']

        answer_grab_neg_end = answers['answer_grab_neg_end']

        if (("red ball") in speech_lower):
            #if (detect_object(memory_service)):
                tts.say(random.choice(answer_grab_pos) + "red ball")
                walk_to_object(motion_service, obj_position, posture_service)
                return pick_up_object(motion_service, obj_position)

            #else: 
                #return tts.say(random.choice(answer_grab_neg) + "red ball" + answer_grab_neg_end)

        if (("green ball") in speech_lower):
            #if (detect_object(memory_service)):
                tts.say(random.choice(answer_grab_pos) + "green ball")
                walk_to_object(motion_service, obj_position, posture_service)
                return pick_up_object(motion_service, obj_position)

            #else: 
                #return tts.say(random.choice(answer_grab_neg) + "green ball" + answer_grab_neg_end)

        else:
            answer_else_grab = answers['answer_else_grab']
            return tts.say(random.choice(answer_else_grab))
    
    else:
        answer_else_speech = answers['answer_else_speech']
        return tts.say(random.choice(answer_else_speech))

def detect_speech(services, obj_position, answers):    
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "speech.wav")

    data, samplerate = soundfile.read(AUDIO_FILE)
    soundfile.write(AUDIO_FILE, data, samplerate)

    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)

    try:
        speech = r.recognize_google(audio)
        recognize_speech(services, obj_position, speech, answers)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


# --------------------------------- OBJECT FUNCTIONS --------------------------------
# Detect the object
def detect_object(memory_service):
    # Example of detection event, replace with actual object detection implementation
    # This function should return the object's position (x, y, z)
    # Here we're using a placeholder
    # obj_position = memory_service.getData("ObjectDetected")
    return (0, 0, 10 )

# Walk towards the object
def walk_to_object(motion_service, obj_position, posture_service):
    posture_service.goToPosture("StandInit", 1.0)
    x, y, z = obj_position 
    distance = math.sqrt(x*2 + y*2)
    angle = math.atan2(y, x)
    
    # Move towards the object
    motion_service.moveTo(distance, 0, angle)

# Pick up the object
def pick_up_object(motion_service, obj_position):
    # Assuming the object is in front and reachable by the arm
    motion_service.setAngles("RShoulderPitch", 0.0, 0.2)  # Adjust the arm pitch
    motion_service.setAngles("RElbowYaw", 0.0, 0.2)       # Adjust the elbow yaw
    motion_service.setAngles("RHand", 1.0, 0.2)           # Open the hand
    time.sleep(1)
    
    # Move the arm to grasp the object
    motion_service.setAngles("RShoulderPitch", 0.5, 0.2)  # Lower the arm
    time.sleep(1)
    motion_service.setAngles("RHand", 0.0, 0.2)           # Close the hand to grasp
    time.sleep(1)
    
    # Lift the object
    motion_service.setAngles("RShoulderPitch", 0.0, 0.2)  # Lift the arm
    time.sleep(1)


# ---------------------------- MAIN FUNCTION -------------------------------
def main():
    app = getConnection()
    
    # Get the services
    memory_service = app.session.service("ALMemory")
    motion_service = app.session.service("ALMotion")
    tts = app.session.service("ALTextToSpeech")
    posture_service = app.session.service("ALRobotPosture")
    audio_service = app.session.service("ALAudioRecorder")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(hostname="IP_ADDRESS", username="username", password="password")
    scp = SCPClient(ssh.get_transport())

    services = memory_service, motion_service, tts, posture_service
    
    # Wake up robot
    motion_service.wakeUp()
    
    # Detect the object
    obj_position = 0.3, 0, 0

    # Get dictionary
    txt_path = "/../dictionary.txt"
    answers = get_answers(txt_path)

    while listening is True:
        listen(audio_service, scp)
        detect_speech(services, obj_position, answers)
        time.sleep(3)

    # Rest robot
    motion_service.rest()

if __name__ == "__main__":
    main()
