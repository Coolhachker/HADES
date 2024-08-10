import numpy
from pandas import read_csv, concat, merge
from tensorflow import constant
import re


def remove_emoji(text: str):
    try:
        regrex_pattern = re.compile(pattern="["
                                            u"\U00000000-\U00000009"
                                            u"\U0000000B-\U0000001F"
                                            u"\U00000080-\U00000400"
                                            u"\U00000402-\U0000040F"
                                            u"\U00000450-\U00000450"
                                            u"\U00000452-\U0010FFFF"
                                            "]+", flags=re.UNICODE)
        return regrex_pattern.sub(r'', text)
    except Exception:
        pass


def set_dataframe_from_csv(path_to_file, path_to_file_ham):
    dataframe_messages = read_csv(path_to_file, delimiter=';').map(remove_emoji).drop_duplicates(keep=False)
    dataframe_messages_ham = read_csv(path_to_file_ham, delimiter=';').map(remove_emoji).drop_duplicates(keep=False)
    dataframe_messages = concat([dataframe_messages, dataframe_messages_ham])
    del dataframe_messages['Unnamed: 1']
    dataframe_messages.update(dataframe_messages_ham)

    dataframe_spam_messages_in_numpy = [(obj[0], 1) for obj in dataframe_messages.to_numpy() if str(obj[0]) != 'nan']
    dataframe_ham_messages_in_numpy = [(obj[1], 0) for obj in dataframe_messages.to_numpy() if str(obj[1]) != 'nan'][:1500]
    dataframe_messages = numpy.concatenate((dataframe_spam_messages_in_numpy, dataframe_ham_messages_in_numpy))
    return dataframe_messages