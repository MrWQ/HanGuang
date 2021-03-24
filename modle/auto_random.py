#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2021/3/5 15:53
# @Author   : ordar
# @File     : auto_random.py
# @Project  : autoer
# @Python   : 3.7.5
import time
import random


class AUTO_RANDOM:
    def auto_random_int(self, max_int, min_int=0):
        """
        生成一个随机整数
        :param min_int:最小数（包含）
        :param max_int:最大数（包含）
        :return:
        """
        return random.randint(min_int, max_int)

    def auto_random_str(self, has_num=True):
        """
        随机生成一个字符
        :param has_num: 是否可以有数字做字符
        :return: 字符
        """
        strs = [
            'a',
            'b',
            'c',
            'd',
            'e',
            'f',
            'g',
            'h',
            'i',
            'j',
            'k',
            'l',
            'm',
            'n',
            'o',
            'p',
            'q',
            'r',
            's',
            't',
            'u',
            'v',
            'w',
            'x',
            'y',
            'z',
            '0',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9']
        strs_no_num = [
            'a',
            'b',
            'c',
            'd',
            'e',
            'f',
            'g',
            'h',
            'i',
            'j',
            'k',
            'l',
            'm',
            'n',
            'o',
            'p',
            'q',
            'r',
            's',
            't',
            'u',
            'v',
            'w',
            'x',
            'y',
            'z']
        if has_num:
            return strs[self.auto_random_int(min_int=0, max_int=35)]
        else:
            return strs_no_num[self.auto_random_int(min_int=0, max_int=25)]

    def auto_random_word(self, min_length=3, max_length=10, first_str_no_num=False, all_str_no_num=False):
        """
        随机生成一个单词
        :param min_length: 单词最小长度
        :param max_length: 单词最大长度
        :param first_str_no_num: 第一个字符可以为数字字符
        :param all_str_no_num: 所有字符都不能含有数字字符
        :return: 单词
        """
        word = ''

        if all_str_no_num:
            # 不含数字字符
            for i in range(
                    self.auto_random_int(
                        min_int=min_length,
                        max_int=max_length)):
                word = word + self.auto_random_str(has_num=False)
        else:
            if first_str_no_num:
                # 第一个字符不能为数字
                # 先生成一个不含数字的字符做为第一个字符
                word = word + self.auto_random_str(has_num=False)
                if min_length > 1:
                    for i in range(
                            self.auto_random_int(
                                min_int=min_length - 1,
                                max_int=max_length - 1)):
                        word = word + self.auto_random_str()
                else:
                    pass
            else:
                # 第一个字符可以为数字
                for i in range(
                    self.auto_random_int(
                        min_int=min_length,
                        max_int=max_length)):
                    word = word + self.auto_random_str()
        return word

    def auto_random_sleep(self, max_int, min_int=0):
        """
        睡眠随机数的秒数的时间
        :param max_int:最小睡眠时间
        :param min_int:最大睡眠时间
        :return:
        """
        time.sleep(self.auto_random_int(max_int))

    def auto_random_void_command(self, max_str=1000, min_str=500, max_int=3, min_int=1):
        """
        返回空白指令字符串
        :param max_str: 随机单词最大长度
        :param min_str: 随机单词最小长度
        :param max_int: 随机睡眠最大时间
        :param min_int: 随机睡眠最小时间
        :return:
        """
        random_word = self.auto_random_word(
            min_length=min_str, max_length=max_str, first_str_no_num=True)
        random_int = self.auto_random_int(max_int=max_int, min_int=min_int)
        void_command = [
            'print("tag")'.replace('tag', random_word),
            'time.sleep(tag)'.replace('tag', str(random_int)),
            'tag1 = tag2 + tag3'.replace('tag1', random_word)
                .replace('tag2', str(self.auto_random_int(99999999)))
                .replace('tag3', str(self.auto_random_int(99999999))),
            'tag1 = tag2 - tag3'.replace('tag1', random_word)
                .replace('tag2', str(self.auto_random_int(99999999)))
                .replace('tag3', str(self.auto_random_int(99999999))),
            'tag1 = tag2 * tag3'.replace('tag1', random_word)
                .replace('tag2', str(self.auto_random_int(99999999)))
                .replace('tag3', str(self.auto_random_int(99999999))),
            'tag1 = tag2 / tag3'.replace('tag1', random_word)
                .replace('tag2', str(self.auto_random_int(99999999)))
                .replace('tag3', str(self.auto_random_int(99999999))),
            'tag1 = "tag2" + "tag3"'.replace('tag1', random_word)
                .replace('tag2', self.auto_random_word(
            min_length=min_str, max_length=max_str, first_str_no_num=True))
                .replace('tag3', self.auto_random_word(
            min_length=min_str, max_length=max_str, first_str_no_num=True)),
        ]
        return void_command[self.auto_random_int(min_int=0, max_int=len(void_command) - 1)]
