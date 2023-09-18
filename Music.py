import os
import pygame
import time
from mingus.containers import NoteContainer, Bar, Track, Composition
import mingus.core.chords as chords
from mingus.midi import midi_file_out

class Music:
    def __init__(self):
        self.scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.tempo = 120
        self.note_fraction = 2
        self.triplet = self.note_fraction * 3 / 2
        self.comp = Composition()
        self.comp.set_title("simple_harmony")
        self.track = Track()
        self.midi_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simple_harmony.mid")
        self.initialize_composition()
        self.create_midi_file()
        self.play_midi_file()

    def initialize_composition(self):
        for i in range(0, len(self.scale)):
            self.track.add_bar(self.create_bar(chords.minor_triad(self.scale[(i + 2) % 12]), self.note_fraction))       # ii
            self.track.add_bar(self.create_bar(chords.major_triad(self.scale[(i + 4) % 12]), self.note_fraction))       # V
            self.track.add_bar(self.create_bar(chords.major_triad(self.scale[i % 12]), self.note_fraction))             # I
            self.track.add_bar(self.create_bar(chords.minor_triad(self.scale[(i + 5) % 12]), self.note_fraction*2))     # vi
            self.track.add_bar(self.create_bar(chords.minor_triad(self.scale[(i + 2) % 12]), self.note_fraction*2))     # ii
            self.track.add_bar(self.create_bar(chords.major_triad(self.scale[(i + 4) % 12]), self.note_fraction))       # V
            self.track.add_bar(self.create_bar(chords.major_triad(self.scale[i % 12]), self.note_fraction))             # I
            self.track.add_bar(self.create_bar(chords.diminished_triad(self.scale[(i + 11) % 12]), self.note_fraction*2)) # vii
            self.track.add_bar(self.create_bar(chords.major_triad(self.scale[(i + 3) % 12]), self.note_fraction*2))       # IV
        self.comp.add_track(self.track)

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
    
