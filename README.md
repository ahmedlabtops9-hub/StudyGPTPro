# StudyGPT Pro

Arabic-first study assistant built with Streamlit and Gemini.

## Features
- AI tutor for school subjects
- Practice exam generator and scoring
- Flashcard generation
- Learning activity and exam analytics
- Google sign-in (requires OAuth setup)
- Cloud progress persistence (requires Supabase setup)

## Streamlit secrets

In Streamlit Cloud, open **App settings → Secrets** and configure:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "your_supabase_service_role_key"

[auth]
redirect_uri = "https://YOUR-APP.streamlit.app/oauth2callback"
cookie_secret = "generate-a-long-random-secret"
client_id = "YOUR_GOOGLE_OAUTH_CLIENT_ID"
client_secret = "YOUR_GOOGLE_OAUTH_CLIENT_SECRET"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

Do not commit real keys or secrets to GitHub.

## Google OAuth setup
1. In Google Cloud Console, create an OAuth 2.0 Client ID of type **Web application**.
2. Add the Streamlit callback URL shown above to **Authorized redirect URIs**.
3. Add your deployed Streamlit URL to **Authorized JavaScript origins** if requested by Google.
4. Put the client ID and client secret in Streamlit Secrets under the `[auth]` section.
5. Add your test Google account to the OAuth consent screen's test users while the app is in testing mode.

## Supabase setup
1. Create a Supabase project.
2. Open the SQL Editor and run the contents of `supabase_schema.sql`.
3. Copy the project URL and service role key into Streamlit Secrets.
4. Keep the service role key private. It must only be stored in Streamlit Secrets.

The app restores and saves a signed-in user's chat, exams, flashcards, and activity using the email returned by Google OAuth.

## Deployment
The Streamlit app deploys from `app.py`. After pushing changes, wait for Streamlit Cloud to finish restarting, then reload the app.
