
class Parser:

  ##### Parser header #####
  def __init__(self, scanner):
    self.next_token = scanner.next_token
    self.token = self.next_token()
    self.used_tokens = []
    self.indentations_index = 0
    self.indentations_counter = 0
    self.indentations_list = []

  def take_token(self, token_type):
    if self.token.type != token_type:
      self.error("Unexpected token: %s" % token_type)
    if token_type != 'EOF':
      self.token = self.next_token()

  def error(self,msg):
    raise RuntimeError('Parser error, %s' % msg)

  ##### Parser body #####

  # Starting symbol
  def start(self):
    # start -> program EOF
    if self.token.type == 'version' or self.token.type == 'SERVICES' or self.token.type == 'SPACE' or self.token.type == 'NEWLINE':
      self.program()
      self.take_token('EOF')
    else:
      self.error("\'%s\' not allowed at the beginning" % self.token.type)

  def program(self):
    # program -> statement program
    if self.token.type != 'EOF':
      self.indentations()
      self.program()
    # program -> eps
    else:
      pass

# check begin indentation
  def indentations(self):
    if self.token.type == 'NEWLINE':
      self.take_token('NEWLINE')
    elif self.token.type == 'SPACE':
      self.take_token('SPACE')
      self.indentations_counter += 1
      self.indentations()
    else:
      self.indentations_list.append(self.indentations_counter)
      self.indentations_counter = 0
      self.statement()

  def statement(self):
    # statement -> print_stmt
    if self.token.type not in self.used_tokens: 
      if self.token.type == 'version':
        self.used_tokens.append(self.token.type)
        self.prod_version()
      else:
        self.error("\'%s\' not allowed" % self.token.type)
    else:
      self.error('\'%s\' already exists' % self.token.type)

  # prod_version -> VERSION COLON value NEWLINE
  def prod_version(self):
    if self.token.type == 'version':
      self.take_token('version')
      self.take_token('COLON')
      self.check_separator()
      self.value()
      # self.take_token('END')
      print "version statement OK"
    else:
      self.error("Epsilon not allowed")

# check separator after COLON token
  def check_separator(self):
    if self.token.type == 'SPACE':
      self.take_token('SPACE')
      self.check_separator()
    elif self.token.type == 'NEWLINE':
      self.newline_skipper(None)
    else:
      pass

# skip all new lines and check indentations
  def newline_skipper(self, fnc):
    if self.token.type == 'NEWLINE':
      self.take_token('NEWLINE')
      self.indentations_counter = 0
      self.newline_skipper(None)
  
    if fnc is None:
      self.indentations_checker()
    else:
      fnc()

# check indentations after COLON
  def indentations_checker(self):
    if self.token.type == 'SPACE':
      self.take_token('SPACE')
      self.indentations_counter += 1
      self.indentations_checker()
    elif self.token.type != 'NEWLINE':
      self.check_indentations()
    else:
      self.newline_skipper(None)

# check indentations value
  def check_indentations(self):
    if self.indentations_counter >= (self.indentations_list[self.indentations_index] + 1):
      pass
    else:
      self.error('indentation is too short')
  
  def value(self):
      # value -> NUMBER
      if self.token.type == 'NUMBER':
        self.take_token('NUMBER')
      # value -> ID
      elif self.token.type == 'ID':
        self.take_token('ID')
      # value -> BOOLEAN
      elif self.token.type == 'BOOLEAN':
        self.take_token('BOOLEAN')
      # value -> STRING
      elif self.token.type == 'STRING':
        self.take_token('STRING')
      # value -> VERSION_VAL
      elif self.token.type == 'VERSION_VAL':
        self.take_token('VERSION_VAL')
      # value -> PORTS_VAL
      elif self.token.type == 'PORTS_VAL':
        self.take_token('PORTS_VAL')
      
      elif self.token.type == 'SPACE':
        self.take_token('SPACE')
        self.value()
      else:
        self.error("Epsilon not allowed")

  def if_stmt(self):
    # if_stmt -> IF ID THEN program ENDIF END
    if self.token.type == 'IF':
      self.take_token('IF')
      self.take_token('ID')
      self.take_token('THEN')
      self.program()
      self.take_token('ENDIF')
      self.take_token('END')
      print "if_stmt OK"
    else:
      self.error("Epsilon not allowed")
       
