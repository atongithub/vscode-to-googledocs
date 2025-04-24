import sys
import re
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os.path

SCOPES = ["https://www.googleapis.com/auth/documents"]
SERVICE_ACCOUNT_FILE = "credentials.json" # Insert the json file you downloaded from google cloud


def get_document_id(document_link):
    match = re.search(r"/document/d/([a-zA-Z0-9_-]+)", document_link)
    if match:
        return match.group(1)
    else:
        print("Invalid Google Document Link")
        sys.exit(1)

def get_googledoc_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("docs", "v1", credentials=creds)


def compile_java_files(java_folder):
    results = {}

    for file in os.listdir(java_folder):
        if file.endswith(".java"):
            java_file = os.path.join(java_folder, file)
            results[file] = (open(java_file,errors="ignore").read())
                
    return results

def get_document_end_index(service, document_id):
    doc = service.documents().get(documentId=document_id).execute()
    return doc["body"]["content"][-1]["endIndex"]


def writing_in_the_document(service, document_id, text):
    end_index = get_document_end_index(service, document_id)
    # https://developers.google.com/workspace/docs/api/how-tos/move-text#insert-text
    requests = [
        # Insert text at the end of the document
        {
            "insertText": {
                "location": {"index": end_index - 1},
                "text": text + "\n\n",
            }
        },
        {
            "updateTextStyle": {
                "range": {"startIndex": end_index, "endIndex": end_index + len(text) + 2},
                "textStyle": {"weightedFontFamily": {"fontFamily": "Courier New"}},
                "fields": "weightedFontFamily",
            }
        },
        {
            "updateParagraphStyle": {
                "range": {"startIndex": end_index, "endIndex": end_index + len(text) + 2},
                "paragraphStyle": {
                    "shading": {
                        "backgroundColor": {
                            "color": {"rgbColor": {"red": 0.9, "green": 0.9, "blue": 0.9}}
                        }
                    }
                },
                "fields": "shading",
            }
        },
    ]

    service.documents().batchUpdate(
        documentId=document_id, body={"requests": requests}
    ).execute()


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <google-doc-link> <java-code-folder>\n"
        "Give the bot access to the document: codesubmissionbot@stoked-courier-000000-n2.iam.gserviceaccount.com")
        sys.exit(1)

    document_link = sys.argv[1]
    java_folder = sys.argv[2]
 
    document_id = get_document_id(document_link)
    service = get_googledoc_service()

    java_files = compile_java_files(java_folder)

    for file,(code) in java_files.items():
        writing_in_the_document(service, document_id, f"{file}")
        writing_in_the_document(service, document_id, code)

    print("Java code successfully added to Google Doc!")

if __name__ == "__main__":
    main()
