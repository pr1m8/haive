Examples
========

Basic Example: Summarization
---------------------------

.. code-block:: python

    from haive.agents.summarizer import SummarizerAgent
    
    text = """
    Machine learning (ML) is a field of inquiry devoted to understanding and building methods that 'learn', 
    that is, methods that leverage data to improve performance on some set of tasks. It is seen as a part 
    of artificial intelligence. Machine learning algorithms build a model based on sample data, known as 
    training data, in order to make predictions or decisions without being explicitly programmed to do so. 
    Machine learning algorithms are used in a wide variety of applications, such as in medicine, email 
    filtering, speech recognition, and computer vision, where it is difficult or unfeasible to develop 
    conventional algorithms to perform the needed tasks.
    """
    
    agent = SummarizerAgent()
    summary = agent.summarize(text)
    
    print(summary)
    # Output: Machine learning is a field that creates methods to learn from data and improve task 
    # performance without explicit programming. It's considered part of AI and is used in applications 
    # like medicine, email filtering, and computer vision.

Web Navigation Example
--------------------

.. code-block:: python

    from haive.agents.web_nav import WebNavAgent
    
    # Initialize the web navigation agent
    agent = WebNavAgent()
    
    # Navigate to a website and extract information
    results = agent.navigate(
        url="https://example.com",
        task="Find the contact information"
    )
    
    print(results)

Tree of Thought Reasoning
-----------------------

.. code-block:: python

    from haive.agents.tot import ToTAgent
    
    problem = "In how many ways can 8 people be seated at a round table?"
    
    # Initialize a Tree of Thought agent
    agent = ToTAgent(max_branches=3, max_depth=4)
    
    # Solve the problem
    solution = agent.solve(problem)
    
    print(solution)
