import collections
import re

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

class Scanner:

  def __init__(self, input):
    self.tokens = []
    self.current_token_number = 0
    for token in self.tokenize(input):
	self.tokens.append(token)
 
  def tokenize(self, input_string):
    keywords = {'version', 'services', 'image', 'ports', 'networks', 'deploy', 'volumes', 'build', 'environment'}
    token_specification = [
        ('NUMBER',           r'[1-9][0-9]*\.?[0-9]*([Ee][+-]?[0-9]+)?'),     # number value
        ('BOOLEAN',          r'(true|false|yes|no|True|False|TRUE|FALSE)$'), # boolean value
        ('PORTS_VAL',      r'("([0-9]{2,5})+:([0-9]{2,5})")|(\'([0-9]{2,5})+:([0-9]{2,5})\')'),                                          
        ('VERSION_VAL',      r'(\"\d+(\.\d+)*\")|(\'\d+(\.\d+)*\')'),        # version value
        ('STRING',           r'\".*\"'),                                     # string value
        ('COLON',            r':'),                                          # colon  sign
        # ('SKIP',             r'[ \t]'),                                      # tab whitespace
        ('SPACE',            r'[ ]'),                                        # space
        ('NEWLINE',          r'\n'),                                         # new line
        ('LIST_VALUE',       r'-'),                                          # list element value
        ('TABLE_OPEN',       r'\['),                                         # table start
        ('TABLE_CLOSE',      r'\]'),                                         # table end
        ('PATH',             r'\..*[A-Za-z]'),                               # path
        ('NULL',             r'~'),    
        ('ID',               r'[a-zA-Z0-9_/]+-?[a-zA-Z0-9_/]+'),             # variable identifier
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex).match
    line_number = 1
    current_position = line_start = 0
    match = get_token(input_string)
    while match is not None:
        type = match.lastgroup
        if type == 'NEWLINE':
            line_start = current_position
            line_number += 1
        value = match.group(type)
        if type == 'ID' and value in keywords:
            type = value
        yield Token(type, value, line_number, match.start()-line_start)
        current_position = match.end()
        match = get_token(input_string, current_position)
    if current_position != len(input_string):
        raise RuntimeError('Error: Unexpected character %r on line %d' % \
                              (input_string[current_position], line_number))
    yield Token('EOF', '', line_number, current_position-line_start)

  def next_token(self):
    self.current_token_number += 1
    if self.current_token_number-1 < len(self.tokens):
      return self.tokens[self.current_token_number-1]
    else:
      raise RuntimeError('Error: No more tokens')

