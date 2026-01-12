import unittest
from unittest.mock import MagicMock, patch
from src.crew.research_crew import ResearchCrew

class TestResearchCrew(unittest.TestCase):

    @patch('src.crew.research_crew.Crew')
    @patch('src.crew.research_crew.Task')
    @patch('src.crew.research_crew.create_researcher_agent')
    @patch('src.crew.research_crew.create_analyst_agent')
    @patch('src.crew.research_crew.create_writer_agent')
    @patch('src.crew.research_crew.create_critic_agent')
    @patch('src.crew.research_crew.create_coordinator_agent')
    def test_run_crew(self, mock_coord, mock_critic, mock_writer, mock_analyst, mock_researcher, mock_task, mock_crew_cls):
        # Setup mocks
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "Research Report Content"
        mock_crew_cls.return_value = mock_crew_instance

        # Execute
        crew = ResearchCrew("Solar Energy")
        result = crew.run()

        # Assert
        self.assertEqual(result, "Research Report Content")
        mock_crew_cls.assert_called_once()
        mock_researcher.assert_called_once()
        mock_analyst.assert_called_once()
        mock_writer.assert_called_once()
        mock_critic.assert_called_once()
        mock_coord.assert_called_once()

if __name__ == '__main__':
    unittest.main()
