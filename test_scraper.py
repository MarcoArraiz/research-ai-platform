from src.tools.web_scraper import web_scraper

# The @tool decorator makes it a Tool object. 
# We can access the original function via .fn
try:
    result = web_scraper.fn("https://www.solotodo.cl/")
    print(result)
except AttributeError:
    # If it's not a wrapper, just call it
    print(web_scraper("https://www.solotodo.cl/"))
