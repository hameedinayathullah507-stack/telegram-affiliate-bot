from google import genai

# Create client
client = genai.Client(api_key="AIzaSyAf8Ru12Yqk92qZqUtFoi4kGnxw_Pl1e4g")

# Generate response
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello"
)

print(response.text)