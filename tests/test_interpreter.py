import unittest
from doublex import *

import boscli
from boscli import exceptions

# Initial tests:
# Eval empty line
# Eval line matching a command

IRRELEVANT_LINE = 'irrelevant_line'
IRRELEVANT_RESULT = 'irrelevant_result'

class InterpreterTest(unittest.TestCase):
	def setUp(self):
		self.interpreter = boscli.Interpreter()

	def test_exception_raised_when_evaluating_a_line_not_matching_any_command(self):
		self.assertRaises(exceptions.NotMatchingCommandFound, self.interpreter.eval, IRRELEVANT_LINE)

	def test_execute_the_command_when_match_found(self):
		with Spy() as command:
			command.match(IRRELEVANT_LINE).returns(True)
			command.execute(ANY_ARG).returns(IRRELEVANT_RESULT)

		self.interpreter.add_command(command)
			
		command_return_value = self.interpreter.eval(IRRELEVANT_LINE)
		
		assert_that(command.execute, called().with_args(line=IRRELEVANT_LINE, interpreter=self.interpreter))
		assert_that(command_return_value, is_(IRRELEVANT_RESULT))
