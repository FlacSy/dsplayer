class Queue:
    def __init__(self):
        self.queue = []
        self.history = []
        self.current_track = None
        self.repeat = False

    def add_track(self, track_info):
        self.queue.append(track_info)

    def get_current_track(self):
        return self.current_track

    def get_queue(self):
        return self.queue

    def get_history(self):
        return self.history

    def remove_track(self, index):
        if 0 <= index < len(self.queue):
            return self.queue.pop(index)
        return None

    def toggle_repeat(self):
        self.repeat = not self.repeat

    def next_track(self):
        if self.repeat and self.current_track:
            return self.current_track
        if self.queue:
            self.current_track = self.queue.pop(0)
            self.history.append(self.current_track)
            return self.current_track
        self.current_track = None
        return None
