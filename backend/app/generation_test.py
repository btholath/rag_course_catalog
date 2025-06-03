# In routes.py (temporary debug)
from .generation import generate_response

@router.post("/debug/generate")
async def debug_generate():
    query = "List prerequisites for advanced data science"
    context_docs = [
        "To enroll in Advanced Data Science, students must complete Intro to DS and Linear Algebra.",
        "This course requires prior exposure to Python and Statistics."
    ]
    response = generate_response(query, context_docs)
    return {"llm_response": response}
