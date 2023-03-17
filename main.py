import requests
import json
import os
import dotenv

from rich.console import Console
from rich.markdown import Markdown



# Set your OpenAI API key
OPENAI_API_KEY = dotenv.get_key(".env", "OPENAI_API_KEY")
# Set the API endpoint
url = "https://api.openai.com/v1/chat/completions"
# Set the request headers
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}



class Conversation :
    data = {}

    def __init__(self):
        self.load(filename="default.json")
        res = self.get_response()
        self.append(res["role"], res["content"])


    def append(self, role, content):
        self.data["messages"].append({ "role": role, "content": content})
    
    def get_response(self):
        response = requests.post(url, headers=headers, data=json.dumps(self.data))
        return response.json()["choices"][0]["message"]
    
    def add_files(self, files):
        for file in files :
            # check if file exists
            if not os.path.isfile(file):
                raise "File not found: " + file
            # read file
            with open(file, "r") as fp:
                content = fp.read()
            # add file content to conversation
            self.append("system", f"{os.path.basename(file)} ==>\n {content}")
    

    def store(self, filename="conversation.json"):
        with open(filename, "w") as fp:
            json.dump(self.data, fp, indent=4)
    
    def load(self, filename="conversation.json"):
        with open(filename) as fp:
            self.data = json.load(fp)


if __name__ == "__main__":
    conv = Conversation()
    os.remove("log.txt")


    while 1 :
        message = input("ChatPKD# ")
        if message.startswith("!"):
            if message == "!store":
                conv.store()
            elif message == "!load":
                conv.load()
            elif message.startswith("!add_files"):
                files = message.split(" ")[1:]
                conv.add_files(files)
            elif message.startswith("!add_url"):
                url = message.split(" ")[1]
                conv.add_url(url)
            elif message.startswith("!add_cmd"):
                cmd = message.split(" ")[1]
                conv.add_cmd(cmd)
            else :
                print("Invalid command")
            continue
        conv.append("user", message)
        response = conv.get_response()
        #find lines that start with a $
        lines = response["content"].split("\n")
        for line in lines:
            if line.startswith("$"):
                # execute cmd and get output
                cmd = line[1:]
                output = os.popen(cmd).read()
                # replace the line with the output
                response["content"] = response["content"].replace(line, line + " -> " + output)
                conv.append(response["role"], response["content"])
        console = Console(record=True)  # Enable recording to capture the output
        markdown = Markdown(f"{response['role']} : {response['content']}")
        console.print(markdown)

        conv.store()
        if message == "exit":
            break



    
