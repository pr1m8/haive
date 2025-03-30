

class AcademicPaperSearchInput(BaseModel):
    topic: str = Field(..., description="The topic to search for academic papers on")
    max_results: int = Field(20, description="Maximum number of results to return")