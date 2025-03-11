import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional, List

from config import NOTION_TOKEN, NOTION_DATABASE_ID

class NotionAPI:
    """Handles all interactions with the Notion API for storing and retrieving goals."""
    
    def __init__(self):
        self.token = NOTION_TOKEN
        self.database_id = NOTION_DATABASE_ID
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.base_url = "https://api.notion.com/v1"
    
    def create_goal_page(self, title: str, goals: str, user_id: str = "User") -> str:
        """Create a new page in the Notion database with the goal information.
        
        Args:
            title: The title for the Notion page
            goals: The extracted goals from the conversation
            user_id: Identifier for the user
        
        Returns:
            URL to the created Notion page
        """
        try:
            # Format the current date
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Prepare the request payload
            payload = {
                "parent": {"database_id": self.database_id},
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": title + " - " + current_date
                                }
                            }
                        ]
                    },
                    "Role": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": "Life Goal"
                                }
                            }
                        ]
                    }
                },
                "children": [
                    # Introduction Section
                    self._create_heading_block(title, 1),
                    self._create_paragraph_block("These yearly goals were developed through a conversation with an AI assistant."),
                    
                    # Goals Section
                    self._create_heading_block("Goals", 2),
                    self._create_paragraph_block(goals),
                    
                    # Created date and user info
                    self._create_heading_block("Info", 3),
                    self._create_paragraph_block(f"Created on: {current_date}\nUser: {user_id}")
                ]
            }
            
            # Make the API request
            response = requests.post(
                f"{self.base_url}/pages",
                headers=self.headers,
                data=json.dumps(payload)
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Return the URL to the created page
            return self.get_page_url(result['id'])
            
        except Exception as e:
            print(f"Error creating Notion page: {e}")
            return None
    
    def get_page_url(self, page_id: str) -> str:
        """Get the URL for a Notion page.
        
        Args:
            page_id: The ID of the Notion page
            
        Returns:
            URL string for the Notion page
        """
        # Extract the page ID without any hyphens
        clean_id = page_id.replace("-", "")
        
        # Format the Notion URL
        return f"https://notion.so/{clean_id}"
    
    def _create_heading_block(self, text: str, level: int = 2) -> Dict[str, Any]:
        """Create a heading block for Notion page content.
        
        Args:
            text: The heading text
            level: Heading level (1-3)
            
        Returns:
            Dictionary representing a Notion heading block
        """
        heading_type = f"heading_{level}"
        return {
            "object": "block",
            "type": heading_type,
            heading_type: {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": text}
                    }
                ]
            }
        }
    
    def _create_paragraph_block(self, text: str) -> Dict[str, Any]:
        """Create a paragraph block for Notion page content.
        
        Args:
            text: The paragraph text
            
        Returns:
            Dictionary representing a Notion paragraph block
        """
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": text}
                    }
                ]
            }
        }
    
    def get_all_goals(self) -> List[Dict[str, Any]]:
        """Retrieve all goals from the Life Goals database.
        
        Returns:
            List of goal pages from Notion
        """
        try:
            # Query the database for all goals with Role = Life Goal
            response = requests.post(
                f"{self.base_url}/databases/{self.database_id}/query",
                headers=self.headers,
                json={
                    "filter": {
                        "property": "Role",
                        "rich_text": {
                            "equals": "Life Goal"
                        }
                    }
                }
            )
            
            response.raise_for_status()
            return response.json().get("results", [])
            
        except Exception as e:
            print(f"Error retrieving goals: {e}")
            return []
    
    # Note: We've removed the get_goals_by_user_id method since we're no longer tracking
    # user IDs in the database. If you need to filter goals by user in the future,
    # you would need to add a User property to the database.
