import cv2

class Boat:
    def __init__(self, box, id=None):
        """
        Initialize a Boat object.

        :param box: tuple of bounding box coordinates (x1, y1, x2, y2) for the boat.
        :param id: optional unique identifier for the boat.
        """
        self.id = id
        self.prev_coords = None
        self.coords = None
        self.update_coords(box)
        self.speed = 0.0
        self.min_dist_from_center = float('inf')
        self.captured = False

    def update_coords(self, box):
        """
        Update the boat's coordinates and compute its speed based on the change in position.

        :param new_box: tuple of bounding box coordinates (x1, y1, x2, y2) for the boat.
        """
        # Update the previous coordinates to the current ones before updating current to new
        self.prev_coords = self.coords

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        self.coords = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'xmid': abs(x2 - x1) / 2 + min(x2, x1),
            'ymid': abs(y2 - y1) / 2 + min(y2, y1)
        }

        # Update speed based on distance traveled and a time unit (assuming 1 for simplicity)
        if self.prev_coords:
            distance = ((self.coords['xmid'] - self.prev_coords['xmid']) ** 2 + (self.coords['ymid'] - self.prev_coords['ymid']) ** 2) ** 0.5
            self.speed = distance  # Here, speed = distance as time is assumed to be 1 unit. You can adjust as needed.
    
    def is_moving_towards_point(self, point):
        """
        Check if the boat is moving towards a point.

        :param point: tuple of coordinates (x, y) for the point.
        """
        previous_distance = ((point[0] - self.prev_coords['xmid']) ** 2 + (point[1] - self.prev_coords['ymid']) ** 2) ** 0.5
        current_distance = ((point[0] - self.coords['xmid']) ** 2 + (point[1] - self.coords['ymid']) ** 2) ** 0.5
        # print(f"{self.id}: {self.coords['xmid']}, {self.coords['ymid']} -- {self.prev_coords['xmid']}, {self.prev_coords['ymid']}")
        # print(f"Previous distance: {previous_distance}, Current distance: {current_distance}")
        # print(current_distance < previous_distance)
        new_min = current_distance < previous_distance and current_distance < self.min_dist_from_center
        if new_min:
            self.min_dist_from_center = current_distance
        return new_min

    def __str__(self):
        return f"Boat ID: {self.id}, Current Coords: {self.coords}, Previous Coords: {self.prev_coords}, Speed: {self.speed}"
    
    def draw(self, frame, confidence):
        cv2.rectangle(frame, (self.coords['x1'], self.coords['y1']), (self.coords['x2'], self.coords['y2']), (0, 255, 0), 2)  # Green color for the box
        label = f"{self.id}: {confidence:.2f}"
        cv2.putText(frame, label, (self.coords['x1'], self.coords['y1'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

