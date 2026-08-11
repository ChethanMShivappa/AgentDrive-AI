import asyncio
import os
import time
import uuid

import edge_tts
import pygame


class VoiceAgent:

    def __init__(self):

        pygame.mixer.init()

        self.last_message = ""

        self.last_spoken_time = 0

        self.cooldown = 5

    def speak(self, message):

        current_time = time.time()

        if not message:
            return

        if (
            message == self.last_message
            and current_time - self.last_spoken_time < self.cooldown
        ):
            return

        self.last_message = message

        self.last_spoken_time = current_time

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