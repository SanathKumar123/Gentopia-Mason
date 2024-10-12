import requests
from typing import Optional, Any
from gentopia.tools import BaseTool, Type, AnyStr
from pydantic import BaseModel, Field

class RottenTomatoesSearchArgs(BaseModel):
    query: str = Field(..., description="a search query")

class RottenTomatoesSearch(BaseTool):
    """Tool that adds the capability to query Rotten Tomatoes search."""
    
    name = "rotten_tomatoes_search"
    description = ("A search engine retrieving top search results from Rotten Tomatoes."
                   "Input should be a search query.")
    
    args_schema: Optional[Type[BaseModel]] = RottenTomatoesSearchArgs
    
    def _run(self, query: AnyStr) -> str:
        rotten_tomatoes_client = f"https://api.rottentomatoes.com/api/public/v1.0/movies.json?q={query}&page_limit=5&apiKey=YOUR_API_KEY"
        
        response = requests.get(rotten_tomatoes_client)
        if response.status_code != 200:
            return "Error fetching results."
        
        results = response.json()
        
        output = []
        for category in ['movies', 'tvSeries', 'franchises']:
            if category in results and results[category]:
                output.append(f"{category.capitalize()}:")
                for item in results[category]:
                    output.append(f"- {item['title']} ({item.get('year', 'N/A')})")
                output.append("")
        
        return '\n'.join(output) if output else "No results found."
    
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    ans = RottenTomatoesSearch()._run("The Matrix")
    print(ans)