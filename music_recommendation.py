# -*- coding: utf-8 -*-
"""
Created on Tue May 26 14:09:19 2026

@author: gersh
"""

def recommend_music(emotion):
    emotion = emotion.lower()

    music_map = {
        "happy": {
            "music": "Pop Music",
            "description": "Energetic and positive music."
        },
        "sad": {
            "music": "Relaxing Piano Music",
            "description": "Soft piano music can help calm sadness."
        },
        "angry": {
            "music": "Calm Meditation Music",
            "description": "Slow music may help reduce anger."
        },
        "neutral": {
            "music": "Lo-fi Music",
            "description": "Lo-fi music is suitable for a neutral mood."
        },
        "surprise": {
            "music": "Light Instrumental Music",
            "description": "Light music can keep the mood stable."
        },
        "fear": {
            "music": "Comforting Music",
            "description": "Warm music may help reduce fear."
        },
        "disgust": {
            "music": "Nature Sounds",
            "description": "Peaceful sounds may improve negative emotions."
        }
    }

    return music_map.get(emotion, {
        "music": "Soft Background Music",
        "description": "General relaxing music."
    })
