import os
import pygame
import time
from mingus.containers import NoteContainer, Bar, Track, Composition
import mingus.core.chords as chords
from mingus.midi import midi_file_out
from mingus.containers import Note

class Music:
    def __init__(self):
        self.scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.tempo = 120
        self.half_note = 2
        self.quarter_note = self.half_note * 2
        self.eighth_note = self.quarter_note * 2
        self.comp = Composition()
        self.comp.set_title("simple_harmony")
        self.track = Track()
        self.midi_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simple_harmony.mid")
        self.initialize_composition()
        self.create_midi_file()
        self.play_midi_file()

    def initialize_composition(self):
        self.bass_track = Track()
        for i in range(0, len(self.scale)):
            self.add_chord_progression_and_bassline(i)
        self.comp.add_track(self.track)
        self.comp.add_track(self.bass_track)

    def add_chord_progression_and_bassline(self, i):
        chord_progressions  = [
            chords.minor_triad(self.scale[(i + 2) % 12]),  # ii
            chords.major_triad(self.scale[(i + 4) % 12]),  # V
            chords.major_triad(self.scale[i % 12]),        # I
            chords.minor_triad(self.scale[(i + 5) % 12]),  # vi
            chords.minor_triad(self.scale[(i + 2) % 12]),  # ii
            chords.major_triad(self.scale[(i + 4) % 12]),  # V
            chords.major_triad(self.scale[i % 12]),        # I
            chords.diminished_triad(self.scale[(i + 11) % 12]), # vii
            chords.major_triad(self.scale[(i + 3) % 12]),  # IV
        ]
        
        duration_list = [
            self.half_note,
            self.half_note,
            self.half_note,
            self.quarter_note,
            self.quarter_note,
            self.half_note,
            self.half_note,
            self.quarter_note,
            self.quarter_note,
        ]
        
        for chord_progression, duration in zip(chord_progressions, duration_list):
            self.track.add_bar(self.create_bar(chord_progression, duration))
            bassline_notes = [Note(chord_progression[1], 2), Note(chord_progression[2], 2), Note(chord_progression[1], 2), Note(chord_progression[0], 2)]
            # bassline_notes = [Note(chord_progression[0], 2), Note(chord_progression[2], 2), Note(chord_progression[1], 2), Note(chord_progression[0], 2)]
            bassline_durations = [self.eighth_note, self.eighth_note, self.eighth_note, self.eighth_note]
            self.bass_track.add_bar(self.create_bassline_bar(bassline_notes, bassline_durations))

    def create_bassline_bar(self, notes, durations):
        bar = Bar()
        for note, duration in zip(notes, durations):
            bar.place_notes(NoteContainer([note]), duration)
        return bar

    def create_bar(self, chord_notes, duration):
        bar = Bar()
        bar.place_notes(NoteContainer(chord_notes), duration)
        return bar

    def create_midi_file(self):
        midi_file_out.write_Composition(self.midi_file_path, self.comp)
        print(f"The MIDI file has been created at: {self.midi_file_path}")

    def play_midi_file(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.midi_file_path)
        pygame.mixer.music.play(-1)  # Loop indefinitely

        while True:
            time.sleep(1)
            if self.game_ended():  # Replace with end condition
                pygame.mixer.music.stop()
                pygame.quit()
                break

    def game_ended(self):
        return False

if __name__ == "__main__":
    Music()
    
