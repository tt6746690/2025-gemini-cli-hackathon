from fastapi import FastAPI
from pydantic import BaseModel
import datetime

app = FastAPI()

# --- Pydantic Models ---

class Ingredient(BaseModel):
    name: str
    category: str | None = None
    calories: float | None = None
    protein_g: float | None = None
    carbs_g: float | None = None
    fat_g: float | None = None

class Meal(BaseModel):
    query: str | None = None
    meal_type: str | None = None
    date: str | None = None
    time: str | None = None
    total_calories: float | None = None
    total_protein_g: float | None = None
    ingredients: list[Ingredient]

@app.get("/")
def read_root():
    return {"message": "MCP Food Log Server is running."}

@app.get("/get_log", response_model=list[Meal])
def get_log():
    try:
        with open("data/food_log.md", "r") as f:
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
                else:
                    continue # Skip lines without a colon
            elif line.startswith("|"):
                if '---' in line: continue
                table_lines.append(line)

        # Basic parsing for totals from metadata
        total_calories = metadata.get("total_calories")
        total_protein_g = metadata.get("total_protein_g")

        # Parse the table
        ingredients = []
        if table_lines:
            header_line = table_lines.pop(0)
            header = [h.strip() for h in header_line.strip('|').split('|')]
            
            try:
                name_idx = header.index("Ingredient")
                cat_idx = header.index("Category")
                cal_idx = header.index("Calories")
                prot_idx = header.index("Protein (g)")
            except ValueError:
                continue

            for row_line in table_lines:
                row = [r.strip() for r in row_line.strip('|').split('|')]
                if len(row) != len(header): continue
                
                try:
                    ingredient_data = {
                        "name": row[name_idx],
                        "category": row[cat_idx] if cat_idx < len(row) and row[cat_idx] else None,
                        "calories": float(row[cal_idx]) if cal_idx < len(row) and row[cal_idx] else None,
                        "protein_g": float(row[prot_idx]) if prot_idx < len(row) and row[prot_idx] else None,
                    }
                    ingredients.append(Ingredient(**ingredient_data))
                except (ValueError, IndexError):
                    continue

        if ingredients:
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

# POST /log_meal endpoint will go here
