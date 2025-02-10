FEEDBACK_PROMPT = """
You are provided with squat analysis data extracted from a video. The data is a two-dimensional array where each inner list represents a batch of frames and each element in a batch is the count of frames that match a specific label. The eight labels correspond by their order to the following descriptions:
Perfect Squat means the frame shows a perfect squat without any defects.
Heel Lift means the frame shows the users heels lifting off the ground.
Lean Forward means the frame shows the user excessively leaning forward or shifting their center of mass forward.
Rounding Back means the frame shows the users back hunching or caving in.
Lateral Shift means the frame shows the users center of mass shifting to the side.
Knee Translation means the frame shows the users knees excessively caving inward or outward.
Uneven Shoulders means the frame shows the barbell as tilted or not resting horizontally.
Not Squat means the frame shows that the user is not performing a squat.

Your Task:
1. Compute the percentage of frames in each batch for every label.
2. Do not include the Not Squat count when assessing squat quality and defects but note if it is significant.
3. If more than 90 percent of the frames in a batch are labeled as Not Squat, add a disclaimer stating that due to potential issues with noise angle or video quality the model’s accuracy may be affected.
4. If 90 percent or more of the frames (excluding Not Squat frames) are labeled as Perfect Squat include a message stating that the squat looks pretty good.
5. If either Perfect Squat or Not Squat appears in ten percent or more of the frames mention this observation.
6. For each defect label (Heel Lift, Lean Forward, Rounding Back, Lateral Shift, Knee Translation, Uneven Shoulders) that appears in ten percent or more of the frames include the corresponding statement:
   - For Heel Lift say Your squat indicates signs of a heel lift where your heels are off the ground.
   - For Lean Forward say Your squat indicates signs of excessive forward lean with your center of mass shifting forward.
   - For Rounding Back say Your squat indicates signs of rounding of the back suggesting a hunch or caving in.
   - For Lateral Shift say Your squat indicates signs of lateral shift with your center of mass moving to the side.
   - For Knee Translation say Your squat indicates signs of knee translation with your knees caving inward or outward excessively.
   - For Uneven Shoulders say Your squat indicates signs of uneven shoulders as the bar appears tilted or not horizontally aligned.
7. The main feedback must be written in no more than three sentences and must not contain any special characters fractions or numerical expressions aside from percentages.
8. Conclude your feedback with the disclaimer: SquatBuddy is not a professionally licensed software and should not be trusted as advice from a certified doctor.

Below are the results from the squat analysis:
"""


def get_prompt(data, prompt=FEEDBACK_PROMPT):

    # Append data to the prompt
    prompt += "\n"
    for batch in data:
        prompt += str(batch) + "\n"
    
    return prompt