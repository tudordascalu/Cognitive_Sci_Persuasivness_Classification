# -*- coding: utf-8 -*-
"""Cog_Sci_Exam_Start

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hib_YZ2tTG6un1Is6bMudKOQcQLM-6d1
"""

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import StratifiedKFold, KFold, train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, ExtraTreesClassifier, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error
from sklearn.feature_selection import SelectKBest, chi2, f_regression
from sklearn.svm import SVC

# Libraries for loading data
import h5py
import pathlib

# Text proccessing
import re
import nltk  
nltk.download('stopwords')
from nltk.corpus import stopwords

# X_text, X_audio, y data is not algined
movies_indices = ['100178', '100232', '100367', '100446', '100499', '100961', '10124', '101513', '101635', '101708', '101787', '101851', '101880', '102168', '102184', '10219', '102213', '10223', '102389', '102408', '102424', '102534', '102858', '103114', '103311', '10397', '104739', '104741', '105507', '105537', '105553', '105906', '105963', '106037', '106077', '106514', '106941', '106973', '107182', '107456', '107551', '107585', '108146', '108793', '109524', '109909', '110003', '110203', '110543', '110565', '110690', '110754', '110766', '110788', '110794', '110824', '110983', '111104', '111363', '111734', '111881', '112029', '112148', '112169', '112172', '112223', '112425', '112433', '112509', '112604', '112631', '112674', '112903', '113162', '113265', '113369', '113491', '114006', '114016', '114419', '114624', '114845', '115134', '116202', '116213', '116219', '116221', '116461', '116481', '11650', '118354', '118371', '118573', '118583', '118639', '119348', '119397', '120342', '120363', '121117', '121128', '121358', '121400', '121427', '121584', '121759', '122439', '122581', '122602', '122842', '123986', '124190', '125344', '125676', '125708', '125726', '125730', '125845', '125868', '125895', '126505', '126542', '126831', '126872', '127470', '127490', '127539', '127622', '127908', '128059', '12812', '128258', '128600', '128752', '128763', '128949', '129728', '129733', '130149', '130366', '130426', '130448', '130456', '130633', '131650', '131871', '131936', '132028', '132476', '132570', '133201', '133888', '134252', '134298', '135623', '135658', '136196', '136205', '136211', '136215', '136234', '136416', '136647', '137455', '137827', '137920', '139006', '139032', '140293', '140315', '140317', '15138', '154449', '15837', '16145', '16530', '167521', '172044', '172048', '172050', '172060', '17622', '176266', '17769', '178163', '17874', '179797', '179875', '180923', '180971', '181504', '181978', '183364', '184784', '186631', '186643', '187033', '187566', '187775', '188004', '188062', '188122', '188343', '188815', '188825', '18938', '189966', '190599', '190726', '190740', '190743', '191616', '191941', '192799', '192978', '193093', '193291', '193322', '193514', '193894', '193921', '193924', '194299', '194625', '195575', '19573', '19664', '196665', '197232', '197778', '198112', '19850', '19915', '199215', '199227', '200941', '201005', '201497', '201582', '201980', '202431', '202810', '202826', '202990', '203466', '203806', '204085', '204378', '204519', '204792', '205268', '206049', '206051', '206148', '206179', '206376', '206507', '206585', '206606', '206621', '207118', '207812', '207867', '207958', '207964', '207977', '208148', '208299', '208322', '208416', '208465', '208592', '209354', '209758', '209775', '209869', '210098', '210238', '210240', '210259', '210433', '210555', '210618', '21137', '211611', '211875', '212532', '21285', '213207', '213327', '213619', '214095', '215259', '215318', '215343', '216007', '216030', '216097', '21638', '216831', '216857', '21696', '21727', '21735', '217395', '21844', '218708', '218757', '218912', '219310', '219350', '219460', '219600', '219605', '219614', '219775', '220134', '220200', '220548', '220809', '221104', '221137', '221153', '221274', '221740', '222116', '222247', '222510', '222605', '22277', '22305', '223333', '223338', '22335', '223377', '223431', '22344', '22360', '22373', '223883', '223885', '223926', '224263', '224292', '224325', '224370', '224472', '224498', '224599', '224622', '224631', '224648', '224649', '224772', '224817', '224869', '225343', '225416', '225768', '225770', '22649', '226601', '226602', '226640', '22689', '227173', '22719', '227416', '227426', '227556', '22785', '22798', '22821', '228561', '22880', '228925', '22901', '229090', '229296', '229808', '229903', '229967', '230252', '230422', '230692', '231025', '231412', '231453', '232464', '23289', '233171', '233356', '233366', '233389', '23343', '233880', '233939', '234046', '234053', '234406', '234587', '234641', '236021', '236306', '236399', '236442', '23656', '236696', '237009', '237363', '238023', '238039', '238060', '238063', '238100', '238567', '238624', '238645', '238683', '238858', '238889', '239180', '239235', '239242', '239572', '240915', '241124', '241164', '241172', '241178', '24157', '241629', '241638', '24196', '24202', '243056', '243338', '243341', '24351', '243646', '243797', '243981', '244180', '244261', '244623', '244817', '244829', '244836', '24504', '24508', '245207', '245243', '245276', '245322', '245497', '245582', '245926', '24602', '246216', '247108', '247318', '247382', '247538', '247764', '248024', '24814', '248400', '248837', '250430', '251417', '251646', '251826', '251839', '252097', '252177', '25271', '252912', '252919', '252998', '253709', '254298', '254427', '255205', '25522', '255224', '255226', '255338', '255343', '255408', '255852', '256174', '25640', '256935', '256976', '257045', '257247', '257277', '257531', '257534', '257771', '258654', '258672', '258802', '259260', '259470', '260011', '260199', '26110', '26113', '26115', '261267', '261326', '261900', '261902', '262165', '262226', '262341', '263444', '263889', '264418', '264446', '265302', '265811', '265959', '266366', '266396', '266791', '266852', '266861', '26690', '266938', '267092', '267252', '267255', '267278', '267354', '267466', '267694', '267799', '26808', '268258', '268536', '268836', '270254', '270416', '270439', '270444', '270449', '270628', '270665', '270956', '270993', '271366', '271594', '271598', '272375', '272624', '272817', '272838', '273032', '273171', '273207', '273237', '273250', '273314', '273510', '273531', '273539', '274073', '274185', '274219', '274917', '275248', '275267', '275603', '275620', '276217', '27798', '277991', '278474', '27857', '27863', '279373', '28006', '280584', '280794', '280951', '28142', '28182', '28191', '282560', '282586', '282985', '283495', '283935', '284673', '286943', '288714', '288766', '290062', '290088', '29044', '290546', '291121', '292277', '294178', '294226', '295793', '29751', '29758', '29771', '298459', '298736', '298774', '29920', '299754', '301320', '301321', '30162', '30171', '302220', '30646', '306700', '30762', '30763', '30858', '31197', '31392', '31474', '31544', '323217', '32459', '32681', '327282', '327283', '33089', '33170', '33272', '33312', '33436', '33439', '341382', '341763', '341983', '342197', '342407', '34346', '34640', '34684', '34984', '34989', '35684', '35694', '35934', '36098', '36116', '36164', '367506', '367576', '368460', '370050', '370404', '37117', '37459', '38019', '38154', '38374', '38387', '40129', '40181', '40247', '40260', '40266', '40970', '41026', '41032', '41381', '41692', '42426', '42946', '43342', '43371', '43444', '43456', '43469', '44457', '44780', '45175', '45184', '45186', '45676', '45860', '46495', '46497', '46503', '46604', '46615', '46618', '46663', '46860', '47472', '47797', '47939', '48019', '48300', '48724', '49029', '49073', '49264', '49358', '49417', '49903', '50103', '50302', '50306', '50307', '50444', '50453', '50478', '50479', '51224', '52067', '52068', '52160', '52839', '535523', '53609', '53742', '53766', '55156', '56006', '56276', '56853', '56989', '57231', '57294', '57295', '57598', '57618', '58096', '58097', '58151', '58554', '58795', '59302', '59333', '59673', '59712', '60037', '60405', '60428', '61277', '61531', '61557', '62438', '63841', '63951', '63956', '65068', '65939', '66505', '66623', '68828', '69234', '69268', '69707', '69824', '69870', '70280', '70299', '70420', '70710', '71459', '7155', '7156', '71736', '71987', '72017', '72385', '73360', '73447', '73449', '74101', '74184', '74447', '74532', '74870', '75393', '75441', '75892', '75938', '76104', '76124', '78398', '78577', '78752', '79203', '79356', '79644', '79858', '79925', '79934', '79935', '80566', '80620', '80627', '80855', '80866', '80914', '81371', '81406', '81538', '81563', '81615', '81668', '81707', '82666', '83119', '83310', '83400', '83859', '8404', '84133', '84140', '84176', '84670', '84772', '84924', '86494', '87161', '87163', '87400', '87434', '88077', '88119', '88245', '88791', '88792', '88797', '88881', '88888', '89184', '89266', '89747', '89787', '89835', '89951', '90008', '90172', '90396', '90667', '90986', '91166', '91276', '91292', '91574', '91844', '91996', '92221', '92291', '92331', '92496', '92521', '92533', '92578', '93116', '93119', '93807', '93821', '93828', '93839', '93843', '94215', '94439', '94481', '94525', '94532', '94983', '95147', '95205', '95388', '95887', '96099', '96179', '96194', '96337', '96350', '96361', '96642', '96694', '96700', '97076', '97095', '97289', '97908', '97992', '98155', '98187', '98442', '98505', '98562', '99331', '99501']

# # This is how data comes in
# y_file = {'100178': [....], '100232': [....], '100367': [....]}
# X_text_file = {'100232': [....], '100178': [....], '100367': [....]}
# X_audio_file = {'100367': [....], '100232': [....], '100178': [....]}

# # This is how we proccess it
# y = []
# for i in movies_indices:
#   y.append(y_file[i])
#   X_text.append(X_text_file[i])

"""# Text Download
We download pre-proccessed data from CMU-Multimodal-SDK.
"""

data_root = '.'
tf.keras.utils.get_file('y_pers', 'http://immortal.multicomp.cs.cmu.edu/POM/labels/POM_Labels_Video_Level_Persuasion.csd', cache_dir=data_root)
# tf.keras.utils.get_file('y_sentiment', 'http://immortal.multicomp.cs.cmu.edu/POM/labels/POM_Labels_Video_Level_Sentiment.csd', cache_dir=data_root)
# tf.keras.utils.get_file('y_traits', 'http://immortal.multicomp.cs.cmu.edu/POM/labels/POM_Labels_Video_Level_Personality_Traits.csd', cache_dir=data_root)
tf.keras.utils.get_file('X_words', 'http://immortal.multicomp.cs.cmu.edu/POM/language/POM_TimestampedWords.csd', cache_dir=data_root)
tf.keras.utils.get_file('X_word_vecs', 'http://immortal.multicomp.cs.cmu.edu/POM/language/POM_TimestampedWordVectors.csd', cache_dir=data_root)
tf.keras.utils.get_file('X_sound', 'http://immortal.multicomp.cs.cmu.edu/POM/acoustic/POM_COVAREP.csd', cache_dir=data_root)

"""# Text Proccessing
1. Extract data from files.
2. Concatenate & clean where necessary (Text)
"""

def extract_data(data_name, file_path, concat_feat=False):
  """
  Arguments:
    data_name: name of the data to be extracted
    file_path: path to file
    concat_feat: concat words for text data
  Returns:
    numpy array with the data from the file
  """
  with h5py.File(file_path, 'r') as hf:
    data = []
    print(hf.keys())
    for i in movies_indices:
      to_append = hf[data_name]['data'][i]['features'][:]
      if (concat_feat):
        to_append = np.array2string(np.concatenate(to_append))
      data.append(to_append)
  return np.array(data)

def clean_text(text):
  """
  Arguments: 
    text: text to be parsed
  Returns
    text without special characters
  """
  text = re.sub(r"\n", " ", text)
  text = re.sub(r"sp", " ", text)
  text = text.lower()
  text = re.sub(r"[^a-z ]", " ", text) # remove everything expect a-z
  text = re.sub(r"\b\w{1,1}\b", " ",text) # remove everything of length 1
  text = " ".join([x for x in text.split()])
  return text

y_pers = extract_data('video level persuasion', './datasets/y_pers').squeeze() # persuasivness labels
# y_traits = extract_data('video level personality traits', './datasets/y_traits').squeeze() # personality labels
# y_sentiment = extract_data('video level sentiment', './datasets/y_sentiment').squeeze() # sentiment polarity labels
X_text = extract_data('words', './datasets/X_words', concat_feat=True) # not clean text
X_text = np.vectorize(clean_text)(X_text) # clean text
X_word_vecs = extract_data('glove_vectors', './datasets/X_word_vecs') # glove word vectors
X_audio = extract_data('COAVAREP', './datasets/X_sound') # COVAREP audio features

print("X_text shape: {}".format(X_text.shape))
print("y_pers: {}".format(y_pers.shape))
# print("y_sentiment: {}".format(y_sentiment.shape))
print("X_text shape: {}".format(X_text.shape))
print("X_audio: {}".format(X_audio.shape))

# Binary split
# persuasive > 5 & persuasive < 3
pers_relevant_i = np.where((y_pers > 5) | (y_pers < 3))
X_text_pers = X_text[pers_relevant_i]
X_audio_pers = X_audio[pers_relevant_i]

y_binary_pers = y_pers[pers_relevant_i]
y_binary_pers[y_binary_pers < 3] = 0.0
y_binary_pers[y_binary_pers > 5] = 1.0

len(pers_relevant_i[0])

X_text[:10]

y_pers[:10]

"""# ML Models"""

def get_dense_model():
  """
  Returns:
    dense model for proccessing word2vec embeddings
  """
  embed_model = 'https://tfhub.dev/google/tf2-preview/nnlm-en-dim128/1'
  hub_layer = hub.KerasLayer(embed_model, output_shape=[128], input_shape=[], dtype=tf.string, trainable=True)

  model = tf.keras.Sequential()
  model.add(hub_layer)
  model.add(tf.keras.layers.Dense(64, activation=tf.keras.activations.relu))
  model.add(tf.keras.layers.Dropout(.4))
  model.add(tf.keras.layers.BatchNormalization())
  model.add(tf.keras.layers.Dense(32, activation=tf.keras.activations.relu))
  model.add(tf.keras.layers.Dense(1, activation=tf.keras.activations.linear))

  model.compile(optimizer='adam', loss='mse')
  return model

def get_dense_doc2vec_classifier():
  """
  Returns:
    dense model for proccessing word2vec embeddings
  """
  embed_model = 'https://tfhub.dev/google/tf2-preview/nnlm-en-dim128/1'
  hub_layer = hub.KerasLayer(embed_model, output_shape=[128], input_shape=[], dtype=tf.string, trainable=True)

  model = tf.keras.Sequential()
  model.add(hub_layer)
  model.add(tf.keras.layers.Dense(32, activation=tf.keras.activations.relu))
  model.add(tf.keras.layers.Dropout(.2))
  model.add(tf.keras.layers.Dense(32, activation=tf.keras.activations.relu))
  model.add(tf.keras.layers.Dense(1, activation=tf.keras.activations.linear))

  model.compile(optimizer='adam', loss='binary_crossentropy')
  return model

def get_dense_classifier(input_dim):
  """
  Arguments:
    input_dim: varies according to the number tfidf values
  Returns:
    NN dense model
  """
  model = tf.keras.Sequential()
  model.add(tf.keras.layers.Dense(32, input_shape=(input_dim,), activation='sigmoid'))
  model.add(tf.keras.layers.Dropout(0.2))
  model.add(tf.keras.layers.Dense(32,  activation='sigmoid'))
  model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

  model.compile(optimizer='adam', loss='binary_crossentropy')
  return model

def get_gradient_boosting_classifier(n_estimators=500):
  return GradientBoostingClassifier(n_estimators=n_estimators, random_state=42)

def get_gradient_boosting_regressor(n_estimators=500):
  return GradientBoostingRegressor(n_estimators=n_estimators, random_state=42)

def get_random_forest_classifier(n_estimators=500):
  return RandomForestClassifier(n_estimators=n_estimators, random_state=42)

def get_random_forest_regressor(n_estimators=100):
  return RandomForestRegressor(n_estimators=n_estimators, random_state=42)

def get_dummy_regressor(strategy='mean'):
  return DummyRegressor(strategy=strategy)

def get_dummy_classifier(strategy='most_frequent'):
  return DummyClassifier(strategy=strategy)

def get_svm_classifier(kernel='rbf'):
  return SVC(kernel=kernel)

"""# Baseline

## Baseline_Regressor
"""

kf = KFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text, y_pers):
  X_text_train, X_text_test = X_text[train_index], X_text[test_index]
  y_train, y_test = y_pers[train_index], y_pers[test_index]

  dummy = get_dummy_regressor()
  dummy.fit(X_text_train, y_train)

  y_pred = dummy.predict(X_text_test)
  mae = mean_absolute_error(y_test, y_pred)

  history.append(mae)
  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))

  print("Mean_Absolute_Error: {}".format(mae))
print("Mean_MAE: {}".format(np.mean(history)))

"""## Baseline_Classifier"""

kf = StratifiedKFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text_pers, y_binary_pers):
  X_text_train, X_text_test = X_text_pers[train_index], X_text_pers[test_index]
  y_train, y_test = y_binary_pers[train_index], y_binary_pers[test_index]

  dummy = get_dummy_classifier()
  dummy.fit(X_text_train, y_train)

  y_pred = dummy.predict(X_text_test)
  accuracy = accuracy_score(y_test, y_pred)

  history.append(accuracy)
  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))

  print("Accuracy: {}".format(accuracy))
print("Mean_Accuracy: {}".format(np.mean(history)))

"""# Doc2Vec embedding"""

kf = KFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text, y_pers):
  X_text_train, X_text_test = X_text[train_index], X_text[test_index]
  y_train, y_test = y_pers[train_index], y_pers[test_index]

  dense = get_dense_model()
  dense.fit(X_text_train, y_train, batch_size=32, epochs=50, verbose=1, validation_split=.1)
  
  y_pred = dense.predict(X_text_test)
  mae = mean_absolute_error(y_test, y_pred)
  
  history.append(mae)
  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))

  print("Mean_Absolute_Error: {}".format(mae))
print("Mean_MAE: {}".format(np.mean(history)))

kf = StratifiedKFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text_pers, y_binary_pers):
  X_text_train, X_text_test = X_text_pers[train_index], X_text_pers[test_index]
  y_train, y_test = y_binary_pers[train_index], y_binary_pers[test_index]

  dense = get_dense_doc2vec_classifier()
  dense.fit(X_text_train, y_train, batch_size=32, epochs=50, verbose=1, validation_split=.1)
  
  y_pred = dense.predict_classes(X_text_test)
  accuracy = accuracy_score(y_test, y_pred)
  
  history.append(accuracy)
  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))

  print("Accuracy: {}".format(accuracy))
print("Mean_Accuracy: {}".format(np.mean(history)))

"""# TFIDF embedding"""

def tfidf_features(text, training=True):
  """
  Arguments:
    text - string
    training - flag
  Returns:
    tfidf feature matrix
  """
  if training:
      x = tfidf.fit_transform(text)
  else:
      x = tfidf.transform(text)
  x = x.astype('float32')
  return x

def tfidf_features_best_plot(X_train, y_train, k=10):
  """
  Arguments:
    X_train - datasets
    y_train - labels
    k - number of features to plot
  Returns:
    plots data
  """ 

  chi2score = chi2(X_train, y_train)[0]
  plt.figure(figsize=(15,10))
  wscores = list(zip(tfidf.get_feature_names(), chi2score))
  wchi2 = sorted(wscores, key=lambda x:x[1])
  topchi2 = list(zip(*wchi2[-k:]))
  x = range(len(topchi2[1]))
  labels = topchi2[0]
  plt.barh(x,topchi2[1], align='center', alpha=0.2)
  plt.plot(topchi2[1], x, '-o', markersize=5, alpha=0.8)
  plt.yticks(x, labels)
  plt.xlabel('$\chi^2$')
  plt.show()

def tfidf_features_select(X_train, X_test, y_train, k=10):
  """
  Arguments:
    X - data
    y - labels
    n - number of features to select
  Returns:
    dataset containing n best features
  """
  # assume that a score higher than 3.5 indicates persuasivness in the content
  y_train_binary = np.zeros(y_train.shape)
  y_train_binary[y_train > 3.5] = 1.0 
  
  ch2 = SelectKBest(score_func=chi2, k=k)
  X_train = ch2.fit_transform(X_train, y_train_binary)
  X_test = ch2.transform(X_test)
  return X_train, X_test

"""## TFIDF_GB_Classification"""

kf = StratifiedKFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text_pers, y_binary_pers):
  X_text_train, X_text_test = X_text_pers[train_index], X_text_pers[test_index]
  y_train, y_test = y_binary_pers[train_index], y_binary_pers[test_index]

  tfidf = TfidfVectorizer(max_features=500, min_df=5, max_df=.7, ngram_range=(1,2), stop_words=stopwords.words('english'))
  X_text_train_tfidf = tfidf_features(X_text_train).todense()
  X_text_test_tfidf = tfidf_features(X_text_test, training=False).todense()

  gb = get_gradient_boosting_classifier(500)
  gb.fit(X_text_train_tfidf, y_train)
  
  y_pred = gb.predict(X_text_test_tfidf)
  accuracy = accuracy_score(y_test, y_pred)
  
  history.append(accuracy)
  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))

  print("Accuracy: {}".format(accuracy))
print("Mean_Accuracy: {}".format(np.mean(history)))

"""## TFIDF_RF_Classification"""

kf = StratifiedKFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text_pers, y_binary_pers):
  X_text_train, X_text_test = X_text_pers[train_index], X_text_pers[test_index]
  y_train, y_test = y_binary_pers[train_index], y_binary_pers[test_index]
  
  tfidf = TfidfVectorizer(max_features=450, min_df=5, max_df=.7, ngram_range=(1,1), stop_words=stopwords.words('english'))
  X_text_train_tfidf = tfidf_features(X_text_train).todense()
  X_text_test_tfidf = tfidf_features(X_text_test, training=False).todense()
  
  # tfidf_features_best_plot(X_text_train_tfidf, y_train, 15)

  rf = get_random_forest_classifier()
  rf.fit(X_text_train_tfidf, y_train)
  
  y_pred = rf.predict(X_text_test_tfidf)
  accuracy = accuracy_score(y_test, y_pred)
  
  history.append(accuracy)
  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))

  print("Accuracy: {}".format(accuracy))
print("Mean_Accuracy: {}".format(np.mean(history)))

"""## TFIDF_RF_Regression"""

kf = KFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text, y_pers):
  X_text_train, X_text_test = X_text[train_index], X_text[test_index]
  y_train, y_test = y_pers[train_index], y_pers[test_index]

  tfidf = TfidfVectorizer(max_features=500, min_df=5, max_df=.7, ngram_range=(1,1), stop_words=stopwords.words('english'))
  X_text_train_tfidf = tfidf_features(X_text_train).todense()
  X_text_test_tfidf = tfidf_features(X_text_test, training=False).todense()

  rf = get_random_forest_regressor()
  rf.fit(X_text_train_tfidf, y_train)
  
  y_pred = rf.predict(X_text_test_tfidf)
  mae = mean_absolute_error(y_test, y_pred)
  
  history.append(mae)
  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))

  print("Mean_Absolute_Error: {}".format(mae))
print("Mean_MAE: {}".format(np.mean(history)))

"""## TFIDF_Dense"""

kf = StratifiedKFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text_pers, y_binary_pers):
  X_text_train, X_text_test = X_text_pers[train_index], X_text_pers[test_index]
  y_train, y_test = y_binary_pers[train_index], y_binary_pers[test_index]

  tfidf = TfidfVectorizer(max_features=1000, min_df=5, max_df=.7, ngram_range=(1,1), stop_words=stopwords.words('english'))
  X_text_train_tfidf = tfidf_features(X_text_train).todense()
  X_text_test_tfidf = tfidf_features(X_text_test, training=False).todense()

  dense = get_dense_classifier(X_text_train_tfidf.shape[1])
  dense.fit(X_text_train_tfidf, y_train, epochs=100, batch_size=5, validation_split=.1, verbose=None)
  
  y_pred = dense.predict_classes(X_text_test_tfidf)
  accuracy = accuracy_score(y_test, y_pred)
  
  history.append(accuracy)
  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))

  print("Accuracy: {}".format(accuracy))
print("Mean_Accuracy: {}".format(np.mean(history)))

"""# Audio_Proccessing"""

def extract_audio_features(dataset):
  """
  Arguments
    dataset - array of time series per 10ms of audio ([[19, 193, 312 3,123 12, ....., 312312], [19, 193, 312 3,123 12, ....., 312312], [19, 193, 312 3,123 12, ....., 312312]])
  Returns
    (mean, std, max, min, skew) along time series for eatch data point
  """
  data_features = []
  for data in dataset:
    mean = np.nan_to_num(np.mean(data, axis=0))
    median = np.nan_to_num(np.median(data, axis=0))
    minimum = np.nan_to_num(np.min(data, axis=0))
    maximum = np.nan_to_num(np.max(data, axis=0))
    std = np.nan_to_num(np.std(data, axis=0))

    # min_max_range = maximum - minimum
    skew = np.nan_to_num(3 * (mean - median) / std)

    data_features.append([mean, median, std, minimum, maximum, skew])
  return np.array(data_features)

X_audio_feat = extract_audio_features(X_audio)
X_audio_feat = X_audio_feat.reshape(903, -1).astype(np.float32)
X_audio_feat_pers = X_audio_feat[pers_relevant_i]

"""## Audio_GB_Classification"""

kf = StratifiedKFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_audio_feat_pers, y_binary_pers):
  X_audio_train, X_audio_test =  X_audio_feat_pers[train_index], X_audio_feat_pers[test_index]
  y_train, y_test = y_binary_pers[train_index], y_binary_pers[test_index]

  gb = get_gradient_boosting_classifier()
  gb.fit(X_audio_train, y_train)
  
  y_pred = gb.predict(X_audio_test)
  accuracy = accuracy_score(y_test, y_pred)
  
  history.append(accuracy)
  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_audio_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_audio_test.shape, y_test.shape))

  print("Accuracy: {}".format(accuracy))
print("Mean_Accuracy: {}".format(np.mean(history)))

"""## Audio_RF_Classification"""

kf = KFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_audio_feat_pers, y_binary_pers):
  X_audio_train, X_audio_test =  X_audio_feat_pers[train_index], X_audio_feat_pers[test_index]
  y_train, y_test = y_binary_pers[train_index], y_binary_pers[test_index]

  rf = get_random_forest_classifier()
  rf.fit(X_audio_train, y_train)
  
  y_pred = rf.predict(X_audio_test)
  accuracy = accuracy_score(y_test, y_pred)
  
  history.append(accuracy)
  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_audio_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_audio_test.shape, y_test.shape))

  print("Mean_Absolute_Error: {}".format(accuracy))
print("Mean_MAE: {}".format(np.mean(history)))

"""## Audio_RF_Regression"""

kf = KFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text, y_pers):
  X_audio_train, X_audio_test =  X_audio_feat[train_index], X_audio_feat[test_index]
  y_train, y_test = y_pers[train_index], y_pers[test_index]

  rf = get_random_forest_regressor()
  rf.fit(X_audio_train, y_train)
  
  y_pred = rf.predict(X_audio_test)
  mae = mean_absolute_error(y_test, y_pred)
  
  history.append(mae)
  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))

  print("Mean_Absolute_Error: {}".format(mae))
print("Mean_MAE: {}".format(np.mean(history)))

"""## Audio_Dense"""

kf = StratifiedKFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_audio_feat_pers, y_binary_pers):
  X_audio_train, X_audio_test =  X_audio_feat_pers[train_index], X_audio_feat_pers[test_index]
  y_train, y_test = y_binary_pers[train_index], y_binary_pers[test_index]

  dense = get_dense_classifier(X_audio_train.shape[1])
  dense.fit(X_audio_train, y_train, epochs=100, batch_size=10, validation_split=.1, verbose=None)
  
  y_pred = dense.predict_classes(X_audio_test)
  accuracy = accuracy_score(y_test, y_pred)
  
  history.append(accuracy)
  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_audio_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_audio_test.shape, y_test.shape))

  print("Mean_Absolute_Error: {}".format(accuracy))
print("Mean_MAE: {}".format(np.mean(history)))

"""# Feature fusion

## Early

### GB_Classification
"""

kf = StratifiedKFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text_pers, y_binary_pers):
  y_train, y_test = y_binary_pers[train_index], y_binary_pers[test_index]
  X_text_train, X_text_test = X_text_pers[train_index], X_text_pers[test_index]
  X_audio_train, X_audio_test = X_audio_feat_pers[train_index], X_audio_feat_pers[test_index]

  tfidf = TfidfVectorizer(max_features=100, min_df=5, max_df=.9, stop_words=stopwords.words('english'))
  X_text_train_feat = tfidf_features(X_text_train).todense()
  X_text_test_feat = tfidf_features(X_text_test, training=False).todense()

  # Fuse features
  X_train = np.hstack((X_text_train_feat, X_audio_train))
  X_test = np.hstack((X_text_test_feat, X_audio_test))

  rf_model = get_gradient_boosting_classifier()
  rf_model.fit(X_train, y_train)

  y_pred = rf_model.predict(X_test)
  accuracy = accuracy_score(y_test, y_pred)
  history.append(accuracy)

  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))
  print("Accuracy: {}".format(accuracy))
print("Mean_Accuracy: {}".format(np.mean(history)))

"""### RF_Classification"""

kf = StratifiedKFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text_pers, y_binary_pers):
  y_train, y_test = y_binary_pers[train_index], y_binary_pers[test_index]
  X_text_train, X_text_test = X_text_pers[train_index], X_text_pers[test_index]
  X_audio_train, X_audio_test = X_audio_feat_pers[train_index], X_audio_feat_pers[test_index]

  tfidf = TfidfVectorizer(max_features=100, min_df=5, max_df=.9, stop_words=stopwords.words('english'))
  X_text_train_feat = tfidf_features(X_text_train).todense()
  X_text_test_feat = tfidf_features(X_text_test, training=False).todense()

  # Fuse features
  X_train = np.hstack((X_text_train_feat, X_audio_train))
  X_test = np.hstack((X_text_test_feat, X_audio_test))

  rf_model = get_random_forest_classifier()
  rf_model.fit(X_train, y_train)

  y_pred = rf_model.predict(X_test)
  accuracy = accuracy_score(y_test, y_pred)
  history.append(accuracy)

  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))
  print("Accuracy: {}".format(accuracy))
print("Mean_Accuracy: {}".format(np.mean(history)))

"""## Dense_Classification"""

kf = StratifiedKFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text_pers, y_binary_pers):
  y_train, y_test = y_binary_pers[train_index], y_binary_pers[test_index]
  X_text_train, X_text_test = X_text_pers[train_index], X_text_pers[test_index]
  X_audio_train, X_audio_test = X_audio_feat_pers[train_index], X_audio_feat_pers[test_index]

  tfidf = TfidfVectorizer(max_features=100, min_df=5, max_df=.9, stop_words=stopwords.words('english'))
  X_text_train_feat = tfidf_features(X_text_train).todense()
  X_text_test_feat = tfidf_features(X_text_test, training=False).todense()

  # Fuse features
  X_train = np.hstack((X_text_train_feat, X_audio_train))
  X_test = np.hstack((X_text_test_feat, X_audio_test))

  dense = get_dense_classifier(X_train.shape[1])
  dense.fit(X_train, y_train, epochs=100, batch_size=10, validation_split=.1, verbose=None)

  y_pred = dense.predict_classes(X_test)
  accuracy = accuracy_score(y_test, y_pred)
  history.append(accuracy)

  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))
  print("Accuracy: {}".format(accuracy))
print("Mean_Accuracy: {}".format(np.mean(history)))

"""### RF_Rgression"""

kf = KFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text, y_pers):
  y_train, y_test = y_pers[train_index], y_pers[test_index]
  X_text_train, X_text_test = X_text[train_index], X_text[test_index]
  X_audio_train, X_audio_test = X_audio_feat[train_index], X_audio_feat[test_index]

  tfidf = TfidfVectorizer(max_features=100, min_df=5, max_df=0.9, stop_words=stopwords.words('english'))
  X_text_train_feat = tfidf_features(X_text_train).todense()
  X_text_test_feat = tfidf_features(X_text_test, training=False).todense()

  # Fuse features
  X_train = np.hstack((X_text_train_feat, X_audio_train))
  X_test = np.hstack((X_text_test_feat, X_audio_test))

  rf_model = get_random_forest_regressor()
  rf_model.fit(X_train, y_train)

  y_pred = rf_model.predict(X_test)
  mae = mean_absolute_error(y_test, y_pred)
  history.append(mae)
  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))
  print("Mean_Absolute_Error: {}".format(mae))
print("Mean_MAE: {}".format(np.mean(history)))

"""## Late"""

def compute_proba_to_pred(y_1, y_2):
  """
  Arguments:
    y_1 - 1st model probabilities for classes
    y_2 - 2nd model probabilities for classes
  Returns:
    0, 1 classes according to probabilities
  """
  y_merged = (y_1 + y_2) / 2
  return np.argmax(y_merged, axis=1)

"""### GB_Classification"""

kf = StratifiedKFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text_pers, y_binary_pers):
  y_train, y_test = y_binary_pers[train_index], y_binary_pers[test_index]
  X_text_train, X_text_test = X_text_pers[train_index], X_text_pers[test_index]
  X_audio_train, X_audio_test = X_audio_feat_pers[train_index], X_audio_feat_pers[test_index]

  tfidf = TfidfVectorizer(max_features=100, min_df=5, max_df=0.9, stop_words=stopwords.words('english'))
  X_text_train_feat = tfidf_features(X_text_train).todense()
  X_text_test_feat = tfidf_features(X_text_test, training=False).todense()

  gb_text = get_gradient_boosting_classifier()
  gb_audio = get_gradient_boosting_classifier()

  gb_text.fit(X_text_train_feat, y_train)
  gb_audio.fit(X_audio_train, y_train)

  y_prob_text = gb_text.predict_proba(X_text_test_feat)
  y_prob_audio = gb_audio.predict_proba(X_audio_test)
  y_pred_text_audio = compute_proba_to_pred(y_prob_text, y_prob_audio)

  accuracy = accuracy_score(y_test, y_pred_text_audio)
  history.append(accuracy)

  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))
  print("Accuracy text and audio: {}".format(accuracy))
print("Mean_Accuracy: {}".format(np.mean(history)))

"""### RF_Classification"""

kf = StratifiedKFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text_pers, y_binary_pers):
  y_train, y_test = y_binary_pers[train_index], y_binary_pers[test_index]
  X_text_train, X_text_test = X_text_pers[train_index], X_text_pers[test_index]
  X_audio_train, X_audio_test = X_audio_feat_pers[train_index], X_audio_feat_pers[test_index]

  tfidf = TfidfVectorizer(max_features=500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
  X_text_train_feat = tfidf_features(X_text_train).todense()
  X_text_test_feat = tfidf_features(X_text_test, training=False).todense()

  rf_text = get_random_forest_classifier()
  rf_audio = get_random_forest_classifier()

  rf_text.fit(X_text_train_feat, y_train)
  rf_audio.fit(X_audio_train, y_train)

  y_prob_text = rf_text.predict_proba(X_text_test_feat)
  y_prob_audio = rf_audio.predict_proba(X_audio_test)
  y_pred_text_audio = compute_proba_to_pred(y_prob_text, y_prob_audio)

  accuracy = accuracy_score(y_test, y_pred_text_audio)
  history.append(accuracy)

  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))
  print("Accuracy text and audio: {}".format(accuracy))
print("Mean_Accuracy: {}".format(np.mean(history)))

"""### RF_Regression"""

kf = KFold(n_splits=5, shuffle=False)
history = []
for train_index, test_index in kf.split(X_text, y_pers):
  y_train, y_test = y_pers[train_index], y_pers[test_index]
  X_text_train, X_text_test = X_text[train_index], X_text[test_index]
  X_audio_train, X_audio_test = X_audio_feat[train_index], X_audio_feat[test_index]

  tfidf = TfidfVectorizer(max_features=100, min_df=5, max_df=0.9, stop_words=stopwords.words('english'))
  X_text_train_feat = tfidf_features(X_text_train).todense()
  X_text_test_feat = tfidf_features(X_text_test, training=False).todense()

  rf_text = get_random_forest_regressor()
  rf_audio = get_random_forest_regressor()

  rf_text.fit(X_text_train_feat, y_train)
  rf_audio.fit(X_audio_train, y_train)

  y_pred_text = rf_text.predict(X_text_test_feat)
  y_pred_audio = rf_audio.predict(X_audio_test)
  y_pred_text_audio = np.mean(np.vstack((y_pred_text, y_pred_audio)), axis=0)

  mae = mean_absolute_error(y_test, y_pred_text_audio)
  history.append(mae)
  print("Fold-------")
  print("X_text_train shape: {} | y_train shape: {}".format(X_text_train.shape, y_train.shape))
  print("X_text_test shape: {} | y_test shape: {}".format(X_text_test.shape, y_test.shape))

  print("MAE text: {}".format(mean_absolute_error(y_test, y_pred_text)))
  print("MAE audio: {}".format(mean_absolute_error(y_test, y_pred_audio)))
  print("MAE text and audio: {}".format(mae))
print("Mean_MAE: {}".format(np.mean(history)))