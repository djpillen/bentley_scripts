import re

string = 'j. m. e. title title title.'
initials = re.compile('\w{1}\.\s\w{1}\.')

if initials.match(string):
    string = re.sub('(?<!\w{2})\.(?=\s\w{2,})', '', string)
    string = re.sub('((?<=[\s\b]\w{1})|(?<=^\w{1}))\.\s(?=\w{1}[\s\.])', '', string)
    print string