# Description: Research assistant class that handles the research process for a given question.

# libraries
import asyncio
import json
import uuid

from actions.local_source_parse import local_source_parse, async_gather_local
from actions.web_search import web_search
from actions.web_scrape import async_gather
from processing.text import \
    write_to_file, \
    create_message, \
    create_chat_completion, \
    read_txt_files, \
    write_md_to_pdf
from config import Config
from agent import prompts
import os
import string
from actions.tavily_search import tavily_client
import time

CFG = Config()


class ResearchAgent:
    def __init__(self, question, agent, agent_role_prompt, websocket, file_list = []):
        """ Initializes the research assistant with the given question.
        Args: question (str): The question to research
        Returns: None
        """

        self.question = question
        self.agent = agent
        self.agent_role_prompt = agent_role_prompt if agent_role_prompt else prompts.generate_agent_role_prompt(agent)
        self.visited_urls = set()
        self.research_summary = ""
        self.directory_name = str(uuid.uuid4())
        self.dir_path = os.path.dirname(f"./outputs/{self.directory_name}/")
        self.file_list = file_list
        self.local_content = local_source_parse(file_list=self.file_list)
        self.websocket = websocket

    async def stream_output(self, output):
        if not self.websocket:
            return print(output)
        await self.websocket.send_json({"type": "logs", "output": output})

    async def summarize(self, text, topic):
        """ Summarizes the given text for the given topic.
        Args: text (str): The text to summarize
                topic (str): The topic to summarize the text for
        Returns: str: The summarized text
        """

        messages = [create_message(text, topic)]
        await self.websocket.send_json({"type": "logs", "output": f"📝 Summarizing text for query: {text}"})

        return await create_chat_completion(
            model=CFG.fast_llm_model,
            messages=messages,
        )

    async def get_new_urls(self, url_set_input):
        """ Gets the new urls from the given url list.
        Args: url_set_input (list[str]): The url list to get the new urls from
        Returns: list[str]: The new urls from the given url set
        """

        new_urls = []
        for url in url_set_input:
            if url not in self.visited_urls:
                await self.websocket.send_json({"type": "logs", "output": f"✅ Adding source url to research: {url}\n"})
                self.visited_urls.add(url)
                new_urls.append(url)

        return new_urls

    async def call_agent(self, action, stream=False, websocket=None):
        t1 = time.time()
        messages = [{
            "role": "system",
            "content": self.agent_role_prompt
        }, {
            "role": "user",
            "content": action,
        }]
        answer = await create_chat_completion(
            model=CFG.smart_llm_model,
            messages=messages,
            stream=stream,
            websocket=websocket,
        )
        print('call_agent:', time.time() - t1)
        return answer

    async def create_search_queries(self):
        """ Creates the search queries for the given question.
        Args: None
        Returns: list[str]: The search queries for the given question
        """
        result = await self.call_agent(prompts.generate_search_queries_prompt(self.question))
        print(result)
        loaded_results = json.loads(result)
        await self.websocket.send_json({"type": "logs", "output": f"🧠 I will conduct my research based on the following queries: {', '.join(loaded_results)}..."})
        return loaded_results


    async def async_search(self, query): 
        """ Runs the async search for the given query.
        Args: query (str): The query to run the async search for
        Returns: list[str]: The async search for the given query
        """
        print(f"Running async_search on query: {query}")
        t1 = time.time()
        search_results = tavily_client.search(query, search_depth="advanced", include_raw_content=True,  max_results=5)
        print("Tavily search:", time.time() - t1)
        urls = [result['url'] for result in search_results['results']] #type: ignore

        # new_search_urls = self.get_new_urls(urls)

        await self.stream_output(f"🌐 Browsing the following sites for relevant information: {', '.join(urls)}...")

        # responses = [f"Information gathered from url {result['url']}: {summary.summarize_text(result['content'], query)}" for result in search_results['results']]

        tasks = [async_gather(result['url'], query, result['raw_content'], self.websocket) for result in search_results['results']] #type: ignore
        
        # adding local files to the tasks
        local_sources = self.local_content
        if local_sources: 
            local_tasks = [async_gather_local(file['file_name'], query, file['content'], self.websocket) for file in local_sources]
            tasks.extend(local_tasks)

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        return responses

    async def run_search_summary(self, query):
        """ Runs the search summary for the given query.
        Args: query (str): The query to run the search summary for
        Returns: str: The search summary for the given query
        """

        await self.websocket.send_json({"type": "logs", "output": f"🔎 Running research for '{query}'..."})

        responses = await self.async_search(query)

        result = "\n".join(responses) #type: ignore
        os.makedirs(os.path.dirname(f"./outputs/{self.directory_name}/research-{query}.txt"), exist_ok=True)
        write_to_file(f"./outputs/{self.directory_name}/research-{query}.txt", result)
        return result

    async def conduct_research(self):
        """ Conducts the research for the given question.
        Args: None
        Returns: str: The research for the given question
        """

        self.research_summary = read_txt_files(self.dir_path) if os.path.isdir(self.dir_path) else ""

        if not self.research_summary:
            search_queries = await self.create_search_queries()
            for query in search_queries:
                research_result = await self.run_search_summary(query)
                self.research_summary += f"{research_result}\n\n"

        await self.websocket.send_json(
            {"type": "logs", "output": f"Total research words: {len(self.research_summary.split(' '))}"})

        return self.research_summary


    async def create_concepts(self):
        """ Creates the concepts for the given question.
        Args: None
        Returns: list[str]: The concepts for the given question
        """
        result = await self.call_agent(prompts.generate_concepts_prompt(self.question, self.research_summary))

        await self.websocket.send_json({"type": "logs", "output": f"I will research based on the following concepts: {result}\n"})
        return json.loads(result) #type: ignore

    async def write_report(self, report_type, websocket):
        """ Writes the report for the given question.
        Args: None
        Returns: str: The report for the given question
        """
        report_type_func = prompts.get_report_by_type(report_type)
        await websocket.send_json(
            {"type": "logs", "output": f"✍️ Writing {report_type} for research task: {self.question}..."})
        answer = await self.call_agent(report_type_func(self.question, self.research_summary), stream=True,
                                       websocket=websocket)

        path = await write_md_to_pdf(report_type, self.directory_name, answer) #type: ignore

        return answer, path

    async def write_lessons(self):
        """ Writes lessons on essential concepts of the research.
        Args: None
        Returns: None
        """
        concepts = await self.create_concepts()
        for concept in concepts:
            answer = await self.call_agent(prompts.generate_lesson_prompt(concept), stream=True)
            await write_md_to_pdf("Lesson", self.directory_name, answer)