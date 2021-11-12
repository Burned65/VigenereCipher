import collections


def encrypt(key, text):
    encrypted_text = ''
    counter = 0
    for char in text:
        encrypted_text += chr((ord(char)+key[counter]) % 128)
        counter = (counter + 1) % len(key)
    return encrypted_text


def decrypt(key, text):
    decrypted_text = ''
    counter = 0
    # subtract the specific key from the char of the string
    for char in text:
        decrypted_text += chr((ord(char)-key[counter]) % 128)
        counter = (counter + 1) % len(key)
    return decrypted_text


def check_common(text):
    # check most common letter of the text
    return collections.Counter(text).most_common(1)[0][0]


def generate_key(common_char):
    # return the key for the given text
    return (ord(common_char) - ord(' ')) % 128


def get_ggT(a, b):
    # sort out the multiples of the key
    while b != 0:
        c = a % b
        a = b
        b = c
    return a


def filter_index(list):
    tmp = []
    # filter out any index of coincidence which is smaller than 0.06
    for item in list:
        if item[0] >= 0.06:
            tmp.append(item)
    return tmp


def index_of_coincidence(text):
    index = 0
    tmp = []
    coincidence_index = []
    # check different key lengths from 1 to 100
    for i in range(1, 101):
        for j in range(1, i+1):
            # split text into different key lengths
            split_text = text[j-1::i]
            distinct_chars = ''.join(set(text))
            # calculate index of coincidence for every text and return them in an array with the key
            for char in distinct_chars:
                index += split_text.count(char)*(split_text.count(char)-1)
            index /= len(split_text)*(len(split_text)-1)
            tmp.append(index)
        index = sum(tmp)/i
        tmp = []
        coincidence_index.append((index, i))
    return coincidence_index


if __name__ == '__main__':
    # loop for all 3 texts
    for i in range(1, 4):
        with open(f"Lorem{str(i)}.txt", "r") as f:
            text = f.read()
        key_list = []
        split_text = []
        index = index_of_coincidence(text)
        index = filter_index(index)
        try:
            key = get_ggT(index[0][1], index[1][1])
        # if there is only one index of coincidence which matches the pre given criteria, just take it
        except IndexError:
            key = index[0][1]
        for i in range(1, key+1):
            # split the texts into the key lengths
            split_text.append(text[i-1::key])
            # check common char for every text
            char = check_common(split_text[i-1])
            # check key for every text and add it to the key list
            key_list.append(generate_key(char))
        print(decrypt(key_list, text))
