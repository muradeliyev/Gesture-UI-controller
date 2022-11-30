class Point:
    def __init__(self, x, y, z=0, label: str = None, connect_to=None):
        self.x = x
        self.y = y
        self.z = z
        self.label = label
        self.connect_to = connect_to

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    @staticmethod
    def from_landmark(landmark):
        return Point(
            x=landmark.x,
            y=landmark.y,
            z=landmark.z
        )
