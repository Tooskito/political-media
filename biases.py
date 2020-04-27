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
    "ap":                                   "center",
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

# Create dictionary to convert from labels i.e. 'right' to a number i.e. '1'.
label_to_compass = {
    "left": -1,
    "lean left": -0.5,
    "center": 0,
    "lean right": 0.5,
    "right": 1
}

# Query user to customize weights.
if query_user("Would you like to personally configure label -> compass? (y/n) "):
    label_to_compass["left"] = float( input("Enter a weight for 'left': ") )
    label_to_compass["lean left"] = float( input("Enter a weight for 'lean left': ") )
    label_to_compass["center"] = float( input("Enter a weight for 'center': ") )
    label_to_compass["lean right"] = float( input("Enter a weight for 'lean right': ") )
    label_to_compass["right"] = float( input("Enter a weight for 'right': ") )
else:
    print('Using default values.')

# Apply dictionary comprehension to translate biases_raw with label_to_compass.
biases_filtered = { key:label_to_compass[value] for (key, value) in biases_raw.items() }
print("Newspaper -> left-right compass weights are as follows.")
print(biases_filtered)