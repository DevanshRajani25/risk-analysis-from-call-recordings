from django.shortcuts import render
import whisper
import tempfile
from .models import CallAnalysis
from textblob import TextBlob

model = whisper.load_model("base")

# Keyword lists for intent detection
SPAM_KEYWORDS = [
    "offer", "promotion", "discount", "congratulations", "lucky", "winner", "limited time", "free", "prize", "claim now"
]

COMPLAINT_KEYWORDS = [
    "complaint", "problem", "issue", "angry", "frustrated", "dissatisfied", "unhappy", "terrible", "horrible", "bad service"
]

CRIME_KEYWORDS = [
    "theft", "robbery", "stolen", "break in", "burglar", "robber", "assault", "murder", "kidnapping", "vandalism", "fraud"
]

EMERGENCY_KEYWORDS = [
    "urgent", "help", "fire", "gun", "shoot", "bleeding", "emergency", "police", "ambulance", "accident", "injury", "danger", "serious"
]

# HOME PAGE
def upload_audio(request):
    return render(request, "upload.html")


# ANALYZE + DASHBOARD
def analyze_call(request):
    if request.method != "POST":
        return render(request, "upload.html")

    audio_file = request.FILES.get("audio")

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        for chunk in audio_file.chunks():
            temp_audio.write(chunk)
        temp_audio_path = temp_audio.name

    # Whisper STT
    result = model.transcribe(temp_audio_path)
    transcript = result["text"]

    # Sentiment analysis (ML-based)
    sentiment_score = TextBlob(transcript).sentiment.polarity

    if sentiment_score > 0.3:
        sentiment_label = "positive"
    elif sentiment_score < -0.3:
        sentiment_label = "negative"
    else:
        sentiment_label = "neutral"

    print("SENTIMENT:", sentiment_label, sentiment_score)

    clean_text = transcript.lower()
    clean_text = clean_text.replace(",", "").replace(".", "")
    words = clean_text.split()

    # Count keywords
    scores = {
        "spam": sum(w in SPAM_KEYWORDS for w in words),
        "complaint": sum(w in COMPLAINT_KEYWORDS for w in words),
        "crime": sum(w in CRIME_KEYWORDS for w in words),
        "emergency": sum(w in EMERGENCY_KEYWORDS for w in words),
    }

    predicted_intent = max(scores, key=scores.get)

    # Emotion
    emotion_map = {
        "emergency": "panicked",
        "crime": "fearful",
        "complaint": "angry",
        "spam": "calm"
    }
    emotion = emotion_map[predicted_intent]

    # Priority
    priority_map = {
        "emergency": 5,
        "crime": 3,
        "complaint": 2,
        "spam": 0
    }
    priority = priority_map[predicted_intent]

    # Explanation (intent-specific)
    keyword_map = {
        "emergency": EMERGENCY_KEYWORDS,
        "crime": CRIME_KEYWORDS,
        "complaint": COMPLAINT_KEYWORDS,
        "spam": SPAM_KEYWORDS
    }

    hits = {}
    for w in words:
        if w in keyword_map[predicted_intent]:
            hits[w] = hits.get(w, 0) + 1

    if hits:
        explanation = (
            f"Classified as {predicted_intent} due to keywords: "
            f"{', '.join([f'{k}({v})' for k, v in hits.items()])}. "
            f"Overall sentiment detected as {sentiment_label}."
        )
    else:
        explanation = (
            f"Classified as {predicted_intent} based on overall context. "
            f"Overall sentiment detected as {sentiment_label}."
        )

    # Save to DB
    call_analysis = CallAnalysis.objects.create(
        audio_file=audio_file,
        detected_emotion=emotion,
        call_category=predicted_intent,
        priority_rating=priority
    )

    # Dashboard data
    stats = {
        "total": CallAnalysis.objects.count(),
        "emergency": CallAnalysis.objects.filter(call_category="emergency").count(),
        "crime": CallAnalysis.objects.filter(call_category="crime").count(),
        "complaint": CallAnalysis.objects.filter(call_category="complaint").count(),
        "spam": CallAnalysis.objects.filter(call_category="spam").count(),
    }

    recent_calls = CallAnalysis.objects.order_by("-created_at")[:5]

    return render(request, "dashboard.html", {
        "result": {
            "emotion": emotion,
            "category": predicted_intent,
            "priority": priority,
            "explanation": explanation,
            "sentiment": sentiment_label
        },
        "current_call": call_analysis,
        "stats": stats,
        "recent_calls": recent_calls
    })