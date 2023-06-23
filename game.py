from hangmanlib import *
import random
import os
from datetime import datetime
import csv


class Player:
    def __init__(self) -> None:
        # 输入的历史记录
        self.guess_characters_history = []
        # 本轮的合法输入
        self.guess_characters = []

    # 非法字符忽略
    # 大小写相同
    # 如果重复输入某个单词中存在的字符则忽略
    # 如果重复输入某个单词中不存在的字符则次数加一
    def guess(self):
        player_input = input()
        characters = []
        for c in player_input:
            if c.isalpha():
                characters.append(c)
                self.guess_characters_history.append(c)
        self.guess_characters = characters
        return characters

    def show_guess_characters(self):
        str = ''
        for c in self.guess_characters:
            str += c
        print(str)
    
    def get_guess_characters(self):
        return self.guess_characters
    
    def get_guess_characters_history(self):
        return self.guess_characters_history


class Computer:
    def __init__(self) -> None:
        self.words = self.read_words()
        self.word = self.get_guess_word()
        self.right_characters = []
        self.mistakes = 0
        # RUNNING SUCCESS FAIL
        self.status = "RUNNING"

    def read_words(self):
        with open("words.txt", "r") as f:
            content = f.read()
            words = content.split()
            return words

    def get_guess_word(self):
        return random.choice(self.words)

    def handle_player_input(self, characters):
        for c in characters:
            # 将大写字母转变为小写字母
            c = c.lower()
            if c in self.word and c not in self.right_characters:
                self.right_characters.append(c)
            elif c not in self.word:
                self.mistakes += 1

            self.judge_result()
            if self.status != "RUNNING":
                return self.status
        return self.status

    def if_success(self):
        for c in self.word:
            if c not in self.right_characters:
                return False
        return True

    def if_fail(self):
        if self.mistakes >= 6:
            return True
        return False

    # 根据游戏情况更新status
    def judge_result(self):
        if self.if_success():
            self.status = "SUCCESS"
        elif self.if_fail():
            self.status = "FAIL"

    def get_mask_word(self):
        mask_word = ''
        for c in self.word:
            if c in self.right_characters:
                mask_word += c
            else:
                mask_word += '_'
            mask_word += ' '
        return mask_word
    
    def get_word(self):
        return self.word
    
    def get_mistakes(self):
        return self.mistakes
    
    def get_status(self):
        return self.status


class Log:
    def __init__(self) -> None:
        self.f = open('guess.csv', "a", newline='')
        
    def log_start(self):
        self.start_time = datetime.now()

    def __del__(self):
        self.f.close()

    def log_end(self, word, word_list, status):
        end_time = datetime.now()
        duration = end_time - self.start_time

        writer = csv.writer(self.f, delimiter=',')
        writer.writerow([self.start_time.strftime('%Y-%m-%d %H:%M:%S'), word, ''.join(word_list), str(duration.total_seconds()) + 's', status])




class Game:
    def __init__(self) -> None:
        self.player = Player()
        self.computer = Computer()
        self.log = Log()
        self.status = "RUNNING"
        self.play()

    def show_two_part(self, left_str, right_str_list):
        total_space = 40
        mid = len(right_str_list) // 2
        for i in range(len(right_str_list)):
            if i == mid:
                space_num = total_space - len(left_str)
                left = space_num // 2
                right = space_num - left
                print(left * ' ' + left_str + right * ' ' + right_str_list[i])
            else:
                print(total_space * ' ' + right_str_list[i])

    def show_interface(self):
        # 用户输入
        self.player.show_guess_characters()

        # mistakes
        print('mistakes:' + str(self.computer.get_mistakes()))

        # 中间部分
        gallow = get_hangman(self.computer.get_mistakes())
        if self.status == 'RUNNING':
            left = self.computer.get_mask_word()
        elif self.status == 'SUCCESS':
            left = 'YOU WIN!'
        elif self.status == 'FAIL':
            left = 'YOU LOSE!'

        self.show_two_part(left, gallow)

    def show_result(self):
        pass

    # 获取用户输入c为继续 q为退出
    def continue_or_quit(self):
        while True:
            player_input = input("Continue game(C[c]Qq)?")
            chioce = player_input[0]
            if chioce == 'C' or chioce == 'c':
                return True
            if chioce == 'Q' or chioce == 'q':
                return False
            print('Wrong input!')

    def new_game(self):
        self.player = Player()
        self.computer = Computer()
        self.status = "RUNNING"

    def clear_interface(self):
        if os.name == 'nt':  # Windows 操作系统
            os.system('cls')
        else:  # Linux 或 macOS 操作系统
            os.system('clear')

    def play(self):
        while True:
            self.log.log_start()
            self.clear_interface()
            self.show_interface()
            while self.status == "RUNNING":
                characters = self.player.guess()
                self.status = self.computer.handle_player_input(characters)
                self.clear_interface()
                self.show_interface()
                print(self.computer.get_word())

            self.log.log_end(self.computer.get_word(), self.player.get_guess_characters_history(), self.status)

            if self.continue_or_quit():
                self.new_game()
            else:
                break

Game()
