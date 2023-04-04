import datetime as dt
import json
import re
import string
import sys

import logging
from os import path

log_file_path = path.join(path.dirname(path.abspath("__file__")), 'log.config')
logger = logging.getLogger("mylogger")


def readfile(json_file: str) -> list:
    """
    json file reader to list
    """
    print('loading tweets')
    tweets_data = []
    with open(json_file, 'r') as read_file:
        for tweet in read_file:
            tweets_data.append(json.loads(tweet))
    # print('loading succesful')
    logger.info("Loaded data from .json file")
    return tweets_data


def separate_number_chars(s):
    """
    function to seperate number and letters
    """
    res = re.split('([-+]?\d+\.\d+)|([-+]?\d+)', s.strip())
    res_f = [r.strip() for r in res if r is not None and r.strip() != '']
    return res_f


class Twitter:
    """
    class that holds our loaded json list and the current TWEET ID
    our twitter api methods
    """

    def __init__(self, tweets_list, tw_id):
        self.tweets_list = tweets_list
        self.tw_id = tw_id

    def get_text(self) -> string:
        text = self.tweets_list[self.tw_id]['text']
        return text

    def get_created_at(self) -> string:
        created_at = self.tweets_list[self.tw_id]['created_at']
        return created_at

    def set_tweetid(self, twid):
        if 0 <= twid < len(self.tweets_list):
            self.tw_id = twid
        else:
            # print('Tweet not found (given id is too big or <0)')
            logger.error('Tweet not found (given id is too big or <0)')

    def lower_tweedid(self):
        if self.tw_id > 0:
            self.tw_id -= 1
        else:
            # print('First tweet')
            logger.info("First tweet")

    def increase_tweetid(self):
        if self.tw_id < len(self.tweets_list) - 1:
            self.tw_id += 1
            self.print_tweet()

        else:
            # print('Last tweet')
            logger.info("Last tweet")

    def set_tweetid_last(self):
        self.tw_id = len(self.tweets_list) - 1

    def print_tweet(self):
        text = self.get_text()
        created_at = self.get_created_at()
        # print("Tweet Id: {i}\t Text: {t}\t Created_at: {c}".format(i=self.tw_id, t=text, c=created_at))
        logging.info("Tweet Id: {i}\t Text: {t}\t Created_at: {c}".format(i=self.tw_id, t=text, c=created_at))

    def create_tweet(self):
        text = input("Tweet Text:")
        created_at = dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        tweet = {
            'text': text,
            'created_at': created_at
        }
        self.tweets_list.append(tweet)
        self.tw_id = len(self.tweets_list) - 1

        logger.info("New tweet created.")

    def update_tweet(self, id):
        if 0 <= id < len(self.tweets_list):
            tweet = self.tweets_list[id]
            text = input("Tweet Text:")
            created_at = dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

            tweet['text'] = text
            tweet['created_at'] = created_at
            self.tw_id = id

            logger.info("Updated tweet with ID: " + str(id))

        else:
            # print('Tweet not found (given id is too big or <0)')
            logger.error('Unable to find tweet with id: ', id)

    def delete_cur_tweet(self):
        del self.tweets_list[self.tw_id]

    def save_to_file(self, json_file: str):
        with open(json_file, "w") as file:
            for tweet in self.tweets_list:
                file.write(f"{json.dumps(tweet)}\n")

    def print_tweetid(self):
        # print("current Tweet Id: ", self.tw_id)
        logger.info("current Tweet Id: ", self.tw_id)

    def save_and_exit(self, json_file: str):
        self.save_to_file(json_file)
        logger.info("Tweets saved. Exiting the program...")
        sys.exit("Tweets saved exiting..")


def print_menu():
    print('Press: \nc.To create a new Tweet.\n' +
          'r.To read tweet.\n' +
          'u.To update tweet.\n' +
          'd.To delete tweet.\n' +
          '$.To read last tweet.\n' +
          '-.To read one tweet up from the current tweet.\n' +
          '+.To read one tweet down from the last tweet.\n' +
          '=.To print current tweet.\n' +
          'q.To quit without save.\n' +
          'w.To write file to disk.\n' +
          'x.To exit and save.')


def menu():
    """
    menu function handles every input
    """
    myfile = 'tweetdhead300000.json'
    twitter = Twitter(readfile(myfile), 0)
    print_menu()

    while True:
        val = input()
        val = separate_number_chars(val)

        try:

            if val[0] == 'c':
                twitter.create_tweet()

            elif val[0] == 'r' and len(val) > 1:
                x = int(val[1])
                twitter.set_tweetid(x)
                twitter.print_tweet()


            elif val[0] == 'u' and len(val) > 1:
                x = int(val[1])
                twitter.update_tweet(x)

            elif val[0] == 'd':
                twitter.delete_cur_tweet()

            elif val[0] == '$':
                twitter.set_tweetid_last()
                twitter.print_tweet()
                logger.info("Read last tweet.")


            elif val[0] == '-':
                twitter.lower_tweedid()
                twitter.print_tweet()

            elif val[0] == '+':
                twitter.increase_tweetid()
                twitter.print_tweet()

            elif val[0] == '=':
                twitter.print_tweetid()

            elif val[0] == 'q':
                logger.info("Quit program without save.")
                sys.exit(0)

            elif val[0] == 'w':
                twitter.save_to_file(myfile)
                print('file saved')

            elif val[0] == 'x':
                twitter.save_and_exit(myfile)

            else:
                logger.error("Invalid input.")

        except KeyboardInterrupt as err:
            pass


def main():
    menu()

if __name__ == "__main__":
    main()

