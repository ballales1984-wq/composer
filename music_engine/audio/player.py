"""
Audio Player for the Music Engine.

This module provides cross-platform audio playback with multiple backend support.
It can play audio waveforms using various libraries.

NOTE: This module is INDEPENDENT from the core. It imports from core
but core does NOT depend on this module.
"""

import threading
import time
from typing import List, Optional, Union

import numpy as np

# Try multiple audio backends
_AUDIO_BACKENDS = []

try:
    import simpleaudio as sa
    _AUDIO_BACKENDS.append('simpleaudio')
except ImportError:
    pass

try:
    import pyaudio
    _AUDIO_BACKENDS.append('pyaudio')
except ImportError:
    pass

try:
    import sounddevice as sd
    _AUDIO_BACKENDS.append('sounddevice')
except ImportError:
    pass

try:
    import winsound
    _AUDIO_BACKENDS.append('winsound')
except ImportError:
    pass


class AudioBackend:
    """Base class for audio backends."""
    
    def __init__(self):
        self.is_playing = False
    
    def play(self, samples: np.ndarray, sample_rate: int = 44100):
        """Play audio samples."""
        raise NotImplementedError
    
    def stop(self):
        """Stop playback."""
        self.is_playing = False


class SimpleAudioBackend(AudioBackend):
    """simpleaudio backend for audio playback."""
    
    def __init__(self):
        super().__init__()
        self.play_obj = None
    
    def play(self, samples: np.ndarray, sample_rate: int = 44100):
        """Play audio using simpleaudio."""
        if len(samples) == 0:
            return
        
        # Convert to 16-bit PCM
        samples_int = (samples * 32767).astype(np.int16)
        
        # Play
        self.play_obj = sa.play_buffer(samples_int, 1, 2, sample_rate)
        self.is_playing = True
        self.play_obj.wait()
        self.is_playing = False
    
    def stop(self):
        """Stop playback."""
        if self.play_obj and self.play_obj.is_playing():
            self.play_obj.stop()
        self.is_playing = False


class PyAudioBackend(AudioBackend):
    """PyAudio backend for audio playback."""
    
    def __init__(self):
        super().__init__()
        self.audio = None
        self.stream = None
        try:
            import pyaudio
            self.audio = pyaudio.PyAudio()
        except Exception:
            pass
    
    def play(self, samples: np.ndarray, sample_rate: int = 44100):
        """Play audio using pyaudio."""
        if self.audio is None or len(samples) == 0:
            return
        
        # Open stream
        self.stream = self.audio.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=sample_rate,
            output=True
        )
        
        self.is_playing = True
        # Write in chunks
        chunk_size = 1024
        samples_bytes = samples.astype(np.float32).tobytes()
        
        for i in range(0, len(samples_bytes), chunk_size):
            if not self.is_playing:
                break
            self.stream.write(samples_bytes[i:i+chunk_size])
        
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        self.is_playing = False
    
    def stop(self):
        """Stop playback."""
        self.is_playing = False
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except Exception:
                pass
            self.stream = None
    
    def __del__(self):
        """Cleanup."""
        if self.audio:
            self.audio.terminate()


class SoundDeviceBackend(AudioBackend):
    """sounddevice backend for audio playback."""
    
    def __init__(self):
        super().__init__()
        self.stream = None
    
    def play(self, samples: np.ndarray, sample_rate: int = 44100):
        """Play audio using sounddevice."""
        if len(samples) == 0:
            return
        
        self.is_playing = True
        sd.play(samples, sample_rate)
        sd.wait()
        self.is_playing = False
    
    def stop(self):
        """Stop playback."""
        sd.stop()
        self.is_playing = False


class WinSoundBackend(AudioBackend):
    """winsound backend for Windows (simple beeps)."""
    
    def __init__(self):
        super().__init__()
    
    def play(self, samples: np.ndarray, sample_rate: int = 44100):
        """Play simple beep using winsound (limited)."""
        if len(samples) == 0:
            return
        
        # Calculate dominant frequency using FFT
        try:
            import numpy as np
            fft = np.fft.fft(samples)
            freqs = np.fft.fftfreq(len(samples), 1/sample_rate)
            dominant_freq = abs(freqs[np.argmax(np.abs(fft))])
            
            # Clamp to valid frequency range for winsound
            freq = max(200, min(20000, int(dominant_freq)))
            duration_ms = max(100, min(1000, int(len(samples) / sample_rate * 1000)))
            
            winsound.Beep(freq, duration_ms)
        except Exception:
            # Fallback to default beep
            winsound.Beep(440, 200)
        
        self.is_playing = False
    
    def stop(self):
        """Stop playback (winsound doesn't support stop)."""
        self.is_playing = False


class Player:
    """
    Cross-platform audio player with automatic backend selection.
    
    Supports multiple backends:
    - simpleaudio (preferred)
    - pyaudio
    - sounddevice
    - winsound (Windows only, limited)
    """
    
    DEFAULT_SAMPLE_RATE = 44100
    
    def __init__(self, sample_rate: int = DEFAULT_SAMPLE_RATE, 
                 backend: Optional[str] = None):
        """
        Initialize the audio player.
        
        Args:
            sample_rate: Audio sample rate in Hz
            backend: Specific backend to use (auto-detect if None)
        """
        self.sample_rate = sample_rate
        self._backend = None
        self._current_thread = None
        
        # Select backend
        if backend:
            self._init_backend(backend)
        else:
            # Try each available backend in order of preference
            for be in ['simpleaudio', 'pyaudio', 'sounddevice', 'winsound']:
                if be in _AUDIO_BACKENDS:
                    if self._init_backend(be):
                        break
    
    def _init_backend(self, backend: str) -> bool:
        """Initialize a specific backend."""
        try:
            if backend == 'simpleaudio':
                self._backend = SimpleAudioBackend()
                return True
            elif backend == 'pyaudio':
                self._backend = PyAudioBackend()
                return self._backend.audio is not None
            elif backend == 'sounddevice':
                self._backend = SoundDeviceBackend()
                return True
            elif backend == 'winsound':
                self._backend = WinSoundBackend()
                return True
        except Exception:
            pass
        return False
    
    @property
    def backend_name(self) -> str:
        """Get the name of the current backend."""
        if self._backend:
            return self._backend.__class__.__name__.replace('Backend', '')
        return 'None'
    
    @property
    def available_backends(self) -> List[str]:
        """Get list of available backends."""
        return _AUDIO_BACKENDS.copy()
    
    def play(self, samples: np.ndarray, async_play: bool = True):
        """
        Play audio samples.
        
        Args:
            samples: Audio samples as numpy array
            async_play: Whether to play asynchronously
        """
        if self._backend is None:
            print("No audio backend available")
            return
        
        if async_play:
            if self._current_thread and self._current_thread.is_alive():
                self.stop()
            self._current_thread = threading.Thread(
                target=self._backend.play, 
                args=(samples, self.sample_rate),
                daemon=True
            )
            self._current_thread.start()
        else:
            self._backend.play(samples, self.sample_rate)
    
    def stop(self):
        """Stop current playback."""
        if self._backend:
            self._backend.stop()
    
    def wait(self):
        """Wait for playback to finish."""
        if self._current_thread and self._current_thread.is_alive():
            self._current_thread.join()
    
    @property
    def is_playing(self) -> bool:
        """Check if audio is currently playing."""
        if self._backend:
            return self._backend.is_playing
        return False


# Global player instance
_player = None

def get_player(sample_rate: int = 44100) -> Player:
    """
    Get the global audio player instance.
    
    Args:
        sample_rate: Sample rate for the player
        
    Returns:
        Player instance
    """
    global _player
    if _player is None:
        _player = Player(sample_rate)
    return _player


def play_samples(samples: np.ndarray, sample_rate: int = 44100, async_play: bool = True):
    """
    Play audio samples using the global player.
    
    Args:
        samples: Audio samples
        sample_rate: Sample rate
        async_play: Play asynchronously
    """
    player = get_player(sample_rate)
    player.play(samples, async_play)


def stop_playback():
    """Stop current playback."""
    player = get_player()
    player.stop()


def get_backend_info() -> dict:
    """Get information about available audio backends."""
    player = get_player()
    return {
        'available_backends': player.available_backends,
        'current_backend': player.backend_name,
        'sample_rate': player.sample_rate
    }

