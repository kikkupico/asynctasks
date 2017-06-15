import unittest
from asynctasks.executor import Executor
from asynctasks.executionplan import ExecutionPlan
import asyncio
import random


class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.tasks_dict_array = [{"dependencies": [], "name": "task0"}, {"dependencies": [0], "name": "task1"},
                                 {"dependencies": [1], "name": "task2"}, {"dependencies": [0], "name": "task3"},
                                 {"dependencies": [], "name": "task4"}, {"dependencies": [], "name": "task5"}]

    @unittest.skip("Useful for manual; not required for automated")
    def test_simple_execution(self):
        async def print_task(loop, task):
            print("Executing task {}".format(task))
            await asyncio.sleep(0.1)

        plan = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("\nBEFORE EXECUTION\n{}".format(plan))
        Executor(plan, 2, 0.01, print_task).trigger_execution()
        print("\nAFTER EXECUTION\n{}".format(plan.as_gantt()))
        self.assertEqual(plan.is_incomplete(), False, "Plan has been marked complete")
        map(lambda x: self.assertIn(x, plan.completed_tasks(), "Task {} has been completed".format(x)), [x for x in range(0, len(plan.plan_as_dict_array))])

    def test_low_granularity_execution(self):
        async def print_task(loop, task):
            print("Executing task {}".format(task['name']))
            await asyncio.sleep(0)

        async def delayed_task(loop, task):
            print("Executing task {}".format(task['name']))
            await asyncio.sleep(0.1)

        plan = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("\nBEFORE EXECUTION\n{}".format(plan))
        Executor(plan, 2, 0.01, print_task).trigger_execution()
        print("\nAFTER EXECUTION\n{}".format(plan))
        self.assertEqual(plan.is_incomplete(), False, "Simple plan has been marked complete during low granularity execution")
        map(lambda x: self.assertIn(x, plan.completed_tasks(), "Task {} has been completed".format(x)), [x for x in range(0, len(plan.plan_as_dict_array))])

        plan = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("\nBEFORE EXECUTION\n{}".format(plan))
        Executor(plan, 3, 0.01, delayed_task).trigger_execution()
        print("\nAFTER EXECUTION\n{}".format(plan))
        self.assertEqual(plan.is_incomplete(), False, "Long plan has been marked complete during low granularity execution")
        map(lambda x: self.assertIn(x, plan.completed_tasks(), "Task {} has been completed".format(x)),
            [x for x in range(0, len(plan.plan_as_dict_array))])

    @unittest.skip("Useful for manual; not required for automated")
    def test_random_data_execution(self):
        async def delayed_task(loop, task):
            duration = random.randint(1, 3)
            print("Executing task {0} for {1} seconds".format(task, duration))
            await asyncio.sleep(float(duration))

        def times_tab(n):
            return "".join(["\t" for x in range(0, n)])

        tree_str = "task0\n"
        prev_indent_level = 0
        for i in range(1, 7):
            if prev_indent_level == 0:
                indent_level = prev_indent_level + random.randint(0, 1)
            else:
                indent_level = prev_indent_level + random.randint(-1, 1)
            tree_str += "{0}task{1}".format(times_tab(indent_level), i) + "\n"
            prev_indent_level = indent_level

        plan = ExecutionPlan().from_tree_string(tree_str[:-1])
        print("PLAN\n{}".format(plan))
        max_concurrency = random.randint(1, 5)
        print("\nExecuting with {} threads".format(max_concurrency))
        Executor(plan, max_concurrency, 0.01, delayed_task).trigger_execution()

        self.assertEqual(plan.is_incomplete(), False, "Plan has been marked complete")

        for i in range(0, len(plan.plan_as_dict_array)):
            self.assertIn(i, plan.completed_list, "Task {} has been completed".format(i))
            for j in plan.get_dependants(i):
                self.assertGreaterEqual(plan.plan_as_dict_array[j]['start_time'], plan.plan_as_dict_array[i]['end_time'], "Task {0} started after Task {1} ended".format(j, i))

        print("\n" + plan.as_gantt())

    def test_multi_random_data_execution(self):
        async def delayed_task(loop, task):
            duration = random.randint(1, 3)
            print("Executing task {0} for {1} deciseconds".format(task['name'], duration))
            await asyncio.sleep(float(duration/10))

        def times_tab(n):
            return "".join(["\t" for x in range(0, n)])

        for q in range(0, 10):
            tree_str = "task1\n"
            prev_indent_level = 0
            for i in range(1, 7):
                if prev_indent_level == 0:
                    indent_level = prev_indent_level + random.randint(0, 1)
                else:
                    indent_level = prev_indent_level + random.randint(-1, 1)
                tree_str += "{0}task{1}".format(times_tab(indent_level), i+1) + "\n"
                prev_indent_level = indent_level

            plan = ExecutionPlan().from_tree_string(tree_str[:-1])
            print("PLAN\n{}".format(plan))
            max_concurrency = random.randint(1, 5)
            granularity = 1/(10**random.randint(1, 4))
            print("\nExecuting with {0} threads, {1} granularity".format(max_concurrency, granularity))
            Executor(plan, max_concurrency, granularity, delayed_task).trigger_execution()

            self.assertEqual(plan.is_incomplete(), False, "Plan has been marked complete")

            for i in range(0, len(plan.plan_as_dict_array)):
                self.assertIn(i, plan.completed_list, "Task {} has been completed".format(i))
                for j in plan.get_dependants(i):
                    self.assertGreaterEqual(plan.plan_as_dict_array[j]['start_time'],
                                            plan.plan_as_dict_array[i]['end_time'],
                                            "Task {0} started after Task {1} ended".format(j, i))

            print(plan.as_gantt())

    def test_long_random_data_execution(self):
        async def delayed_task(loop, task):
            duration = random.randint(1, 3)
            print("Executing task {0} for {1} deciseconds".format(task['name'], duration))
            await asyncio.sleep(float(duration/10))

        def times_tab(n):
            return "".join(["\t" for x in range(0, n)])

        for q in range(0, 1):
            tree_str = "task1\n"
            prev_indent_level = 0
            for i in range(1, 200):
                if prev_indent_level == 0:
                    indent_level = prev_indent_level + random.randint(0, 1)
                else:
                    indent_level = prev_indent_level + random.randint(-1, 1)
                tree_str += "{0}task{1}".format(times_tab(indent_level), i+1) + "\n"
                prev_indent_level = indent_level

            plan = ExecutionPlan().from_tree_string(tree_str[:-1])
            print("PLAN\n{}".format(plan))
            max_concurrency = 10
            granularity = 1/(10**random.randint(1, 4))
            print("\nExecuting with {0} threads, {1} granularity".format(max_concurrency, granularity))
            Executor(plan, max_concurrency, granularity, delayed_task).trigger_execution()

            self.assertEqual(plan.is_incomplete(), False, "Plan has been marked complete")

            for i in range(0, len(plan.plan_as_dict_array)):
                self.assertIn(i, plan.completed_list, "Task {} has been completed".format(i))
                for j in plan.get_dependants(i):
                    self.assertGreaterEqual(plan.plan_as_dict_array[j]['start_time'],
                                            plan.plan_as_dict_array[i]['end_time'],
                                            "Task {0} started after Task {1} ended".format(j, i))

            #print(plan.as_gantt(resolution=300.0))

if __name__ == '__main__':
    unittest.main()
