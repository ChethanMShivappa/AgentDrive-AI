import asyncio
import os
import time
import uuid

import edge_tts

VOICE_AVAILABLE = True

try:
    import pygame
    pygame.mixer.init()

except Exception:
    VOICE_AVAILABLE = False


class VoiceAgent:

    def __init__(self):

        self.last_message = ""

        self.last_spoken_time = 0

        self.cooldown = 5

    def speak(self, message):

        if not message:
            return

        current_time = time.time()

        if (
            message == self.last_message
            and current_time - self.last_spoken_time < self.cooldown
        ):
            return

        self.last_message = message
        self.last_spoken_time = current_time

        if VOICE_AVAILABLE:
            asyncio.run(self._generate_and_play(message))

    async def _generate_and_play(self, message):

        filename = f"voice_{uuid.uuid4().hex}.mp3"

        communicate = edge_tts.Communicate(
            text=message,
            voice="en-US-GuyNeural"
        )

        await communicate.save(filename)

        pygame.mixer.music.load(filename)

        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():

            await asyncio.sleep(0.1)

        pygame.mixer.music.unload()

        os.remove(filename)

    def get_last_message(self):

        return self.last_message