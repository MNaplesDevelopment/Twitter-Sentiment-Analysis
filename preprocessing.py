import pickle
from nltk.stem import WordNetLemmatizer
import re
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

lemmatizer = WordNetLemmatizer()

# print('loading embs...')
# with open('test1_public.txt', 'r') as handle:
#     embeddings = handle.readlines()
# embs = {}
# for line in embeddings:
#     split = line.split()
#     word = split[0]
#     embs[word] = 0

print('Reading words...')
f = open("test2_public.txt", 'r')
lines = f.readlines()
f.close()
# line = lines[1].split()[2:]
# print(lines[1].split()[2:])
missing = 0

symbols = ['[', ']', '(', ')', '{', '}', ':', ';', '-', '_', '`', '&', '?', '!', '.', ',', "'", '"', '*']
junk = ['&quot', '&lt', '$', '&amp', '&gt']
happy = [':)', ';)', ':d', ':]', 'c:', '(:', '^^']
sad = [':(', ';(', ':[', ' d:', ':c', ':x', '):', '-_-']
arr = []
label = []
out = open('words2.txt', 'w+')
for n, line in enumerate(lines):
    label.append(line.split()[0])
    # if len(line.split()) < 2: continue
    # if line.split()[1] == '-':
    #     label.append(0)
    # elif line.split()[1] == '+':
    #     label.append(1)
    # else: continue
    line = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", '<url>', line)
    line = re.sub(r'[0-9]{1,2}:[0-9]{2}\W*(?i)(AM|PM)', '<time>', line)
    line = re.sub(r'[0-9]{1,2}[0-9]{2}\W*(?i)(AM|PM)', '<time>', line)
    line = re.sub(r'[0-9]{1,2}\W*(?i)(AM|PM)', '<time>', line)
    line = re.sub(r'(\d)+\.(\d)+', '<number>', line)
    line = re.sub(r'(\d)+', '<number>', line)
    line = line.replace('/', ' or ')
    line = line.replace('=', ' ')
    #line = line.split()[2:]
    line = line.split()[1:]
    for i in range(len(line)):
        line[i] = line[i].lower().strip()
        line[i] = line[i].replace('&gt', '')
        if line[i].startswith('www') and line[i].endswith('com'):
            line[i] = '<url>'
        if line[i].startswith('@'):
            line[i] = '<user>'
        if line[i].startswith('#'):
            line[i] = '<hashtag>'
        for symbol in happy:
            line[i] = line[i].replace(symbol, ' <smile> ')
        for symbol in sad:
            line[i] = line[i].replace(symbol, ' <sadface> ')
        for j in junk:
            line[i] = line[i].replace(j, '')
        for symbol in symbols:
            line[i] = line[i].replace(symbol, ' ' + symbol + ' ')
        for x in ['<number>', '<time>']:
            if x in line[i]:
                line[i] = x
        if len(line[i]) > 3:
            if line[i][-1] == line[i][-2] == line[i][-3]:
                while line[i][-1] == line[i][-2] and len(line[i]) > 3:
                    line[i] = line[i][:-1]
        # if line[i].strip() not in embs and '<' not in line[i] and line[i]:
        #     missing += 1
        #line[i] = lemmatizer.lemmatize(line[i])
    lineout = ''.join(x.strip() + ' ' for x in line if x)
    out.write(lineout + '\n')
    arr.append([x.strip() for x in line if x])
    if (n+1) % 50000 == 0:
        print(f'{n+1}/{len(lines)}')
        print(f'Missing: {missing}\n')

out.close()

# with open('training.pkl', 'wb') as f:
#     pickle.dump(arr, f, protocol=pickle.HIGHEST_PROTOCOL)
# with open('labels.pkl', 'wb') as f:
#     pickle.dump(label, f, protocol=pickle.HIGHEST_PROTOCOL)

with open('test2.pkl', 'wb') as f:
    pickle.dump(arr, f, protocol=pickle.HIGHEST_PROTOCOL)
with open('labels2.pkl', 'wb') as f:
    pickle.dump(label, f, protocol=pickle.HIGHEST_PROTOCOL)
