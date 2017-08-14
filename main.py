from bs4 import BeautifulSoup
import random, requests, os, sys

class Colors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

pink = Colors.PINK
blue = Colors.BLUE
green = Colors.GREEN
yellow = Colors.YELLOW
red = Colors.RED
end = Colors.END

# === CHANGE THESE VARIABLES ===

MAX_WORDS = 30
CHAIN_LENGTH = 2

# ==============================

class Markov:
    chain_length = CHAIN_LENGTH
    max_words = MAX_WORDS
    separator = "\x01"
    stop = "\x02"

    @classmethod
    def parse_messages(self, messages):
        chain_map = {}
        starting = []

        for message in messages:
            message = message + " " + self.stop
            message = message.split(" ")
            chains = []

            if message[0] not in starting:
                starting.append(message[0])


            for i in range(len(message) - self.chain_length):
                chains.append(message[i:i + self.chain_length + 1])

            for chain in chains:
                head = tuple(chain[:self.chain_length])
                tail = chain[self.chain_length:]

                if head in chain_map:
                    chain_map[head].append(tail[0])

                else:
                    chain_map[head] = tail

        return [starting, chain_map]

    @classmethod
    def create_message(self, chains):
        starting = random.choice(chains[0])
        chains = chains[1]

        curr = [starting]

        for i in range(self.max_words):
            previous = curr[-1]
            possible = []

            if previous == "\n":
                break

            for chain in chains:
                if chain[0] == previous:
                    possible.append(chain)

            if len(possible) == 0:
                break

            possible = random.choice(possible)
            curr.append(possible[1])
            curr.append(random.choice(chains[possible]))

        return " ".join(curr).strip("\x02")

    @classmethod
    def create_paragraph(self, chains, length = 5):
        text = ""

        for i in range(length):
            text += self.create_message(chains)
            text += "\n"

        return text


    @classmethod
    def parse_file(self, name):
        result = ""

        with open(name, "r") as f:
            result = f.read()

        return self.parse_messages(result.split("\n"))

    @classmethod
    def message_from_file(self, name):
        return self.create_message(self.parse_file(name))


    @classmethod
    def paragraph_from_file(self, name, length = 5):
        return self.create_paragraph(self.parse_file(name), length)

print(blue + "Please enter whether you'd like to use the (o)ld subreddit data or create a (n)ew one, followed by the amount to generate (defualt 5): " + end, end = "")
full = input(pink).lower()
choice = full.split(" ")[0]
amount = 0

try:
    amount = int(full.split(" ")[1])

except IndexError:
    amount = 5

else:
    True

if choice == "o":
    print(end, end = "")

elif choice == "":
    print(end, end = "")

elif choice == "n":
    print(end + blue + "Please enter your subreddit: " + end + pink, end = "")

    subreddit = input()
    print(end)

    i = 0
    output = ""
    curr = "https://www.reddit.com/r/" + subreddit + "/top/"

    while True:
        if i > 50:
            break

        headers = {
            'User-Agent': 'Normal Human',
            'From': 'bloopetybleep12@domain4.com'
        }

        r  = requests.get(curr, headers = headers)
        data = r.text
        soup = BeautifulSoup(data, "lxml")

        for link in soup.find_all("p", {"class": "title"}):
            output += link.find_all("a")[0].string + "\n"

        try:
            curr = soup.find_all("a", {"rel": "next"})[0].get("href")

        except IndexError:
            break

        else:
            i += 1

    with open("titles.txt", "w") as f:
        f.write(output)

else:
    print(red + "That's not a choice." + end)
    sys.exit()

j = 0
while j < amount:
    chains = ""

    with open("titles.txt", "r") as f:
        chains = Markov.parse_messages(f.read().split("\n"))

    print(green + Markov.create_message(chains).split("\n")[0] + end)
    j += 1
