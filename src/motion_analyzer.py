class MotionAnalyzer:

    def __init__(self):

        self.previous_positions = {}

    def analyze(self, result):

        motion_info = {}

        if result.boxes.id is None:
            return motion_info

        ids = result.boxes.id.int().tolist()
        boxes = result.boxes.xyxy.tolist()
        classes = result.boxes.cls.int().tolist()

        for track_id, box, cls in zip(ids, boxes, classes):

            class_name = result.names[cls]

            x1, y1, x2, y2 = box

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            current_position = (center_x, center_y)

            if track_id in self.previous_positions:

                previous_position = self.previous_positions[track_id]

                dy = center_y - previous_position[1]

                if dy > 2:
                    movement = "Approaching"

                elif dy < -2:
                    movement = "Moving Away"

                else:
                    movement = "Stable"

            else:

                movement = "New Object"

            motion_info[track_id] = {
                "class": class_name,
                "movement": movement
            }

            self.previous_positions[track_id] = current_position

        return motion_info