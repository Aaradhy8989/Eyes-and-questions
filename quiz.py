import numpy as np
import cv2
import random
import pandas as pd

class Quiz:
    """
    Class for quiz data
    Attributes:
        questions: a dictionary contains all questions (id: string)
        answers: a dictionary contains all the user answers (id: list of answers)
        scores: a dictionary contains the acrual answers
    """
    def __init__(self):
        df = pd.read_csv('que.csv')
        self.questions = {}
        self.answers = {id_q: list() for id_q in range(0,len(df['Questions'])) }
        self.scores = {}
        self.load_questions()


    def load_questions(self):
        df = pd.read_csv('que.csv')
        self.questions = {}
        self.scores = {}
        for i in range (0, len(df['Questions'])):
            self.questions[i] = df.iloc[i,0]
            self.scores[i] = df.iloc[i,1]


    def add_answer(self, id_q, answer):
        self.answers[id_q] = self.answers.get(id_q, list())
        self.answers[id_q].append(answer)

    def get_answer(self, id_q):
        answers = self.answers.get(id_q, list())
        num_yes = answers.count('yes') 
        num_no = answers.count('no') 

        if num_yes >= num_no:
            return 'yes'
        elif num_yes < num_no:
            return 'no'


    def compute_result(self):
        score = 0
        for id_q in self.answers.keys():
            if self.get_answer(id_q) == self.scores[id_q]:
            # print(id_q)
                score+=1
        
        return score




