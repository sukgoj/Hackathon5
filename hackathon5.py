import hashlib
import random
from cryptography.fernet import Fernet

# Generate encryption key for votes
key = Fernet.generate_key()
cipher = Fernet(key)

# Voter registration with unique ID generation
def generate_voter_id():
    return str(random.randint(1000, 9999))

voters = {}
candidates = ["Alice", "Bob", "Charlie", "Diana"]

def register_voter(voter_name):
    voter_id = generate_voter_id()
    voters[voter_id] = {'name': voter_name, 'vote': None}
    print(f"Voter {voter_name} registered with ID: {voter_id}")
    return voter_id

def cast_vote(voter_id):
    if voters[voter_id]['vote'] is not None:
        print("You have already voted!")
        return

    print("Candidates:")
    for idx, candidate in enumerate(candidates, start=1):
        print(f"{idx}. {candidate}")
    
    choice = int(input("Enter the number of your choice: ")) - 1
    vote = candidates[choice]
    
    # Encrypt the vote
    encrypted_vote = cipher.encrypt(vote.encode())
    voters[voter_id]['vote'] = encrypted_vote
    print("Your vote has been cast successfully!")

def count_votes():
    results = {candidate: 0 for candidate in candidates}
    
    for voter_id, info in voters.items():
        if info['vote'] is not None:
            decrypted_vote = cipher.decrypt(info['vote']).decode()
            results[decrypted_vote] += 1
    
    print("\nElection Results:")
    for candidate, count in results.items():
        print(f"{candidate}: {count} votes")

    winner = max(results, key=results.get)
    print(f"\nThe winner is: {winner}")

# Main program execution
if __name__ == "__main__":
    print("Welcome to the Electronic Voting System!\n")

    # Register voters
    num_voters = int(input("Enter the number of voters: "))
    for _ in range(num_voters):
        voter_name = input("Enter voter's name: ")
        voter_id = register_voter(voter_name)

        # Voting process
        cast_vote(voter_id) 

    # Count and display results
    count_votes()
