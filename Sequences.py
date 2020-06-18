#!/usr/bin/env python
# coding: utf-8

# # Séquences d'événements logiciels
# 
# Jusqu'ici j'ai analysé les données brutes sans faire de traitements qui n'étaient pas nécéssaires à l'affichage. Mais les données représentent des événenements logiciels comme naviguer vers une page, charger une video, quitter une page et non pas des événemnts directements liés à l'apprentissage.
# 
# Afin de pouvoir montrer des données pertinentes aux utilisateurs, il faudrait déterminer ce à quoi correspondent certaines séquences d'évenements logiciels et lier ces séquences à un objectif éducatif.
# 
# 

# ## Obtenir la liste d'événements
# Dans un premier temps, il faut lister les actions effectuées et les trier par date afin d'obtenir des séquences chronologiques.
# 
# Pourt cela on importe tout d'abord les données. Celles-ci étant très volumineuse car en très grande quantité on été limitées à un extrait correspondant au 40000 premières lignes.

# In[2]:


import pandas as pd
import datetime as dt

data = pd.read_csv("data/trackinglogs_course-v1_minestelecom_04026_session02_chunk_1.csv")


# Les actions sont décrites dans la colone "event_type" par un URL relatif menant à différents endroits d'un cours ou par un mot clef représentant une interaction avec un élément de la page. A cela s'ajoute le contexte qui correspond à la page sur laquelle était l'utilisateur au moement de l'action.
# 
# Afin de mieux filter ces informations, on divise les infomations en jetons correspondant aux différents niveux d'imbrication des URL et on retire les identifiant communs qui correspondent au cours dont proviennent les données. Ensuite on crée une colonne "event_category" correspondant au premier niveau d'action qui correspond au type d'action effectuée.

# In[3]:


data["event_type_tokens"] = data["event_type"].apply(lambda x: x.split('/'))
data["path_tokens"] = data["context.path"].apply(lambda x: x.split('/'))
for line in data["event_type_tokens"]:
    try :
        line.remove('')
        line.remove('courses')
        line.remove('course-v1:MinesTelecom+04026+session02')
        line.remove('')
    except :
        pass
for line in data["path_tokens"]:
    try :
        line.remove('')
        line.remove('courses')
        line.remove('course-v1:MinesTelecom+04026+session02')
        line.remove('')
    except :
        pass
data["event_category"] = data["event_type_tokens"].apply(lambda x: 'null' if len(x) == 0 else x[0])


# Afin de mieux visualiser les informations, on fait le tri sur les catégories d'actions ainsi que sur l'horodatage de celles-ci.

# In[4]:


user687522 = data[data["context.user_id"] == 1055391].sort_values(by='time')

#display value couts
#print(data["context.user_id"].value_counts())
user1055391 = data[data["context.user_id"] == 1055391].sort_values(by='time')
user617997  = data[data["context.user_id"] == 617997 ].sort_values(by='time')
user7214527 = data[data["context.user_id"] == 7214527].sort_values(by='time')
user7206957 = data[data["context.user_id"] == 7206957].sort_values(by='time')

event_category_array = pd.concat([user1055391["event_category"].reset_index(drop=True), user1055391["time"].reset_index(drop=True), user617997["event_category"].reset_index(drop=True),user617997["time"].reset_index(drop=True),user7214527["event_category"].reset_index(drop=True),user7214527["time"].reset_index(drop=True), user7206957["event_category"].reset_index(drop=True),user7206957["time"].reset_index(drop=True)],axis=1)
event_category_array.to_csv("./event_category_array.csv", index=False)


# ## Recherche de Séquences
# 
# Dans un premier temps, on peut chercher à repérer des séquences en observant simplement les données. Certains motifs sont facilement observables mais il pourrait être pertinent de fournir ces données à un algorithme de recherche de séquences afin de trouver des séquences que l'on ne remarque pas au premier coup d'oeil ou encore des séquences plus englobantes.
# ### Résolutions de problèmes
# 
# On peut observer que lors de la résolution de problèmes il y a deux événements "problem_check" quasi simultanés, un événement "xblock" correspondant à une interaction de l'utilisateur avec un élément de la page (QCM, quizz) et un événement "problem_graded".
# 
# ![](./pictures/seq_problem_check_01.png)
# 
# ![](./pictures/seq_problem_check_02.png)
# 
# La séquence peut commencer de deux manières différentes mais reste toujours ininterrompue sur les données étudiées et correspond à la demande d'évaluation d'un problème.
# 
# ### Visionnage de videos
# 
# Lors du visionnage de vidéos, la séquences est plus compliquée car il y a beaucoup de répétitions en fonction du temps passé par l'utilisateur à visionner certains passages.
# 
# ![](./pictures/seq_play_video_01.png)
# 
# Il pourrait être intéressant de comparer comment différents apprenants interagissent avec les videos.
# 

# In[5]:


data["event_category_detailed"] = data["event_type_tokens"].apply(lambda x: 'null' if len(x) == 0 else x[0] if len(x) == 1 else x[0]+'+'+str(len(x)) )

user1055391 = data[data["context.user_id"] == 1055391].sort_values(by='time')
user617997  = data[data["context.user_id"] == 617997 ].sort_values(by='time')
user7214527 = data[data["context.user_id"] == 7214527].sort_values(by='time')
user7206957 = data[data["context.user_id"] == 7206957].sort_values(by='time')

event_category_array = pd.concat([user1055391["event_category_detailed"].reset_index(drop=True), user1055391["time"].reset_index(drop=True), user617997["event_category_detailed"].reset_index(drop=True),user617997["time"].reset_index(drop=True),user7214527["event_category_detailed"].reset_index(drop=True),user7214527["time"].reset_index(drop=True), user7206957["event_category_detailed"].reset_index(drop=True),user7206957["time"].reset_index(drop=True)],axis=1)
event_category_array.to_csv("./event_category_array_detailed.csv", index=False)

parser_input_user1055391 = ' '.join(user1055391["event_category"].reset_index(drop=True).tolist())
parser_input_user617997  = ' '.join(user617997["event_category"].reset_index(drop=True).tolist())
parser_input_user7214527 = ' '.join(user7214527["event_category"].reset_index(drop=True).tolist())
parser_input_user7206957 = ' '.join(user7206957["event_category"].reset_index(drop=True).tolist())


# ##### Regrouper les evenements et mesurer le temps écoulé
# 
# Afin d'obtenir des visualisation plus pertinentes, il est important de filtrer les resultats obtenus plus tÃ´t. En rassemblant les séquences, on peut non seulement observer un comprtement plus "humain" mais aussi déduire le temps passé sur certaines actions.
# 

# In[6]:



from ply import lex
import ply.yacc as yacc


tokens = (
    "WIKIACCESS",
    "COURSEWAREACCESS",
    "VIDEOSTART",
    "VIDEOINTERACT",
    "VIDEOSTOP",
    "PAGENAV",
    "PROBLEMSAVE",
    "TIMESTAMP",
    "EXIT",
    "FORUM",
    "ODD"
)

t_ignore = ' \t,'

t_WIKIACCESS = r'(course_)?wiki|info|about'
t_COURSEWAREACCESS  = r'courseware|progress'
t_VIDEOSTART   = r'(load_)?video(_player_ready)?'
t_VIDEOINTERACT     = r'(pause|seek|play)_video'
t_VIDEOSTOP = r'stop_video'
t_PAGENAV  = r'(xblock|seq_next|seq_prev|seq_goto|jump_to_id)'
t_PROBLEMSAVE  = r'(problem_save|save_problem_success|problem_graded|showanswer|problem_check|problem_show)'
t_TIMESTAMP = r'[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])T(2[0-3]|[01][0-9]):[0-5][0-9]:[0-5][0-9].[0-9]{6}(\+|-)(2[0-3]|[01][0-9]):[0-5][0-9]'
t_EXIT = r'page_close|null'
t_FORUM = r'edx.forum.thread.created|discussion'
t_ODD = r'(58dc5075b29a4479964195d35aff3e34|c560da3cea8c4414b3d0bb0250e7a52d|054968ecd9fe42ae80d7fc5e5054e37c|ebbe69dcda76411f97524f328bae8895|edx.course.enrollment.activated)'

def t_error(t):
    print("Invalid Token: ", t.value)
    t.lexer.skip(1)


lexer = lex.lex()
#lexer.input(parser_input)


def p_PAGENAV( p ) :
    'expr : PAGENAV expr'
    p[0] = "PAGENAV " + p[2]

def p_VIDEOINTERACT(p):
    'expr : VIDEOINTERACT expr'
    p[0] =  p[2]

def p_VIDEO(p):
    'expr : VIDEOSTART p_VIDEOINTERACT VIDEOSTOP expr'
    p[0] = "VIDEO " + p[2] + p[4]
    
def p_VIDEO_STARTONLY(p):
    'expr : VIDEOSTART expr'
    p[0] =  "VIDEO " + p[2]
    
def p_WIKIACCESS(p):
    'expr : WIKIACCESS expr'
    p[0] = "WIKI_ACCESS " + p[2]

def p_COURSEWAREACCESS(p):
    'expr : COURSEWAREACCESS expr'
    p[0] = "COURSEWAREACCESS " + p[2]


def p_PROBLEMSAVE(p):
    'expr : PROBLEMSAVE expr'
    p[0] = "PROBLEMSAVE " + p[2]

def p_TIMESTAMP(p):
    'expr : TIMESTAMP expr'
    p[0] = "TIMESTAMP " + p[2]

def p_EXIT(p):
    'expr : EXIT expr'
    p[0] = "EXIT " + p[2]

def p_FORUM(p):
    'expr : FORUM expr'
    p[0] = "FORUM " + p[2]

def p_ODD(p):
    'expr : ODD expr'
    p[0] = p[2]

def p_error(p):
    print("Syntax error at '%s'" % p.value)



def p_single_WIKIACCESS(p):
    'expr : WIKIACCESS      '
    p[0] = "WIKIACCESS "
def p_single_COURSEWAREACCESS(p):
    'expr : COURSEWAREACCESS'
    p[0] = "COURSEWAREACCESS "
def p_single_VIDEOSTART(p):
    'expr : VIDEOSTART'
    p[0] = "VIDEOSTART "
def p_single_VIDEOINTERACT(p):
    'expr : VIDEOINTERACT'
    p[0] = "VIDEOINTERACT "
def p_single_VIDEOSTOP(p):
    'expr : VIDEOSTOP'
    p[0] = "VIDEOSTOP "
def p_single_PAGENAV(p):
    'expr : PAGENAV'
    p[0] = "PAGENAV "
def p_single_PROBLEMSAVE(p):
    'expr : PROBLEMSAVE     '
    p[0] = "PROBLEMSAVE "
def p_single_TIMESTAMP(p):
    'expr : TIMESTAMP'
    p[0] = "TIMESTAMP "
def p_single_EXIT(p):
    'expr : EXIT'
    p[0] = "EXIT "
def p_single_FORUM(p):
    'expr : FORUM'
    p[0] = "FORUM "
def p_single_ODD(p):
    'expr : ODD'
    p[0] = null


parser = yacc.yacc()

# res = parser.parse(parser_input) # the input
# print(res)
print(parser.parse(parser_input_user1055391))
print(parser.parse(parser_input_user617997))
print(parser.parse(parser_input_user7214527))
print(parser.parse(parser_input_user7206957))
