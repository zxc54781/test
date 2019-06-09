#!/usr/bin/env python
# coding: utf-8

# In[1]:
import numpy as np
import Basic_Operation 
 
class prouning:
    def __init__(self, Nx, max_eva, man_value, king_value, CHECKERS):
        self.Nx = Nx
        self.max_eva = max_eva
        self.man_value = man_value
        self.king_value = king_value
        self.CHECKERS = CHECKERS
    def EVALUATION(self, side, list_of_checkers):
        #LIST_CHECKER(list_of_checkers, man_r, man_w, king_r, king_w)
        total_r = len(np.argwhere(np.array(list_of_checkers)<0))
        total_w = len(np.argwhere(np.array(list_of_checkers)>0))
        (man_jump, king_jump, man_walk, king_walk, taken_by_man, taken_by_king) = self.CHECKERS.AVAILABLE_MOVE(side, list_of_checkers)
        available_move = man_jump + king_jump + man_walk + king_walk
        if total_r == 0:
            evaluation = self.max_eva;
        elif total_w == 0 :
            evaluation = -self.max_eva;
        elif available_move == []:
            if side == 1:
                evaluation = self.max_eva
            else:
                evaluation = -self.max_eva
        else:
            #evaluation = 1.0*(len(man_w)-len(man_r)) + 2.0*(len(king_w)-len(king_r))
            evaluation = np.array(list_of_checkers).sum()
            #for i in man_w:
                #if i//self.Nx == self.Nx-2:
                #    evaluation += 0.1
                #elif i//self.Nx == self.Nx-3:
                #    evaluation += 0.2
            #for i in king_w:
                #if i//self.Nx == self.Nx-1:
                #    evaluation -= 0.2
                #elif i//self.Nx == self.Nx-2:
                #    evaluation -= 0.1
            #for i in man_r:
                #if i//self.Nx == 1:
                #    evaluation -= 0.1
                #elif i//self.Nx == 2:
                #    evaluation -= 0.2
            #for i in king_r:
                #if i//self.Nx == 0:
                #    evaluation += 0.2
                #elif i//self.Nx == self.Nx-2:
                #    evaluation += 0.1
        if abs(evaluation)!= self.max_eva:
                if evaluation>0:
                    evaluation *= 0.5+total_w/(total_w+total_r)
                elif evaluation<0:
                    evaluation *= 0.5+total_r/(total_w+total_r)
        return evaluation

    def ONE_MOVE(self, side, list_of_checkers):
        (man_jump, king_jump, man_walk, king_walk, taken_by_man, taken_by_king ) = self.CHECKERS.AVAILABLE_MOVE(side, list_of_checkers)
        checkers_tree = []
        if man_jump+king_jump != []:
            man_jump_tree = []
            man_jump_tree.append((man_jump.copy(),list_of_checkers.copy()))
            while man_jump_tree != []:
                #print(man_jump)
                temp = man_jump_tree[-1][1].copy()
                man_jump = man_jump_tree[-1][0].copy()
                del man_jump_tree[-1]
                for (start, stop) in man_jump:
                    virtual_checkers = temp.copy()
                    taken = (start+stop)//2
                    virtual_checkers[start] = 0
                    virtual_checkers[taken] = 0
                    if side == 1:
                        if stop//self.Nx == 0:
                            virtual_checkers[stop] = -self.king_value
                            checkers_tree.append(virtual_checkers.copy())
                        else:
                            virtual_checkers[stop] = -self.man_value             
                            man_jump_prime = []
                            taken_by_man = []
                            self.CHECKERS.MAN_JUMP_RED(stop, virtual_checkers, man_jump_prime, taken_by_man)
                            if man_jump_prime == []:
                                checkers_tree.append(virtual_checkers.copy())
                            else:
                                man_jump_tree.append((man_jump_prime.copy(),virtual_checkers.copy()))
                    else:
                        if stop//self.Nx == self.Nx-1:
                            virtual_checkers[stop] = self.king_value
                            checkers_tree.append(virtual_checkers.copy())
                        else:
                            virtual_checkers[stop] = self.man_value       
                            man_jump_prime = []
                            taken_by_man = []
                            self.CHECKERS.MAN_JUMP_WHITE(stop, virtual_checkers, man_jump_prime, taken_by_man)
                            if man_jump_prime == []:
                                checkers_tree.append(virtual_checkers.copy())
                            else:
                                man_jump_tree.append((man_jump_prime.copy(),virtual_checkers.copy()))
            king_jump_tree = []
            king_jump_tree.append((king_jump.copy(), list_of_checkers.copy()))
            while king_jump_tree != []:
                temp = king_jump_tree[-1][1].copy()
                king_jump = king_jump_tree[-1][0].copy()
                del king_jump_tree[-1]
                for (start, stop) in king_jump:
                    virtual_checkers = temp.copy()
                    taken = (start+stop)//2
                    virtual_checkers[start] = 0
                    virtual_checkers[taken] = 0
                    if side == 1:
                        virtual_checkers[stop] = -self.king_value             
                        king_jump_prime = []
                        taken_by_king = []
                        self.CHECKERS.KING_JUMP_RED(stop, virtual_checkers, king_jump_prime, taken_by_king)
                        if king_jump_prime == []:
                            checkers_tree.append(virtual_checkers.copy())
                        else:
                            king_jump_tree.append((king_jump_prime.copy(), virtual_checkers.copy()))
                    else:
                        virtual_checkers[stop] = self.king_value 
                        king_jump_prime = []
                        taken_by_king = []
                        self.CHECKERS.KING_JUMP_WHITE(stop, virtual_checkers, king_jump_prime, taken_by_king)
                        if king_jump_prime == []:
                            checkers_tree.append(virtual_checkers.copy())
                        else:
                            king_jump_tree.append((king_jump_prime.copy(), virtual_checkers.copy()))
        elif man_walk+king_walk != []:
            for (start, stop) in man_walk:
                virtual_checkers = list_of_checkers.copy()
                virtual_checkers[start] = 0
                if side == 1:
                    if stop//self.Nx == 0:
                        virtual_checkers[stop] = -self.king_value
                    else:
                        virtual_checkers[stop] = -self.man_value
                else:
                    if stop//self.Nx == self.Nx-1:
                        virtual_checkers[stop] = self.king_value
                    else:
                        virtual_checkers[stop] = self.man_value
                checkers_tree.append(virtual_checkers.copy())
            for (start, stop) in king_walk:
                virtual_checkers = list_of_checkers.copy()
                virtual_checkers[start] = 0
                if side == 1:
                    virtual_checkers[stop] = -self.king_value
                else:
                    virtual_checkers[stop] = self.king_value
                checkers_tree.append(virtual_checkers.copy())
        else:
            checkers_tree.append(list_of_checkers)
        return checkers_tree

    def BUILD_TREE(self, side, list_of_checkers, depth):
        temp = self.ONE_MOVE(side,list_of_checkers)
        if depth != 1:
            A = []
            for i in temp:
                A.append(BUILD_TREE(-side, i, depth-1))
            return A.copy()
        elif depth == 1:
            point = np.zeros((len(temp)))
            for index,element in enumerate(temp):
                point[index] = self.EVALUATION(side, element)
            return point

    def MIN_MAX_SEARCH(self, side, list_of_checkers, depth):
        temp = self.ONE_MOVE(side,list_of_checkers)
        point = np.zeros((len(temp)))
        if depth > 1:
            for index, element in enumerate(temp):
                point[index] = self.MIN_MAX_SEARCH(-side, element, depth-1)
            if side == 1:
                return point.min()
            else:
                return point.max()
        elif depth == 1:
            #print(side)
            for index,element in enumerate(temp):
                point[index] = self.EVALUATION(side, element)
            if side == 1:
                return point.min()
            else:
                return point.max()

    def FIND_BEST_MOVE_MIN_MAX(self, side, list_of_checkers, depth):
        temp = self.ONE_MOVE(side, list_of_checkers)
        point = np.zeros((len(temp)))
        for index,element in enumerate(temp):
            if depth > 1:
                point[index] = self.MIN_MAX_SEARCH(-side, element, depth-1)
            elif depth == 1:
                point[index] = self.EVALUATION(side, element)
        choice = np.random.choice(np.argwhere(point==point.max()).reshape(-1))
        ##################
        #choice_list = np.argwhere(point==point.max()).reshape(-1)
        #a = np.zeros((len(choice_list)))
        #for index, element in enumerate(choice_list):
        #    a[index] = EVALUATION(side, temp[element])
        #choice =  choice_list[np.random.choice(np.argwhere(a==a.max()).reshape(-1))]
        ##################
        return (temp[choice].copy(), point.max() )

    def ALPHA_BETA_SEARCH(self, side, list_of_checkers, depth, alpha, beta):
        if depth > 0:
            temp = self.ONE_MOVE(side, list_of_checkers)
            if side == 1: #minimum node, evaluate beta
                for i in temp:
                    if depth != 1:
                        beta = min(beta, self.ALPHA_BETA_SEARCH(-side, i, depth-1, alpha, beta))
                    else:
                        beta = min(beta, self.ALPHA_BETA_SEARCH(side, i, depth-1, alpha, beta))
                    if beta <= alpha:
                        break
                return beta
            else:
                for i in temp:
                    if depth != 1:
                        alpha = max(alpha, self.ALPHA_BETA_SEARCH(-side, i, depth-1, alpha, beta))
                    else:
                        alpha = max(alpha, self.ALPHA_BETA_SEARCH(side, i, depth-1, alpha, beta))
                    if beta <= alpha:
                        break
                return alpha
        elif depth == 0:
            point = self.EVALUATION(side, list_of_checkers)
            return point

    def FIND_BEST_MOVE_ALPHA_BETA(self, side, list_of_checkers, depth, alpha, beta):
        temp = self.ONE_MOVE(side, list_of_checkers)
        point = np.zeros((len(temp)))
        for index,element in enumerate(temp):
            point[index] = self.ALPHA_BETA_SEARCH(-side, element, depth-1, alpha, beta)
        choice = np.random.choice(np.argwhere(point==point.max()).reshape(-1))
        ##################
        #choice_list = np.argwhere(point==point.max()).reshape(-1)
        #a = np.zeros((len(choice_list)))
        #for index, element in enumerate(choice_list):
        #    a[index] = EVALUATION(side, temp[element])
        #choice =  choice_list[np.random.choice(np.argwhere(a==a.max()).reshape(-1))]
        ##################
        return (temp[choice].copy(), point.max() )

    def REVERSE_COLOR_AND_BOARD(self, list_of_checkers):  # designed for red if alpha-beta prouning need to be applied
        reverse = []
        for i in range(0, self.Nx**2):
            a = list_of_checkers[63-i]
            if a!=0:
                reverse.append(-a)
            else:
                reverse.append(0)
        return reverse.copy()


# In[ ]:




