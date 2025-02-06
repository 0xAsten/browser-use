"""
Simple demonstration of the CDP feature.

To test this locally, follow these steps:
1. Create a shortcut for the executable Chrome file.
2. Add the following argument to the shortcut:
   - On Windows: `--remote-debugging-port=9222`
3. Open a web browser and navigate to `http://localhost:9222/json/version` to verify that the Remote Debugging Protocol (CDP) is running.
4. Launch this example.

@dev You need to set the `GEMINI_API_KEY` environment variable before proceeding.
"""



import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from pydantic import SecretStr

from browser_use.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from langchain_anthropic import ChatAnthropic

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
	raise ValueError('ANTHROPIC_API_KEY is not set')

browser = Browser(
	config=BrowserConfig(
		headless=False,
		cdp_url="http://localhost:9222",
	)
)
controller = Controller()


async def main():
	# task = f'In docs.google.com write my Papa a quick thank you for everything letter \n - Magnus'
	# task += f' and save the document as pdf'

	task  = '''
In localhost:3000 playing a grid-based inventory management game. Your goal is to optimize character stats (Attack, Defense, Health) by strategically placing and managing items on a grid while managing your gold resources.
Key Game Mechanics to Consider:
1. Grid Placement
	- Items can be placed on a grid with specific dimensions
	- Items can be rotated (0°, 90°, 180°, 270°) with shift button clicked while dragging
	- Items must be placed validly (within bounds, not overlapping)
	- Items can be discarded by dragging them off the grid
	- All non-bag items must be placed on top of bags
	- Bags serve as the foundation for other items
	- Exception: Bags themselves can be placed directly on the grid
	- Items cannot overlap with other items
2. Shop System
	- Shop offers 4 items at a time
	- Can reroll shop items for a gold cost (REROLL_COST)
	- Each item has:
		a. Price (gold cost)
		b. Stats (attack, defense, health)
		c. Dimensions (width, height)
	- Each reroll will randomize the items
	- Consider rerolling if the items are not optimal
3. Resource Management
	- Manage gold currency
	- Balance between buying items vs saving for rerolls
	- Consider special effects from item combinations
4. Dragging Items
	- From Shop to Grid
		a. Click and hold on a shop item
		b. Drag it over the grid
		c. A preview will appear showing where the item will be placed
		d. Release to place the item if position is valid
	- Discarding Items
		a. Click and hold on a placed item
		b. Drag it outside the grid boundaries
		c. Release to discard
		d. Note: Cannot discard bags that have items on top
Note: 
- Always to reroll to have a bag to start with
- Click and hold left mouse button to drag items
- When it is successfully dragged to the inventory, it means the purchase is successful
- Shift + click and hold left mouse button to rotate items
		
Objectives:
1. Primary: Maximize total stats (ATK + DEF + HP)
2. Secondary: Efficient gold usage
3. Tertiary: Optimal grid space utilization

For each turn, you should:
1. Evaluate current inventory layout
2. Analyze available shop items for:
	a. Stats per gold cost efficiency
	b. Space efficiency (dimensions vs stats)
	c. Potential synergies with existing items
3. Decide between:
	a. Buying and placing an available item
	b. Rerolling the shop
	c. Reorganizing existing items (including discarding)
'''


	model = ChatAnthropic(model_name='claude-3-5-sonnet-20240620', timeout=25, stop=None, temperature=0.5)

	agent = Agent(
		task=task,
		llm=model,
		controller=controller,
		browser=browser,
		save_conversation_path='tmp/conversation/',
	)

	await agent.run()
	# await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())
