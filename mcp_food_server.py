#!/usr/bin/env python3
"""
MCP Food Tracking Server
A Model Context Protocol server for logging and analyzing food/nutrition data.
"""

import json
import os
from datetime import datetime
from typing import Any, List, Dict, Optional
from pathlib import Path

from fastmcp import FastMCP
from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    category: Optional[str] = None
    calories: Optional[float] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None


class Meal(BaseModel):
    query: Optional[str] = None
    meal_type: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    total_calories: Optional[float] = None
    total_protein_g: Optional[float] = None
    ingredients: List[Ingredient]


# Data directory
DATA_DIR = Path("data")
FOOD_LOG_FILE = DATA_DIR / "food_log.md"
DATA_DIR.mkdir(exist_ok=True)

# Ensure food log file exists
if not FOOD_LOG_FILE.exists():
    FOOD_LOG_FILE.write_text("# Food Log\n\n")


def parse_food_log() -> List[Meal]:
    """Parse the food log markdown file into Meal objects."""
    try:
        with open(FOOD_LOG_FILE, "r") as f:
            content = f.read()
    except FileNotFoundError:
        return []

    meal_blocks = content.strip().split("### MEAL START")[1:]
    parsed_meals = []

    for block in meal_blocks:
        block = block.strip().replace("### MEAL END", "").strip()
        lines = block.split('\n')

        metadata = {}
        table_lines = []
        
        for line in lines:
            if line.startswith("**"):
                colon_index = line.find(':')
                if colon_index != -1:
                    key_str = line[:colon_index]
                    value_str = line[colon_index+1:]
                    
                    key = key_str.replace("**", "").strip().lower().replace(" ", "_").replace("(", "").replace(")", "")
                    value = value_str.replace("**", "").strip()
                    metadata[key] = value
            elif line.startswith("|") and '---' not in line:
                table_lines.append(line)

        # Parse ingredients table
        ingredients = []
        if table_lines and len(table_lines) > 1:
            header_line = table_lines[0]
            header = [h.strip() for h in header_line.strip('|').split('|')]
            
            try:
                name_idx = header.index("Ingredient")
                cat_idx = header.index("Category")
                cal_idx = header.index("Calories")
                prot_idx = header.index("Protein (g)")
            except ValueError:
                continue

            for row_line in table_lines[1:]:
                row = [r.strip() for r in row_line.strip('|').split('|')]
                if len(row) >= len(header):
                    try:
                        ingredient_data = {
                            "name": row[name_idx],
                            "category": row[cat_idx] if cat_idx < len(row) and row[cat_idx] else None,
                            "calories": float(row[cal_idx]) if cal_idx < len(row) and row[cal_idx] and row[cal_idx] != '-' else None,
                            "protein_g": float(row[prot_idx]) if prot_idx < len(row) and row[prot_idx] and row[prot_idx] != '-' else None,
                        }
                        ingredients.append(Ingredient(**ingredient_data))
                    except (ValueError, IndexError):
                        continue

        if ingredients:
            total_calories = metadata.get("total_calories")
            total_protein_g = metadata.get("total_protein_g")
            
            meal = Meal(
                query=metadata.get("query"),
                meal_type=metadata.get("meal"),
                date=metadata.get("date"),
                time=metadata.get("time"),
                total_calories=float(total_calories) if total_calories else None,
                total_protein_g=float(total_protein_g) if total_protein_g else None,
                ingredients=ingredients
            )
            parsed_meals.append(meal)

    return parsed_meals


def add_meal_to_log(meal_data: Dict[str, Any]) -> str:
    """Add a new meal entry to the food log."""
    try:
        # Parse the meal data
        query = meal_data.get("query", "")
        meal_type = meal_data.get("meal_type", "")
        ingredients = meal_data.get("ingredients", [])
        
        # Get current timestamp if not provided
        now = datetime.now()
        date = meal_data.get("date", now.strftime("%Y-%m-%d"))
        time = meal_data.get("time", now.strftime("%H:%M"))
        
        # Calculate totals
        total_calories = sum(ing.get("calories", 0) for ing in ingredients if ing.get("calories"))
        total_protein = sum(ing.get("protein_g", 0) for ing in ingredients if ing.get("protein_g"))
        
        # Format the meal entry
        meal_entry = f"""
### MEAL START
**Query:** "{query}"
**Meal:** {meal_type}
**Date:** {date}
**Time:** {time}
**Total Calories:** {total_calories}
**Total Protein (g):** {total_protein}

| Ingredient         | Category | Calories | Protein (g) |
|--------------------|----------|----------|-------------|
"""
        
        for ing in ingredients:
            name = ing.get("name", "")
            category = ing.get("category", "")
            calories = ing.get("calories", 0)
            protein = ing.get("protein_g", 0)
            meal_entry += f"| {name:<18} | {category:<8} | {calories:<8} | {protein:<11} |\n"
        
        meal_entry += "### MEAL END\n\n"
        
        # Append to file
        with open(FOOD_LOG_FILE, "a") as f:
            f.write(meal_entry)
        
        return f"Successfully logged meal: {meal_type} on {date} at {time}"
    
    except Exception as e:
        return f"Error logging meal: {str(e)}"


# Initialize the FastMCP server
mcp = FastMCP("food-tracker")


@mcp.tool()
def add_food_entry(
    query: str,
    ingredients: List[Dict[str, Any]],
    meal_type: Optional[str] = None,
    date: Optional[str] = None,
    time: Optional[str] = None
) -> str:
    """Log a new food/meal entry with ingredients and nutrition data.
    
    Args:
        query: Original user query describing the meal
        ingredients: List of ingredients with nutrition information
        meal_type: Type of meal (breakfast, lunch, dinner, snack)
        date: Date of the meal (YYYY-MM-DD format)
        time: Time of the meal (HH:MM format)
    """
    meal_data = {
        "query": query,
        "meal_type": meal_type,
        "date": date,
        "time": time,
        "ingredients": ingredients
    }
    return add_meal_to_log(meal_data)


@mcp.tool()
def get_food_log(
    limit: Optional[int] = None,
    date_filter: Optional[str] = None
) -> str:
    """Retrieve all logged food entries.
    
    Args:
        limit: Maximum number of entries to return (optional)
        date_filter: Filter by specific date (YYYY-MM-DD format, optional)
    """
    meals = parse_food_log()
    
    # Apply filters
    if date_filter:
        meals = [m for m in meals if m.date == date_filter]
    
    if limit:
        meals = meals[-limit:]  # Get most recent entries
    
    # Format response
    if not meals:
        return "No food entries found."
    else:
        result = f"Found {len(meals)} food entries:\n\n"
        for meal in meals:
            result += f"**{meal.meal_type}** on {meal.date} at {meal.time}\n"
            result += f"Query: {meal.query}\n"
            result += f"Total Calories: {meal.total_calories}, Protein: {meal.total_protein_g}g\n"
            result += f"Ingredients: {', '.join([ing.name for ing in meal.ingredients])}\n\n"
        return result


@mcp.tool()
def analyze_nutrition(
    analysis_type: str,
    date_range: Optional[str] = None
) -> str:
    """Analyze nutrition trends and provide insights from food log.
    
    Args:
        analysis_type: Type of analysis (daily_summary, weekly_trends, macro_breakdown, ingredient_analysis)
        date_range: Date range for analysis (e.g., 'last_7_days', 'this_week', 'YYYY-MM-DD to YYYY-MM-DD')
    """
    meals = parse_food_log()
    
    if not meals:
        return "No food data available for analysis."
    
    if analysis_type == "daily_summary":
        # Group by date and calculate daily totals
        daily_data = {}
        for meal in meals:
            date = meal.date
            if date not in daily_data:
                daily_data[date] = {"calories": 0, "protein": 0, "meals": 0}
            
            daily_data[date]["calories"] += meal.total_calories or 0
            daily_data[date]["protein"] += meal.total_protein_g or 0
            daily_data[date]["meals"] += 1
        
        result = "Daily Nutrition Summary:\n\n"
        for date, data in sorted(daily_data.items()):
            result += f"**{date}**: {data['calories']:.0f} calories, {data['protein']:.1f}g protein ({data['meals']} meals)\n"
        return result
    
    elif analysis_type == "ingredient_analysis":
        # Analyze ingredient frequency and nutrition contribution
        ingredient_stats = {}
        for meal in meals:
            for ing in meal.ingredients:
                name = ing.name
                if name not in ingredient_stats:
                    ingredient_stats[name] = {"count": 0, "calories": 0, "protein": 0}
                
                ingredient_stats[name]["count"] += 1
                ingredient_stats[name]["calories"] += ing.calories or 0
                ingredient_stats[name]["protein"] += ing.protein_g or 0
        
        result = "Ingredient Analysis:\n\n"
        for ing, stats in sorted(ingredient_stats.items(), key=lambda x: x[1]["count"], reverse=True):
            result += f"**{ing}**: Used {stats['count']} times, {stats['calories']:.0f} total calories, {stats['protein']:.1f}g total protein\n"
        return result
    
    else:
        return f"Analysis type '{analysis_type}' not yet implemented."


@mcp.tool()
def search_food_entries(
    search_term: str,
    search_type: str = "all"
) -> str:
    """Search food entries by ingredient, meal type, or other criteria.
    
    Args:
        search_term: Term to search for in ingredients, meal types, or queries
        search_type: Type of search (ingredient, meal_type, query, all)
    """
    meals = parse_food_log()
    search_term_lower = search_term.lower()
    
    matching_meals = []
    for meal in meals:
        match = False
        
        if search_type in ["ingredient", "all"]:
            for ing in meal.ingredients:
                if search_term_lower in ing.name.lower():
                    match = True
                    break
        
        if search_type in ["meal_type", "all"] and meal.meal_type and search_term_lower in meal.meal_type.lower():
            match = True
        
        if search_type in ["query", "all"] and meal.query and search_term_lower in meal.query.lower():
            match = True
        
        if match:
            matching_meals.append(meal)
    
    if not matching_meals:
        return f"No entries found matching '{search_term}'"
    else:
        result = f"Found {len(matching_meals)} entries matching '{search_term}':\n\n"
        for meal in matching_meals:
            result += f"**{meal.meal_type}** on {meal.date}: {meal.query}\n"
        return result


if __name__ == "__main__":
    mcp.run()  # FastMCP automatically uses stdio transport by default
