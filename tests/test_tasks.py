# exercises/test-suite/tests/test_tasks.py
# L11 — Task API test suite
#
# Your task: Write 8+ tests for the Task CRUD API.
# Run with: pytest tests/ -v  (from the test-suite/ folder)

# Key concept: Test structure — AAA (Arrange / Act / Assert)
# Every test follows the same pattern:
#   Arrange: Set up any prerequisite state (e.g., create a task first)
#   Act:     Make the HTTP request via the TestClient
#   Assert:  Check the response status code and body

# TODO: Write the following tests:


    #"""
  #  Test: POST /tasks creates a task and returns 201.

    # TODO:
    # 1. POST to /tasks with {"title": "Buy groceries", "completed": False}
    # 2. Assert response.status_code == 201
    # 3. Assert response.json()["title"] == "Buy groceries"
    # 4. Assert "id" is in the response
    # """
    #pass  # TODO: implement
def test_create_task(client):
    #arrange; prepare the teask data
    task_data={
        "title": "Buy groceries", "completed": False
        }
    
    # Act: Create the task
    response = client.post("/tasks", json=task_data)
    #assert: check the response
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["completed"] is False
    assert "id" in data



    """
    Test: GET /tasks returns 200 and a list.

    TODO:
    1. GET /tasks
    2. Assert 200
    3. Assert isinstance(response.json(), list)
    """
    pass  # TODO: implement
def test_list_tasks(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


    """
    Test: GET /tasks/{id} returns the created task.

    TODO:
    1. Create a task first (POST)
    2. GET /tasks/{id} using the returned id
    3. Assert 200 and correct title
    """
    pass  # TODO: implement

def test_get_task_by_id(client):
    #Arrange: create a task 
    create_response = client.post(
        "/tasks",
        json={
            "title": "Buy groceries",
            "completed": False
        },         
    )
    assert create_response.status_code == 201
    #to get Id for the new created task
    task_id = create_response.json()["id"]
    # 3. Get the task using its ID
    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Buy groceries"

def test_get_nonexistent_task_returns_404(client):
    """
    Test: GET /tasks/9999 returns 404.

    TODO:
    1. GET /tasks/9999
    2. Assert response.status_code == 404
    """
    pass  # TODO: implement

    response = client.get("/tasks/9999")

    assert response.status_code == 404


def test_get_nonexistent_task_returns_404(client):
    
    response = client.get("/tasks/9999")

    assert response.status_code == 404

def test_patch_task(client):
    """
    Test: PATCH /tasks/{id} updates only the specified fields.

    TODO:
    1. Create a task
    2. PATCH with {"completed": True}
    3. Assert 200 and completed == True in response
    4. Assert title is unchanged
    """
    pass  # TODO: implement

    #create a task
    create_response = client.post(
        "/tasks",
        json={
            "title": "Buy groceries",
            "completed": False
        }
    )

    assert create_response.status_code == 201

    #get a task ID
    task_id = create_response.json()["id"]

    #patch only the completed field
    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "completed": True
        }
    )

    #check that the update was succsessful
    assert response.status_code == 200
    assert response.json()["completed"] is True

    #make sure the title did not change
    assert response.json()["title"] == "Buy groceries"

def test_delete_task(client):
    """
    Test: DELETE /tasks/{id} removes the task.

    TODO:
    1. Create a task
    2. DELETE /tasks/{id}
    3. Assert 200
    4. GET /tasks/{id} again — assert 404
    """
    #pass  # TODO: implement

#create a task
    create_response = client.post(
        "/tasks",
        json={
            "title": "Buy groceries",
            "completed": False
        }
    )

    assert create_response.status_code == 201
#get ID od teh creared task
    task_id = create_response.json()["id"]
#delete the task
    response = client.delete(f"/tasks/{task_id}")
#make sure the delete was successful
    assert response.status_code == 200
#try to get the task again
    get_response = client.get(f"/tasks/{task_id}")
#task should no loger be there
    assert get_response.status_code == 404


def test_create_task_invalid_data_returns_422(client):
    """
    Test: POST /tasks with an empty title returns 422.

    TODO:
    1. POST /tasks with {"title": ""}  (empty string violates min_length=1)
    2. Assert response.status_code == 422
    """
    #pass  # TODO: implement

    response = client.post(
        "/tasks",
        json={"title": ""
        }

    )

    assert response.status_code == 422


def test_duplicate_task_title_returns_409(client):
    """
    Test: Creating two tasks with the same title returns 409.

    TODO:
    1. POST /tasks with title "Unique Task"
    2. POST /tasks with the same title again
    3. Assert second response.status_code == 409
    """
    pass  # TODO: implement
#create the first task
    first_response = client.post(
        "/tasks",
        json={
            "title": "Unique Task",
            "completed": False
        }
    )
 
    assert first_response.status_code == 201
#try to create the same task  title again
    second_response = client.post(
        "/tasks",
        json={
            "title": "Unique Task",
            "completed": False
        }
    )

# 2nd request should be rejected
    assert second_response.status_code == 409