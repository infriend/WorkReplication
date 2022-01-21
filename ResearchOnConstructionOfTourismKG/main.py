"""
First, get eneities from hudong wikipedia, get info box to construct raw triples.(we have triples)
Second, ltp processes the text data for word segmentation and any other processes.
For pattern match, we maintain a vocabulary and synonym as patterns to match the potential attribute value.
For labeling, we label the candidate attribute and its part of speech.
For machine learning, we train several classifiers, vote for the final result.
For searching engine, search the entity, attribute to get the value.# html label changed, we cannot directly get values.
For word field, give words a weight, get all the field words in the sentence and calculate the weights to
choose the candidate.

We extract 地址 and 著名景点 in this paper, for it's the same attribute we need in our KG.

Test: we know the text and its corresponding city/entity, we predict the triple.
"""


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
