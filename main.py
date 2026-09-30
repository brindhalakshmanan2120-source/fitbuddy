from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Gemini API Setup
genai.configure(api_key="YOUR_GEMINI_API_KEY")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, name: str = Form(...), goal: str = Form(...), level: str = Form(...)):
    # Gemini 1.5 Pro for workout plan
    model_pro = genai.GenerativeModel("gemini-1.5-pro")
    workout_prompt = f"Create a structured 7-day workout plan for {name}, goal: {goal}, fitness level: {level}. Give day-wise with sections."
    workout_plan = model_pro.generate_content(workout_prompt).text

    # Gemini Flash for nutrition tips
    model_flash = genai.GenerativeModel("gemini-1.5-flash")
    nutrition_prompt = f"Give fast, practical nutrition tips for goal: {goal}"
    nutrition_tip = model_flash.generate_content(nutrition_prompt).text

    return templates.TemplateResponse("result.html", {
        "request": request,
        "plan": workout_plan,
        "tip": nutrition_tip,
        "name": name
    })

@app.post("/feedback")
async def feedback(feedback_text: str = Form(...)):
    model_pro = genai.GenerativeModel("gemini-1.5-pro")
    updated = model_pro.generate_content(f"Update workout plan based on this feedback: {feedback_text}").text
    return {"updated_plan": updated}
