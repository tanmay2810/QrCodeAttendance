class category_index:
  def __init__(self,df):
    self.dataframe=df
    self.index_dict=dict()
    self.cat_list=[st.lower() for st in df['categoryName'].unique()]

  def get_cat_index(self,cat):
    cat_df=self.dataframe[self.dataframe['categoryName']==cat]
    #print(cat)
    return list(cat_df.index.values)

  def make_index(self):
    for cat in self.cat_list:
      self.index_dict[cat.lower()]=self.get_cat_index(cat)
      
  def get_cat_list(self):
    return self.cat_list




class state_index:
  def __init__(self,df):
    self.dataframe=df
    self.index_dict=dict()
    self.state_list=[st.lower() for st in df['state'].unique()]

  def get_st_index(self,st):
    st_df=self.dataframe[self.dataframe['state']==st]
    return list(st_df.index.values)

  def make_index(self):
    for st in self.state_list:
      self.index_dict[st.lower()]=self.get_st_index(st)

  def get_state_list(self):
    return self.state_list




class city_index:
  def __init__(self,df):
    self.dataframe=df
    self.index_dict=dict()
    self.city_list=[st.lower() for st in df['city'].unique()]

  def get_city_index(self,ct):
    ct_df=self.dataframe[self.dataframe['city']==ct]
    return list(ct_df.index.values)

  def make_index(self):
    for ct in self.city_list:
      self.index_dict[ct.lower()]=self.get_city_index(ct)

  def get_ct_list(self):
    return self.city_list



class MainIndex:
  def __init__(self):
    self.cat_i=None
    self.st_i=None
    self.city_i=None
    self.cross_index=dict()
    self.cross_list=list()

  def get_indices(self):
    fobj1=open('cat_index.pkl','rb')
    self.cat_i=pkl.load(fobj1)
    fobj1.close()
    fobj2=open('state_index.pkl','rb')
    self.st_i=pkl.load(fobj2)
    fobj2.close()
    fobj3=open('city_index.pkl','rb')
    self.city_i=pkl.load(fobj3)
    fobj3.close()

  def merger(self,cat,st='',ct=''):
    if len(ct)>0:
      l1=self.cat_i.get_cat_index(cat)
      l2=self.ct_i.get_ct_index(ct)
      fin_index=set(l1).intersection(set(l2))
      return list(fin_index)
    elif len(st)>0:
      l1=self.cross_index[cat]
      l2=self.cross_index[st]
      fin_index=set(l1).intersection(set(l2))
      return list(fin_index)
    else:
      return []

  def create_cross_index(self):
    self.get_indices()
    for cat in self.cat_i.get_cat_list():
        self.cross_index[cat]=list()
        self.cross_index[cat].extend(self.cat_i.get_cat_index(cat))
    for st in self.st_i.get_state_list():
      self.cross_index[st]=list()
      self.cross_index[st].extend(self.st_i.get_st_index(st))
    for city in self.city_i.get_ct_list():
        if city in self.st_i.get_state_list():
              self.cross_index[city].extend(self.city_i.get_city_index(city))
        else:
              self.cross_index[city]=list()
              self.cross_index[city].extend(self.city_i.get_city_index(city))
    for cat in self.cat_i.get_cat_list():
      for st in self.st_i.get_state_list():
        tup=tuple([cat,st])
        self.cross_index[tup]=self.merger(cat,st)
    for cat in self.cat_i.get_cat_list():
      for ct in self.city_i.get_ct_list():
        tup=tuple([cat,ct])
        self.cross_index[tup]=self.merger(cat,ct)

  def index_lookup(self,cat='',pl=''):
    if len(cat)>0:
      if len(pl)>0:
        tup=tuple([cat,pl])
        return self.cross_index[tup]
      else:
        return self.cross_index[cat]
    elif len(pl)>0:
      return self.cross_index[pl]
    else:
      return []


import nltk
import re
import pickle as pkl   
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words=list(stopwords.words("english"))

class Query_Processing:
  def __init__(self):
    self.cat_index=None
    self.state_index=None
    self.city_index=None
    self.cross_index = None
    self.res_df = None
    self.st_syn_dict = None
    self.cat_syn_dict = None
    self.bigram = []
  
  def get_indices(self):
    fobj1=open('cat_index.pkl','rb')
    self.cat_index=pkl.load(fobj1)
    fobj1.close()
    fobj2=open('state_index.pkl','rb')
    self.state_index=pkl.load(fobj2)
    fobj2.close()
    fobj3=open('city_index.pkl','rb')
    self.city_index=pkl.load(fobj3)
    fobj3.close()
    fobj4=open('synonym_cat_dict.pkl','rb')
    self.cat_syn_dict=pkl.load(fobj4)
    fobj4.close()
    fobj5=open('synonym_st_dict.pkl','rb')
    self.st_syn_dict=pkl.load(fobj5)
    fobj5.close()
    fobj6=open('cross_index.pkl','rb')
    self.cross_index=pkl.load(fobj6)
    fobj6.close()

  
  def preprocess_query(self,query):
    query = query.lower()                                        # converting the texts of query string into lowercase
    words = re.sub('[^\w\s\d]',' ',query)                        # removing non-alphanumeric and non-space characters from the query string
    tokens = nltk.word_tokenize(words)                           # tokenizing the modified query string
    words_list = [t for t in tokens if t not in stop_words]      # removing stopwords from the tokens obtained in last step
    for k in self.st_syn_dict.keys():
        for i in range(len(words_list)):
            if words_list[i] == k:
                words_list[i] = self.st_syn_dict[k]
    for k in self.cat_syn_dict.keys():
        for i in range(len(words_list)-1):
            if words_list[i] == k:
                words_list[i] = self.cat_syn_dict[k]
            else:
                key = ' '.join(words_list[i:i+2])
                if key == k:
                    print(self.cat_syn_dict[k])
                    words_list[i] = self.cat_syn_dict[k]
                    words_list[i+1] = ' '
    for k in self.cat_syn_dict.keys():
        if words_list[-1] == k:
            words_list[-1] = self.cat_syn_dict[k]
    words_list = [t for t in words_list if t!=' ']               # removing all blank-space tokens
    if(len(words_list)>10):                                      
      words_list = words_list[:10]
    return words_list


  def make_bigrams(self,words_list):
    index_dict = {word:i for i,word in enumerate(words_list)}
    categories, places, bigram = [],[],[]
    cat_list, city_list, state_list = self.cat_index.get_cat_list(), self.city_index.get_ct_list(), self.state_index.get_state_list()
    for w in words_list:
      if w in cat_list:
        categories.append([w,index_dict[w]])
    for i in range(len(words_list)-1):
        cat = ' '.join(words_list[i:i+2])
        if cat in cat_list:
          categories.append([cat,index_dict[words_list[i]]])
    for w in words_list:
      if w in city_list:
        places.append([w,index_dict[w]])
      elif w in state_list:
        places.append([w,index_dict[w]])
    for i in range(len(words_list)-1):
        plc = ' '.join(words_list[i:i+2])
        if plc in city_list:
          places.append([plc,index_dict[words_list[i]]])
        elif plc in state_list:
          places.append([plc,index_dict[words_list[i]]])
    categories.sort(key = lambda x: x[1])
    places.sort(key = lambda x: x[1])
    if len(categories) == len(places):
      for i in range(len(places)):
        self.bigram.append(tuple([categories[i][0],places[i][0]]))
    elif len(categories)>0 and len(places)>0:
        for i in range(len(categories)):
            for j in range(len(places)):
              tup = tuple([categories[i][0],places[j][0]])
              if tup in self.cross_index.cross_index:
                self.bigram.append(tup)
    elif len(categories)>0:
        for i in range(len(categories)):
            self.bigram.append(categories[i][0])
    elif len(places)>0:
        for i in range(len(places)):
            self.bigram.append(places[i][0])



  def query_processor(self,query):
    self.get_indices()
    words_list = self.preprocess_query(query)
    self.make_bigrams(words_list)
    res_indices = set()
    df = self.cat_index.dataframe
    for bg in self.bigram:
      if type(bg)==tuple():
          res = self.cross_index.index_lookup(bg[0],bg[1])
      else:
          res = self.cross_index.index_lookup(bg)
      res_indices = res_indices.union(res)
    if len(res_indices) > 0 :
      self.res_df = df.iloc[list(res_indices)]
    else:
      self.res_df = df
    self.res_df.drop(['categoryName','address','neighborhood','reviewsTags','totalScore'], axis=1, inplace=True)
    return self.res_df
  

q = Query_Processing()
query = input("Enter a search query : ")
res_df = q.query_processor(query)
res_df