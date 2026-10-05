from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import base64
import wave

app = FastAPI()


@app.get("/")
def home():
    return {"status": "Voxora voice server running"}


def load_audio():
    with open("greeting.pcm", "rb") as f:
        audio = f.read()

    print("🎵 Greeting PCM:")
    print("Audio bytes:", len(audio))

    return audio


@app.websocket("/media")
async def media(websocket: WebSocket):
    await websocket.accept()

    print("✅ Exotel WebSocket connected")

    stream_sid = None
    greeting_sent = False

    try:
        while True:
            message = await websocket.receive_text()

            data = json.loads(message)
            event = data.get("event")

            print(f"📞 Event: {event}")

            if event == "connected":
                print("🔗 Exotel connection established")

            elif event == "start":

                stream_sid = data["start"]["stream_sid"]

                print("▶️ Stream started")
                print("Stream SID:", stream_sid)
                print("Caller:", data["start"].get("from"))
                print("Called:", data["start"].get("to"))
                print("Audio format:", data["start"].get("media_format"))

                # Send greeting only once
                if not greeting_sent:

                    audio = load_audio()

                    # Send audio in chunks
                    chunk_size = 3200

                    for i in range(0, len(audio), chunk_size):

                        chunk = audio[i:i + chunk_size]

                        payload = base64.b64encode(chunk).decode("utf-8")

                        await websocket.send_text(json.dumps({
                            "event": "media",
                            "stream_sid": stream_sid,
                            "media": {
                                "payload": payload
                            }
                        }))

                    greeting_sent = True

                    print("🔊 Greeting sent to caller")

            elif event == "media":

                payload = data["media"]["payload"]

                audio_bytes = base64.b64decode(payload)

                # DO NOT echo audio anymore

            elif event == "dtmf":

                print("🔢 DTMF:", data["dtmf"])

            elif event == "mark":

                print("🏁 Mark:", data["mark"])

            elif event == "stop":

                print("🛑 Call ended")
                break

    except WebSocketDisconnect:

        print("❌ WebSocket disconnected")

    except Exception as e:

        print("❌ Error:", e)

    finally:

        print("🔚 WebSocket session closed")