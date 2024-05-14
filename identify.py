import pandas as pd
import spacy
from fuzzywuzzy import fuzz

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Load the device list from CSV into a DataFrame
device_df = pd.read_csv("data.csv")

def fuzzy_match_device(user_device, available_devices):
    # Perform fuzzy matching and return the best match
    matches = [(device, fuzz.partial_ratio(user_device, device)) for device in available_devices]
    best_match = max(matches, key=lambda x: x[1])

    # Consider a match if the ratio is above a certain threshold (adjust as needed)
    if best_match[1] > 80:
        return best_match[0]
    else:
        return None

def extract_device_and_command(text):
    # Process the user input text with spaCy
    doc = nlp(text)

    # Initialize variables for target devices and desired command
    target_devices = []
    device_ids = set()
    desired_command = None

    # Get all available device labels for fuzzy matching
    available_devices = device_df['label'].str.lower().unique()

    # Define a mapping of equivalent verbs
    equivalent_verbs = {
        "turn": "switch",
        # Add more equivalent verb pairs as needed
    }

    # Define a mapping of equivalent nouns
    equivalent_nouns = {
        "light": "bulb",
        "lights": "bulb",
        "bulbs": "bulb",
        "fridge": "refrigerator",
        "tv": "television",
        "cam": "camera",
        # Add more equivalent noun pairs as needed
    }

    # Iterate through the processed tokens
    for token in doc:
        # Check for potential target devices (nouns)
        if token.pos_ == "NOUN" and token.dep_ not in ("aux", "prep"):
            noun_lower = token.text.lower()
            print("Noun : ", noun_lower)
            # Check for equivalent nouns
            equivalent_noun = equivalent_nouns.get(noun_lower, noun_lower)
            print("Equivalent Noun : ", equivalent_noun)

            # Use fuzzy matching to find the closest device labels
            matched_devices = [device for device in available_devices if fuzzy_match_device(equivalent_noun, [device])]
            target_devices.extend(matched_devices)

            print("Devices : ", target_devices)
    # Find device IDs for the matched devices
    device_ids.update(device_df[device_df['label'].str.lower().isin(target_devices)]['device_id'].tolist())

    for token in doc:
        # Check for potential commands (verbs)
        if token.pos_ == "VERB":
            verb_lower = token.lemma_.lower()
            print("Verb : ", verb_lower)

            # Check if the verb is in the commands for the identified device
            if target_devices:
                # Check for equivalent verbs
                equivalent_verb = equivalent_verbs.get(verb_lower, verb_lower)
                print("Equivalent Verb : ", equivalent_verb)

                command_info = device_df[(device_df['label'].str.lower().isin(target_devices)) & (device_df['command_name'].str.lower() == equivalent_verb)]
                if not command_info.empty:
                    desired_command = equivalent_verb

                if desired_command == 'switch':
                    if 'on' in text:
                        desired_command = 'switch_on'
                    else:
                        desired_command = 'switch_off'

    return target_devices, device_ids, desired_command

# Example usage
# user_input = "Please switch off the lights."
# devices, device_ids, command = extract_device_and_command(user_input)

# if devices and command:
#     print(f"Devices Found: {devices}, Device_Ids: {device_ids}, Desired Command: {command}")
# elif not command and devices:
#     print("Command not found. Devices:", devices)
# elif not devices and command:
#     print("Devices not found. Command:", command)
# else:
#     print("Nothing found!")
