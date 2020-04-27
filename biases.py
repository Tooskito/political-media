from util import query_user

''' DEFINE NEWSPAPER BIASES '''
# Taken from: 
# https://www.allsides.com/sites/default/files/AllSidesMediaBiasChart_Version1.1_11.18.19.jpg
biases_raw = {
    "alternet":                             "left",
    "democracy now!":                       "left",
    "the daily best":                       "left",
    "the huffington post":                  "left",
    "the intercept":                        "left",
    "jacobin":                              "left",
    "mother jones":                         "left",
    "msnbc":                                "left",
    "the new yorker":                       "left",
    "the nation":                           "left",
    "slate":                                "left",
    "vox":                                  "left",
    "abc":                                  "lean left", 
    "the atlantic":                         "lean left",
    "buzzfeed news":                        "lean left",
    "cbs":                                  "lean left",
    "cnn":                                  "lean left",
    "the economist":                        "lean left",
    "the guardian":                         "lean left",
    "nbc":                                  "lean left",
    "new york times":                       "lean left",
    "npr opinion":                          "lean left",
    "politico":                             "lean left",
    "time":                                 "lean left",
    "the washington post":                  "lean left",
    "associated press":                     "center",
    "bbc":                                  "center",
    "bloomberg":                            "center",
    "christian science monitor":            "center",
    "npr":                                  "center",
    "reuters":                              "center",
    "the hill":                             "center",
    "usa today":                            "center",
    "wall street journal":                  "center",
    "fox news":                             "lean right",
    "reason free minds free markets":       "lean right",
    "washington examiner":                  "lean right",
    "washington times":                     "lean right",
    "the american spectator":               "right",
    "breitbart":                            "right",
    "the blaze":                            "right",
    "cbn":                                  "right",
    "the daily caller":                     "right",
    "daily mail":                           "right",
    "the daily wire":                       "right",
    "the federalist":                       "right",
    "national review":                      "right",
    "new york post":                        "right",
    "newsmax":                              "right"
}

print('Media source -> Right-Left Label.')
print(biases_raw)
print()

# Create dictionary to convert from labels i.e. 'right' to a number i.e. '1'.
label_to_compass = {
    "left": -1,
    "lean left": -0.5,
    "center": 0,
    "lean right": 0.5,
    "right": 1
}

# Query user to customize weights.
if query_user("Would you like to configure how compass labels i.e. 'right', 'left' are weighted? (y/n) "):
    label_to_compass["left"] = float( input("Enter a weight for 'left': ") )
    label_to_compass["lean left"] = float( input("Enter a weight for 'lean left': ") )
    label_to_compass["center"] = float( input("Enter a weight for 'center': ") )
    label_to_compass["lean right"] = float( input("Enter a weight for 'lean right': ") )
    label_to_compass["right"] = float( input("Enter a weight for 'right': ") )
else:
    print('Using default values.')
    print()

# Apply dictionary comprehension to translate biases_raw with label_to_compass.
biases_filtered = { key:label_to_compass[value] for (key, value) in biases_raw.items() }
print("Media source -> left-right compass weights are as follows.")
print(biases_filtered)
print()

# Ask user if they would like to change/add new media sources.
print("Would you like to personally configure a given media source's compass weight? ")
answer = query_user("(You cannot add a new source, data takes hours to scrape from Google.) (y/n) ")
while answer:
    media_name = input("Enter in a media source's name: ")
    media_value = float(input(f'Enter in {media_name}\'s compass (right is pos, left is neg): '))
    if media_name not in biases_raw.keys():
        print(f'\'{media_name}\' is not in the list of keys.')
        answer = query_user("Would you like to personally configure another source? (y/n) ")
        continue
    biases_filtered[media_name] = media_value
    biases_raw[media_name] = f'user: {media_value}'
    answer = query_user("Would you like to personally configure another source? (y/n) ")
print("Newspaper -> left-right compass weights are as follows.")
print(biases_filtered)