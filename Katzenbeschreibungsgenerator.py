import os
from flask import Flask, request, render_template_string
import openai  # Korrektes Importieren der OpenAI-Bibliothek

app = Flask(__name__)

# Setze deinen OpenAI API-Schlüssel
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Überprüfe, ob der API-Schlüssel gesetzt ist
if not openai.api_key:
    raise ValueError("Bitte setze den OpenAI API-Schlüssel in der Umgebungsvariable 'OPENAI_API_KEY'.")

@app.route('/', methods=['GET', 'POST'])
def home():
    output_text = ''
    output_text_en = ''
    output_text_gr = ''
    input_text = ''
    error_message = ''

    if request.method == 'POST':
        input_text = request.form['input_text']

        prompt = f"""
Du bist ein KI-Assistent, der hilft, Katzen für die Adoption zu präsentieren. Basierend auf den folgenden Informationen über eine oder mehrere Katzen erstellst du eine ausführliche und ansprechende Katzenbeschreibung in Deutsch im folgenden Stil:

🐈 Name: Malkisho (m, ...)

🎂 Alter: ...

📌 Standort: Zypern, bereit innerhalb der EU + CH zu reisen

🏡 Haltung: Wohnungshaltung mit gesichertem Balkon/Garten empfohlen

Hallo, ich bin Malkisho! Meine Geschichte begann nicht gerade glücklich – mit nur sechs Wochen fand man mich ganz allein in einem Gebüsch. Zum Glück wurde ich gerettet und liebevoll aufgepäppelt. Jetzt bin ich ein aufgeweckter junger Kater, bereit für mein neues Leben!

Meine süßen Kulleraugen erkunden neugierig die Welt. Mein goldorangenes Fell ist unglaublich weich, wie Seide! Meine bernsteinfarbenen Augen sind einfach zum Dahinschmelzen. Ich bin sanft und unglaublich süß. Gegenüber neuen Katzen bin ich sehr scheu, Menschen gegenüber öffne ich mich jedoch schnell.

Ich wünsche mir so sehr, geliebt und umsorgt zu werden. Mit meiner sehr verspielten Art werde ich deinen Alltag bereichern und mit Leben füllen. Ich freue mich darauf, Teil deiner Familie zu werden und dir mit meiner Zuneigung und meinem verspielten Wesen viel Freude zu bereiten.

Möchtest du mich kennenlernen? Ich würde mich sehr über eine Nachricht (PN) an die Heroes for Cyprus Cats freuen! Wenn du mir helfen möchtest, kannst du gerne mein Album teilen, liken oder kommentieren. So bekomme ich mehr Aufmerksamkeit und finde vielleicht schneller meine liebevolle Familie. Ich danke dir schon jetzt dafür!

Bitte nutze nicht das Wort "Zuhause" und halte dich an den oben genannten Aufbau und Stil.

**Wichtige Hinweise**:
- Wenn keine Informationen zum Alter vorliegen, schreibe "XXX" anstelle des Alters.
- Wenn keine Informationen zur Kastration vorliegen, lass diese Information komplett weg.
- Füge keine erfundenen Informationen hinzu.
- Bei den Charaktereigenschaften halte dich genau an die gegebenen Informationen.

Hier sind die Informationen über die Katze(n):

{input_text}

**Hinweis:** Wenn der eingegebene Text in einer anderen Sprache als Deutsch ist, übersetze ihn ins Deutsche, bevor du die Katzenbeschreibung erstellst.
"""

        try:
            # Erstelle die deutsche Beschreibung
            response_de = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7,
            )
            output_text = response_de.choices[0].message.content.strip()

            # Erstelle die englische Übersetzung
            translation_prompt_en = f"""
Übersetze den folgenden Text ins Englische und behalte den gleichen Stil und die Formatierung bei:

{output_text}
"""

            response_en = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": translation_prompt_en}],
                max_tokens=1000,
                temperature=0.7,
            )
            output_text_en = response_en.choices[0].message.content.strip()

            # Erstelle die griechische Übersetzung
            translation_prompt_gr = f"""
Übersetze den folgenden Text ins Griechische und behalte den gleichen Stil und die Formatierung bei:

{output_text}
"""

            response_gr = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": translation_prompt_gr}],
                max_tokens=1500,
                temperature=0.7,
            )
            output_text_gr = response_gr.choices[0].message.content.strip()

        except Exception as e:
            error_message = f"Es ist ein Fehler aufgetreten: {e}"

    else:
        input_text = ''

    # HTML-Code mit den Anpassungen
    html_code = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Heroes of Cyprus Cats - Beschreibung für das Album</title>
        <style>
            body {{
                background-color: #F8E6FF; /* Heller Lavendel-Ton */
                font-family: Calibri, sans-serif;
                color: #4A0E4E; /* Dunkles Violett für Text */
                padding: 20px;
            }}
            h1 {{
                color: #8E4585; /* Dunkles Pink für Überschriften */
                font-size: 36px; /* Schriftgröße vergrößert */
            }}
            textarea {{
                width: 100%;
                padding: 10px;
                border: 1px solid #D8A1D5; /* Helles Pink für Ränder */
                border-radius: 5px;
                font-size: 16px;
                color: #4A0E4E; /* Dunkles Violett für Text */
                background-color: #FFFFFF;
            }}
            .copy-button {{
                margin-top: 5px;
                padding: 5px 10px;
                font-size: 14px;
                background-color: #FFFFFF;
                color: #4A0E4E; /* Dunkles Violett für Button-Text */
                border: 2px solid #8E4585; /* Dunkles Pink für Button-Ränder */
                border-radius: 5px;
                cursor: pointer;
            }}
            .copy-button:hover {{
                background-color: #D8A1D5; /* Helles Pink für Button-Hover */
                color: #FFFFFF;
            }}
            input[type="submit"] {{
                background-color: #FFFFFF;
                color: #4A0E4E; /* Dunkles Violett für Button-Text */
                padding: 10px 20px;
                border: 2px solid #8E4585; /* Dunkles Pink für Button-Ränder */
                border-radius: 10px;
                font-size: 16px;
                cursor: pointer;
            }}
            input[type="submit"]:hover {{
                background-color: #D8A1D5; /* Helles Pink für Button-Hover */
                color: #FFFFFF;
            }}
            .output-container {{
                margin-top: 20px;
            }}
            .separator {{
                margin: 40px 0;
                text-align: center;
                font-size: 24px;
                color: #8E4585; /* Dunkles Pink für Überschriften */
            }}
            .processing {{
                margin-top: 20px;
                font-size: 18px;
                color: #ff0000;
            }}
            .success-message {{
                margin-top: 20px;
                font-size: 18px;
                color: #008000;
                font-weight: bold;
            }}
            .error-message {{
                margin-top: 20px;
                font-size: 18px;
                color: #ff0000;
                font-weight: bold;
            }}
            .highlight-note {{
                background-color: #FF69B4; /* Helles Pink für Hervorhebungen */
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                color: #4A0E4E; /* Dunkles Violett für Text */
            }}
            .contact {{
                margin-top: 40px;
                font-size: 14px;
                color: #4A0E4E; /* Dunkles Violett für Text */
            }}
            .contact a {{
                color: #8E4585; /* Dunkles Pink für Links */
            }}
            /* Bestätigungsmeldung */
            .confirmation-message {{
                display: none;
                margin-top: 20px;
                font-size: 18px;
                color: #008000;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>Heroes of Cyprus Cats - Beschreibung für das Album</h1>
        <form method="post" id="cat-form">
            <p>
                Gib hier den Text über die Katze(n) ein (in beliebiger Sprache):<br><br>
                Enter the text about the cat(s) here (in any language):<br><br>
                Εισαγάγετε το κείμενο για τη(τις) γάτα(ες) εδώ (σε οποιαδήποτε γλώσσα):
            </p>
            <p class="highlight-note">
                Eine Anfrage dauert bis zu 1 Minute. Bitte Geduld!<br>
                A request can take up to 1 minute. Please be patient!<br>
                Ένα αίτημα μπορεί να διαρκέσει έως 1 λεπτό. Παρακαλώ υπομονή!
            </p>
            <textarea name="input_text" rows="10" placeholder="...">{input_text}</textarea><br><br>
            <input type="submit" value="Beschreibung generieren (generate description)">
        </form>
        <div class="confirmation-message" id="confirmation">
            <p>⏳ Danke! Bitte warten!<br>
            ⏳ Thank you! Please wait!<br>
            ⏳ Ευχαριστώ! Παρακαλώ περιμένετε!</p>
        </div>
    '''

    if request.method == 'POST':
        if error_message:
            html_code += f'''
            <div class="error-message">
                <p>{error_message}</p>
            </div>
            '''
        elif output_text:
            html_code += '''
            <div class="success-message">
                <p>Juhuu! Das hat geklappt!<br>
                    Yay! It worked!<br>
                    Ουάου! Τα κατάφερε!</p>
            </div>
            '''
            html_code += f'''
            <div class="output-container">
                <h2>Textvorschlag für die süßen Katzen (Deutsch):</h2>
                <textarea id="output_de" rows="15">{output_text}</textarea><br>
                <button class="copy-button" onclick="copyToClipboard('output_de')">Kopieren</button>
                <div class="separator">🐾🐾🐾</div>
                <h2>Description for the sweet cats (English):</h2>
                <textarea id="output_en" rows="15">{output_text_en}</textarea><br>
                <button class="copy-button" onclick="copyToClipboard('output_en')">Copy</button>
                <div class="separator">🐾🐾🐾</div>
                <h2>Περιγραφή για τις γλυκές γάτες (Ελληνικά):</h2>
                <textarea id="output_gr" rows="15">{output_text_gr}</textarea><br>
                <button class="copy-button" onclick="copyToClipboard('output_gr')">Αντιγραφή</button>
            </div>
            '''
    html_code += '''
        <div class="contact">
            <p>Es gibt Probleme? Bitte schreibe an <a href="mailto:mariechristinereiter@googlemail.com">mariechristinereiter@googlemail.com</a> eine E-Mail.<br>
            Having issues? Please send an email to <a href="mailto:mariechristinereiter@googlemail.com">mariechristinereiter@googlemail.com</a>.<br>
            Έχετε προβλήματα; Παρακαλούμε στείλτε ένα email στο <a href="mailto:mariechristinereiter@googlemail.com">mariechristinereiter@googlemail.com</a>.</p>
        </div>
        <!-- JavaScript-Code -->
        {% raw %}
        <script>
            // Funktion zum Kopieren der Texte
            function copyToClipboard(elementId) {
                var copyText = document.getElementById(elementId);
                copyText.select();
                copyText.setSelectionRange(0, 99999); /* Für mobile Geräte */
                document.execCommand("copy");
                alert("Text kopiert!");
            }

            // Bestätigungsmeldung anzeigen beim Absenden des Formulars
            document.getElementById('cat-form').addEventListener('submit', function() {
                var confirmation = document.getElementById('confirmation');
                confirmation.style.display = 'block';
            });
        </script>
        {% endraw %}
    </body>
    </html>
    '''

    return render_template_string(html_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500)
