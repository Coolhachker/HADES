from pandas import read_csv
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


def set_dataframe_from_csv(path_to_file):
    dataframe_messages = read_csv(path_to_file, delimiter=';').map(remove_emoji).drop_duplicates(keep=False)
    return dataframe_messages.to_numpy()


if __name__ == '__main__':
    set_dataframe_from_csv('../../data/spam_messages.csv')