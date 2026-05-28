import pretty_midi
import random

def generate_music(emotion, output_file="generated_full_pop_music.mid"):
    emotion = emotion.lower()

    settings = {
        "happy": {
            "chords": [[60, 64, 67], [67, 71, 74], [69, 72, 76], [65, 69, 72]],
            "melody": [60, 62, 64, 67, 69, 72],
            "tempo": 0.5,
            "velocity": 100
        },
        "sad": {
            "chords": [[57, 60, 64], [65, 69, 72], [60, 64, 67], [67, 71, 74]],
            "melody": [57, 60, 62, 64, 65, 69],
            "tempo": 0.75,
            "velocity": 70
        },
        "angry": {
            "chords": [[55, 58, 62], [58, 62, 65], [60, 63, 67], [53, 57, 60]],
            "melody": [55, 58, 60, 62, 65, 67],
            "tempo": 0.45,
            "velocity": 110
        },
        "neutral": {
            "chords": [[60, 64, 67], [62, 65, 69], [57, 60, 64], [67, 71, 74]],
            "melody": [60, 62, 64, 65, 67, 69],
            "tempo": 0.6,
            "velocity": 85
        },
        "surprise": {
            "chords": [[60, 64, 67], [65, 69, 72], [67, 71, 74], [72, 76, 79]],
            "melody": [60, 64, 67, 71, 72, 76],
            "tempo": 0.4,
            "velocity": 105
        },
        "fear": {
            "chords": [[56, 59, 63], [58, 61, 65], [55, 59, 62], [60, 63, 67]],
            "melody": [56, 58, 59, 61, 63, 65],
            "tempo": 0.8,
            "velocity": 65
        },
        "disgust": {
            "chords": [[58, 61, 65], [61, 65, 68], [56, 60, 63], [63, 67, 70]],
            "melody": [58, 60, 61, 63, 65, 68],
            "tempo": 0.7,
            "velocity": 75
        }
    }

    setting = settings.get(emotion, settings["neutral"])

    midi = pretty_midi.PrettyMIDI()

    melody_inst = pretty_midi.Instrument(program=0)      # Piano
    chord_inst = pretty_midi.Instrument(program=4)       # Electric Piano
    bass_inst = pretty_midi.Instrument(program=33)       # Electric Bass
    drum_inst = pretty_midi.Instrument(program=0, is_drum=True)

    beat = setting["tempo"]
    total_bars = 32
    time = 0

    for bar in range(total_bars):
        chord = setting["chords"][bar % len(setting["chords"])]

        # Chords
        for note_pitch in chord:
            note = pretty_midi.Note(
                velocity=setting["velocity"] - 20,
                pitch=note_pitch,
                start=time,
                end=time + beat * 4
            )
            chord_inst.notes.append(note)

        # Bass
        bass_pitch = chord[0] - 24
        for i in range(4):
            bass_note = pretty_midi.Note(
                velocity=setting["velocity"],
                pitch=bass_pitch,
                start=time + i * beat,
                end=time + i * beat + beat * 0.8
            )
            bass_inst.notes.append(bass_note)

        # Melody
        for i in range(4):
            pitch = random.choice(setting["melody"])
            melody_note = pretty_midi.Note(
                velocity=setting["velocity"],
                pitch=pitch,
                start=time + i * beat,
                end=time + i * beat + beat * 0.8
            )
            melody_inst.notes.append(melody_note)

        # Drums
        for i in range(4):
            drum_inst.notes.append(pretty_midi.Note(
                velocity=90,
                pitch=36,   # Kick
                start=time + i * beat,
                end=time + i * beat + 0.1
            ))

        drum_inst.notes.append(pretty_midi.Note(
            velocity=80,
            pitch=38,   # Snare
            start=time + beat * 1,
            end=time + beat * 1 + 0.1
        ))

        drum_inst.notes.append(pretty_midi.Note(
            velocity=80,
            pitch=38,
            start=time + beat * 3,
            end=time + beat * 3 + 0.1
        ))

        for i in range(8):
            drum_inst.notes.append(pretty_midi.Note(
                velocity=50,
                pitch=42,   # Hi-hat
                start=time + i * beat / 2,
                end=time + i * beat / 2 + 0.05
            ))

        time += beat * 4

    midi.instruments.append(melody_inst)
    midi.instruments.append(chord_inst)
    midi.instruments.append(bass_inst)
    midi.instruments.append(drum_inst)

    midi.write(output_file)

    return output_file