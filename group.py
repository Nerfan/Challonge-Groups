#!/usr/bin/python3
"""
Given a challonge tournament ID, pulls down the list of participants and seeds
according to a saved elo list.

Participants who do not have any elo records will be seeded at the bottom.
"""

import challonge
import sys

try:
    import set_credentials
    # This is a file I made with two lines:
    # import challonge
    # challonge.set_credentials("USERNAME", "API_KEY")
    # USERNAME and API_KEY were replaced with my info, quotes included
    # The only reason I made the file is so that I don't accidentally upload my
    # challonge API key

    # Alternatively, uncomment the folliwing line and add your information:
    # challonge.set_credentials("USERNAME", "API_KEY")
except ImportError:
    print("File set_credentials.py was not found. Prompting for credentials.")
    print("Information provided will be written out to set_credentials.py.")
    username = input("Username: ")
    apikey = input("API Key: ")
    challonge.set_credentials(username, apikey)
    with open("set_credentials.py", "w") as f:
        f.write("import challonge\n")
        f.write("challonge.set_credentials(\"")
        f.write(username)
        f.write("\", \"")
        f.write(apikey)
        f.write("\")")


USAGE = "Usage: python3 group.py <tournament id> <number of groups>"


def group(tourney_id, num_groups):
    print("Fetching tournament information...")
    tournament = challonge.tournaments.show(tourney_id)
    participants = challonge.participants.index(tournament["id"])
    participants = sorted(participants, key=lambda x: x["seed"])
    total = len(participants)
    pergroup = ((total - 1)//num_groups) + 1
    currgroup = 1
    i = 0
    seed = 1
    for j in participants:
        participant = participants[i]
        print(participant["name"] + " is seeded " + str(seed))
        challonge.participants.update(tourney_id, participant["id"],
                name=participant["name"], seed=seed)
        i = (i + num_groups)
        if i >= total:
            i = currgroup
            currgroup += 1
        seed += 1


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) is not 3:
        print(USAGE)
    else:
        group(argv[1], int(argv[2]))

