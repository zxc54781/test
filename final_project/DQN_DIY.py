#!/usr/bin/env python
# coding: utf-8

# In[4]:


"""
This part of code is the DQN brain, which is a brain of the agent.
All decisions are made in here.
Using Tensorflow to build the neural network.
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
Using:
Tensorflow: 1.0
gym: 0.7.3
"""
import numpy as np
import keras
from keras.layers import Dense, Input
from keras.models import Model
from keras.optimizers import SGD, RMSprop ,adam
from keras import backend as K

np.random.seed(1)

# Deep Q Network off-policy
class DeepQNetwork:
    def __init__(self, n_actions, n_features, Nx, king_value, step_fr_r, step_fl_r, step_br_r, step_bl_r, step_fr_w, step_fl_w, step_br_w, step_bl_w, learning_rate=0.1, reward_decay=0.9, e_greedy=0.9, replace_target_iter=300, memory_size=500, batch_size=128, e_greedy_increment=None ):#給輸出輸多少 action ,接收多少feature
        self.n_actions = n_actions
        self.n_features = n_features
        self.Nx = Nx
        self.king_value = king_value
        self.step_fr_r = step_fr_r
        self.step_fl_r = step_fl_r
        self.step_br_r = step_br_r
        self.step_bl_r = step_bl_r
        self.step_fr_w = step_fr_w
        self.step_fl_w = step_fl_w
        self.step_br_w = step_br_w
        self.step_bl_w = step_bl_w
        
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon_max = e_greedy
        self.replace_target_iter = replace_target_iter
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.epsilon_increment = e_greedy_increment
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max
        
        # total learning step
        self.learn_step_counter = 0 ## 記錄學了多少步

        # initialize zero memory [s, a, r, s_] 
        self.memory = np.zeros((self.memory_size, n_features * 2 + 2))# 製作出一個空的資料庫兩個state 以及選擇的動作以及 reward

        # consist of [target_net, evaluate_net]
        self._build_net()
        
        ###t_params = tf.get_collection('target_net_params')
        ###e_params = tf.get_collection('eval_net_params')
        ###self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)]

        ###self.sess = tf.Session()

        '''if output_graph:
            # $ tensorboard --logdir=logs
            # tf.train.SummaryWriter soon be deprecated, use following
            tf.summary.FileWriter("logs/", self.sess.graph)'''

        ###self.sess.run(tf.global_variables_initializer())
        ###self.cost_his = []
        
    def target_replace_op(self):
        v1 = self.model2.get_weights() ## 把trage 的權重丟到eval  這個返回得型態 為 array
        self.model1.set_weights(v1)
        print("params has changed")

    def _build_net(self):
        # evaluate
        eval_inputs = Input(shape=(self.n_features,)) ## input 是features 
        x1_ev = Dense(64, activation='relu')(eval_inputs)
        x2_ev = Dense(256, activation='relu')(x1_ev)
        x3_ev = Dense(128, activation='relu')(x2_ev)
        self.q_eval = Dense(self.n_actions)(x3_ev)
        
        # target
        target_inputs = Input(shape=(self.n_features,))
        x1_ta = Dense(64, activation='relu')(target_inputs)
        x2_ta = Dense(256, activation='relu')(x1_ta)
        x3_ta = Dense(128, activation='relu')(x2_ta)
        self.q_next = Dense(self.n_actions)(x3_ta)

        self.model1 = Model(target_inputs, self.q_next) ## 有兩個輸入
        self.model2 = Model(eval_inputs, self.q_eval)
        ####rmsprop = RMSprop(lr=self.lr) ## 優化器
        lr=self.lr
        #self.model1.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr), metrics=['accuracy']) #mean_squared_error
        #self.model2.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr), metrics=['accuracy'])
        #self.model1.compile(loss='mse', optimizer=RMSprop(lr), metrics=['accuracy']) #mean_squared_error
        #self.model2.compile(loss='mse', optimizer=RMSprop(lr), metrics=['accuracy'])
        self.model1.compile(loss='mse', optimizer=adam(), metrics=['accuracy']) #mean_squared_error
        self.model2.compile(loss='mse', optimizer=adam(), metrics=['accuracy'])

    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'): #判断对象是否包含对应的属性
            self.memory_counter = 0 
        
        
        #以相同size 使之存取
        a=np.reshape(a,[1,1])
        r=np.reshape(r,[1,1])
        s=np.reshape(s,[1,64])
        s_=np.reshape(s_,[1,64])
        
        transition = np.hstack((s, a, r, s_))
        #在0行插入 trans 接著再1行插入 
        
        # replace the old memory with new memory
        index = self.memory_counter % self.memory_size # 好像是因為要取前後的s
        self.memory[index, :] = transition

        self.memory_counter += 1
#-----------------------------------------------------------------------
    def choose_action(self, observation):
        # to have batch dimension when feed into tf placeholder
        # observation = observation[np.newaxis, :] ## 把observation變成二維 [1,2,3]=>[[1],[2],[3]]
       
        if np.random.uniform() < self.epsilon: ##前者為0~1隨機出一個數
            actions_value = self.model1.predict(observation)
            action_index = np.argmax(actions_value) # 最大值的位置
        else: 
            action_index = np.random.randint(0, self.n_actions) # 隨機返回一個整數 here should be 0-7
        return action_index
#-----------------------------------------------------------------------
    def learn(self):#確定要不要換參數（targe 換成 eval) 
        # check to replace target parameters
        if self.learn_step_counter % self.replace_target_iter == 0:
            self.target_replace_op() ## target 帶入 
            print('\ntarget_params_replaced\n')
        
        # sample batch memory from all memory
        
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]
        q_next, q_eval = self.model1.predict(batch_memory[:, -self.n_features:]), self.model2.predict(
            batch_memory[:, :self.n_features])# fixed params newest params
        
        # change q_target w.r.t q_eval's action
        
        q_target = q_eval.copy() # 加了 copy 可以避免target 被洗掉
        batch_index = np.arange(self.batch_size, dtype=np.int32) #np.arange(3)=[0,1,2]
        eval_act_index = batch_memory[:, self.n_features].astype(int) #把記憶庫裡面的 action  轉成 int 
        reward = batch_memory[:, self.n_features + 1] 
        q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1) ## 學習就是在這邊！
        
        # train eval network
        self.model2.fit(batch_memory[:, :self.n_features], q_target, epochs=10)
        
        # increasing epsilon
        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1
        
    '''def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()'''
    
    def ACTION(self, action_index, array_of_checkers):
        position = np.argwhere(array_of_checkers==self.king_value).reshape(-1)
        position_opponent = np.argwhere(array_of_checkers==-self.king_value).reshape(-1)
        piece_1 = position[0]
        piece_2 = position[1]
        piece_3 = position_opponent[0]
        #piece_3 = 55
        x_1_start = piece_1%self.Nx
        y_1_start = piece_1//self.Nx
        x_2_start = piece_2%self.Nx
        y_2_start = piece_2//self.Nx
        x_3_start = piece_3%self.Nx
        y_3_start = piece_3//self.Nx

        if piece_2<piece_1:
            temp = piece_1
            piece_1 = piece_2
            piece_2 = temp
        if action_index == 0 :
            start = piece_1
            if start%self.Nx!=self.Nx-1 and start//self.Nx!=self.Nx-1:
                stop = start + self.step_fr_w
            else:
                stop = start
        elif action_index == 1:
            start = piece_1
            if start%self.Nx!=0 and start//self.Nx!=self.Nx-1:
                stop = start + self.step_fl_w
            else:
                stop = start
        elif action_index == 2:
            start = piece_1
            if start%self.Nx!=self.Nx-1 and start//self.Nx!=0:
                stop = start + self.step_br_w
            else:
                stop = start
        elif action_index == 3:
            start = piece_1
            if start%self.Nx!=0 and start//self.Nx!=0:
                stop = start + self.step_bl_w
            else:
                stop = start
        elif action_index == 4:
            start = piece_2
            if start%self.Nx!=self.Nx-1 and start//self.Nx!=self.Nx-1:
                stop = start + self.step_fr_w
            else:
                stop = start
        elif action_index == 5:
            start = piece_2
            if start%self.Nx!=0 and start//self.Nx!=self.Nx-1:
                stop = start + self.step_fl_w
            else:
                stop = start
        elif action_index == 6:
            start = piece_2
            if start%self.Nx!=self.Nx-1 and start//self.Nx!=0:
                stop = start + self.step_br_w
            else:
                stop = start
        elif action_index == 7:
            start = piece_2
            if start%self.Nx!=0 and start//self.Nx!=0:
                stop = start + self.step_bl_w
            else:
                stop = start

        x_stop = stop%self.Nx
        y_stop = stop//self.Nx

        if action_index<4:
            delta_x_start = abs(x_1_start-x_3_start)
            delta_y_start = abs(y_1_start-y_3_start)
            delta_start = max(delta_x_start, delta_y_start)
        else:
            delta_x_start = abs(x_2_start-x_3_start)
            delta_y_start = abs(y_2_start-y_3_start)
            delta_start = max(delta_x_start, delta_y_start)

        delta_x_stop = abs(x_stop-x_3_start)
        delta_y_stop = abs(y_stop-y_3_start)
        delta_stop = max(delta_x_stop, delta_y_stop)

        if delta_stop<delta_start:
            give_reward = 0.5
        else:
            give_reward = 0.0

        if array_of_checkers[stop]!=self.king_value and array_of_checkers[stop]!= -self.king_value: 
            # If red king is at the side, we need to prevent the white king step into that square(in this case taken is 
            # not availabe so it cannot be detected by checking taken by king or something similiar)
            return(start, stop, give_reward)
        else:
            return(start, start, give_reward)

    def APPLY_ACTION(self, action, list_of_checkers):
        list_of_checkers_next = list_of_checkers.copy()
        list_of_checkers_next[action[0]] = 0
        list_of_checkers_next[action[1]] = 2
        #opponent_position = np.argwhere(observation_next== -2).reshape(-1)[0]
        #reward = .0
        #if abs(action[1]//self.Nx-opponent_position//self.Nx) < (action[0]//self.Nx-opponent_position//self.Nx) or \
        #    abs(action[1]%self.Nx-opponent_position%self.Nx) < (action[0]%self.Nx-opponent_position%self.Nx):
            #reward = 1.0
        #return reward, observation_next
        return list_of_checkers_next.copy()

    def POSITION_INITIALIZE(self):
        submit = False
        while not submit:
            #initialize = np.random.choice(list(np.arange(0,self.Nx**2/2)),3, replace=False)
            initialize = np.random.choice(list(np.arange(0,self.Nx**2/2)),2, replace=False)
            x_k = (2*initialize)%self.Nx
            y_k = (2*initialize)//self.Nx
            parity = (x_k+y_k+1)%2
            x_k += parity

            initialize = np.int32(x_k + self.Nx*y_k)
            king_w = list(initialize[0:2])
            #king_r = initialize[-1]
            king_r = 55
            if king_r%self.Nx==self.Nx-1:
                if king_r//self.Nx==0:
                    if king_r+self.step_bl_r not in king_w:
                        submit = True
                else:
                    if king_r+self.step_bl_r not in king_w and king_r+self.step_fl_r not in king_w:
                        submit = True
            elif king_r%self.Nx==0:
                if king_r//self.Nx==self.Nx-1:
                    if king_r+self.step_fr_r not in king_w:
                        submit = True
                else:
                    if king_r+self.step_br_r not in king_w and king_r+self.step_fr_r not in king_w:
                        submit = True
            elif king_r//self.Nx==0:
                if king_r+self.step_br_r not in king_w and king_r+self.step_bl_r not in king_w:
                    submit = True
            elif king_r//self.Nx==self.Nx-1:
                if king_r+self.step_fr_r not in king_w and king_r+self.step_fl_r not in king_w:
                    submit = True
            else:
                if king_r+self.step_fr_r not in king_w and king_r+self.step_fl_r not in king_w            and king_r+self.step_br_r not in king_w and king_r+self.step_bl_r not in king_w:
                    submit = True
            if king_r in king_w:
                submit = False
        return [king_r], king_w

