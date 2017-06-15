asynctasks
==========

|BuildStatus| |Coverage|

Task scheduler based on asyncio. Allows max-concurrency and granularity to be specified. Execution results are printed as a Gantt chart.

Sample Usage
------------

.. code-block:: python

   from asynctasks.executor import Executor
   from asynctasks.executionplan import ExecutionPlan
   import asyncio

   #create an array of tasks
   tasks_dict_array = [{"dependencies": [], "name": "task0"}, {"dependencies": [0], "name": "task1"},
                           {"dependencies": [1], "name": "task2"}, {"dependencies": [0], "name": "task3"},
                           {"dependencies": [], "name": "task4"}, {"dependencies": [], "name": "task5"}]

   #define an async function that should be executed for each task
   async def print_task(loop, task):
      print("Executing task {}".format(task))
      await asyncio.sleep(0.1)

   #create an execution plan for the tasks
   plan = ExecutionPlan().from_dict_array(tasks_dict_array)
   print("\nBEFORE EXECUTION\n{}".format(plan))

   #execute the plan with print_task function and max_concurrency as 2
   Executor(plan, 2, 0.01, print_task).trigger_execution()
   print("\nAFTER EXECUTION\n{}".format(plan.as_gantt()))

Sample Output
-------------

.. code-block:: python

    BEFORE EXECUTION
    task0 Ready
        task1
            task2
        task3
    task4 Ready
    task5 Ready

    Executing task {'dependencies': [], 'name': 'task0', 'start_time': 1497528994.1246588}
    Executing task {'dependencies': [], 'name': 'task4', 'start_time': 1497528994.1246588}
    Executing task {'dependencies': [0], 'name': 'task1', 'start_time': 1497528994.236074}
    Executing task {'dependencies': [0], 'name': 'task3', 'start_time': 1497528994.2370954}
    Executing task {'dependencies': [1], 'name': 'task2', 'start_time': 1497528994.340769}
    Executing task {'dependencies': [], 'name': 'task5', 'start_time': 1497528994.3417716}

    AFTER EXECUTION
          ....................................................................................................
    task0 ...............................
    task1                                   .............................
    task2                                                                    ................................
    task3                                    .............................
    task4 ...............................
    task5                                                                     ...............................


.. |BuildStatus| image:: https://travis-ci.org/vramakin/asynctasks.svg?branch=master
   :target: https://travis-ci.org/vramakin/asynctasks
.. |Coverage| image:: https://coveralls.io/repos/github/vramakin/asynctasks/badge.svg?branch=master
   :target: https://coveralls.io/github/vramakin/asynctasks?branch=master
