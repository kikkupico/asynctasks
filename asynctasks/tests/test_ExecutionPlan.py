import unittest
import time
from asynctasks.executionplan import ExecutionPlan

# TEST NOTES
# Completing third ready task fails


class TestExecutionPlan(unittest.TestCase):
    def setUp(self):
        self.tasks_dict_array = [{"dependency": None, "name": "task0"}, {"dependency": "task0", "name": "task1"},
                                 {"dependency": "task1", "name": "task2"}, {"dependency": "task0", "name": "task3"},
                                 {"dependency": None, "name": "task4"}]

    @unittest.skip("skipping for now")
    def test___str__(self):
        execution_plan = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("Printing plan...\n" + str(execution_plan))

    def test_ready_tasks_simple(self):
        e = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("Simple ready test plan \n" + str(e))
        print(e.ready_tasks())
        t = e.ready_tasks()[0]
        e.mark_started(t)
        e.mark_completed(t)
        print(e.ready_tasks())
        t = e.ready_tasks()[0]
        e.mark_started(t)
        e.mark_completed(t)

        self.assertEqual(len(e.ready_tasks()), 3, "ready tasks simple case")

    def test_ready_tasks_two_plans(self):
        e1 = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        e2 = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("Twin ready test plan\n" + str(e1) + "\n" + str(e2))
        print(e1.ready_tasks())
        t = e1.ready_tasks()[0]
        e1.mark_started(t)
        e1.mark_completed(t)
        print(e1.ready_tasks())
        t = e1.ready_tasks()[0]
        e1.mark_started(t)
        e1.mark_completed(t)

        self.assertEqual(len(e1.ready_tasks()), 3, "ready tasks plan 1(modified)")
        self.assertEqual(len(e2.ready_tasks()), 2, "ready tasks plan 2 (unmodified)")

    def test_ready_tasks_till_empty(self):
        e = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        print("Till empty ready test plan\n" + str(e))
        print(e.ready_tasks())
        t = e.ready_tasks()[0]
        e.mark_started(t)
        e.mark_completed(t)
        print(e.ready_tasks())
        t = e.ready_tasks()[0]
        e.mark_started(t)
        e.mark_completed(t)
        print(e.ready_tasks())
        t = e.ready_tasks()[0]
        e.mark_started(t)
        e.mark_completed(t)
        print(e.ready_tasks())
        t = e.ready_tasks()[0]
        e.mark_started(t)
        e.mark_completed(t)
        print(e.ready_tasks())
        t = e.ready_tasks()[0]
        e.mark_started(t)
        e.mark_completed(t)

        self.assertEqual(len(e.ready_tasks()), 0, "ready tasks till empty")

    def test_from_tree_string(self):
        simple_plan_string = "task0\n\ttask1\ntask2"
        print(simple_plan_string)
        e = ExecutionPlan().from_tree_string(simple_plan_string)
        print(e.plan_as_dict_array)
        print(e)
        self.assertEqual(simple_plan_string, str(e).replace(" Ready ", "")[:-1])  # str returns string with trailing \n

    def test_as_json(self):
        e = ExecutionPlan().from_dict_array(self.tasks_dict_array)
        t = e.ready_tasks()[0]
        e.mark_started(t)
        time.sleep(2)
        e.mark_completed(t)
        t = e.ready_tasks()[0]
        e.mark_started(t)
        time.sleep(1)
        e.mark_completed(t)
        print(e)
        print(e.as_json())

    def test_as_gantt(self):
        e = ExecutionPlan().from_dict_array(self.tasks_dict_array)

        def complete_a_task():
            t = e.ready_tasks()[0]
            e.mark_started(t)
            time.sleep(1)
            e.mark_completed(t)

        for task in e.plan_as_dict_array:
            complete_a_task()

        print(e)
        print(e.as_gantt())

if __name__ == '__main__':
    unittest.main()
