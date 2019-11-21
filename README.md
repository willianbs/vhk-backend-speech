# Vanhack English Pre-Test - Backend

_This is was a submission to [Vanhack](https://www.vanhack.com) for vanhackathon 2019_

## Overview

#### Install and run

For instructions for the **Frontend**, please [click here](https://github.com/willianbs/vhk-frontend-speech/).

For the **Backend**, follow these steps:
_You need to have **pip3**/**python 3** installed_

`git clone https://github.com/willianbs/vhk-backend-speech.git`

Go to the project directory and run:

`python3 main.py`

The API endpoint is [POST] <http://localhost:5000/file-upload> to upload a MP4 file.

## Design and Architecture

### Frontend App

A lightweight React.js app

### Backend API

The backend api was implemented as a Python simple server with Flask to deal with the upload request and the speech analysis. No login required at this time.

## About the project

### Problem

One important part of VanHack process is the English verification process.
It needs a real person to evaluate all entries and it can take a lot of time of a small team.

### Solution

My idea can go 2 ways (or both):

- Using as a tool for the users (Premium only?) to test their proficiency before submitting each video. So they'll know if they've performed well enough to get a good grade.
- As an auto evaluation system for the Staff to reject/approve based on AI and if the machine isn't able to get it right or there's a claim, the Staff can optimize the work.

And that's about it :)

_Analysis based on: <https://github.com/Shahabks/my-voice-analysis>_
