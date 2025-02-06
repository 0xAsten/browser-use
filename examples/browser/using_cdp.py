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

# from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

load_dotenv()
# api_key = os.getenv('ANTHROPIC_API_KEY')
# api_key = os.getenv('DEEPSEEK_API_KEY')
# api_key = os.getenv('GEMINI_API_KEY')
api_key = os.getenv('OPENAI_API_KEY')

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

# 	task  = '''
# In localhost:3000 playing a grid-based inventory management game. Your goal is to optimize character stats (Attack, Defense, Health) by strategically placing and managing items on a grid while managing your gold resources.
# Key Game Mechanics to Consider:
# 1. Grid Placement
# 	- Items can be placed on a grid with specific dimensions
# 	- Items can be rotated (0°, 90°, 180°, 270°) with shift button clicked while dragging
# 	- Items must be placed validly (within bounds, not overlapping)
# 	- Items can be discarded by dragging them off the grid
# 	- All non-bag items must be placed on top of Small Pouch
# 	- Small Pouch serve as the foundation for other items
# 	- Exception: Small Pouch themselves can be placed directly on the grid
# 	- Items cannot overlap with other items
# 2. Shop System
# 	- Shop offers 4 items at a time
# 	- Can reroll shop items for a gold cost (REROLL_COST)
# 	- Each item has:
# 		a. Price (gold cost)
# 		b. Stats (attack, defense, health)
# 		c. Dimensions (width, height)
# 	- Each reroll will randomize the items
# 	- Consider rerolling if the items are not optimal
# 3. Resource Management
# 	- Manage gold currency
# 	- Balance between buying items vs saving for rerolls
# 	- Consider special effects from item combinations
# 4. Buying and Dragging Items
# 	- From Shop to Grid
# 		a. Hold on a shop item
# 		b. Drag it over the grid
# 		c. A preview will appear showing where the item will be placed
# 		d. Release to place the item if position is valid
# 	- Discarding Items
# 		a. Hold on a placed item
# 		b. Drag it outside the grid boundaries
# 		c. Release to discard
# 		d. Note: Cannot discard Small Pouch that have items on top
# Note: 
# - Always to reroll to have a Small Pouch to start with
# - Hold left mouse button to drag items
# - When it is successfully dragged to the inventory, it means the purchase is successful
# - Shift + click and hold left mouse button to rotate items
		
# Objectives:
# 1. Primary: Maximize total stats (ATK + DEF + HP)
# 2. Secondary: Efficient gold usage
# 3. Tertiary: Optimal grid space utilization

# For each turn, you should:
# 1. Evaluate current inventory layout
# 2. Analyze available shop items for:
# 	a. Stats per gold cost efficiency
# 	b. Space efficiency (dimensions vs stats)
# 	c. Potential synergies with existing items
# 3. Decide between:
# 	a. Buying and placing an available item
# 	b. Rerolling the shop
# 	c. Reorganizing existing items (including discarding)
# '''

	task = '''
Grid System:
	1.	The grid consists of 9 columns and 7 rows, forming a 9x7 layout.
	2.	The grid coordinates start from the bottom-left corner (0, 0) and extend to (8, 6).
	3.	Item placement is based on the bottom-left position of the item, meaning the item’s position is defined by the coordinate of its bottom-left corner.

Item Rules:
	1.	Items vary in size (width x height).
		•	For example, a 2x2 Small Pouch placed at (0, 0) occupies coordinates (0, 0), (0, 1), (1, 0), and (1, 1).
		•	A 1x2 Sword placed at (1, 0) occupies coordinates (1, 0) and (1, 1).
	2.	Items can be rotated (0°, 90°, 180°, 270°) using Shift during placement.
	3.	Non-bag items must be placed directly on top of Small Pouch tiles.
	4.	Multiple Small Pouches can be placed directly on the grid to expand usable space.	
	
Item Placement Rules:
	1.	Items can only be validly placed if they:
		•	Stay within grid bounds.
		•	Do not overlap with other items.
		•	Fully overlap with Small Pouch tiles unless they are Small Pouches themselves.
	2.	Important Placement Constraints:
		•	Non-bag items cannot extend beyond Small Pouch areas.
		•	Example 1: A 1x2 Sword placed on a Small Pouch at (1, 0) occupies (1, 0) and (1, 1) only if those coordinates are fully on top of the Small Pouch.
		•	Example 2: A 2x2 Armor cannot be placed if Small Pouch space is insufficient—rerolling the shop may be required.
	3.	Items can be discarded by dragging them off the grid, except for Small Pouches with items on top.

Shop System:
	1.	The shop offers up to 4 items at a time, with an option to reroll for a gold cost.
	2.	Each item has:
		•	A gold price
		•	Stat bonuses (Attack, Defense, Health)
		•	Dimensions (width x height) that impact grid space usage
	3.	Special synergies may apply when combining items.

Gold and Resource Management:
	1.	Balance between purchasing items and rerolling for better options.
	2.	Evaluate the stats-to-gold efficiency of shop items.
	3.	Strategically manage limited grid space and consider discarding or reorganizing items for better layouts.

Buying and Dragging Items
	1. From Shop to Grid
		a. Hold on a shop item
		b. Drag it over the grid
		c. Release to place the item if position is valid
	2. Discarding Items
		a. Hold on a placed item
		b. Drag it outside the grid boundaries
		c. Release to discard
		d. Note: Cannot discard Small Pouch that have items on top

Turn Objectives:
	1.	Maximize Stats (ATK + DEF + HP)
	2.	Optimize the use of grid space.
	3.	Use gold efficiently, deciding whether to:
		•	Buy and place shop items.
		•	Reroll for better inventory.
		•	Reorganize or discard existing items.

Decision Guidelines:
	1.	Always check whether the grid has enough valid space on top of existing Small Pouches before suggesting item placements.
	2.	If there is insufficient space for placement, suggest rerolling the shop to find additional Small Pouches.
	3.	If multiple valid placements are possible:
		•	Prioritize configurations that minimize empty space and preserve room for future items.
		•	Consider item rotations (0°, 90°, 180°, 270°) for optimal grid utilization.	'''

	if not api_key:
		raise ValueError('OPENAI_API_KEY is not set')
	# llm = ChatAnthropic(model_name='claude-3-5-sonnet-20240620', timeout=25, stop=None, temperature=0.5)
	# anthropic/claude-3.5-sonnet openai/gpt-4o-2024-11-20
	llm =ChatOpenAI(base_url='https://openrouter.ai/api/v1', model='anthropic/claude-3.5-sonnet', api_key=SecretStr(api_key))
	# llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(api_key))

	agent = Agent(
		task=task,
		llm=llm,
		controller=controller,
		browser=browser,
		save_conversation_path='tmp/conversation/',
	)

	await agent.run()
	# await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())
