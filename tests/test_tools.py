import unittest
from unittest.mock import MagicMock
from src.utils import agent_logic

class TestAgentLogic(unittest.TestCase):

    def test_get_agent_display_name(self):
        self.assertEqual(agent_logic.get_agent_display_name("Senior Research Assistant"), "Investigador")
        self.assertEqual(agent_logic.get_agent_display_name("Unknown Agent"), "Agente")

    def test_detect_agent_role_explicit(self):
        step = MagicMock()
        role = "Senior Research Assistant"
        self.assertEqual(agent_logic.detect_agent_role(step, role), "Senior Research Assistant")

    def test_detect_agent_role_implicit(self):
        step = MagicMock()
        step.thought = "I need to search for information about this topic."
        self.assertEqual(agent_logic.detect_agent_role(step, None), "Senior Research Assistant")

        step.thought = "I will write a report based on the findings."
        self.assertEqual(agent_logic.detect_agent_role(step, None), "Senior Technical Writer")

if __name__ == '__main__':
    unittest.main()
