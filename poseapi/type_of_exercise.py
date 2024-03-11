from body_part_angle import BodyPartAngle


class TypeOfExercise(BodyPartAngle):
    def __init__(self, landmarks):
        super().__init__(landmarks)

    def bicep_curl(self, counter, stage):
        angle = self.angle_of_the_left_arm()
        if angle > 160 and stage != "down":
            stage = "down"
            voice_prompt = "Go Up"
        elif angle < 30 and stage == "down":
            stage = "up"
            counter += 1
            voice_prompt = "Go Down"
        else:
            voice_prompt = ""
        return counter, stage, voice_prompt

    def squat(self, counter, stage):
        left_leg_angle = self.angle_of_the_left_leg()
        right_leg_angle = self.angle_of_the_right_leg()
        avg_leg_angle = (left_leg_angle + right_leg_angle) / 2

        if avg_leg_angle > 160 and stage != "up":
            stage = "up"
            voice_prompt = "Squat Down"
        elif avg_leg_angle < 80 and stage != "down":
            stage = "down"
            counter += 1
            voice_prompt = "Go Up"
        else:
            voice_prompt = ""
        return counter, stage, voice_prompt
