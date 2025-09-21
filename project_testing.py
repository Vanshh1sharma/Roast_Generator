import cv2
from PIL import Image, ImageDraw, ImageFont
import pyttsx3 as sx
import random
import textwrap
import time

# -------------------
# Roast generator function
# -------------------
def mood(user_input):
    moods = {
        "happy": [
            "You're so happy, even therapists feel unemployed around you.",
            "Your smile is brighter than your future—good luck with that.",
            "You're proof that caffeine can walk and talk.",
            "Your vibe is so high, even Wi-Fi signals get jealous.",
            "You laugh like life’s a joke. It is — you’re the punchline."
        ],
        "sad": [
            "You're not unlucky—just consistently bad at everything.",
            "Even your shadow looks like it’s trying to leave.",
            "You post sad quotes like Wi-Fi signals — weak and desperate.",
            "If tears could pay bills, you’d be a millionaire.",
            "You’re the reason Spotify suggests 'sad lo-fi at 3AM'.",
            "Your aura is so gloomy, even Alexa whispers around you.",
            "You don’t carry emotional baggage — you own a whole airline.",
            "Even the tissue box filed a complaint for emotional burnout."
        ]
    }
    if user_input in moods:
        return random.choice(moods[user_input])
    else:
        return "Mood not recognised baby doll"

# -------------------
# Load cascades
# -------------------
face_cascade = cv2.CascadeClassifier(
    r"C:\Users\vansh\OneDrive\Desktop\Project\Roast generator\Prototypes\Prototype_2\haarcascade_frontalface_alt.xml"
)
smile_cascade = cv2.CascadeClassifier(
    r"C:\Users\vansh\OneDrive\Desktop\Project\Roast generator\Prototypes\Prototype_2\haarcascade_smile.xml"
)

cap = cv2.VideoCapture(0)
mood_detected = "sad"  # default
timeout = 5  # camera auto-close after 3 seconds

start_time = time.time()
final_frame = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.8, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]

        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=20)

        if len(smiles) > 0:
            mood_detected = "happy"
            cv2.putText(frame, "Smile Detected!", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    cv2.imshow("Smile Detector", frame)
    final_frame = frame.copy()  # save last frame for roast image

    if time.time() - start_time >= timeout:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# -------------------
# Roast Generator Logic
# -------------------
roast = mood(mood_detected)

# Convert OpenCV frame (BGR) to PIL image (RGB)
img = Image.fromarray(cv2.cvtColor(final_frame, cv2.COLOR_BGR2RGB))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("arial.ttf", 32)
wrapped_text = textwrap.fill(roast, width=40)

# Write roast on image
draw.text((50, 50), wrapped_text, fill="black", font=font, stroke_width=2, stroke_fill="white")

# Save image with time in filename
filename = f"THE_FINAL_ROAST_{int(time.time())}.jpg"
img.save(filename)
img.show()

# -------------------
# Text-to-Speech
# -------------------
engine = sx.init()
engine.setProperty("rate", 150)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.say(roast)
engine.runAndWait()
engine.stop()

print(f"Mood: {mood_detected}")
print(f"Roast saved as: {filename}")
print(roast)
