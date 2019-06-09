#!/usr/bin/env python
# coding: utf-8

# In[1]:
class Checkers_Basic:
    def __init__(self, Nx, man_value, king_value, step_fr_r, step_fl_r, step_br_r, step_bl_r, step_fr_w, step_fl_w, step_br_w, step_bl_w, man_r, man_w, king_r, king_w):
        self.Nx = Nx
        self.man_value = man_value
        self.king_value = king_value  
        self.step_fr_r = step_fr_r
        self.step_fl_r = step_fl_r
        self.step_br_r = step_br_r
        self.step_bl_r = step_bl_r
        self.step_fr_w = step_fr_w
        self.step_fl_w = step_fl_w
        self.step_br_w = step_br_w
        self.step_bl_w = step_bl_w
        self.man_r = man_r
        self.man_w = man_w
        self.king_r = king_r
        self.king_w = king_w
    
    def CHECKER_LIST(self, list_of_checkers):
        for element in self.man_r:
            list_of_checkers[element] = -self.man_value
        for element in self.man_w:
            list_of_checkers[element] = self.man_value
        for element in self.king_r:
            list_of_checkers[element] = -self.king_value
        for element in self.king_w:
            list_of_checkers[element] = self.king_value
        return(list_of_checkers)

    def LIST_CHECKER(self, list_of_checkers):
        for index, element in enumerate(list_of_checkers):
            if element == -self.man_value:
                self.man_r.append(index)
            elif element == self.man_value:
                self.man_w.append(index)
            elif element == -self.king_value:
                self.king_r.append(index)
            elif element == self.king_value:
                self.king_w.append(index)
        return(self.man_r, self.man_w, self.king_r, self.king_w)

    def MAN_JUMP_RED(self, index, list_of_checkers, man_jump, taken_by_man):
        if index%self.Nx != self.Nx-1:
            temp = index + self.step_fr_r
            temp2 = temp + self.step_fr_r
            if index//self.Nx>1 and temp%self.Nx!=self.Nx-1 and list_of_checkers[temp]>0 and list_of_checkers[temp2] == 0:
                #record the position of taken pieces
                taken_by_man.append(temp)
                man_jump.append( (index,temp2) )
        if index%self.Nx != 0:
            temp = index + self.step_fl_r
            temp2 = temp + self.step_fl_r
            if index//self.Nx>1 and temp%self.Nx!=0 and list_of_checkers[temp]>0 and list_of_checkers[temp2] == 0:
                #record the position of taken pieces
                taken_by_man.append(temp)
                man_jump.append( (index,temp2) )

    def MAN_WALK_RED(self, index, list_of_checkers, man_walk):
        if index%self.Nx != self.Nx-1:
            temp = index + self.step_fr_r
            if list_of_checkers[temp] == 0:
                man_walk.append( (index,temp) )
        if index%self.Nx != 0:
            temp = index + self.step_fl_r
            if list_of_checkers[temp] == 0:
                man_walk.append( (index,temp) )

    def KING_JUMP_RED(self, index, list_of_checkers, king_jump, taken_by_king):
        if index%self.Nx != self.Nx-1:
            temp = index + self.step_fr_r
            temp2 = temp + self.step_fr_r
            if index//self.Nx>1 and temp%self.Nx!=self.Nx-1 and list_of_checkers[temp]>0.0 and list_of_checkers[temp2] == 0:
                #record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append( (index,temp2) )                  
            temp = index + self.step_br_r
            temp2 = temp + self.step_br_r
            if index//self.Nx<self.Nx-2 and temp%self.Nx!=self.Nx-1 and list_of_checkers[temp]>0 and list_of_checkers[temp2] == 0:
                #record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append( (index,temp2) )
        if index%self.Nx != 0:
            temp = index + self.step_fl_r
            temp2 = temp + self.step_fl_r
            if index//self.Nx>1 and temp%self.Nx!=0 and list_of_checkers[temp]>0.0 and list_of_checkers[temp2] == 0:
                #record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append( (index,temp2) )
            temp = index + self.step_bl_r
            temp2 = temp + self.step_bl_r
            if index//self.Nx<self.Nx-2 and temp%self.Nx!=0 and list_of_checkers[temp]>0 and list_of_checkers[temp2] == 0:
                #record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append( (index,temp2) )

    def KING_WALK_RED(self, index, list_of_checkers, king_walk):
        if index%self.Nx != self.Nx-1:
            temp = index + self.step_fr_r
            if index//self.Nx>0 and list_of_checkers[temp] == 0:
                king_walk.append( (index,temp) )
            temp = index + self.step_br_r
            if index//self.Nx<self.Nx-1 and list_of_checkers[temp] == 0:
                king_walk.append( (index,temp) )
        if index%self.Nx != 0:
            temp = index + self.step_fl_r
            if index//self.Nx>0 and list_of_checkers[temp] == 0:
                king_walk.append( (index,temp) )
            temp = index + self.step_bl_r
            if index//self.Nx<self.Nx-1 and list_of_checkers[temp] == 0:
                king_walk.append( (index,temp) )

    def MAN_JUMP_WHITE(self, index, list_of_checkers, man_jump, taken_by_man):
        if index%self.Nx != self.Nx-1:
            temp = index + self.step_fr_w
            temp2 = temp + self.step_fr_w
            if index//self.Nx<self.Nx-2 and temp%self.Nx!=self.Nx-1 and list_of_checkers[temp]<0 and list_of_checkers[temp2] == 0:
                #record the position of taken pieces
                taken_by_man.append(temp)
                man_jump.append( (index,temp2) )
        if index%self.Nx != 0:
            temp = index + self.step_fl_w
            temp2 = temp + self.step_fl_w
            if index//self.Nx<self.Nx-2 and temp%self.Nx!=0 and list_of_checkers[temp]<0 and list_of_checkers[temp2] == 0:
                #record the position of taken pieces
                taken_by_man.append(temp)
                man_jump.append( (index,temp2) )

    def MAN_WALK_WHITE(self, index, list_of_checkers, man_walk):
        if index%self.Nx != self.Nx-1:
            temp = index + self.step_fr_w
            if list_of_checkers[temp] == 0:
                man_walk.append( (index,temp) )
        if index%self.Nx != 0:
            temp = index + self.step_fl_w
            if list_of_checkers[temp] == 0:
                man_walk.append( (index,temp) )

    def KING_JUMP_WHITE(self, index, list_of_checkers, king_jump, taken_by_king):
        if index%self.Nx != self.Nx-1:
            temp = index + self.step_fr_w
            temp2 = temp + self.step_fr_w
            if index//self.Nx<self.Nx-2 and temp%self.Nx!=self.Nx-1 and list_of_checkers[temp]<0 and list_of_checkers[temp2] == 0:
                #record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append( (index,temp2) )                  
            temp = index + self.step_br_w
            temp2 = temp + self.step_br_w
            if index//self.Nx>1 and temp%self.Nx!=self.Nx-1 and list_of_checkers[temp]<0 and list_of_checkers[temp2] == 0:
                #record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append( (index,temp2) )                 
        if index%self.Nx != 0:
            temp = index + self.step_fl_w
            temp2 = temp + self.step_fl_w
            if index//self.Nx<self.Nx-2 and temp%self.Nx!=0 and list_of_checkers[temp]<0 and list_of_checkers[temp2] == 0:
                #record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append( (index,temp2) )
            temp = index + self.step_bl_w
            temp2 = temp + self.step_bl_w
            if index//self.Nx>1 and temp%self.Nx!=0 and list_of_checkers[temp]<0 and list_of_checkers[temp2] == 0:
                #record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append( (index,temp2) )

    def KING_WALK_WHITE(self, index, list_of_checkers, king_walk):
        if index%self.Nx != self.Nx-1:
            temp = index + self.step_fr_w
            if index//self.Nx<self.Nx-1 and list_of_checkers[temp] == 0:
                king_walk.append( (index,temp) )
            temp = index + self.step_br_w
            if index//self.Nx>0 and list_of_checkers[temp] == 0:
                king_walk.append( (index,temp) )
        if index%self.Nx != 0:
            temp = index + self.step_fl_w
            if index//self.Nx<self.Nx-1 and list_of_checkers[temp] == 0:
                king_walk.append( (index,temp) )
            temp = index + self.step_bl_w
            if index//self.Nx>0 and list_of_checkers[temp] == 0:
                king_walk.append( (index,temp) )

    def AVAILABLE_MOVE(self, side, list_of_checkers):
        man_jump = []
        king_jump = []
        man_walk = []
        king_walk = []
        taken_by_man = []
        taken_by_king = []
        have_man = []
        have_king = []

        # red
        if side==1:
            for index, element in enumerate(list_of_checkers):
                # red man jump
                if element==-self.man_value:
                    self.MAN_JUMP_RED(index, list_of_checkers, man_jump, taken_by_man)
                    have_man.append(index)  #save the position having man so no need to go through the empty sites again 
                # red king jump
                elif element==-self.king_value:
                    self.KING_JUMP_RED(index, list_of_checkers, king_jump, taken_by_king)
                    have_king.append(index)  #save the position having king so no need to go through the empty sites again
            if man_jump == [] and king_jump == []:
                for index in have_man:
                    self.MAN_WALK_RED(index, list_of_checkers, man_walk)
                for index in have_king:
                    self.KING_WALK_RED(index, list_of_checkers, king_walk)
        # white            
        if side==-1:
            for index, element in enumerate(list_of_checkers):
                # white man jump
                if element==self.man_value:                 
                    self.MAN_JUMP_WHITE(index, list_of_checkers, man_jump, taken_by_man)
                    have_man.append(index)  #save the position having man so no need to go through the empty sites again 
                # white king jump
                elif element==self.king_value:
                    self.KING_JUMP_WHITE(index, list_of_checkers, king_jump, taken_by_king)
                    have_king.append(index)  #save the position having king so no need to go through the empty sites again
            if man_jump == [] and king_jump == []:
                for index in have_man:
                    self.MAN_WALK_WHITE(index, list_of_checkers, man_walk)
                for index in have_king:
                    self.KING_WALK_WHITE(index, list_of_checkers, king_walk)

        return (man_jump, king_jump, man_walk, king_walk, taken_by_man, taken_by_king)

    def saving(self, list_of_checkers, save):
            save.append(list_of_checkers.copy())  # Use copy to clone the element of list. If use '=' directly, what is really cloned
                                                  # is the address of the list! See http://www.runoob.com/python3/python3-att-list-copy.html

# In[ ]:




