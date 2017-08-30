import pandas as pd
import re

print('Reading data')
df=pd.read_csv('data.csv')

print('Reading template')
with open('template.html') as f:
    lines = f.read()

rowno = 0

def replace_special(input):
    return input.replace('&', '&amp;')

def square_replace(match):
    match = match.group()
    com = match.strip("[]")
    if com[:1]!="#":
        return match
    for x in re.findall(regexcaret, match):
        if df[x][rowno] == 1:
            if len(re.findall(regexdollar, match)) > 0:
                print(x, ' == true -- ', re.findall(regexdollar, match)[0])
                return re.findall(regexdollar, match)[0]
        elif df[x][rowno] == 0:
            if len(re.findall(regexnotdollar, match)) > 0:
                print(x, ' == false -- ', re.findall(regexnotdollar, match)[0])
                return re.findall(regexnotdollar, match)[0]

    print(match, " -- no match")
    return ""

def curl_replace(match):
    match = match.group()
    col = match.strip("{}")
    if col in df.columns:
        if 'file=' in df[col][rowno]:
            print ('Inserting file', df[col][rowno][5:])
            with open(df[col][rowno][5:]) as fl:
                temp = fl.read()
            return re.sub(regexcurl,curl_replace,temp)
        print (match, ' -- ', df[col][rowno])
        if df[col][rowno][:4] == 'http':
            print('Detected http link')
            return replace_special(df[col][rowno])
        return df[col][rowno]
    else:
        return match
    
regexsquare = r"\[(.*?)\]"
regexcurl = r"{{([^}]+)}}"
regexcaret = r"\^\^([^}]+)\^\^"
regexdollar = r"\$\$(.*?)\$\$"
regexnotdollar = r"\$!(.*?)!\$"

for index,row in df.iterrows():
    rowno = index
    filename = '../' + row['os_abbr'] + '/' + row['code_name'] + '.html'
    print(' ------------ Now working on ', filename, '------------')
    f = open(filename, 'w')
    square_processed = re.sub(regexsquare,square_replace,lines)
    f.write(re.sub(regexcurl,curl_replace,square_processed))
    f.close()
print('Everything done')