class DrivingMemory:

    def __init__(self):

        self.last_advice = ""

    def get_last_advice(self):

        return self.last_advice

    def save_advice(self, advice):

        self.last_advice = advice