# 2025-gemini-cli-hackathon

## MCP Food Tracking Server (FastMCP Implementation)

A Model Context Protocol server for logging and analyzing food/nutrition data, now refactored to use FastMCP for simplified development.

### Overview

This project implements an MCP server that allows language models to:
- Log food entries with detailed ingredient and nutrition information
- Retrieve and analyze food consumption data
- Perform nutrition analysis (daily summaries, ingredient analysis)
- Search through food entries

### Recent Changes

**✅ Refactored to use FastMCP** (January 2025)
- Migrated from the original MCP SDK to FastMCP for cleaner, more maintainable code
- Simplified tool definitions using Python decorators
- Reduced boilerplate code significantly
- Maintained all original functionality

### Features

- **Food Entry Logging**: Add meals with detailed ingredient breakdown
- **Data Retrieval**: Get food logs with filtering options
- **Nutrition Analysis**: Daily summaries and ingredient analysis
- **Search Functionality**: Find entries by ingredient, meal type, or query
- **Markdown Storage**: Simple markdown-based data persistence

### Installation & Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python mcp_food_server.py

# Validate the setup
python test_simple.py
```

### Dependencies

- `fastmcp`: Simplified MCP server framework
- `pydantic`: Data validation and serialization

### Tools Available

1. **add_food_entry**: Log new meals with ingredients and nutrition data
2. **get_food_log**: Retrieve logged food entries with optional filtering
3. **analyze_nutrition**: Perform nutrition analysis (daily summaries, ingredient breakdown)
4. **search_food_entries**: Search entries by various criteria

### Data Structure

Food data is stored in `data/food_log.md` with the following structure:
- Each meal entry contains metadata (query, meal type, date, time, totals)
- Ingredient table with nutrition information (calories, protein, etc.)
- Support for multiple ingredients per meal

### Original Project Goals

Im in a hackathon, we are thinking building some functionality where we can allow LM to save information about food to a data store (e.g., database) format them nicely, and also allow LM to fetch these information when user ask about their diet habits/health trends we are thinking of using mcp (model context protocol) server to do this, and maybe jsut very simple 1 markdown file to keep track all the data. 

clarifications
- this should be done with vibe coding in 3hrs. give me a concrete plan
- this is more of a cool lm integration with mcp for a useful practical task, so don't worry about polished ui/ux etc.
- we are trying to use gemini-cli as the lm that runs locally, we want to hook it up to gemini-cli. user just interact with gemini-cli
- data/historical.md is historical data. im thinking we should have another mardkwon that keep track of formatted data. just use markdown for simplicity
- food/health data, we are pretty interested in calories, meals, macros, all the standard stuff.
  

Note 
- the historical data is under `data/historical.md`
- lets use the conda environment before installing packages. i think the env is called `gemini-hackathon`. do `source ~/.profile` to get conda in path.


ok lets expand on foundation and server setup. make a very concrete plan for this. ask for clarifications. plan dont code

clarifications
- use fastapi
- one thing to note is that for a meal, there is probably multiple ingridients each with its own carlories, protein, etc. we probably want to have one ingriendient each for self cooked meals. so probably 1 table per meal? what do you think. lets go for the more complicated view where we list ingridients as well. this is very useful for answering things like what are proportion of calorie come from meat? type of queries.
- for the post /add_entry, also try to include the original user query, as well as enriched information about the meal (e.g., nutrition, calorie), 

brainstorm with me on this. ways to improve, things to clarify, potential plans
