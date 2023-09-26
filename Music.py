import os
import pygame
import time
from mingus.containers import NoteContainer, Bar, Track, Composition
import mingus.core.chords as chords
from mingus.midi import midi_file_out
from mingus.containers import Note

class Music:
    def __init__(self):
        self.setup()
        
    def setup(self):
        self.init_constants()
        self.init_tracks()
        self.init_composition()
        self.generate_midi_file()
        self.play_midi()

    def init_constants(self):
        """Initialize constants."""
        self.scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.tempo = 120
        self.half_note = 2
        self.quarter_note = self.half_note * 2
        self.eighth_note = self.quarter_note * 2
        self.midi_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simple_harmony.mid")
    
    def init_tracks(self):
        """Initialize tracks for melody, harmony, and bassline."""
        self.harmony_track = Track()
        self.bass_track = Track()
        self.melody_track = Track()

    def init_composition(self):
        """Initialize composition and add tracks."""
        self.comp = Composition()
        self.comp.set_title("simple_harmony")
        for i in range(len(self.scale)):
            self.add_chord_progression_and_bassline(i)
        self.comp.add_track(self.harmony_track)
        self.comp.add_track(self.bass_track)
        self.comp.add_track(self.melody_track)

    def add_chord_progression_and_bassline(self, i):
        # 7/4 time signature
        chord_progressions  = [
            # Bar 1, 4/4.
            chords.major_triad(self.scale[(i + 5) % 12]),  # IV
            chords.minor_triad(self.scale[(i + 9) % 12]),  # vi
            chords.minor_triad(self.scale[(i + 2) % 12]),  # ii

            chords.major_triad(self.scale[(i + 7) % 12]),  # V
            chords.minor_triad(self.scale[(i + 4) % 12]),  # iii

            # Bar 2, 3/4.
            chords.minor_triad(self.scale[(i + 9) % 12]),  # vi
            chords.minor_triad(self.scale[(i + 2) % 12]),  # ii

            chords.major_triad(self.scale[(i + 7) % 12]),  # V
            chords.major_triad(self.scale[(i + 5) % 12])  # IV
            # chords.diminished_triad(self.scale[(i + 11) % 12]),  # vii°
        ]
        
        chord_duration_list = [
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

        melody_notes = []
        melody_durations = []

        bassline_notes = [
        # Bar 1, 4/4.
        Note(self.scale[(i + 5) % 12], 2), Note(self.scale[(i + 9) % 12], 2),
        Note(self.scale[(i + 9) % 12], 2), Note(self.scale[(i + 0) % 12], 2), 
        Note(self.scale[(i + 2) % 12], 2), Note(self.scale[(i + 5) % 12], 2),

        Note(self.scale[(i + 7) % 12], 2), Note(self.scale[(i + 4) % 12], 2), Note(self.scale[(i + 7) % 12], 2),

        # Bar 2, 3/4.
        Note(self.scale[(i + 9) % 12], 2), Note(self.scale[(i + 0) % 12], 2),
        Note(self.scale[(i + 2) % 12], 2), Note(self.scale[(i + 5) % 12], 2),
        
        Note(self.scale[(i + 7) % 12], 2), Note(self.scale[(i + 5) % 12], 2), Note(self.scale[(i + 9) % 12], 2)
        ]

        bassline_durations = [
            self.quarter_note, self.quarter_note,
            self.quarter_note, self.quarter_note,
            self.quarter_note, self.quarter_note,

            self.quarter_note, self.eighth_note, self.eighth_note,

            self.quarter_note, self.quarter_note,
            self.quarter_note, self.quarter_note,

            self.quarter_note, self.eighth_note, self.eighth_note
        ]

        harmony_bar = Bar()
        bassline_bar = Bar()
        melody_bar = Bar()  # Empty for now

        for chord_progression, chord_duration, bass_note, bass_duration in zip(chord_progressions, chord_duration_list, bassline_notes, bassline_durations):
            print(f"Adding bass note: {bass_note} with duration {bass_duration}")
            harmony_bar.place_notes(NoteContainer(chord_progression), chord_duration)
            bassline_bar.place_notes(NoteContainer([bass_note]), bass_duration)

        # Add Bars to Respective Tracks
        self.harmony_track.add_bar(harmony_bar)
        self.bass_track.add_bar(bassline_bar)
        self.melody_track.add_bar(melody_bar)

    def create_line_bar(self, notes, durations):
        bar = Bar()
        for note, duration in zip(notes, durations):
            bar.place_notes(NoteContainer([note]), duration)
        return bar

    def create_bar(self, chord_notes, duration):
        bar = Bar()
        bar.place_notes(NoteContainer(chord_notes), duration)
        return bar

    def generate_midi_file(self):
            """Generate MIDI file from composition."""
            midi_file_out.write_Composition(self.midi_file_path, self.comp)
            print(f"MIDI file generated at: {self.midi_file_path}")

    def play_midi(self):
        """Initialize pygame and play MIDI file."""
        pygame.mixer.init()
        pygame.mixer.music.load(self.midi_file_path)
        pygame.mixer.music.play(-1)  # Loop indefinitely
        self.loop_until_game_ends()

    def loop_until_game_ends(self):
        """Keep running until game ends."""
        while True:
            time.sleep(1)
            if self.game_ended():  # Replace with end condition
                pygame.mixer.music.stop()
                pygame.quit()
                break

    def game_ended(self):
        """Check if game has ended."""
        return False

if __name__ == "__main__":
    def main():
        music = Music()
    main()
