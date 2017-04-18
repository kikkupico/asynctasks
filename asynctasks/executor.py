import asyncio
import sys


class Executor:
    def __init__(self, execution_plan, max_concurrency, granularity, execution_coroutine):
        self.execution_plan = execution_plan
        self.max_concurrency = max_concurrency
        self.granularity = granularity
        if sys.platform == 'win32':
            self.loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(self.loop)
        else:
            self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue(loop=self.loop, maxsize=max_concurrency)
        self.execution_coroutine = execution_coroutine
        self.executors = 0

    async def get_one_ready_task(self):
        #print("func:get_one_ready_task")
        while self.execution_plan.is_incomplete():
            t = self.execution_plan.ready_tasks()
            if len(t) > 0:
                return t[0]
            else:
                await asyncio.sleep(self.granularity)

        return None  # IMPORTANT: None can be returned if execution plan get completed in the middle of above loop (during await)

    async def execute_task(self, task_id):
        self.executors += 1
        self.execution_plan.mark_started(task_id)
        await self.execution_coroutine(loop=self.loop, task=self.execution_plan.plan_as_dict_array[task_id])
        self.execution_plan.mark_completed(task_id)
        self.executors -= 1

    async def execute(self):
        started_tasks = []
        while self.execution_plan.is_incomplete():
            if self.executors < self.max_concurrency:
                task_id = await self.get_one_ready_task()
                if task_id is not None:  # check last comment in get_one_ready_task to understand this check
                    task = asyncio.ensure_future(self.execute_task(task_id))
                    started_tasks.append(task)
                await asyncio.sleep(self.granularity)
            else:
                await asyncio.sleep(self.granularity)

        # for task in started_tasks:  # ensure that all tasks are completed before exiting execution
        #     print(task)             # not sure if this is required; but just leaving it here in case it is required later
        #     await task

    def trigger_execution(self):
        self.loop.run_until_complete(asyncio.gather(self.execute()))
