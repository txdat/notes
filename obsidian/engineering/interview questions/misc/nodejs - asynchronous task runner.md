Your task is to implement a NodeJS server that exposes one single endpoint which is meant to run asynchronous tasks. More precisely, the server has to accept the following requests:

POST `/api/runTasks`

and the request's payload is a JSON-formatted object; for example:

```
{
"taskIds": ["id422", "id2444", "id424", "id4242"]
}
```

The array consists of IDs of the tasks that need to be run.
You will be provided with a TaskRunner service which has the following methods:

```javascript
runTask(id: string): Promise<undefined>
hasTask(id: string): boolean
```

The runTask method is asynchronous and returns a promise which might resolve after a random period of time. A request to the endpoint should initiate the execution of all tasks at the same time, so that they can work in parallel, and should return a response as soon as all tasks have been finished. It is supposed to return an array that has the same length as the taskIds array and that represents the order in which the tasks have finished in the following way:

The i-th item of the array equals i if all tasks from the taskIds array with a lower index than i had been completed before the i-th task was completed – in other words, when the 0th, 1st, 2nd, ..., (i - 1)-th tasks finished before the i-th task was finished; otherwise, the i-th item should equal -1, which symbolizes that prior tasks from original array have not been completed before.

The endpoint should return status code 400 if taskIds contains at least one ID of a task that is not registered in TaskRunner (you can check this by using the hasTask method). If such a case occurs, you must make sure that none of tasks has been run. If you happen to execute TaskRunner.runTask on a ID of a task that is not recognized, the promise that is returned by the method will be rejected.

Assumptions:

The maximum value of the taskIds array's length is 200. You may expect at least 1 task ID to be sent in the request's payload. Only one import is allowed: express (v4.17.1).


Example 1: Let's assume that a request with four task IDs was sent. All task IDs are recognizable by TaskRunner. The execution order of the given task was: 0, 2, 1, 3, which means that:

the first completed task was the task with the first task ID from the taskIds array;
the second completed task was the task with the third task ID from the array;
the third completed task was the task with the second task ID from the array;
the last completed task was the task with the last task ID from the array.

![[Pasted image 20240613230738.png | 400]]


Thus, the response should have status code 200 and the body should be an array:

`[0, 1, -1, 3]`

Example 2 Let's make the same assumptions as in the first example apart from the execution order, which in this case is: 0, 1, 2, 3. The response body should be an array:

`[0, 1, 2, 3]`

Example 3 Analogously, if the execution order is 3, 2, 1, 0, then the response body should be:

`[0, -1, -1, -1]`

Example 4 If the execution order is 2, 0, 3, 1, 5, 4, then the response body should be:

`[0, 1, -1, -1, 4, -1]`

Example 5 On the other hand, when four task IDs are provided in a request and one of them has not been registered in the TaskRunner service, then the response should have status code 400 and no task should have been run.