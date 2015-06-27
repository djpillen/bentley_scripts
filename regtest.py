import re

string = 'j. m. e. title title title.'
initials = re.compile(r'\w{1}\.\s\w{1}\.')

if initials.match(string):
    string = re.sub(r'(?<!\w{2})\.(?=\s\w{2,})', '', string)
    string = re.sub(r'((?<=[\s\b]\w{1})|(?<=^\w{1}))\.\s(?=\w{1}[\s\.])', '', string)
    print string
