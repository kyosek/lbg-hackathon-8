from sys import argv

wrong_arguments = ValueError("usage: fositive-vibes-only {test,llm}")

if len(argv) < 2:
    raise wrong_arguments

if argv[1] == "test":
    def get_answer(query: str) -> str:
        return f"<placeholder for response to to '{query}'"
elif argv[1] == "llm":
    from query_storage import main
    get_answer = main
else:
    raise wrong_arguments
